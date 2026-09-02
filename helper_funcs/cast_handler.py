from helper_funcs.collager import write_text
from helper_funcs.downloader import download_file
from helper_funcs.progress import report, check_cancelled


def cast_writer(cast: dict, path: str):
    saved = 0
    for a in cast["actors"]:
        check_cancelled()
        photo_path = download_file(a["profile_path"], path)
        if not photo_path:
            continue
        write_text(photo_path, a)
        saved += 1

    for d in cast["d&w"]:
        check_cancelled()
        photo_path = download_file(d["profile_path"], path)
        if not photo_path:
            continue
        write_text(photo_path, d)
        saved += 1
    if saved:
        report("log.cast_saved", saved)
