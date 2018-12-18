from bs4 import BeautifulSoup
import time
import requests
import re
import types
PTT_URL = "https://www.ptt.cc"


def init():
    global img_urls
    img_urls = []  # A list to store images


def get_web_page(url):
    time.sleep(0.1)
    resp = requests.get(  # if the web page have Cookies, auto fill-in it.
        url=url,
        cookies={'over18': '1'}
    )
    if resp.status_code != 200:
        print('Invalid url:', resp.url)
        return None
    else:
        return resp.text


def save_image():
    global img_urls
    articles = []
    current_page = get_web_page(PTT_URL + '/bbs/Beauty/index.html')
    if current_page:
        month = time.strftime("%m").lstrip('0')  # Today's date format, to fit PTT URL format.(ex. 03/28 --> 3/28)
        day = int(time.strftime("%d"))
        for i in range(3):
            date = month + "/" + str(day - i)  # Access the last three days articles
            current_articles, prev_url = get_articles(current_page, date, 3)
            while current_articles:  # if current page has articles we want to add
                articles += current_articles # add them
                current_page = get_web_page(PTT_URL + prev_url)  # ready to previous page
                current_articles, prev_url = get_articles(current_page, date, 3)  # Go!
            for article in articles:
                page = get_web_page(PTT_URL + article['href'])  # Enter the article
                if page:
                    img_urls = parse(page)  # Store every image hyperlink


def parse(dom):
    global img_urls
    soup = BeautifulSoup(dom, 'html.parser')
    links = soup.find(id='main-content').find_all('a')
    # The code below is to get the image's link
    for link in links:
        if re.match(r'^https?://(i.)?(m.)?imgur.com', link['href']):
            img_urls.append(link['href'])
    return img_urls


def get_articles(dom, date, threshold):
    soup = BeautifulSoup(dom, 'html.parser')  # Get the html
    # To access prev_url
    paging_div = soup.find('div', 'btn-group btn-group-paging')
    prev_url = paging_div.find_all('a')[1]['href']

    articles = []
    divs = soup.find_all('div', 'r-ent')
    for d in divs:
        if d.find('div', 'date').string.strip() == date:  # The date is correct
            # To Access the push_count
            push_count = 0
            if d.find('div', 'nrec').string:
                try:
                    push_count = int(d.find('div', 'nrec').string)  # String to integer
                except ValueError:
                    pass
            if push_count > threshold:  # Get the articles which is "push >= threshold"
                # To access the href & title
                if d.find('a'):  # Have a href, the article is existed (not empty)
                    href = d.find('a')['href']
                    title = d.find('a').string
                    articles.append({
                        'title': title,
                        'href': href,
                        'push_count': push_count
                    })

    return articles, prev_url


def money():
    articles = []
    current_page = get_web_page(PTT_URL + '/bbs/Lifeismoney/index.html')
    if current_page:
        date = time.strftime("%m/%d").lstrip('0')  # Today's date format, to fit PTT URL format.
        current_articles, prev_url = get_articles(current_page, date, 0)
        while current_articles:  # if current page has articles we want to add
            articles += current_articles  # add them
            current_page = get_web_page(PTT_URL + prev_url)  # ready to previous page
            current_articles, prev_url = get_articles(current_page, date, 0)  # Go!
        message = "貼文:\n\n"
        for x in articles:
            message = message + x["title"] + "\n"  # Title
            message = message + PTT_URL + x["href"] + "\n"  # Hyperlink
            message = message + "推文數:" + str(x["push_count"]) + "\n"  # Push_Count

        return message
