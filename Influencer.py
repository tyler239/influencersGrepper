import os, time, random
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

randomAwait = lambda : time.sleep(random.randint(1, 7))

class Influencer :
    def __init__(self, cookies_path, driver, influencer) -> None:
        self.cookies_path = cookies_path
        self.driver = driver
        self.influencer = influencer

    
    def loadCookies(self) -> bool :
        if os.path.exists(self.cookies_path) :
            with open(self.cookies_path, 'r') as file :
                cookies = eval(file.read())
                for cookie in cookies :
                    self.driver.add_cookie(cookie)
                self.driver.refresh()
        else :
            print('The cookies were not found. Pls check the path and try again.')
            print('Some features only work with cookies...')
            return False
        return True
    
    #Just possible with cookies
    def messageTo(self, message : str) :
        self.driver.get(f'https://www.instagram.com/{self.influencer}/')
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
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@aria-label="Message"]/p'))).send_keys(message)
        except Exception as e :
            print('Message box not found. Probably the xpath changed... Check it out.')
            print(f'Exeception: {e}')
        
    def getStatsOf(self) :
        self.driver.get(f'https://www.instagram.com/{self.influencer}/')
        randomAwait()
        try :
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//section/ul/li')))

            posts, followers, following = self.driver.find_elements(By.XPATH, '//section/ul/li')
            posts = posts.find_element(By.XPATH, './/span/span').text
            followers = followers.find_element(By.XPATH, './/span/span').text
            following = following.find_element(By.XPATH, './/span/span').text
            return [posts, followers, following]
        except Exception as e :
            print('Stats not found. Probably the xpath changed... Check it out.')
            print(f'Exeception: {e}')
            return None
        
    
    def getRelatedInfluencers(self) : 
        self.driver.get(f'https://www.instagram.com/{self.influencer}/')
        randomAwait()
        usernames = []

        try :
            #Here I m considering that both the message and the related button render at the same time
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[text()="Message"]')))
            self.driver.find_elements(By.XPATH, '//div[@role="button"]')[2].click()
            

            #There are two ways to get them. Is good to have the both in the sleeve

            #1 - By the see all link
            randomAwait()
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//span[text()="See All"]'))).click()

            randomAwait()
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[text()="Suggested for you"]')))
            a_tags = self.driver.find_elements(By.CSS_SELECTOR, 'div[role="dialog"] div[role="dialog"] canvas + a')
        
        except :
            try : 
                #2 - By the suggedted under the stories
                #$x('(//div[@role="presentation"])[2]//ul/li//a[img]') ---> Working
                randomAwait()
                presentation = self.driver.find_elements(By.XPATH, '//div[@role="presentation"]')[1] 
                a_tags = presentation.find_elements(By.CSS_SELECTOR, '. div ul li a:has(img)')

            except Exception as e :
                print('Related influencers not found with the 2 methods. Probably the xpath changed... Check it out.')
                print(f'Exeception: {e}')
                return None
            
        usernames = [a_tag.get_attribute('href').replace('/', '') for a_tag in a_tags]
        return usernames