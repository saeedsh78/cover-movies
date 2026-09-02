import re


def movie_name(full_name):
    full_name = full_name.replace("_", ".").replace("-", ".")
    regex = r"([. ([{\w]+)(\d{4})[^p]"
    regex_m_name = r"([\w]+)"
    if re.findall(regex, full_name):
        m_name, year = re.search(regex, full_name).groups()
        m_name = " ".join(re.findall(regex_m_name, m_name))
        return m_name, year
    return None, None

def series_name(full_name: str, season: bool = False):
    full_name = full_name.replace("_", ".").replace("-", ".")
    # Regex to capture name, optional season, and episode
    regex = r"(.*?)\.?(?:[Ss](\d{1,3})\.?)?[Ee](\d{1,4})"

    name, s, e = None, None, None

    match = re.search(regex, full_name, re.IGNORECASE)

    if match:
        name = ' '.join(match.group(1).split('.')).strip()
        season_digits = match.group(2)
        episode_digits = match.group(3)

        if season_digits:
            s_num = int(season_digits)
            s = f"S0{s_num}" if s_num < 10 else f"S{s_num}"
        else:
            s = "S01"  # Default to season 1

        if episode_digits:
            e_num = int(episode_digits)
            e = f"E0{e_num}" if e_num < 10 else f"E{e_num}"

    if season:
        return s

    return name, s