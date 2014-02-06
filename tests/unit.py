import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from resources.lib import rsa

class UnitTests(unittest.TestCase):
    def test_scraped_video_page_returns_list_of_dicts(self):
        contents = """
            <div class="video-result">
                <img src="thumb_url">
                <h3>
                    <a href="video_url">Video Title</a></h3>
                    <p></p>
          </div>
        """
        results = rsa.scrape_videos(contents)
        self.assertTrue(results[0]['title'] == 'Video Title')
        self.assertTrue(results[0]['thumbnail'] == 'thumb_url')

if __name__ == '__main__':
    unittest.main()
