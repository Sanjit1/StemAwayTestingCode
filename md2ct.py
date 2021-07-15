import json
import time
from selenium import webdriver
import csv 

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--allow-insecure-localhost')

home_page_browser = webdriver.Chrome(options=options)
post_page_browser = webdriver.Chrome(options=options)
home_page_url = "https://community.cartalk.com/"
home_page_request = home_page_browser.get(home_page_url)
for each in range(0,20):
    home_page_browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(0.4)
post_list = home_page_browser.find_element_by_class_name('topic-list').find_element_by_tag_name('tbody').find_elements_by_tag_name("tr")
post_information_list = []
for each in post_list:
    post_page_url = each.find_element_by_class_name('main-link').find_elements_by_tag_name("span")[0].find_elements_by_tag_name("a")[0].get_attribute('href').encode("utf-8")
    post_page_request = post_page_browser.get(post_page_url)
    height = post_page_browser.execute_script("return document.body.scrollHeight")
    while True:
        post_page_browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.4)
        if height == post_page_browser.execute_script("return document.body.scrollHeight"):
            break
        height = post_page_browser.execute_script("return document.body.scrollHeight")
    try:
        reply_post_list = post_page_browser.find_element_by_class_name('post-stream').find_elements_by_class_name("topic-post")
        words = 0
        for reply_post in reply_post_list:
            try:
                words += len(reply_post.find_element_by_class_name('contents').get_attribute('innerText').encode("utf-8").split())
            except:
                reply_post_list.remove(reply_post)

        post_information_list.append({
            "words": words,
            "topic": each.find_element_by_class_name('main-link').find_elements_by_tag_name("span")[0].find_elements_by_tag_name("a")[0].get_attribute('innerHTML').encode("utf-8"),
            "category": each.find_element_by_class_name('main-link').find_elements_by_class_name('category-name')[0].get_attribute('innerHTML').encode("utf-8") if len(each.find_element_by_class_name('main-link').find_elements_by_class_name('category-name')) > 0 else "None",
            "replies": len(reply_post_list),
            "views": each.find_element_by_class_name('views').find_elements_by_tag_name("span")[0].get_attribute('innerHTML').encode("utf-8")
            })
    except:
        post_list.remove(each)
    

print(post_information_list)

mycroft_csv_file = open("cartalk.csv", 'w')
mycroft_csv_writer = csv.writer(mycroft_csv_file)

mycroft_csv_writer.writerow(post_information_list[0].keys())
for post_info in post_information_list:
    mycroft_csv_writer.writerow(post_info.values())
    

mycroft_csv_file.close()