import os
import json
import requests
from dotenv import load_dotenv
load_dotenv()

fanart_api_key = "3dbcd21be550346d2a54dc516f804cc4"
thetvdb_api_key = "052722d0-9e9a-4a37-ad28-b0949719e1c2"
THEMOVIEDB_API_KEY = os.getenv("THEMOVIEDB_API_KEY")
THEMOVIEDB_API_TOKEN = os.getenv("THEMOVIEDB_API_TOKEN")
THEMOVIEDB_SEARCH_LINK = "https://api.themoviedb.org/3/search/movie?query={}&year={}&api_key={}"
THEMOVIEDB_SEARCH_LINK_TV = "https://api.themoviedb.org/3/search/tv?query={}&api_key={}"
THEMOVIEDB_FIND_LINK = "https://api.themoviedb.org/3/find/{}?external_source=imdb_id&api_key={}"
THEMOVIEDB_GET_INFO_LINK = "https://api.themoviedb.org/3/movie/{}?api_key={}"
THEMOVIEDB_GET_INFO_LINK_TV = "https://api.themoviedb.org/3/tv/{}?api_key={}"
THEMOVIEDB_GET_CAST_LINK = "https://api.themoviedb.org/3/movie/{}/credits?language=en-US"
THEMOVIEDB_GET_CAST_LINK_TV = "https://api.themoviedb.org/3/tv/{}/credits?language=en-US"
THEMOVIEDB_GET_EXTERNAL_ID_LINK_TV = "https://api.themoviedb.org/3/tv/{}/external_ids"
THEMOVIEDB_API_DOWNLOAD_IMAGE_300 = "https://image.tmdb.org/t/p/w300{}"
OMDB_API_KEY = os.getenv("OMDB_API_KEY")
OMDB_GET_INFO_LINK = "http://www.omdbapi.com/?i={}&apikey={}"


def api_test(type_ = "omdb"):
    if type_ == "omdb":
        url = f"https://www.omdbapi.com/?i=tt9458304&apikey={OMDB_API_KEY}"
        result = requests.get(url=url).content
        data = json.loads(result)
        test = data.get("imdbID", None)
        
    else:
        print(THEMOVIEDB_API_KEY)
        url = f"https://api.themoviedb.org/3/movie/808?api_key={THEMOVIEDB_API_KEY}"
        result = requests.get(url=url).content
        data = json.loads(result)
        test = data.get("id", None)
        
    if test:
        return True
    return False