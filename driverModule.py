from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium_stealth import stealth


'''
The chrome just relesead the "Chrome For Testing" feature that is made for the developers.
Because the stadart chrome is auto-updated
I just downloed the driver binary, not the chrome binary. So  probabilly Im not doing everything right. 
'''

def getDriver(cookiesPath=None) : 
    options = Options()
    options.add_experimental_option('detach',True)
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-blink-features=AutomationControlled')

    service = Service(executable_path=r'C:\Users\victo\chromedriver\win64-116.0.5845.96\chromedriver-win64\chromedriver.exe')

    for op in [ '--disable-notifications', '--disable-infobars', '--disable-extensions', 
               '--disable-dev-shm-usage', '--no-sandbox', '--disable-gpu', 
                '--log-level=3', '--ignore-certificate-errors', '--ignore-ssl-err'
                'start-maximized', '--disable-blink-features=AutomationControlled', '--lang=en-US'] :
        options.add_argument(op)
    return webdriver.Chrome(options=options, service=service)


def getStealth() :
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")

    options.add_experimental_option('detach',True)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=options, service= Service(ChromeDriverManager().install()))

    stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )
    
    return driver
