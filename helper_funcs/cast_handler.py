from helper_funcs.collager import write_text
from helper_funcs.downloader import download_file


def cast_writer(cast: dict, path: str):
    collage_photos = []
    for a in cast["actors"]:
        photo_path = download_file(a["profile_path"], path)
        if not photo_path:
            continue
        collage_photos += [write_text(photo_path, a)]
        
    for d in cast["d&w"]:
        photo_path = download_file(d["profile_path"], path)
        if not photo_path:
            continue
        collage_photos += [write_text(photo_path, d)]
    return