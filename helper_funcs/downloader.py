import os
from helper_funcs.net import get

TIMEOUT = 25

def download_file(url, base_path):
    try:
        local_filename = os.path.join(base_path, url.split('/')[-1])
        with get(url, stream=True, timeout=TIMEOUT) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return local_filename
    except Exception:
        if 'local_filename' in locals() and os.path.exists(local_filename):
            try:
                os.remove(local_filename)
            except OSError:
                pass
        return None
