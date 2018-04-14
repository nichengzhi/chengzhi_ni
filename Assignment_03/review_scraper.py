from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
import random
normal_delay = random.normalvariate(2, 0.5)
from datetime import datetime ,date
from bs4 import BeautifulSoup
import re
import pandas as pd
#beacuse i need more data, so scrape all the review.
#end_date = datetime(2017,1,1)
#review_list = pd.DataFrame(columns = ["name","date","text","score"])
'''driver = webdriver.Firefox(executable_path=r'geckodriver.exe')
driver.get('https://www.amazon.com/RockBirds-Flashlights-Bright-Aluminum-Flashlight/product-reviews/B00X61AJYM')
sort_element = driver.find_element_by_xpath("""//*[@id="sort-order-dropdown"]""")
webdriver.ActionChains(driver).move_to_element(sort_element).click(sort_element).perform()
recent_element = driver.find_element_by_xpath("""//*[@id="sort-order-dropdown_1"]""")
webdriver.ActionChains(driver).move_to_element(recent_element).click(recent_element).perform()
time.sleep(random.uniform(0.5, 1.5))
filter_element = driver.find_element_by_xpath("""//*[@id="reviewer-type-dropdown"]""")
webdriver.ActionChains(driver).move_to_element(filter_element).click(filter_element).perform()
time.sleep(random.uniform(0.5, 1.5))
verified_purchase_element = driver.find_element_by_xpath("""//*[@id="reviewer-type-dropdown_1"]""")
webdriver.ActionChains(driver).move_to_element(verified_purchase_element).click(verified_purchase_element).perform()
time.sleep(random.uniform(0.5, 1.5))
while True:
    reviews_element = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, "cm_cr-review_list"))
    )
    reviews_html = reviews_element.get_attribute('innerHTML')
    time.sleep(random.uniform(0.5, 1.5))
    review_soup = BeautifulSoup(reviews_html, "html.parser")
    reviews = review_soup.find_all("div",{"class":"a-section review"})
    for review in reviews:
        score = float(review.find("a",{"class":"a-link-normal"}).text.split()[0])
        name = review.find("a",{"data-hook":"review-author"}).text
        date_string=review.find("span",{"data-hook":"review-date"}).text
        review_date = datetime.strptime(re.sub('on|,',  '',date_string).strip(),"%B %d %Y")
        if review_date < end_date:
            break
        text = review.find("span",{"data-hook":"review-body"}).text
        review_list.loc[-1] = [name,str(review_date) , text,score]
        review_list.index = review_list.index + 1
        review_list = review_list.sort_index()
        review_list = review_list.drop_duplicates()
    time.sleep(random.uniform(0.5, 1.5))
    if review_date > end_date:
        next_element = driver.find_element_by_class_name("a-last")
        driver.execute_script("arguments[0].scrollIntoView();", next_element)
        time.sleep(random.uniform(0.5, 1.5))
        webdriver.ActionChains(driver).move_to_element(next_element).click(next_element).perform()
    else:
        driver.close()
        break'''

review_list = pd.DataFrame(columns = ["name","date","text","score","name_tag"])
driver = webdriver.Firefox(executable_path=r'geckodriver.exe')
driver.get('https://www.amazon.com/RockBirds-Flashlights-Bright-Aluminum-Flashlight/product-reviews/B00X61AJYM')
sort_element = driver.find_element_by_xpath("""//*[@id="sort-order-dropdown"]""")
webdriver.ActionChains(driver).move_to_element(sort_element).click(sort_element).perform()
recent_element = driver.find_element_by_xpath("""//*[@id="sort-order-dropdown_1"]""")
webdriver.ActionChains(driver).move_to_element(recent_element).click(recent_element).perform()
time.sleep(random.uniform(0.5, 1.5))
filter_element = driver.find_element_by_xpath("""//*[@id="reviewer-type-dropdown"]""")
webdriver.ActionChains(driver).move_to_element(filter_element).click(filter_element).perform()
time.sleep(random.uniform(0.5, 1.5))
verified_purchase_element = driver.find_element_by_xpath("""//*[@id="reviewer-type-dropdown_1"]""")
webdriver.ActionChains(driver).move_to_element(verified_purchase_element).click(verified_purchase_element).perform()
time.sleep(random.uniform(0.5, 1.5))
while True:
    reviews_element = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, "cm_cr-review_list"))
    )
    reviews_html = reviews_element.get_attribute('innerHTML')
    time.sleep(random.uniform(0.5, 1.5))
    review_soup = BeautifulSoup(reviews_html, "html.parser")
    reviews = review_soup.find_all("div",{"class":"a-section review"})
    for review in reviews:
        score = float(review.find("a",{"class":"a-link-normal"}).text.split()[0])
        name = review.find("a",{"data-hook":"review-author"}).text
        date_string=review.find("span",{"data-hook":"review-date"}).text
        review_date = datetime.strptime(re.sub('on|,',  '',date_string).strip(),"%B %d %Y")
        try:
            name_tag = re.sub('By{}|{}'.format(name,date_string),'',review.find("a",{"data-hook":"review-author"}).parent.parent.text)
        except:
            name_tag == ''
        if name_tag == '':
            name_tag = "no tag"
        text = review.find("span",{"data-hook":"review-body"}).text
        review_list.loc[-1] = [name,str(review_date) , text,score,name_tag]
        review_list.index = review_list.index + 1
        review_list = review_list.sort_index()
        review_list = review_list.drop_duplicates()
    time.sleep(random.uniform(0.5, 1.5))
    next_element = driver.find_element_by_class_name("a-last")
    try:
        next_element_a = next_element.find_element_by_tag_name("a")
    except:
        driver.close()
        break
    if next_element_a.get_attribute('href') is not None:

        driver.execute_script("arguments[0].scrollIntoView();", next_element)
        time.sleep(random.uniform(0.5, 1.5))
        webdriver.ActionChains(driver).move_to_element(next_element).click(next_element).perform()
    else:
        driver.close()
        break


with open('reviews.json', 'w') as f:
    f.write(review_list.to_json(orient='records', lines=True))