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
    time.sleep(4)
    return driver

def souper(driver: webdriver.Chrome):
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
    university = None
    count_articles = None
    for i in soup.find_all('div'):
        for j in i.find_all('td', class_='midtext'):
            for a in j.find_all("a"):
                if a.get('href', '').startswith("org_about"):
                    university = a.text
                if a.get('title', '').startswith("Полный список публикаций автора"):
                    count_articles = a.text
    return university, count_articles

# def find_count_articles(soup: BeautifulSoup):
#     items = soup.find_all('td')
#     td_num = 0
#     for n, i in enumerate(items, start=0):
#         tags = i.find_all('font')
#         for j in tags:
#             if j.text == "Всего найдено":
#                 td_num = n
#     return items[td_num].find_all('font')[1].text

def find_articles(soup: BeautifulSoup):
    data = []
    for items in soup.find_all('span', attrs={'style': "overflow-wrap: break-word;"}):
        span = items.findChild().findChild()
        data.append({
            "name": span.text,
            "href": items.find('a').get('href', '')
        })
    return data

def get_reference(driver: webdriver.Chrome):
    # button = driver.find_element(By.XPATH, "//a[@href='javascript:for_reference()']")
    button = driver.find_element(By.T, "Ссылка для цитирования")
    button.click()
    # driver.execute_script("https://elibrary.ru/javascript:for_reference()")
    time.sleep(3)
    element = driver.find_element(By.ID, "ref")
    return element.text

def main(args):
#     url = "https://elibrary.ru/author_profile.asp?authorid=997309"
#     soup = scripe(url)
#     univer, count = find_university_name(soup)
#     print(f"""Author: {find_author_name(soup)}
# University: {univer}
# Count of articles: {count}
# """)
    # url_articles = "https://elibrary.ru/author_items.asp?authorid=997309"
    # driver = scripe(url_articles)
    # soup_articles = souper(driver)
    # print(find_articles(soup_articles))
    url_article = "https://elibrary.ru/item.asp?id=47455088"
    driver = scripe(url_article)
    print(get_reference(driver))
    driver.quit()

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
