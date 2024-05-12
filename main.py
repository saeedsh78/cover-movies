import os
from config import api_test
from folder_cover import handler

logo = """
 ██████╗ ██████╗ ██╗   ██╗███████╗██████╗       
██╔════╝██╔═══██╗██║   ██║██╔════╝██╔══██╗      
██║     ██║   ██║██║   ██║█████╗  ██████╔╝      
██║     ██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗      
╚██████╗╚██████╔╝ ╚████╔╝ ███████╗██║  ██║      
 ╚═════╝ ╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝      
                                                
███╗   ███╗ ██████╗ ██╗   ██╗██╗███████╗███████╗
████╗ ████║██╔═══██╗██║   ██║██║██╔════╝██╔════╝
██╔████╔██║██║   ██║██║   ██║██║█████╗  ███████╗
██║╚██╔╝██║██║   ██║╚██╗ ██╔╝██║██╔══╝  ╚════██║
██║ ╚═╝ ██║╚██████╔╝ ╚████╔╝ ██║███████╗███████║
╚═╝     ╚═╝ ╚═════╝   ╚═══╝  ╚═╝╚══════╝╚══════╝
"""
TEXT =f"""
{logo}


[1] Movies Folder Path
[2] Coverd Movie By IMDBID/TMDBID
[3] TV-Series Folder Path
[4] Coverd TV-Series By IMDBID/TMDBID

[5] Test API KEY(OMDBID/TMDBID)

[6] Star Project in GitHub ()

[0] Exit...

==> """

clear = lambda: os.system('cls')

if __name__ == "__main__":
    while 1:
        try:
            clear()
            p = int(input(TEXT))
            match p:
                case 1:
                    f = input(":) Insert Movies Folder Path: ")
                    handler(f)
                    input("Press any key...")
                case 2:
                    f = input(":) Insert Movie Path With File Name Movie: ")
                    if not os.path.isfile(f):
                        pass
                    i = input(":) Insert Movie IMDBID/TMDBID: ")
                    if i.startswith("tt"):
                        handler(f, imdbid=i)
                    else:
                        handler(f, tmdbid=i)
                    input("Press any key...")
                case 3:
                    f = input(":) Insert TV-Series Folder Path: ")
                    handler(f, type_="s")
                    input("Press any key...")
                case 4:
                    f = input(":) Insert TV-Series Folder Path: ")
                    if not os.path.isfile(f):
                        pass
                    i = input(":) Insert TV-Series IMDBID/TMDBID: ")
                    if i.startswith("tt"):
                        handler(f, imdbid=i, type_="s")
                    else:
                        handler(f, tmdbid=i, type_="s")
                    input("Press any key...")

                case 5:
                    omdb = api_test("omdb")
                    tmdb = api_test("tmdb")
                    
                    print(f"OMDB = {"Valid API key" if omdb else "Invalid API key"}\nTMDB = {"Valid API key" if tmdb else "Invalid API key"}")
                    input("Press any key...")
                    
                case 6:
                    
                case 0:
                    exit()

        except ValueError:
            clear()
            continue