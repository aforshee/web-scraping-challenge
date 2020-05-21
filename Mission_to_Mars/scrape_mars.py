import pandas as pd
import requests
from bs4 import BeautifulSoup
from splinter import Browser
import re
import time


def scrape():

    news_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    info_url = 'https://space-facts.com/mars/'
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    mars_data = {}

    executable_path = {'executable_path': "chromedriver"}
    browser = Browser('chrome', **executable_path, headless=False)

    browser.visit(news_url)
    news_title_results = []
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    news_title = soup.find_all('div', class_='content_title')
    for title in news_title:
        news_title_to_print = title.text
        news_title_results.append(news_title_to_print)
    mars_data['news_titles'] = news_title_results

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    news_p = soup.find_all('div', class_='article_teaser_body')
    mars_data['news_paragraphs'] = news_p

    browser.visit(image_url)
    image_results = []
    image_title_results = []
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    featured_image_url = soup.find_all(class_='img')
    for image in featured_image_url:
        #print image source
        link = image.img['src']
        images_to_print = ('https://www.jpl.nasa.gov' + link)
        image_results.append(images_to_print)
        #print alternate text
        image_title_to_print = image.img['alt']
        image_title_results.append(image_title_to_print)
    mars_data['image_links'] = image_results
    mars_data['image_titles_'] = image_title_results

    # Retrieve page with the requests module
    response = requests.get(twitter_url)
    # Create BeautifulSoup object; parse with 'lxml'
    soup = BeautifulSoup(response.text, 'lxml')
    results = soup.find_all('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')
    # Loop through returned results
    for result in results:
    # Error handling
        try:
            # Identify and return price of listing
            mars_weather = result.text
            #print(mars_weather)
        except Exception as e:
            print(e)
    mars_weather = results[0]
    mars_data['twitter_info'] = mars_weather
    

    tables = pd.read_html(info_url)
    df = tables[0]
    html_table = df.to_html()
    mars_data['mars_facts_html_table'] = html_table
    
    browser.visit(hemisphere_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    header_links = soup.find_all('div', class_='description')
    results = []
    for row in header_links:
        link =row.a['href']
        link_to_print = ('https://astrogeology.usgs.gov/' + link)
        results.append(link_to_print)
        #print(link_to_print)
    mars_data['image_header_links']=results

    url = mars_data['image_header_links'][0]
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    results = []
    images = soup.find_all(class_='wide-image')
    for image in images:
        #print image source
        link = image['src']
        link_to_print = ('https://astrogeology.usgs.gov' + link)
        results.append(link_to_print)

    url = mars_data['image_header_links'][1]
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    images = soup.find_all(class_='wide-image')
    for image in images:
        #print image source
        link = image['src']
        link_to_print = ('https://astrogeology.usgs.gov' + link)
        results.append(link_to_print)

    url = mars_data['image_header_links'][2]
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    images = soup.find_all(class_='wide-image')
    for image in images:
        #print image source
        link = image['src']
        link_to_print = ('https://astrogeology.usgs.gov' + link)
        results.append(link_to_print)

    url = mars_data['image_header_links'][3]
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    images = soup.find_all(class_='wide-image')
    for image in images:
        #print image source
        link = image['src']
        link_to_print = ('https://astrogeology.usgs.gov' + link)
        results.append(link_to_print)
    
    mars_data['usgs_image_links'] = results
    
    browser.quit()      

    return(mars_data)

