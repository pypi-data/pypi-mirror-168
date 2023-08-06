# utils.py

import tqdm
import time
import pymongo
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait

class scrap_reddit:
    
    def __init__(self, starting_url, banned_words = None, client_name = None, db_name = None,
                 collection_name = None):
        
        options = Options()
        #options.headless = True
        self.driver = webdriver.Firefox(options=options)
        self.starting_url = starting_url
        self.banned_words = banned_words
        self.driver.get(starting_url)
        self.client_name = client_name
        
        if self.client_name:
            self.client = pymongo.MongoClient(client_name)
            self.db = self.client[db_name]
            self.collection = self.db[collection_name]
        
    def check_banned_words(self,data):
        n = len([word for word in data["title"] if word in self.banned_words])
        n += len([word for word in data["post_content"] if word in self.banned_words])
        return n
        
    def parse(self, driver, url):
        
        driver.get(url)
        WebDriverWait(driver, 15).until(
            lambda driver: driver.find_elements(By.XPATH, "//h1[@class='_eYtD2XCVieq6emjKBH3m']")
            )
        title = driver.find_element(By.XPATH, "//h1[@class='_eYtD2XCVieq6emjKBH3m']").text
        post_content = driver.find_element(By.XPATH, "//p[@class='_1qeIAgB0cPwnLhDF9XSiJM']").text
        return {"title": title, "post_content": post_content, "url": url}
        
    def scrolldown(self,driver, bottom = False, n = 0 ):
        SCROLL_PAUSE_TIME = 3
        last_height = driver.execute_script("return document.body.scrollHeight")
        if bottom == True:
            while True:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(SCROLL_PAUSE_TIME)
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
        else:
            for i in range(n):            
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(SCROLL_PAUSE_TIME)
                new_height = driver.execute_script("return document.body.scrollHeight")
                last_height = new_height

    def get_jokes(self):
        self.scrolldown(driver = self.driver, bottom = True)
        posts = self.driver.find_elements(By.XPATH,
                                          "//a[@class='SQnoC3ObvgnGjWt90zD9Z _2INHSNB8V5eaWp4P0rY_mE']")
        urls = [post.get_attribute('href') for post in posts]
        self.list_of_insertion = []
        for url in tqdm.tqdm(urls, desc = 'Looping through urls found'):
            data = self.parse(driver = self.driver, url = url)
            time.sleep(3)
            if len(data["post_content"]) > 400 :
                continue
            if self.check_banned_words(data) > 0:
                continue
            self.list_of_insertion.append(data)

        self.collection.insert_many(self.list_of_insertion)
        self.driver.close()
