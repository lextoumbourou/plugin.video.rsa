import requests
import re
from BeautifulSoup import BeautifulSoup

BASE_URL = 'http://comment.rsablogs.org.uk/videos/page/'
VIDEO_PAGE_URL = (
    'http://www.thersa.org/events/video?result_4377_result_page={0}')
RSA_ANIMATE_PAGE_URL = (
    'http://www.thersa.org/events/rsaanimate')


def get_videos(page_no):
    """
    Return videos from RSA > Events > Videos as a list of dicts
    """
    contents = requests.get(VIDEO_PAGE_URL.format(page_no))
    return scrape_videos(contents.text)


def scrape_videos(contents):
    """
    Turn RSA Video HTML into list of dicts
    """
    output = []
    soup = BeautifulSoup(contents)
    posts = soup.findAll('div', 'video-result')

    for post in posts:
        h3 = post.find('h3')
        title_link = h3.find('a')
        thumbnail = post.find('img')['src']

        output.append({
            'title': title_link.text,
            'url': title_link['href'],
            'thumbnail': thumbnail
        })

    return output


def get_youtube_id_from_video(url):
    """
    Turn RSA Video page HTML into a youtube ID string
    """
    contents = requests.get(url)
    return scrape_video_page(contents.text)


def scrape_video_page(contents):
    soup = BeautifulSoup(contents)
    youtube_id = None
    iframe = soup.findAll('iframe')[0]
    if iframe is not None:
        url = iframe["src"]
        if url.startswith("//www.youtube.com/"):
            youtube_id = url.split('/')[-1]
    else:
        obj = contents.find('object')
        for param in obj.findAll("param"):
            if param["name"] in ["movie", "src"]:
                url = param["value"]
                youtube_id = url.split('/')[-1]

    return youtube_id


def get_rsa_animate_videos():
    """
    Returns videos from RSA > RSA Animate as list of dicts
    """
    contents = requests.get(RSA_ANIMATE_PAGE_URL)
    return scrape_rsa_animate_videos(contents.text)


def scrape_rsa_animate_videos(contents):
    """
    Scrapes the RSA Animate Video site
    Returns an array of dictionaries
    """
    output = []
    soup = BeautifulSoup(contents)
    posts = soup.findAll('div', 'post')

    for post in posts:
        title = post.h3.a.string
        title = clean_rsa_animate_title(title)

        date = post.find(
            'p', 'postmetadata').find('span', 'alignleft')
        ifram = (post.findAll('p')[1]).find('iframe')
        if ifram is not None:
            url = ifram["src"]
            if url.startswith("//www.youtube.com/"):
                url = "http:" + url
        else:
            obj = post.findAll('p')[1].find('object')
            for param in obj.findAll("param"):
                if param["name"] in ["movie", "src"]:
                    url = param["value"]

        if url is not None and url.startswith("http://www.youtube.com/"):
            final_title = "{0} ({1})".format(title, date.string)
            output.append(
                {'title': final_title, 'url': url})

    return output


def clean_rsa_animate_title(title):
    """
    Assorted cleanups
    """
    # Remove Unicode characters
    title = re.sub('&#8211; ', '', title)
    # Remove the unneccessary prefix
    title = re.sub('RSA Animate', '', title)
    # Remove white space
    title = title.lstrip(' ')

    return title
