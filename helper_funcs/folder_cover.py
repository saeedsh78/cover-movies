import ctypes
import os
import shutil
from PIL import Image, ImageOps, ImageDraw
from helper_funcs.cast_handler import cast_writer
from helper_funcs.downloader import download_file
from helper_funcs.information import get_all_info, get_all_info_tv
from helper_funcs.name_support import movie_name, series_name
from helper_funcs.progress import report, check_cancelled

VIDEO_EXTS = ["mp4", "mkv", "avi", "mov", "wmv", "flv", "webm", "m4v"]

FILE_ATTRIBUTE_READONLY = 0x0001
FILE_ATTRIBUTE_HIDDEN = 0x0002
FILE_ATTRIBUTE_SYSTEM = 0x0004
FILE_ATTRIBUTE_NORMAL = 0x0080


def _set_win_attrs(path, attrs):
    """Direct Windows Win32 API to set attributes instantly without cmd shell overhead."""
    try:
        ctypes.windll.kernel32.SetFileAttributesW(str(path), attrs)
    except Exception:
        pass


def add_corners(im, rad):
    if not isinstance(im, Image.Image):
        im = Image.open(im)
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2 - 1, rad * 2 - 1), fill=255)
    alpha = Image.new('L', im.size, 255)
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    im.putalpha(alpha)
    return im


def convert(poster_path, icon_path):
    image_corner_path = os.path.join(icon_path, "poster.ico")
    img = add_corners(Image.open(poster_path), 24)
    img = ImageOps.expand(img, (58, 0, 58, 0), fill=0)
    img = ImageOps.fit(img, (256, 256), method=Image.Resampling.LANCZOS).convert("RGBA")
    sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
    img.save(image_corner_path, format="ICO", sizes=sizes)
    return image_corner_path


def _notify_shell(folder):
    folder = os.path.abspath(folder)
    try:
        shell = ctypes.windll.shell32
        SHCNF_PATHW_FLUSHNOWAIT = 0x0005 | 0x2000
        shell.SHChangeNotify(0x00002000, SHCNF_PATHW_FLUSHNOWAIT, ctypes.c_wchar_p(folder), None)  # UPDATEITEM
        shell.SHChangeNotify(0x00002000, SHCNF_PATHW_FLUSHNOWAIT, ctypes.c_wchar_p(os.path.join(folder, "poster.ico")), None)
        shell.SHChangeNotify(0x00001000, SHCNF_PATHW_FLUSHNOWAIT, ctypes.c_wchar_p(folder), None)  # UPDATEDIR
        shell.SHChangeNotify(0x00001000, SHCNF_PATHW_FLUSHNOWAIT, ctypes.c_wchar_p(os.path.dirname(folder)), None)
    except Exception:
        pass


# set when set_cover lays down at least one icon during a handler() run
_icon_dirty = False


def _refresh_if_dirty():
    global _icon_dirty
    if not _icon_dirty:
        return
    _icon_dirty = False
    try:
        # Flush Windows Shell icon associations
        ctypes.windll.shell32.SHChangeNotify(0x08000000, 0x0000, None, None)  # SHCNE_ASSOCCHANGED
    except Exception:
        pass

    # Send refresh (F5 / ShellView update) to all open Explorer windows so they render the new icons immediately
    try:
        user32 = ctypes.windll.user32
        WM_COMMAND = 0x0111

        def enum_cb(hwnd, lparam):
            cls_buf = ctypes.create_unicode_buffer(256)
            user32.GetClassNameW(hwnd, cls_buf, 256)
            if cls_buf.value in ("CabinetWClass", "ExploreWClass", "Progman", "WorkerW"):
                user32.PostMessageW(hwnd, WM_COMMAND, 28931, 0)
                user32.PostMessageW(hwnd, WM_COMMAND, 41504, 0)
            return True

        ENUM_PROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_int, ctypes.c_int)
        user32.EnumWindows(ENUM_PROC(enum_cb), 0)
    except Exception:
        pass


def set_cover(mk_dir_name, cast_path, poster_link):
    global _icon_dirty
    if not poster_link:
        return False
    check_cancelled()
    report("status.poster", os.path.basename(mk_dir_name))

    poster_path = download_file(poster_link, cast_path)
    if not poster_path:
        report("log.poster_fail")
        return False
    convert(poster_path, icon_path=mk_dir_name)

    icon_file_path = os.path.join(mk_dir_name, "poster.ico")
    desktop_ini_path = os.path.join(mk_dir_name, "desktop.ini")

    # utf-16 with BOM is the encoding Explorer itself writes; anything else
    # (e.g. the default cp1252) breaks parsing on non-ascii paths
    with open(desktop_ini_path, "w", encoding="utf-16", newline="\r\n") as f:
        f.write("[.ShellClassInfo]\n")
        f.write("IconResource=.\\poster.ico,0\n")

    # Set attributes via Win32 API
    _set_win_attrs(desktop_ini_path, FILE_ATTRIBUTE_HIDDEN | FILE_ATTRIBUTE_SYSTEM)
    _set_win_attrs(icon_file_path, FILE_ATTRIBUTE_HIDDEN)
    _set_win_attrs(mk_dir_name, FILE_ATTRIBUTE_READONLY)

    _notify_shell(mk_dir_name)
    _icon_dirty = True
    return True


def _write_information_file(mk_dir_cast, all_info, skip_keys=()):
    with open(os.path.join(mk_dir_cast, "information.txt"), "w") as i:
        for k, v in all_info.items():
            if k in skip_keys:
                continue
            v = "|".join(v) if isinstance(v, list) else v
            i.write("{}: {}\n\n".format(k.upper(), v))


def change_cover(dir_path: str, file_path: str, all_info: dict, cast: dict):
    # icon
    mk_dir_name = os.path.join(dir_path, all_info["full_name"].replace(":", ""))
    if not os.path.exists(mk_dir_name):
        os.mkdir(mk_dir_name)
    mk_dir_cast = os.path.join(mk_dir_name, "cast")
    if not os.path.exists(mk_dir_cast):
        os.mkdir(mk_dir_cast)
    if set_cover(mk_dir_name, mk_dir_cast, all_info["poster_link"]):
        report("log.icon", all_info["full_name"])

    # cast
    cast_writer(cast, mk_dir_cast)

    # information
    _write_information_file(mk_dir_cast, all_info)

    try:
        shutil.move(file_path, mk_dir_name)
        report("log.move", os.path.basename(file_path))
    except shutil.Error:
        report("log.move_fail", os.path.basename(file_path))
    return


def change_cover_tv(dir_path: str, all_info: dict, cast: dict):
    # icon
    mk_dir_name = os.path.join(dir_path, all_info["full_name"].replace(":", ""))
    if not os.path.exists(mk_dir_name):
        os.mkdir(mk_dir_name)
    mk_dir_cast = os.path.join(mk_dir_name, "cast")
    if not os.path.exists(mk_dir_cast):
        os.mkdir(mk_dir_cast)
    if set_cover(mk_dir_name, mk_dir_cast, all_info["poster_link"]):
        report("log.icon", all_info["full_name"])

    # cast
    cast_writer(cast, mk_dir_cast)

    # information
    _write_information_file(mk_dir_cast, all_info, skip_keys=("seasons",))

    for f in range(1, all_info["number_of_seasons"] + 1):
        check_cancelled()
        dir_season = os.path.join(mk_dir_name, "S0{}".format(f)) if f < 10 else os.path.join(mk_dir_name, "S{}".format(f))

        if not os.path.exists(dir_season):
            os.mkdir(dir_season)

        for s in all_info["seasons"]:
            if s["season_number"] == f:
                if set_cover(dir_season, mk_dir_cast, s["poster_path"]):
                    report("log.season_poster", "S{}".format(f))

    dir_list = os.listdir(dir_path)
    for file in dir_list:
        if file.split(".")[-1].lower() in VIDEO_EXTS:
            check_cancelled()
            season = series_name(file, season=True)
            if season == "None":
                continue
            if os.path.exists(os.path.join(mk_dir_name, season)):
                try:
                    shutil.move(os.path.join(dir_path, file), os.path.join(mk_dir_name, season))
                    report("log.move", file)
                except shutil.Error:
                    report("log.move_fail", file)
            else:
                if not os.path.exists(os.path.join(mk_dir_name, "other")):
                    os.mkdir(os.path.join(mk_dir_name, "other"))
                try:
                    shutil.move(os.path.join(dir_path, file), os.path.join(mk_dir_name, "other"))
                    report("log.other", file)
                except shutil.Error:
                    report("log.move_fail", file)


def handler(dir_path: str, imdbid: str = None, tmdbid: str = None, type_: str = "m"):
    try:
        return _handler(dir_path, imdbid, tmdbid, type_)
    finally:
        _refresh_if_dirty()


def _handler(dir_path: str, imdbid: str = None, tmdbid: str = None, type_: str = "m"):
    if not os.path.exists(dir_path):
        report("log.path_invalid", dir_path)
        return None
    if type_ == "m":
        if imdbid or tmdbid:
            if not os.path.isfile(dir_path):
                report("msg.wrong_file_t", "")
                return None
            report("status.info", os.path.basename(dir_path))
            all_info, cast = get_all_info(imdbid=imdbid) if imdbid else get_all_info(tmdbid=tmdbid)
            check_cancelled()
            if all_info:
                report("log.found", all_info["full_name"])
                change_cover(os.path.dirname(dir_path), dir_path, all_info, cast)
                report("log.summary", all_info["full_name"])
            else:
                report("log.not_found", os.path.basename(dir_path))
            return True

        elif os.path.isfile(dir_path):
            # file mode without an ID: search by the filename
            m_name, year = movie_name(os.path.basename(dir_path))
            if not m_name:
                report("log.skip_file", os.path.basename(dir_path))
                return None
            report("status.searching", m_name)
            all_info, cast = get_all_info(m_name=m_name, year=year)
            check_cancelled()
            if all_info:
                report("log.found", all_info["full_name"])
                change_cover(os.path.dirname(dir_path), dir_path, all_info, cast)
                report("log.summary", all_info["full_name"])
            else:
                report("log.not_found", os.path.basename(dir_path))
            return True

        else:
            dir_list = os.listdir(dir_path)
            video_files = [f for f in dir_list
                           if f.split(".")[-1].lower() in VIDEO_EXTS
                           and os.path.isfile(os.path.join(dir_path, f))]
            if not video_files:
                report("log.no_video", dir_path)
                return True
            for i, file in enumerate(video_files):
                check_cancelled()
                file_path = os.path.join(dir_path, file)
                m_name, year = movie_name(file)
                if not m_name:
                    report("log.skip_file", file)
                    continue
                report("status.searching", m_name, i, len(video_files))
                all_info, cast = get_all_info(m_name=m_name, year=year)
                check_cancelled()
                if all_info:
                    report("log.found", all_info["full_name"])
                    change_cover(dir_path, file_path, all_info, cast)
                    report("log.summary", all_info["full_name"])
                else:
                    report("log.not_found", file)
            return True
    else:
        if os.path.isfile(dir_path):
            report("msg.series_dir_t", "")
            return None
        if imdbid or tmdbid:
            report("status.info", os.path.basename(dir_path))
            all_info, cast = get_all_info_tv(imdbid=imdbid) if imdbid else get_all_info_tv(tmdbid=tmdbid)
            check_cancelled()
            if all_info:
                report("log.found", all_info["full_name"])
                change_cover_tv(dir_path, all_info, cast)
                report("log.summary", all_info["full_name"])
            else:
                report("log.not_found", imdbid or tmdbid)
            return True
        else:
            dir_list = os.listdir(dir_path)
            s_name = None
            for file in dir_list:
                file_path = os.path.join(dir_path, file)
                if os.path.isfile(file_path):
                    if file.split(".")[-1].lower() in VIDEO_EXTS:
                        report("status.scanning", file)
                        s_name, season = series_name(file)
                        if s_name:
                            break
            if not s_name:
                report("log.no_video", dir_path)
                return True
            report("status.searching", s_name)
            all_info, cast = get_all_info_tv(s_name=s_name)
            check_cancelled()
            if all_info:
                report("log.found", all_info["full_name"])
                change_cover_tv(dir_path, all_info, cast)
                report("log.summary", all_info["full_name"])
            else:
                report("log.not_found", s_name)
            return True
