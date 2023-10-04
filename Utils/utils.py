import os, random, time

randomAwait = lambda : time.sleep(random.randint(3, 7))


def makeCookiesPath() :
    abs_dir = os.path.dirname(os.path.abspath(__file__))
    if not os.path.exists(os.path.join( abs_dir , 'Cookies')) :
        os.mkdir(os.path.join( abs_dir , 'Cookies'))

# Returns the cookie of that username
def getCookies(username : str) :
    makeCookiesPath()
    dirname = os.path.dirname(os.path.abspath(__file__))
    for f in os.listdir(os.path.join(dirname, 'Cookies')):
        with open(os.path.join(dirname, 'Cookies', f), 'r') as file:
            if username in file.readline():
                return file.readline().strip()
    return None