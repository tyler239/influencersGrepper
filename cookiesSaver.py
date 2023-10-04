import os, re
from Utils.utils import randomAwait
from driverModule import getDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


'''
Would be usefull to have logs of this file
'''


if __name__ == '__main__' :
    try : 
        driver = getDriver(headless=False)
        driver.get('https://www.instagram.com/')

        # Got 5 minutes to make the login
        WebDriverWait(driver, 300).until(EC.presence_of_element_located((By.XPATH, '//span[text()="For you"]')))
        
        driver.find_element(By.XPATH, '//span[text()="For you"]')
        print('Logged in!')

        # Just go to the profile page, check everything
        driver.find_elements(By.XPATH, '//div[count(div)=8]/div')[7].click()

        # See if the name matches
        WebDriverWait(driver, 300).until(EC.presence_of_element_located((By.XPATH, '//h2')))
        name = driver.find_element(By.XPATH, '//h2').text
        print(f'Name: {name}')
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
    
    except Exception as e :
        print(f'Error while creating the cookies: {e}')
        driver.close()
        driver.quit()
        exit()

    