import requests
import os

def download_file(url, base_path):
    try:
        local_filename = os.path.join(base_path, url.split('/')[-1])
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    #if chunk: 
                    f.write(chunk)
        return local_filename
    except:
        return None