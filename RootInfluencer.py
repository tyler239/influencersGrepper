import os, re
import logging
import random, time
from Utils.Typer import Typer
from bs4 import BeautifulSoup
from driverModule import getDriver
from Utils.constants import sanitation
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Utils.utils import getCookies, grepFileName, getInfluencersFile


# Basic logging configuration
logger = logging.getLogger(grepFileName(__file__))
logger.setLevel(logging.INFO)

handler = logging.FileHandler('log.log', encoding='utf-8')
handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s-%(levelname)s %(name)s -> %(message)s')

handler.setFormatter(formatter)
logger.addHandler(handler)

randomAwait = lambda : time.sleep(random.randint(1, 7))
grepName = lambda url : re.findall(r'/(.+)/', url)[0]

class RootInfluencer :
    def __init__(self, _username, _hashtag, _message) -> None:
        self.cookies = getCookies(_username)
        self.driver = getDriver(headless=True)
        self.typer = Typer()
        self.driver.get('https://www.instagram.com/')
        randomAwait()
        self.driver.set_window_size(1440, 900)
        self.username = _username
        self.hashtag = _hashtag
        self.msg = _message
    
    def loadCookies(self) -> bool :
        if self.cookies :
            cookies = eval(self.cookies)
            for cookie in cookies :
                self.driver.add_cookie(cookie)
            self.driver.refresh()
            randomAwait()
        else :
            logger.error('The cookies were not found. Pls check the path and try again.')
            logger.error('Some features only work with cookies...')
            return False
        return True

    def headersAndCookies(self) -> tuple:
        cookies = eval(str(self.driver.get_cookies()))
        cookies = {c['name'] : c['value'] for c in cookies}

        headers = self.driver.execute_script("var req = new XMLHttpRequest();req.open('GET', document.location, false);req.send(null);return req.getAllResponseHeaders()")
        finalHeaders = {}
        for h in headers.splitlines() :
            temp = h.split(':')
            finalHeaders[temp[0].strip()] = ':'.join(temp[1:]).strip()

        return (finalHeaders, cookies)
    
    #Just possible with cookies
    def message(self, to) -> bool :
        self.driver.get(f'https://www.instagram.com/{to}/')
        randomAwait()

        #Click on the message button
        try : 
            WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//div[text()="Message"]'))).click()
        except : 
            try : 
                self.driver.find_elements(By.XPATH, '//div[@role="button"]')[1].click()
            except Exception as e :
                logger.error(f'Could not message {to}')
                logger.error('The message button, just to get into the chat not found :(.')
                logger.error(f'Exeception: {e}')
                return False
        
        #Send the message
        randomAwait()
        try :
            WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//div[@aria-label="Message"]/p')))
            x = self.driver.find_element(By.XPATH, '//div[@aria-label="Message"]/p')
            self.typer.send(x, self.msg)
            x.send_keys(Keys.ENTER)
            return True
        except Exception as e :
            logger.error(f'Could not message {to}')
            logger.error('Message box not found. Probably the xpath changed... Check it out.')
            logger.error(f'Exeception: {e}')
            return False
        

    def getStatsOf(self, influencer : str) :
        if f'https://www.instagram.com/{influencer}/' != self.driver.current_url :
            self.driver.get(f'https://www.instagram.com/{influencer}/')
            randomAwait()

        try :
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//section/ul/li')))

            posts, followers, following = self.driver.find_elements(By.XPATH, '//section/ul/li')
            posts = posts.find_element(By.XPATH, './/span/span').text
            followers = followers.find_element(By.XPATH, './/span/span').text
            following = following.find_element(By.XPATH, './/span/span').text
            return [sanitation(posts), sanitation(followers), sanitation(following)]
        except Exception as e :
            print('Stats not found. Probably the xpath changed... Check it out.')
            print(f'Exeception: {e}')
            return None
        
    def getLinksOf(self, influencer) -> list :
        if f'https://www.instagram.com/{influencer}/' != self.driver.current_url :
            self.driver.get(f'https://www.instagram.com/{influencer}/')
            randomAwait()

        links = []
        try : 
            links = self.driver.find_elements(By.CSS_SELECTOR, 'main section ul + div a')
            links = [link.get_attribute('href') for link in links]
        except Exception as e :
            print(f'Error getting links of {influencer}...')
            print(f'Exeception: {e}')
        finally :
            return links
    
    def getInfluencers(self) -> list : 
        self.hashtag = self.hashtag.replace('#', '')
        self.driver.get(f'https://www.instagram.com/explore/tags/{self.hashtag}/')
        randomAwait()
        links = []
        currentInfluencers = []
        
        savedInfluencers = getInfluencersFile()

        '''
        Here the name of the accounts are not visiable, so we are grepping the url to that post 
        and them, getting the name of the account
        '''
        WebDriverWait(self.driver, 90).until(EC.presence_of_element_located((By.XPATH, '//article//div[count(div)=3]')))

        # Get only the rows that have 3 divs, which are the posts
        for i in self.driver.find_elements(By.XPATH, '//article//div[count(div)=3]') :
            soup = BeautifulSoup(i.get_attribute('innerHTML'), 'html.parser')
            
            # Get the href of the 3 links
            for _ in soup.css.select('a') : 
                if _.get('href') not in links : links.append(_.get('href',''))
        
        # Now go to each one of this links just to get the name of the account
        for link in links : 
            try :
                self.driver.get(f'https://www.instagram.com{link}')
                randomAwait();randomAwait()
                
                WebDriverWait(self.driver, 70).until(EC.presence_of_element_located((By.XPATH, '//main//a//span')))
                name = self.driver.find_elements(By.XPATH, '//main//a//span')[0].text
                if name not in savedInfluencers and name not in currentInfluencers : 
                    currentInfluencers.append(name)  
            except Exception as e :
                print(f'Error going to {link}...')
                print(f'Exeception: {e}')
                
        return currentInfluencers


    def getRelatedInfluencers(self, influ : str) :
        self.driver.get(f'https://www.instagram.com/{influ}/')
        randomAwait();randomAwait()

        usernames = []

        try :
            #Here I m considering that both the message and the related button render at the same time
            WebDriverWait(self.driver, 70).until(EC.presence_of_element_located((By.XPATH, '//div[text()="Message"]')))
            self.driver.find_elements(By.XPATH, '//div[@role="button"]')[2].click()

            #There are two ways to get them. Is good to have the both in the sleeve

            #1 - By the see all link
            randomAwait()
            WebDriverWait(self.driver, 70).until(EC.presence_of_element_located((By.XPATH, '//span[text()="See all"]'))).click()

            WebDriverWait(self.driver, 70).until(EC.presence_of_element_located((By.XPATH, '//div[text()="Suggested for you"]')))
            randomAwait()

            #Scrolling functonality to load more influencers
            sx, sy = 0, 0
            for _ in range(3) :
                #Getting all the visible a tags
                soup = (BeautifulSoup(self.driver.find_element(By.CSS_SELECTOR, 'div[style="height: 400px; overflow: hidden auto;"]')
                                      .get_attribute('innerHTML'), 'html.parser'))
                a_tags = soup.find_all('a')
            
                #Extracting the usernames and setting them in the usernames list
                for a in a_tags :
                    username = grepName(a.get('href', 'Not found'))
                    if username not in usernames : usernames.append(username)

                #The code for scrolling
                randomAwait()
                sy += 810
                self.driver.execute_script(f'document.querySelector(\'div[style="height: 400px; overflow: hidden auto;"]\').scroll({sx},{sy})')

        except Exception as e:
            try : 
                #2 - By the suggested under the stories
                randomAwait()
                self.driver.get(f'https://www.instagram.com/{influ}/')
                randomAwait()
                WebDriverWait(self.driver, 70).until(EC.presence_of_element_located((By.XPATH, '//div[text()="Message"]')))
                self.driver.find_elements(By.XPATH, '//div[@role="button"]')[2].click()

                randomAwait()

                #Scrolling functionality 
                while True : 
                    presentation = self.driver.find_elements(By.XPATH, '//div[@role="presentation"]')[0]
                    soup = BeautifulSoup(presentation.get_attribute('innerHTML'), 'html.parser')
                    a_tags = soup.find_all('a')

                    for a in a_tags :
                        username = grepName(a.get('href', 'Not found'))
                        if username not in usernames : usernames.append(username)

                    randomAwait()
                    randomAwait()

                    try : 
                        button = self.driver.find_element(By.CSS_SELECTOR, 'div[role="presentation"] + button[aria-label="Next"]')
                    except :
                        break 

                    if button :
                        button.click()
                        randomAwait()

            except Exception as e :
                print('Related influencers not found with the 2 methods. Probably the xpath changed... Check it out.')
                print(f'Exeception: {e}')

        
        return usernames