from bs4 import BeautifulSoup as bs 
import requests
from splinter import Browser
from urllib.parse import urljoin
import pandas as pd
from pprint import pprint
import time
import datetime as dt

def mars_news():
    #url to scrape
    url= "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"

    executable_path = {'executable_path': 'chromedriver'} #path to chromedriver; in this case it's in the same file
    browser = Browser('chrome', **executable_path, headless = False) #gives us a broswer object

    browser.visit(url)#visit url

    html_code = browser.html #get html text from page
    soup = bs(html_code, "html.parser") #beautiful soup to parse
    
    news_title = soup.find_all("div", class_='content_title')[0].text #title of first article 
    news_p = soup.find_all('div', class_="article_teaser_body")[0].text #paragraph of first article
    
    browser.quit()
    return [news_title, news_p] #return a dict of title and paragraph


def featured_image():

    url= "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

    executable_path = {'executable_path': 'chromedriver'} #path to chromedriver; in this case it's in the same file
    browser = Browser('chrome', **executable_path, headless = False) #gives us a broswer object

    browser.visit(url)#visit url

    html_code = browser.html #get html text from page
    soup = bs(html_code, "html.parser") #beautiful soup to parse

    button=browser.find_by_id('full_image') #find button
    button.click() #click button

    html2=browser.html #get html from new page
    soup2 = bs(html2, "html.parser") #beautiful soup to parse new page

    browser.quit() #quit browser

    class_containing_img=soup2.find('a',class_='button fancybox')['data-link'] #gets relative image link "/img.jpg"

    return urljoin(url, class_containing_img) #join base url and relative url


def hemispheres():
    url= "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    executable_path = {'executable_path': 'chromedriver'} #path to chromedriver; in this case it's in the same file
    browser = Browser('chrome', **executable_path, headless = False) #gives us a broswer object

    browser.visit(url)#visit url

    html_code = browser.html #get html text from page
    soup = bs(html_code, "html.parser") #beautiful soup to parse

    data = soup.find('div', class_='collapsible results').find_all('div', class_='item')

    data_dict = []
    for i in range(len(data)):
        title = data[i].find('div', class_="description").find('h3').text
        browser.find_by_css('div[class="collapsible results"]').find_by_css('div[class="item"]')[i].find_by_css('div[class="description"]').find_by_css('a').click()
        for img in browser.find_by_css('div[class="downloads"]').find_by_css('a'):
            if ('Original' in img.text):
                img_url = img['href']

        browser.back()
        mydict = {'title': title, 'img_url': img_url}
        data_dict.append(mydict)
        
    return data_dict
    
def twitter_weather():
    url= "https://twitter.com/marswxreport?lang=en"

    executable_path = {'executable_path': 'chromedriver'} #path to chromedriver; in this case it's in the same file
    browser = Browser('chrome', **executable_path, headless = False) #gives us a broswer object

    browser.visit(url)#visit url

    html_code = browser.html #get html text from page
    soup = bs(html_code, "html.parser") #beautiful soup to parse

    browser.quit() #quit browser
    
    return soup.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text #get first tweet; text only

def mars_facts():

    url= "https://space-facts.com/mars/" #url to scrape

    tables= pd.read_html(url) #read html
    df=pd.DataFrame(tables[0]) #convert all tables to dfs ;only select the first table [0]

    return df.to_html() #return html

def scrape_all():
    mydict={}
    headline=mars_news()
    mydict['headline']=headline
    # img=featured_image()
    # mydict['img']=img
    hemis=hemispheres()
    mydict['hemis']=hemis
    twit=twitter_weather()
    mydict['twit']=twit
    # table=mars_facts()
    # mydict['table']=table

    return  mydict

if __name__ == "__main__":

    # If running as script, print scraped data
    scrape_all()

# scrape_all()