import sys
import json

from bs4 import BeautifulSoup
from selenium import webdriver

# NB: need to use PhantomJS because the ACLU page is all JavaScripty. :(
#      http://phantomjs.org/download.html
ACLU_URL = "https://www.aclu.org/"
PJS_WIN_PATH = "C:\\Program Files\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe"

def uniqify_preserve(mess):
    seen = {}
    result = []
    for item in mess:
        if item in seen:
            continue
        seen[item] = 1
        result.append(item)
    return result

if sys.platform == "win32":
    driver = webdriver.PhantomJS(executable_path=PJS_WIN_PATH)
else:
    driver = webdriver.PhantomJS()

driver.set_window_size(1366, 768)
driver.get(ACLU_URL)
issues_menu = driver.find_element_by_id("main_menu-issues")
# issues_menu = driver.find_element_by_css_selector(".issues-button-added-processed .js-added")
webdriver.ActionChains(driver).move_to_element(issues_menu).click(issues_menu).perform()

soup = BeautifulSoup(driver.page_source, "html.parser")
driver.close()

topics = []

for link in soup.find_all("a"):
    href = link.get("href")
    if href == None:
        continue

    if href.startswith("/issues/"):
        text = link.getText()
        if text.startswith("<img src"):
            continue
        topics.append(text)

topics = uniqify_preserve(topics)

with open('data/issues-aclu.json', 'w') as output:
    json.dump(topics, output, indent=2)
