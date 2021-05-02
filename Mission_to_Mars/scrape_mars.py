from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    nasa = 'https://mars.nasa.gov/news/'
    browser.visit(nasa)

    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    latest_article = soup.find_all('div', class_='list_text')[0]
    news_title = latest_article.find('div', class_='content_title').text
    news_p = latest_article.find('div', class_='article_teaser_body').text

    url1 = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url1)

    time.sleep(1)

    html1 = browser.html
    soup1 = BeautifulSoup(html1, 'lxml')

    imgresult = soup1.find('img', class_="headerimage fade-in")['src']
    newurl = url1[:-11]
    featured_image_url = newurl + "/" + imgresult

    

    
    url2 = 'https://space-facts.com/mars/'
    time.sleep(1)
    tables = pd.read_html(url2)
    df = tables[0]
    df.columns = ["Description", "Mars"]
    df.set_index("Description")
    html_table = df.to_html()

    

    
    url3 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url3)
    time.sleep(1)
    html2 = browser.html
    soup2 = BeautifulSoup(html2, 'html.parser')

    links = soup2.find_all('div', class_="description")
    
    hemisphere_image_urls = []

    url4 = "https://astrogeology.usgs.gov"

    for link in links:

        img = link.find('a', class_="itemLink product-item")['href']
        title = link.find('h3').text

        browser.visit(url4 + img)
        time.sleep(1)

        html3 = browser.html
        soup3 = BeautifulSoup(html3, 'html.parser')

        img_url = url4 + soup3.find("img", class_="wide-image")["src"]

        hemisphere_image_urls.append({'title':title, 'img_url':img_url})
        

   
    mars_data = {
    "hemisphere_image_urls": hemisphere_image_urls,
    "news_title": news_title,
    "news_p": news_p,
    "html_table": html_table,
    "featured_image_url":featured_image_url
    }
    
        

    browser.quit()

    return mars_data



