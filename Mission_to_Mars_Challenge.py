
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

# Set the executable path and initialize the chrome browser in splinter
# Initiate headless driver for deployment
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=True)

# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)

html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide')

slide_elem.find("div", class_='content_title')

# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p

# Featured Images

# Visit URL
url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use the base URL to create an absolute URL
img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
img_url

df = pd.read_html('http://space-facts.com/mars/')[0]
df.columns=['description', 'value']
df.set_index('description', inplace=True)
df


# Deliverable 1

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
# 4. Print the list that holds the dictionary of each image url and title.
[print(i) for i in hemisphere_image_urls]

# 5. Quit the browser
browser.quit()
