import sys, os
import logging
from Utils.constants import *
from RootInfluencer import RootInfluencer, randomAwait
from Utils.utils import grepFileName, updateInfluencersFile

# Basic logging configuration
logger = logging.getLogger(grepFileName(__file__))
logger.setLevel(logging.INFO)

handler = logging.FileHandler('log.log', encoding='utf-8')
handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s-%(levelname)s %(name)s -> %(message)s')

handler.setFormatter(formatter)
logger.addHandler(handler)

# Auxiliary functions
def filterInfluencers(influencer : RootInfluencer, influencers : list = []) :
    try : 
        if len(influencers) == 0 : return

        for i in influencers :
            # Filter based on the posts, followers or following attributes
            posts_followers_following = influencer.getStatsOf(i)
            if posts_followers_following == None : continue
            if posts_followers_following[1] < 1000 : continue

            # Filter based on links in the bio
            links = influencer.getLinksOf(i)
            if any(['/?u' in link for link in links]) : continue
            
            RELATED_INFLUENCERS.append(i)
            logger.info(f'{i} was selected.')

    except Exception as e :
        logger.error(f'Error filtering the influencers : {e}')

       
def spamMessage(influencer : RootInfluencer) :
    # Record the influencers that have been messaged
    messagedInfluencers =[]
    try :
        counter = 0
        for i in RELATED_INFLUENCERS :
            influencer.message(i)
            randomAwait();randomAwait()
            messagedInfluencers.append(i)
            counter += 1

            # The limit of users to message
            if counter == 10 : break

    except Exception as e :
        logger.error(f'Error while spamming the message: {e}')

    finally :
        updateInfluencersFile(messagedInfluencers)


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

    influencers = rootInfluencer.getInfluencers()

    # Basically cleaning the list
    influencers = [ i for i in influencers if i ] 

    if influencers == [] :
        logger.error('Was not possible to get the related influencers.')
        exit()
    logger.info(f'Got {len(influencers)} influencers')

    filterInfluencers(rootInfluencer, influencers)
    spamMessage(rootInfluencer)
    
    randomAwait()   
    rootInfluencer.driver.close()

    logger.info('Finished the execution.')