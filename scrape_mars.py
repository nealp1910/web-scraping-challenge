#!/usr/bin/env python
# coding: utf-8

#Import Dependencies 
from bs4 import BeautifulSoup
from splinter import Browser
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from webdriver_manager.chrome import ChromeDriverManager
import os
import requests
import time
import pandas as pd
import numpy as np

##############################################################################
########## Part 1: Scraping ########## 
##### NASA Mars News #####

def scrape():


    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #Scrape from site https://redplanetscience.com/ 
    #Retrieve data for news_title & news_p
    url = "https://redplanetscience.com/"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # Examine the results, then determine element that contains sought info
    print(soup.prettify())

    #Finding the latest news title and latest news teaser body
    news_title = soup.find('div', class_='content_title').text
    news_paragraph = soup.find('div', class_='article_teaser_body').text

    print(news_title)
    print('--------------------------------------------------------------------')
    print(news_paragraph)

    ##### JPL Mars Spece Images - Featured Image #####
    #Scrape from site https://spaceimages-mars.com/
    url = "https://spaceimages-mars.com/"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # Url of the Featured Image
    image_path = soup.find_all('img')[1]["src"]
    featured_image_url = url + image_path
    featured_image_url

    ##### Mars Facts #####
    #Scrape from site https://galaxyfacts-mars.com/
    url = "https://galaxyfacts-mars.com/"
    browser.visit(url)
    html = browser.html

    # Visit the Mars Facts webpage and use Pandas to scrape the table containing facts about the planet including diameter, mass, etc
    table = pd.read_html(url)
    mars_planet_profile = table[1]
    # mars_planet_profile

    # Rename Columns
    mars_planet_profile.columns = ['', 'Values']
    mars_planet_profile.set_index('', inplace = True)
    mars_planet_profile

    # Use Pandas to convert the data to a HTML table string.
    mars_planet_profile.to_html('table.html')


    ##### Mars Hemispheres #####
    # Visit the astrogeology site to obtain high-resolution images for each hemisphere of Mars.
    url = "https://marshemispheres.com/"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    #Save the image URL string for the full resolution hemisphere image and the hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys img_url and title.
    hemisphere_image_urls=[]
    products = soup.find ('div', class_='result-list')
    hemispheres = products.find_all('div',{'class':'item'})

    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://marshemispheres.com/" + end_link    
        browser.visit(image_link)
        html_hemispheres = browser.html
        soup=BeautifulSoup(html_hemispheres, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        hemisphere_image_urls.append({"title": title, "img_url": image_url})
            
    hemisphere_image_urls

    browser.quit()

    return hemisphere_image_urls