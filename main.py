import sys
import logging
from constants import *
from RootInfluencer import RootInfluencer, randomAwait


# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='log.log', encoding='utf-8')

# Auxiliary functions
def spamStats(influencer : RootInfluencer) :
    try : 
        if len(influencer.relatedInfluencers) == 0 : return

        for i in influencer.relatedInfluencers :
            posts_followers_following = influencer.getStatsOf(i)
            
            if posts_followers_following == None : continue
            RELATED_INFLUENCERS.append({i : posts_followers_following})
            randomAwait()

    except Exception as e :
        logging.error(f'Error while spamming the stats: {e}')

def filterRelatedInfluencers() :
    try : 
        for i in RELATED_INFLUENCERS :
            for key in i.keys() :
                # 50M is the minimum number of followers
                if i[key][1] < 50000000 : RELATED_INFLUENCERS.remove(i)
    except Exception as e :
        logging.error(f'Error while filtering the related influencers: {e}')

def spamMessage(influencer : RootInfluencer, message : str) :
    try :
        for i in RELATED_INFLUENCERS :
            print(i)
            for key in i.keys() :
                influencer.message(message, key)
                randomAwait()
    except Exception as e :
        logging.error(f'Error while spamming the message: {e}')


if __name__ == '__main__' :
    # Get the rootInfluecer passed in the command line
    if len(sys.argv) < 2 :
        logging.error('Was not passed the root influencer as an argument.')
        print('Please, pass the root influencer as an argument.')
        exit()

    x = sys.argv[1].strip()
    logging.info(f'Root influencer: {x}')

    # Create the rootInfluencer object
    rootInfluencer = RootInfluencer(x)
    rootInfluencer.loadCookies()

    # If wasn't possible to get the related influencers, exit
    if rootInfluencer.getRelatedInfluencers() == [] :
        logging.error('Was not possible to get the related influencers.')
        exit()
    logging.info(f'Got {len(rootInfluencer.relatedInfluencers)} influencers')

    spamStats(rootInfluencer)
    filterRelatedInfluencers()
    spamMessage(rootInfluencer, PITCH)

    logging.info('Finished the execution.')