# NASA Mars News

from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import pandas as pd
import time

def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def scrape_info():
    browser = init_browser()

    # create empty dictionary to store variables
    mars = {}

    # ------------------
    # Mars News
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    time.sleep(2)

    # Create BeautifulSoup object
    html=browser.html
    soup = bs(html, 'html.parser')

    # Collect the latest News Title and Paragraph Text
    results = soup.find('div', class_="list_text")
    
    # news title results
    news_title = results.find('div', class_='content_title').text
    # paragraph results
    news_p = results.find('div', class_='article_teaser_body').text

    # add to dictionary
    mars["news_title"] = news_title
    mars["news_p"] = news_p
    

    # ------------------
    # JPL Mars Space Images - Featured Image
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)
    
    browser.find_by_id('full_image').click()
    time.sleep(2)
    
    browser.click_link_by_partial_text('more info')
    html=browser.html
    soup = bs(html, 'html.parser')
    jpl_results = soup.find('figure', class_='lede').a.img['src']
    
    jpl_home = 'https://www.jpl.nasa.gov'
    mars_image = jpl_home + jpl_results
    
    # add to mars dictionary
    mars["featured_img"] = mars_image
    mars


    # ------------------
    # Mars Facts
    mars_facts_url = 'https://space-facts.com/mars/'
    facts_table = pd.read_html(mars_facts_url)
    mars_table = (facts_table[0])
    mars_table = mars_table.set_index(0)
    mars_table.index.name = ''
    mars_table.columns = ['']
    mars_html = mars_table.to_html()
    mars_html.replace('\n', '')

    # add to mars dictionary
    mars["facts"] = mars_html


    # ------------------
    # Mars Hemispheres
    mars_hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(mars_hemi_url)
    hemisphere_image_urls = []

    hemisphere_link = browser.find_by_css('a.product-item h3')
    for i in range(len(hemisphere_link)):
        hemisphere = {}
        browser.find_by_css('a.product-item h3')[i].click()
        element = browser.find_by_text('Sample').first
        hemisphere["img_url"] = element['href']
        hemisphere["title"] = browser.find_by_css('h2.title').text
        
        hemisphere_image_urls.append(hemisphere)
        browser.back()
    
    # add to mars dictionary
    mars["hemisphere"] = hemisphere_image_urls
    
    return mars

if __name__== "__main__":
    print(scrape_info())



