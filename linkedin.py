import argparse
import urllib.request
import os 
import shutil
import time


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
import gspread
from oauth2client.service_account import ServiceAccountCredentials


"""
utils
"""

def find_by_xpath(driver, xpath):
    return WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.XPATH, xpath)))


"""
steps
"""
def login(driver):
    email = WebDriverWait(driver, 11).until(lambda x: x.find_element_by_xpath("//*[@id='username']"))
    """
    this is where you put your email
    """
    email.send_keys("youremail")
    password = WebDriverWait(driver, 11).until(lambda x: x.find_element_by_xpath("//*[@id='password']"))
    """
    this is where you put your password
    """
    password.send_keys("yourpassword")
    password.send_keys(Keys.RETURN)
    return 

def getConnections(driver):
    goto_connections = WebDriverWait(driver, 11).until(lambda x: x.find_elements_by_class_name("feed-identity-module__stat"))
    goto_connections[1].click()
    to_all = WebDriverWait(driver, 11).until(lambda x: x.find_element_by_class_name("mn-community-summary__sub-section"))
    to_all.click()
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(3)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    all_connections = WebDriverWait(driver, 11).until(lambda x: x.find_elements_by_class_name("mn-connection-card__details"))
    for connection in all_connections:
        print(connection.get_attribute("innerHTML"))
    print(len(all_connections))


parser = argparse.ArgumentParser(description='Linkedin connections, automated.')
parser.add_argument('-d', '--debug', nargs='?', const=True, type=bool)
args = parser.parse_args()

def run():
    driver = webdriver.Chrome()
    driver.get("https://www.linkedin.com/uas/login?trk=guest_homepage-basic_nav-header-signin")
    driver.maximize_window()
    driver.implicitly_wait(10)
    login(driver)
    getConnections(driver)


    if not vars(args)['debug']:
        driver.close()

if __name__ == "__main__":
    run()

