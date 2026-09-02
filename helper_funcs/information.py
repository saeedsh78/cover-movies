import json
from config import (
    OMDB_API_KEY,
    OMDB_GET_INFO_LINK,
    THEMOVIEDB_API_KEY,
    THEMOVIEDB_API_TOKEN,
    THEMOVIEDB_API_DOWNLOAD_IMAGE_300,
    THEMOVIEDB_FIND_LINK,
    THEMOVIEDB_GET_CAST_LINK,
    THEMOVIEDB_GET_CAST_LINK_TV,
    THEMOVIEDB_GET_EXTERNAL_ID_LINK_TV,
    THEMOVIEDB_GET_INFO_LINK,
    THEMOVIEDB_GET_INFO_LINK_TV,
    THEMOVIEDB_SEARCH_LINK,
    THEMOVIEDB_SEARCH_LINK_TV,
)
from helper_funcs.net import get

TIMEOUT = 25


def get_info_omdb(imdb_id):
    try:
        info_imdb_id = get(OMDB_GET_INFO_LINK.format(imdb_id, OMDB_API_KEY), timeout=TIMEOUT)
        return json.loads(info_imdb_id.content)
    except Exception:
        return {}


def get_info_tmdb(tmdb_id, tv: bool = False):
    try:
        url = THEMOVIEDB_GET_INFO_LINK_TV if tv else THEMOVIEDB_GET_INFO_LINK
        get_info_themoviedb = get(url.format(tmdb_id, THEMOVIEDB_API_KEY), timeout=TIMEOUT)
        return json.loads(get_info_themoviedb.content)
    except Exception:
        return {}


def get_cast_tmdb(tmdb_id, cast, series: bool = False):
    try:
        url = THEMOVIEDB_GET_CAST_LINK_TV if series else THEMOVIEDB_GET_CAST_LINK
        headers = {
            "accept": "application/json",
            "Authorization": THEMOVIEDB_API_TOKEN
        }
        response = get(url.format(tmdb_id), headers=headers, timeout=TIMEOUT)
        result = json.loads(response.content)
    except Exception:
        return {"actors": [], "d&w": []}

    cast_info = {"actors": [], "d&w": []}
    actors_result = result.get("cast") or []
    crew_result = result.get("crew") or []

    for a in cast["actors"]:
        for ct in actors_result:
            if (ct["name"].lower() == a.lower() or ct.get("original_name", "").lower() == a.lower()) and ct.get("profile_path"):
                cast_info["actors"] += [
                    {
                        "job": ct["known_for_department"],
                        "name": ct["name"],
                        "profile_path": THEMOVIEDB_API_DOWNLOAD_IMAGE_300.format(ct["profile_path"]),
                        "character": ct["character"]
                    }
                ]
    for d in cast["director"]:
        for ct in crew_result:
            if (ct["name"].lower() == d.lower() or ct.get("original_name", "").lower() == d.lower()) and ct.get("profile_path"):
                cast_info["d&w"] += [
                    {
                        "job": "Director",
                        "name": ct["name"],
                        "profile_path": THEMOVIEDB_API_DOWNLOAD_IMAGE_300.format(ct["profile_path"])
                    }
                ]
    for w in cast["writer"]:
        for ct in crew_result:
            if (ct["name"].lower() == w.lower() or ct.get("original_name", "").lower() == w.lower()) and ct.get("profile_path"):
                cast_info["d&w"] += [
                    {
                        "job": "Writer",
                        "name": ct["name"],
                        "profile_path": THEMOVIEDB_API_DOWNLOAD_IMAGE_300.format(ct["profile_path"])
                    }
                ]
    return cast_info

def get_all_info(m_name: str = None, year: str = None, imdbid: str = None, tmdbid: str = None):
    if imdbid:
        find_themoviedb = get(THEMOVIEDB_FIND_LINK.format(imdbid, THEMOVIEDB_API_KEY), timeout=TIMEOUT)
        result = json.loads(find_themoviedb.content).get("movie_results", [{}])[0]
        movie_id = result.get("id")
        if not movie_id:
            return None, None
        full_name = "{} ({})".format(result.get("title"), result.get("release_date", "0000").split("-")[0])

    elif tmdbid:
        get_info_movie_id = get_info_tmdb(tmdbid)
        if not get_info_movie_id:
            return None, None
        movie_id = tmdbid
        full_name = "{} ({})".format(get_info_movie_id.get("title"), get_info_movie_id.get("release_date", "0000").split("-")[0])

    else:
        search_themoviedb = get(
            THEMOVIEDB_SEARCH_LINK.format(m_name.replace(" ", "+").replace(".", "+").replace("_", "+"), year, THEMOVIEDB_API_KEY),
            timeout=TIMEOUT
        )
        result = json.loads(search_themoviedb.content).get("results", [])
        if len(result) > 1:
            for movie in result:
                release_date = movie.get("release_date", "0000").split("-")[0]
                if release_date == year:
                    movie_id = movie.get("id")
                    if not movie_id:
                        return None, None
                    full_name = "{} ({})".format(movie.get("title"), year)
                    break
            else:
                return None, None
        elif len(result) == 1:
            movie_id = result[0].get("id")
            if not movie_id:
                return None, None
            full_name = "{} ({})".format(result[0].get("title"), year)
        else:
            return None, None
    if not tmdbid:
        get_info_movie_id = get_info_tmdb(movie_id)
    imdb_id = get_info_movie_id.get("imdb_id")
    get_info_imdb_id = {}
    if imdb_id:
        get_info_imdb_id = get_info_omdb(imdb_id)
    all_info = {
        "full_name": full_name,
        "movie_id": movie_id,
        "imdb_id": imdb_id,
        "poster_link": THEMOVIEDB_API_DOWNLOAD_IMAGE_300.format(get_info_movie_id.get("poster_path")),
        "genres": [g.get("name", "None") for g in get_info_movie_id.get("genres", [{}])],
        "rated": get_info_imdb_id.get("Rated"),
        "released": get_info_imdb_id.get("Released"),
        "runtime": get_info_imdb_id.get("Runtime"),
        "director": [d.strip() for d in get_info_imdb_id.get("Director", "None").split(",")],
        "writer": [w.strip() for w in get_info_imdb_id.get("Writer", "None").split(",")],
        "actors": [a.strip() for a in get_info_imdb_id.get("Actors", "None").split(",")],
        "plot": get_info_imdb_id.get("Plot"),
        "language": get_info_imdb_id.get("Language"),
        "country": get_info_imdb_id.get("Country"),
        "awards": get_info_imdb_id.get("Awards"),
        "rotten tomatoes": None,
        "metacritic": None,
        "imdbRating": None,
        "imdbVotes": get_info_imdb_id.get("imdbVotes"),
        "type": get_info_imdb_id.get("Type"),
        "boxOffice": get_info_imdb_id.get("BoxOffice"),
    }
    _fill_ratings(all_info, get_info_imdb_id)
    return all_info, get_cast_tmdb(movie_id, {"director": all_info["director"], "writer": all_info["writer"], "actors": all_info["actors"]})


def get_all_info_tv(s_name: str = None, imdbid: str = None, tmdbid: str = None):
    if imdbid:
        find_themoviedb = get(THEMOVIEDB_FIND_LINK.format(imdbid, THEMOVIEDB_API_KEY), timeout=TIMEOUT)
        result = json.loads(find_themoviedb.content).get("tv_results", [{}])[0]
        series_id = result.get("id")
        if not series_id:
            return None, None
        full_name = "{} ({})".format(result.get("name"), result.get("first_air_date", "0000").split("-")[0])

    elif tmdbid:
        get_info_series_id = get_info_tmdb(tmdbid, tv=True)
        if not get_info_series_id:
            return None, None
        series_id = tmdbid
        full_name = "{} ({})".format(get_info_series_id.get("name"), get_info_series_id.get("first_air_date", "0000").split("-")[0])

    else:
        if not s_name:
            return None, None
        search_themoviedb = get(
            THEMOVIEDB_SEARCH_LINK_TV.format(s_name.replace(" ", "+").replace(".", "+"), THEMOVIEDB_API_KEY),
            timeout=TIMEOUT
        )
        result = json.loads(search_themoviedb.content).get("results", [])
        if len(result) > 0:
            result = result[0]
            series_id = result.get("id")
            if not series_id:
                return None, None
            full_name = "{} ({})".format(result.get("name"), result.get("first_air_date", "0000").split("-")[0])
        else:
            return None, None
    if not tmdbid:
        get_info_series_id = get_info_tmdb(series_id, tv=True)
    headers = {
        "accept": "application/json",
        "Authorization": THEMOVIEDB_API_TOKEN
    }

    response = get(THEMOVIEDB_GET_EXTERNAL_ID_LINK_TV.format(series_id), headers=headers, timeout=TIMEOUT)
    imdb_id = json.loads(response.content).get("imdb_id")
    get_info_imdb_id = {}
    if imdb_id:
        get_info_imdb_id = get_info_omdb(imdb_id)
    all_info = {
        "full_name": full_name,
        "series_id": series_id,
        "imdb_id": imdb_id,
        "number_of_seasons": get_info_series_id.get("number_of_seasons", 0),
        "seasons": [
            {
                "poster_path": THEMOVIEDB_API_DOWNLOAD_IMAGE_300.format(x.get("poster_path")) if x.get("poster_path") else None,
                "season_number": x.get("season_number", 0)
            }
            for x in get_info_series_id.get("seasons", [{}])
        ],
        "poster_link": THEMOVIEDB_API_DOWNLOAD_IMAGE_300.format(get_info_series_id.get("poster_path")),
        "genres": [g.get("name", "None") for g in get_info_series_id.get("genres", [{}])],
        "rated": get_info_imdb_id.get("Rated"),
        "released": get_info_imdb_id.get("Released"),
        "runtime": get_info_imdb_id.get("Runtime"),
        "director": [d.strip() for d in get_info_imdb_id.get("Director", "None").split(",")],
        "writer": [w.strip() for w in get_info_imdb_id.get("Writer", "None").split(",")],
        "actors": [a.strip() for a in get_info_imdb_id.get("Actors", "None").split(",")],
        "plot": get_info_imdb_id.get("Plot"),
        "language": get_info_imdb_id.get("Language"),
        "country": get_info_imdb_id.get("Country"),
        "awards": get_info_imdb_id.get("Awards"),
        "rotten tomatoes": None,
        "metacritic": None,
        "imdbRating": None,
        "imdbVotes": get_info_imdb_id.get("imdbVotes"),
        "type": get_info_imdb_id.get("Type"),
        "boxOffice": get_info_imdb_id.get("BoxOffice"),
    }
    _fill_ratings(all_info, get_info_imdb_id)
    return all_info, get_cast_tmdb(series_id, {"director": all_info["director"], "writer": all_info["writer"], "actors": all_info["actors"]}, series=True)


def _fill_ratings(all_info, get_info_imdb_id):
    for r in get_info_imdb_id.get("Ratings", []):
        source = r.get("Source")
        if source == "Internet Movie Database":
            all_info["imdbRating"] = r.get("Value")
        elif source == "Rotten Tomatoes":
            all_info["rotten tomatoes"] = r.get("Value")
        elif source == "Metacritic":
            all_info["metacritic"] = r.get("Value")
