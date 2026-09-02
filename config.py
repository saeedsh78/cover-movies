import sys
import os
import json
import requests

def get_base_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))


BASE_PATH = get_base_path()
CONFIG_PATH = os.path.join(BASE_PATH, "config.json")
VERSION = "1.1.1"

# scale factor must be set before QApplication is created
UI_SCALES = {"S": "1.0", "M": "1.15", "L": "1.3", "XL": "1.5"}

def load_ui_prefs():
    keys = load_api_keys()
    return keys.get("ui_prefs", {})

def save_ui_prefs(prefs):
    keys = load_api_keys()
    keys["ui_prefs"] = prefs
    save_api_keys(keys)

def load_api_keys():
    if not os.path.exists(CONFIG_PATH):
        return {}
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return {}


def save_api_keys(keys):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(keys, f, indent=2, ensure_ascii=False)


def change_api(type_, api_key, api_token=None):
    keys = load_api_keys()
    if type_ == "omdb":
        keys["OMDB_API_KEY"] = api_key
    elif type_ == "tmdb":
        keys["THEMOVIEDB_API_KEY"] = api_key
        keys["THEMOVIEDB_API_TOKEN"] = api_token
    save_api_keys(keys)
    reload_keys()


def reload_keys():
    global OMDB_API_KEY, THEMOVIEDB_API_KEY, THEMOVIEDB_API_TOKEN
    keys = load_api_keys()
    OMDB_API_KEY = keys.get("OMDB_API_KEY", "")
    THEMOVIEDB_API_KEY = keys.get("THEMOVIEDB_API_KEY", "")
    THEMOVIEDB_API_TOKEN = "Bearer " + keys.get("THEMOVIEDB_API_TOKEN", "")

def api_test(type_="omdb", custom_key=None, custom_token=None):
    """
    Tests an API key/token and returns (success: bool, message/detail: str).
    """
    try:
        from helper_funcs.net import get
        if type_ == "omdb":
            k = custom_key if custom_key is not None else OMDB_API_KEY
            if not k:
                return False, "Key is empty"
            url = f"https://www.omdbapi.com/?i=tt0111161&apikey={k}"
            resp = get(url, timeout=15)
            data = resp.json()
            if data.get("Response") == "True" or data.get("imdbID"):
                title = data.get("Title", "OK")
                return True, f"'{title}'"
            return False, data.get("Error", f"HTTP {resp.status_code}")

        elif type_ == "tmdb":
            k = custom_key if custom_key is not None else THEMOVIEDB_API_KEY
            if not k:
                return False, "Key is empty"
            url = f"https://api.themoviedb.org/3/movie/550?api_key={k}"
            resp = get(url, timeout=15)
            data = resp.json()
            if data.get("id"):
                title = data.get("title", "OK")
                return True, f"'{title}'"
            return False, data.get("status_message", f"HTTP {resp.status_code}")

        elif type_ == "tmdb_token":
            tok = custom_token if custom_token is not None else THEMOVIEDB_API_TOKEN
            if not tok or tok.strip() in ("Bearer", "Bearer "):
                return None, "Token is empty"
            token_str = tok if tok.startswith("Bearer ") else f"Bearer {tok}"
            url = "https://api.themoviedb.org/3/authentication"
            resp = get(url, headers={"Authorization": token_str}, timeout=15)
            data = resp.json()
            if data.get("success"):
                return True, "Token Authenticated"
            return False, data.get("status_message", f"HTTP {resp.status_code}")

        return False, "Unknown test type"
    except Exception as e:
        return False, str(e)

keys = load_api_keys()
ICON_PATH = os.path.join(BASE_PATH, "CoverMovies.ico")
if not os.path.exists(ICON_PATH):
    ICON_PATH = os.path.join(BASE_PATH, "CoverMovies.jpg")
OMDB_API_KEY = keys.get("OMDB_API_KEY", "")
THEMOVIEDB_API_KEY = keys.get("THEMOVIEDB_API_KEY", "")
THEMOVIEDB_API_TOKEN = "Bearer " + keys.get("THEMOVIEDB_API_TOKEN", "")
THEMOVIEDB_SEARCH_LINK = "https://api.themoviedb.org/3/search/movie?query={}&year={}&api_key={}"
THEMOVIEDB_SEARCH_LINK_TV = "https://api.themoviedb.org/3/search/tv?query={}&api_key={}"
THEMOVIEDB_FIND_LINK = "https://api.themoviedb.org/3/find/{}?external_source=imdb_id&api_key={}"
THEMOVIEDB_GET_INFO_LINK = "https://api.themoviedb.org/3/movie/{}?api_key={}"
THEMOVIEDB_GET_INFO_LINK_TV = "https://api.themoviedb.org/3/tv/{}?api_key={}"
THEMOVIEDB_GET_CAST_LINK = "https://api.themoviedb.org/3/movie/{}/credits?language=en-US"
THEMOVIEDB_GET_CAST_LINK_TV = "https://api.themoviedb.org/3/tv/{}/credits?language=en-US"
THEMOVIEDB_GET_EXTERNAL_ID_LINK_TV = "https://api.themoviedb.org/3/tv/{}/external_ids"
THEMOVIEDB_API_DOWNLOAD_IMAGE_300 = "https://image.tmdb.org/t/p/w300{}"
OMDB_GET_INFO_LINK = "http://www.omdbapi.com/?i={}&apikey={}"
