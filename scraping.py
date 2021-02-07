# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=True)

def scrape_all():
    # Initiate headless driver for deployment
    # from webdriver_manager.chrome import ChromeDriverManager
    # executable_path = {'executable_path': ChromeDriverManager().install()}
    # browser = Browser('chrome', **executable_path, headless=False)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title"       : news_title,
        "news_paragraph"   : news_paragraph,
        "featured_image"   : featured_image(browser),
        "facts"            : mars_facts(),
        "last_modified"    : dt.datetime.now(),
        "hemispheres"      : hem_img()
    }

    # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one("ul.item_list li.slide")
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find("div", class_="content_title").get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find("div", class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


def featured_image(browser):
    # Visit URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'

    return img_url

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

def hem_img():
    # 1. Use browser to visit the URL 
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    html_soup = soup(html, 'html.parser')

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []
    
    
    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    # Gets title of first image
    tag_box   = html_soup.find_all('div', class_='description')
    em = 5
    
    for tag in tag_box:
        browser.visit(url)
        img_title = tag.find("h3").text
    
    # Clicking can happen before or after scaping first page, html stored in html_soup
    # But does change browser object
        link = browser.find_by_tag("a")[em]
        link.click()
        html = browser.html
    
    # Soups up new page and find .png link
        summ_soup = soup(html, 'html.parser')
        summ_page = summ_soup.find("ul")
    
    # Get href (img link)
        img_link = summ_page.find("a", href = True)
        img_url  = img_link["href"]
    
        
        HS = {"img_url" : img_url,
              "img_title" : img_title}
    
        hemisphere_image_urls.append(HS)
        em = em + 2
    return(hemisphere_image_urls)

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())




