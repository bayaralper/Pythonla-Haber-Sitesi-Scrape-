import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
name_counter=0
def driver_chrome_settings(height): #Chromedeki haber sayfasıyla alakası olmayan kısımları kaldırır.
    chrome_options=Options() 
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--hide-scrollbars")
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_window_size(1920,height)
    return driver

def driver_find_height(url,driver):
    driver.get(url)
    time.sleep(2)
    height=driver.execute_script('return (document.bodyPn.scrollHeight)')#Sayfanın boyutunu döndürür.
    driver.close()
    return height 

def screenshot_with_driver(url,driver):
    global name_counter
    driver.get(url)
    time.sleep(2)
    file_name=str(name_counter)+'.png'
    driver.save_screenshot('/'+url[12:17]+"_"+file_name)#Ss alır ve bunu bir dosya içine kaydeder
    name_counter+=1
    driver.close()
    return name_counter
    