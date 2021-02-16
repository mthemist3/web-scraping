#!/usr/bin/env python
# coding: utf-8

from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd


def mars_news(browser):
# Visit the website Mars_news
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    # Scrape page into Soup
    html = browser.html
    news_soup = bs(html, "html.parser")

    # searching through different elements to find what we're looking for
    # need to get very specific to not confuse the search
   news_title = news_soup.find_all('div', class_='content_title')[0].text
   news_p = news_soup.find_all('div', class_='article_teaser_body')[0].text

    return news_title, news_p
    # print(news_title)
    # print(news_p)

def featured_image(browser):
    # Scraping Mars Image
    url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"

    # Visit Website
    browser.visit(url)

    # Find and click the full image button
    full_image= browser.find_by_tag('button')[1]
    full_image.click()

    # Scrape page into Soup
    html_image = browser.html
    image_soup = bs(html_image, 'html.parser')

    # find url with src
    img_url = image_soup.find("img", class_="fancybox-image").get("src")

    # create a final URL
    final_img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url}'
    return final_img_url
    # print(final_img_url)


def mars_facts():
    # Mars Facts
    facts_df = pd.read_html('http://space-facts.com/mars/')[0]
    # df.head()
    # give 2 columns headers and replace the index
    facts_df.columns= ['Description','Mars']
    facts_df.set_index('Description',inplace=True)
    # df.head()
    # Convert to html
    facts_df.to_html(classes=["table-bordered", "table-striped"])
    return facts_df


def hemispheres(browser):
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    # For Loop to find each value for each picture (4 total)
    hemisphere_image_urls = []
    for i in range(4):
        browser.find_by_css("a.product-item h3")[i].click()
        hemi_data = scrape_hemisphere(browser.html)
        # Append the information into a list
        hemisphere_image_urls.append(hemi_data)
        browser.back()

    return hemisphere_image_urls


def scrape_hemisphere(html_text):
    # parse html text
    hemi_soup = bs(html_text, "html.parser")

    # adding try/except for error handling
    try:
        title_elem = hemi_soup.find("h2", class_="title").get_text()
        sample_elem = hemi_soup.find("a", text="Sample").get("href")

    except AttributeError:
        # Image error will return None, for better front-end handling
        title_elem = None
        sample_elem = None

    hemispheres = {
        "title": title_elem,
        "img_url": sample_elem
    }

    return hemispheres

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())
