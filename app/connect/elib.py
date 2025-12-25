from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

def scripe(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(1)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'lxml')
    return soup

def find_author_name(soup: BeautifulSoup):
    items = soup.find_all('div')
    div_num = 0
    for n, i in enumerate(items, start=0):
        tags = i.find_all('span', class_='aster')
        for j in tags:
            if j.text == '*':
                div_num = n
    return items[div_num].find('b').text

def find_university_name(soup: BeautifulSoup):
    items = soup.find_all('div')
    div_num = 0
    for n, i in enumerate(items, start=0):
        tags = i.find_all('td', class_='midtext')
        for j in tags:
            if j.text == '*':
                div_num = n
        return items[div_num].find('a')

def find_count_articles(soup: BeautifulSoup):
    items = soup.find_all('td')
    td_num = 0
    for n, i in enumerate(items, start=0):
        tags = i.find_all('font')
        for j in tags:
            if j.text == "Всего найдено":
                td_num = n
    return items[td_num].find_all('font')[1].text

def find_article(soup: BeautifulSoup, span_num = 0):
    items = soup.find_all('span', attrs={'style': 'line-height:1.0;'})
    return items

def main(args):
    url = "https://elibrary.ru/author_profile.asp?authorid=997309"
    soup = scripe(url)
    print(f"""Author: {find_author_name(soup)}
University: {find_university_name(soup)}
Count of articles: {find_count_articles(soup)}
Article 1: {find_article(soup)}
""")

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))