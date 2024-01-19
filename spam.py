import sys, os
import logging
from Utils.constants import *
from Utils.utils import grepFileName
from RootInfluencer import RootInfluencer, randomAwait

# Basic logging configuration
logger = logging.getLogger(grepFileName(__file__))
logger.setLevel(logging.INFO)

handler = logging.FileHandler('log.log', encoding='utf-8')
handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s-%(levelname)s %(name)s -> %(message)s')

handler.setFormatter(formatter)
logger.addHandler(handler)

# Auxiliary functions
def spamStats(influencer : RootInfluencer, influencers : list = []) :
    try : 
        if len(influencers) == 0 : return

        for i in influencers :
            posts_followers_following = influencer.getStatsOf(i)
            
            if posts_followers_following == None : continue
            RELATED_INFLUENCERS.append({i : posts_followers_following})
            randomAwait()

    except Exception as e :
        logger.error(f'Error while spamming the stats: {e}')

def filterRelatedInfluencers() :
    toDelete = []
    try : 
        for i in RELATED_INFLUENCERS :
            for key in i.keys() :
                # 1K is the minimum number of followers
                if i[key][1] < 1000 : 
                    toDelete.append(i)
        
        logger.info(f'Will delete {len(toDelete)} influencers, that was not suitable for the operation.')
        for i in toDelete : RELATED_INFLUENCERS.remove(i)
    except Exception as e :
        logger.error(f'Error while filtering the related influencers: {e}')
       

def spamMessage(influencer : RootInfluencer) :
    # Record the influencers that have been messaged
    messagedInfluencers =[]
    try :
        counter = 0
        for i in RELATED_INFLUENCERS :
            for key in i.keys() :
                influencer.message(key)
                randomAwait();randomAwait()
                messagedInfluencers.append(key)
                counter += 1

            # The limit of users to message
            if counter == 1 : break

    except Exception as e :
        logger.error(f'Error while spamming the message: {e}')

    finally :
        influencersFileLoc = os.path.join(os.getcwd(), 'Cookies', 'influencers.txt')
         # Get the old ones
        with open(influencersFileLoc, 'r') as file : influencers = file.read().strip().split(';')

        # Add the new ones
        influencers += messagedInfluencers

        # Save them all in a CSV file
        with open(influencersFileLoc, 'w') as f : f.write(';'.join(influencers)) 



if __name__ == '__main__' :
    if len(sys.argv) < 4 :
        logger.error('Was not passed the username, or the target hashtag, or the message to spam.s')
        logger.error(f'{sys.argv}')
        print('Please, pass the necessary arguments (username, hashtag, message).')
        exit()

    x = sys.argv[1].strip()
    y = sys.argv[2].strip()
    z = sys.argv[3].strip()
    logger.info(f'Username being used: {x}')
    logger.info(f'Target hashtag: {y}')
    logger.info(f'Message to spam: {z}')

    # Create the rootInfluencer object
    rootInfluencer = RootInfluencer(x, y, z)
    rootInfluencer.loadCookies()

    # If wasn't possible to get the related influencers, exit
    influencers = rootInfluencer.getInfluencers()

    # Basically cleaning the list
    influencers = [ i for i in influencers if i ] 

    if influencers == [] :
        logger.error('Was not possible to get the related influencers.')
        exit()
    logger.info(f'Got {len(influencers)} influencers')

    spamStats(rootInfluencer, influencers)
    filterRelatedInfluencers()
    spamMessage(rootInfluencer)
    
    randomAwait()   
    rootInfluencer.driver.close()

    logger.info('Finished the execution.')