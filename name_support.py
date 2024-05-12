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
    regex = r"([Ss]\d{1,3}).?[Ee]\d{1,4}"
    regex_s_name = r"(.*).[Ss]\d{1,3}.?[Ee]\d{1,4}"
    s = "None"
    name = None
    if re.findall(regex, full_name):
        s = int(re.search(regex, full_name).group(1).lower().replace("s", ""))
        s= f"S0{s}" if s < 10 else f"S{s}"
    
    if season:
        return s
    
    if re.findall(regex_s_name, full_name):
        name = re.search(regex_s_name, full_name).group(1)
    return name, s