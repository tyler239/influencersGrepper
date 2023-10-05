import re
import random, time
from Utils.Typer import Typer
from bs4 import BeautifulSoup
from Utils.utils import getCookies
from Utils.constants import sanitation
from driverModule import getDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

randomAwait = lambda : time.sleep(random.randint(1, 7))
grepName = lambda url : re.findall(r'/(.+)/', url)[0]

class RootInfluencer :
    def __init__(self, username, rootInfluencer) -> None:
        self.cookies = getCookies(username)
        self.driver = getDriver(headless=False)
        self.rootInfluencer = rootInfluencer
        self.relatedInfluencers = []
        self.typer = Typer()
        self.driver.get('https://www.instagram.com/')
        randomAwait()
        self.driver.set_window_size(1440, 900)
    
    def loadCookies(self) -> bool :
        if self.cookies :
            cookies = eval(self.cookies)
            for cookie in cookies :
                self.driver.add_cookie(cookie)
            self.driver.refresh()
            randomAwait()
        else :
            print('The cookies were not found. Pls check the path and try again.')
            print('Some features only work with cookies...')
            return False
        return True
    
    #Just possible with cookies
    def message(self, message : str, to) :
        self.driver.get(f'https://www.instagram.com/{to}/')
        randomAwait()

        #Click on the message button
        try : 
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[text()="Message"]'))).click()
        except : 
            try : 
                self.driver.find_elements(By.XPATH, '//div[@role="button"]')[1].click()
            except Exception as e :
                print('Message button not found. Probably the xpath changed... Check it out.')
                print(f'Exeception: {e}')
        
        #Send the message
        randomAwait()
        try :
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@aria-label="Message"]/p')))
            x = self.driver.find_element(By.XPATH, '//div[@aria-label="Message"]/p')
            self.typer.send(x, message)
            x.send_keys(Keys.ENTER)
        except Exception as e :
            print('Message box not found. Probably the xpath changed... Check it out.')
            print(f'Exeception: {e}')
        

    def getStatsOf(self, influencer : str) :
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
        
    
    def getRelatedInfluencers(self) : 
        self.driver.get(f'https://www.instagram.com/{self.rootInfluencer}/')
        randomAwait()
        usernames = []

        try :
            #Here I m considering that both the message and the related button render at the same time
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[text()="Message"]')))
            self.driver.find_elements(By.XPATH, '//div[@role="button"]')[2].click()

            #There are two ways to get them. Is good to have the both in the sleeve

            #1 - By the see all link
            randomAwait()
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//span[text()="See all"]'))).click()

            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[text()="Suggested for you"]')))
            randomAwait()

            #Scrolling functonality to load more influencers
            sx, sy = 0, 0
            for _ in range(1,2) :
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
                self.driver.get(f'https://www.instagram.com/{self.rootInfluencer}/')
                randomAwait()
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[text()="Message"]')))
                self.driver.find_elements(By.XPATH, '//div[@role="button"]')[2].click()

                randomAwait()

                #Scrolling functionality 
                while True : 
                    presentation = self.driver.find_elements(By.XPATH, '//div[@role="presentation"]')[1]
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

            except Exception as e :
                print('Related influencers not found with the 2 methods. Probably the xpath changed... Check it out.')
                print(f'Exeception: {e}')
            
        self.relatedInfluencers = usernames[0:10]

        return self.relatedInfluencers