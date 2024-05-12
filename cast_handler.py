import os
from collager import Collager, write_text
from downloader import download_file


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
    # width, height = (1920, 1080)
    # lines = 5
    
    # collager = Collager(path)
    # collage = collager.collage(width, height, lines)
    # collage_path = os.path.join(path, "cast.png")
    # collage.save(collage_path)
    
    # return collage_path