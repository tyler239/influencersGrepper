import os, re, time, random

randomAwait = lambda : time.sleep(random.randint(3, 7))

grepFileName = lambda s : re.findall(r'[^\\]+$', s)[0]


def makeCookiesPath() :
    abs_dir = os.path.dirname(os.path.abspath(__file__))
    if not os.path.exists(os.path.join( abs_dir , '..', 'Cookies')) :
        os.mkdir(os.path.join( abs_dir , '..', 'Cookies'))

# Returns the cookie of that username
def getCookies(username : str) :
    makeCookiesPath()
    dirname = os.path.dirname(os.path.abspath(__file__))
    for f in os.listdir(os.path.join(dirname, '..', 'Cookies')):
        with open(os.path.join(dirname, '..', 'Cookies', f), 'r') as file:
            if username in file.readline():
                return file.readline().strip()
    return None 

# Function related to the rudimentary influencers database
def getInfluencersFile(username : str) -> list:
    abs_dir = os.path.dirname(os.path.abspath(__file__))

    # Case the Influencers folder does not exist
    if not os.path.exists(os.path.join( abs_dir , '..', 'Influencers')) :
        os.mkdir(os.path.join( abs_dir , '..', 'Influencers'))
    
    # Case the file does not exist
    if not os.path.exists(os.path.join(abs_dir, '..', 'Influencers', f'influencers{username}.txt')) :
        with open(os.path.join(abs_dir, '..', 'Influencers', f'influencers{username}.txt'), 'w') as file :
            file.write(f'{username}\n;')
        return []
    
    # Case the file exists
    with open(os.path.join(abs_dir, '..', 'Influencers', f'influencers{username}.txt'), 'r') as file :
        file.readline()
        return file.read().strip().split(';')

def updateInfluencersFile(username : str, influencers : list) :
    abs_dir = os.path.dirname(os.path.abspath(__file__))

    with open(os.path.join(abs_dir, '..', 'Influencers', f'influencers{username}.txt'), 'r') as file :
        file.readline()
        old = file.read().strip().split(';')
    
    with open(os.path.join(abs_dir, '..', 'Influencers', f'influencers{username}.txt'), 'w') as file :
        file.write(f'{username}\n')
        file.write(';'.join(old + influencers))
        