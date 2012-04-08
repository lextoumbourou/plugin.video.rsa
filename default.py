import re
import sys
import xbmcaddon

from resources.lib import scraper, xbmc_handler

### get addon info
__addon__             = xbmcaddon.Addon()
__addonid__           = __addon__.getAddonInfo('id')
__addonidint__        = int(sys.argv[1])

params = xbmc_handler.get_params()

def main(params):
	# See if page number is set, or set it to 1 
	try:
		page_no = int(params['page_no'])
	except:
		page_no = 1

	contents = scraper.open_page('http://comment.rsablogs.org.uk/videos/page/'+str(page_no))
	video_list = scraper.scrape_site(contents)

	for video in video_list:
		xbmc_handler.add_video_link(video['title'], video['url'])

	xbmc_handler.add_next(page_no + 1)
	xbmc_handler.end_directory()

if __name__ == '__main__':
	main()


	
	
