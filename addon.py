import sys
import xbmcaddon
from xbmcswift2 import Plugin

from resources.lib import scraper, xbmc_handler

plugin = Plugin()

@plugin.route('/')
def index():
    items = [{
        'label': 'RSA Animate',
        'path': plugin.url_for('rsa_animate', page_no=1),
    }]

    return items

@plugin.route('/rsa_animate/<page_no>')
def rsa_animate(page_no):
    if page_no is None:
        page_no = 1
    else:
        page_no = int(page_no) + 1

    contents = scraper.open_page(
        'http://comment.rsablogs.org.uk/videos/page/{0}'.format(page_no)
    )

    video_list = scraper.scrape_site(contents)
    youtube_url = (
        'plugin://plugin.video.youtube?action=play_video&videoid={0}')

    items = []
    for video in video_list:
        items.append({
            'label': video['title'],
            'path': youtube_url.format(video['url'])
         })

    if video_list:
        items.append({
            'label': 'Next Page',
            'path': plugin.url_for('rsa_animate', page_no=page_no + 1)
        })

    return items

if __name__ == '__main__':
    plugin.run()
