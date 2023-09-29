from constants import RELATED_INFLUENCERS
from RootInfluencer import RootInfluencer, randomAwait


#   Auxiliary functions
def spamStats(influencer : RootInfluencer) :
    if len(influencer.relatedInfluencers) == 0 : return

    for i in influencer.relatedInfluencers :
        posts_followers_following = influencer.getStatsOf(i)
        
        if posts_followers_following == None : continue
        RELATED_INFLUENCERS.append({i : posts_followers_following})
        randomAwait()

def filterRelatedInfluencers() :
    for i in RELATED_INFLUENCERS :
        for key in i.keys() :
            if i[key][1] < 1000 : RELATED_INFLUENCERS.remove(i)

def spamMessage(influencer : RootInfluencer, message : str) :
    if len(influencer.relatedInfluencers) == 0 : return

    for i in influencer.relatedInfluencers :
        influencer.message(message, i)
        randomAwait()
