import os
import logging
from Utils.utils import randomAwait, grepFileName
from driverModule import getDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Basic logging configuration
logger = logging.getLogger(grepFileName(__file__))
logger.setLevel(logging.INFO)

handler = logging.FileHandler('log.log', encoding='utf-8')
handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s-%(levelname)s %(name)s -> %(message)s')

handler.setFormatter(formatter)
logger.addHandler(handler)


if __name__ == '__main__' :
    try : 
        logger.info('Creating the cookies...')
        driver = getDriver(headless=False)
        driver.get('https://www.instagram.com/')

        # Got 5 minutes to make the login
        WebDriverWait(driver, 300).until(EC.presence_of_element_located((By.XPATH, '//span[text()="For you"]')))
        
        driver.find_element(By.XPATH, '//span[text()="For you"]')
        logger.info('Logged in successfully')

        # Just go to the profile page, check everything
        driver.find_elements(By.XPATH, '//div[count(div)=8]/div')[7].click()

        # See if the name matches
        WebDriverWait(driver, 300).until(EC.presence_of_element_located((By.XPATH, '//h2')))
        name = driver.find_element(By.XPATH, '//h2').text
        logger.info(f'Name of the logged in user: {name}')
        randomAwait()  

        # Create the cookies file
        cookiesDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Cookies')
        if not os.path.exists(cookiesDir) : os.mkdir(cookiesDir)

        with open(os.path.join(cookiesDir, f'cookie{name}.txt'), 'w') as file :
            file.write(f'{name}\n')
            file.write(str(driver.get_cookies()))
        
        randomAwait()

        # Just exit
        driver.close()
        driver.quit()
        logger.info('Finished creating the cookies')
    
    except Exception as e :
        logger.error(f'Error while creating the cookies: {e}')
        driver.close()
        driver.quit()
        exit()

    