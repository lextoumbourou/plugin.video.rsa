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
    return scrape_video_list(contents.text)


def scrape_video_list(contents):
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
    return scrape_video_page(contents.text.encode('utf-8', 'ignore'))


def scrape_video_page(contents):
    soup = BeautifulSoup(contents)
    youtube_id_meta = soup.find('meta', attrs={'name': 'youtube_url'})
    if youtube_id_meta:
        # Occassionally the meta tags with the youtube id have 
        # URLs in them, this extracts the Youtube ID in such cases
        if youtube_id_meta['content'].startswith('http://youtu.be/'):
            youtube_id = youtube_id_meta['content'].split('/')[-1]
        else:
            youtube_id = youtube_id_meta['content']
    
        return youtube_id


def get_rsa_animate_videos():
    """
    Returns videos from RSA > RSA Animate as list of dicts
    """
    contents = requests.get(RSA_ANIMATE_PAGE_URL)
    return scrape_video_list(contents.text.encode('utf-8', 'ignore'))


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
