import os, random


def makeCookiesPath() :
    abs_dir = os.path.dirname(os.path.abspath(__file__))
    if not os.path.exists(os.path.join( abs_dir , 'Cookies')) :
        os.mkdir(os.path.join( abs_dir , 'Cookies'))

def getCookiesPath() :
    makeCookiesPath()
    abs_dir = os.path.dirname(os.path.abspath(__file__))
    cookie = random.choice(os.listdir(os.path.join( abs_dir , 'Cookies')))
    return os.path.join( abs_dir , 'Cookies', cookie)