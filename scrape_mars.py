from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
import requests

def scrape():
    news_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    response = requests.get(nasa_mars_news_url)
    soup = bs(response.text, "html.parser")
    title1 = soup.find('div', class_ = 'content_title').text.strip()
    news_p = soup.find('div', class_="rollover_description_inner").text.strip()

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    time.sleep(1)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(2)
    browser.click_link_by_partial_text('more info')
    html = browser.html
    soup = bs(html, 'html.parser')
    download_links = soup.find_all('div', class_='download_tiff')
    for link in download_links:
        if "JPG" in link.p.text:
            featured_image_url = link.a['href']
    browser.quit()

    mars_weather = "https://twitter.com/marswxreport?lang=en"
    response = requests.get(mars_weather)
    soup = bs(response.text, "html.parser")
    mars_weather = soup.find('p', class_ = 'tweet-text').text
    mars_weather = "pic".join(mars_weather.split("pic")[:-1])
    mars_weather = mars_weather.replace('\n','')

    facts_url = "https://space-facts.com/mars/"
    tables = pd.read_html(facts_url)
    facts_df = tables[2]
    facts_df.columns = ['item', 'value']
    facts_df = mars_facts_df.set_index('item')
    facts = mars_facts_df.to_dict()
    facts = mars_facts["value"]

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)
    time.sleep(3)
    mars_hemisphere = ["Cerberus Hemisphere", "Schiaparelli Hemisphere", "Syrtis Major Hemisphere", "Valles Marineris Hemisphere"]
    hemisphere_image_urls = []
    for hemisphere in mars_hemisphere:
        time.sleep(3)
        browser.click_link_by_partial_text(hemisphere)
        html = browser.html
        soup = bs(html, 'html.parser')
        downloads = soup.find_all('div', class_='downloads')
        for link in downloads:
            if "Sample" in link.li.text:
                my_dict = {'title': hemisphere, 'img_url': link.a['href']}
        hemisphere_image_urls.append(my_dict)
        time.sleep(1)
        browser.visit(hemisphere_url)
    browser.quit()

    data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "hemisphere_image_urls": hemisphere_image_urls,
        "mars_facts": mars_facts}
    return data