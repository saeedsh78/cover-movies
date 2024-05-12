import os
import shutil
from PIL import Image, ImageOps, ImageDraw
from helper_funcs.cast_handler import cast_writer
from helper_funcs.downloader import download_file
from helper_funcs.information import get_all_info, get_all_info_tv
from helper_funcs.name_support import movie_name, series_name

def add_corners(im_path, rad):
    im = Image.open(im_path)
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

    # this discussion helped me a lot: https://stackoverflow.com/questions/765736/using-pil-to-make-all-white-pixels-transparent

    image_corner_path = os.path.join(icon_path,"poster.ico")
    img = add_corners(poster_path, 30)
    img = ImageOps.expand(img, (69, 0, 69, 0), fill=0)
    img = ImageOps.fit(img, (300, 300)).convert("RGBA")
    img.save(image_corner_path)
    return image_corner_path
    
    
def set_cover(mk_dir_name, cast_path, poster_link):
    poster_path = download_file(poster_link, cast_path)
    if not poster_path:
        return
    create_icon = convert(poster_path, icon_path=mk_dir_name)
    
    with open(mk_dir_name + "\\desktop.ini", "w+") as f:
        f.write("[.ShellClassInfo]\n")
        f.write("IconResource=poster.ico,0")
        f.close()

    os.system('attrib +r \"{}\"'.format(mk_dir_name))
    os.system('attrib +h \"{}\\desktop.ini\"'.format(mk_dir_name))
    os.system('attrib +h \"{}\\poster.ico\"'.format(mk_dir_name))
    return True


def chenge_cover(dir_path: str, file_path: str, all_info: dict, cast: dict):
    # icon
    mk_dir_name = os.path.join(dir_path, all_info["full_name"].replace(":", ""))
    if not os.path.exists(mk_dir_name):
        os.mkdir(mk_dir_name)
    mk_dir_cast = os.path.join(mk_dir_name, "cast")
    if not os.path.exists(mk_dir_cast):
        os.mkdir(mk_dir_cast)
    setcover = set_cover(mk_dir_name, mk_dir_cast, all_info["poster_link"])
    
    # cast
    cast_path = cast_writer(cast, mk_dir_cast)
    
    # # information
    with open(os.path.join(mk_dir_cast, "information.txt"), "w") as i:
        for k, v in all_info.items():
            v= "|".join(v) if isinstance(v, list) else v
            i.write(f"{k.upper()}: {v}\n\n")
        i.close()

    shutil.move(file_path, mk_dir_name)
    return

def chenge_cover_tv(dir_path: str, all_info: dict, cast: dict):
    # icon
    mk_dir_name = os.path.join(dir_path, all_info["full_name"].replace(":", ""))
    if not os.path.exists(mk_dir_name):
        os.mkdir(mk_dir_name)
    mk_dir_cast = os.path.join(mk_dir_name, "cast")
    if not os.path.exists(mk_dir_cast):
        os.mkdir(mk_dir_cast)
    setcover = set_cover(mk_dir_name, mk_dir_cast, all_info["poster_link"])
    # cast
    cast_path = cast_writer(cast, mk_dir_cast)
    
    # # information
    with open(os.path.join(mk_dir_cast, "information.txt"), "w") as i:
        for k, v in all_info.items():
            if k == "seasons":
                continue
            v= "|".join(v) if isinstance(v, list) else v
            i.write(f"{k.upper()}: {v}\n\n")
        i.close()

    for f in range(1, all_info["number_of_seasons"]+1):
        dir_season = os.path.join(mk_dir_name, f"S0{f}") if f < 10 else os.path.join(mk_dir_name, f"S{f}")
        
        if not os.path.exists(dir_season):
            os.mkdir(dir_season)
        
        for s in all_info["seasons"]:
            if s["season_number"] == f:
                set_cover(dir_season, mk_dir_cast, s["poster_path"])
                
    dir_list = os.listdir(dir_path)
    for file in dir_list:
        if file.split(".")[-1] in ["mp4", "mkv", "avi"]:
            season = series_name(file, season=True)
            if season == "None":
                continue
            if os.path.exists(os.path.join(mk_dir_name, season)):
                shutil.move(os.path.join(dir_path, file), os.path.join(mk_dir_name, season))
            else:
                if not os.path.exists(os.path.join(mk_dir_name, "other")):
                    os.mkdir(os.path.join(mk_dir_name, "other"))
                shutil.move(os.path.join(dir_path, file), os.path.join(mk_dir_name, "other"))
                    
    return


def handler(dir_path: str, imdbid: str = None, tmdbid: str = None, type_: str = "m"):
    if type_ == "m":
        if imdbid:
            if not os.path.isfile(dir_path):
                return        
            all_info, cast = get_all_info(imdbid=imdbid)
            if all_info:
                chenge_cover(os.path.dirname(dir_path), dir_path, all_info, cast)
                print(f"Folder icon changed successfully. | {all_info["full_name"]}")
            
        elif tmdbid:
            if not os.path.isfile(dir_path):
                return  
            all_info, cast = get_all_info(tmdbid=tmdbid)
            if all_info:
                chenge_cover(os.path.dirname(dir_path), dir_path, all_info, cast)
                print(f"Folder icon changed successfully. | {all_info["full_name"]}")
            
        else:
            if os.path.isfile(dir_path):
                return 
            dir_list = os.listdir(dir_path)
            for file in dir_list:
                file_path = os.path.join(dir_path, file)
                if os.path.isfile(file_path):
                    if file.split(".")[-1] in ["mp4", "mkv", "avi"]:
                        m_name, year = movie_name(file)
                        all_info, cast = get_all_info(m_name=m_name, year=year)
                        if all_info:
                            chenge_cover(dir_path, file_path, all_info, cast)
                            print(f"Folder icon changed successfully. | {all_info["full_name"]}")
    else:
        if imdbid:
            if os.path.isfile(dir_path):
                return
            all_info, cast = get_all_info_tv(imdbid=imdbid)
            if all_info:
                chenge_cover_tv(dir_path, all_info, cast)
                print(f"Folder icon changed successfully. | {all_info["full_name"]}")
            
        elif tmdbid:
            if os.path.isfile(dir_path):
                return
            all_info, cast = get_all_info_tv(tmdbid=tmdbid)
            if all_info:
                chenge_cover_tv(dir_path, all_info, cast)
                print(f"Folder icon changed successfully. | {all_info["full_name"]}")
            
        else:
            if os.path.isfile(dir_path):
                return
            dir_list = os.listdir(dir_path)
            for file in dir_list:
                file_path = os.path.join(dir_path, file)
                if os.path.isfile(file_path):
                    if file.split(".")[-1] in ["mp4", "mkv", "avi"]:
                        s_name, season= series_name(file)
                        break
            all_info, cast = get_all_info_tv(s_name=s_name)
            if all_info:
                chenge_cover_tv(dir_path, all_info, cast)
                print(f"Folder icon changed successfully. | {all_info["full_name"]}")
                    
    return