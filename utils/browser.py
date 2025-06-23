import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def main(*options):
    chrome_options = webdriver.ChromeOptions()
    
    if options is not None:
        for option in options:
            chrome_options.add_argument(option)
    
    service = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service, options=chrome_options)

    browser.get('https://www.google.com.br/')
    print("Título da página:", browser.title)

    time.sleep(5)   
    browser.quit()

if __name__ == "__main__":
    main()
