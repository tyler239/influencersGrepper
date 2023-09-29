import os, random


def getCookiesPath() :
    abs_dir = os.path.dirname(os.path.abspath(__file__))
    cookie = random.choice(os.listdir(os.path.join( abs_dir , 'Cookies')))
    return os.path.join( abs_dir , 'Cookies', cookie)