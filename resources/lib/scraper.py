import urllib2
import re
from BeautifulSoup import BeautifulSoup

base_url = 'http://comment.rsablogs.org.uk/videos/page/'


def open_page(url):
    """Return the contents of a page as a string"""
    # Fool the page into thinking it's a request from Firefox on Windows
    user_agent = (
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) '
        'Gecko/2008092417 Firefox/3.0.3')

    # Open a request URL object (which is what we'll use to get the page)
    req = urllib2.Request(url)
    # Tell the object to use the user agent
    req.add_header('User_Agent', user_agent)
    # Open the URL with the urlopen method
    response = urllib2.urlopen(req)
    # Read the response
    output = response.read()
    response.close()

    return output.decode('ascii', 'ignore')


def scrape_site(contents):
    """
    Scrapes the RSA Animate Video site
    Returns an array of dictionaries
    """
    output = []

    # Using BeautifulSoup to parse the HTML
    soup = BeautifulSoup(str(contents))

    # All the H3s on the page appear to be video titles,
    # let get the title string from each one
    posts = soup.findAll('div', 'post')

    for post in posts:
        # Clean titles
        title = post.h3.a.string
        # Remove Unicode characters
        title = re.sub('&#8211; ', '', title)
        # Remove the unneccessary prefix
        title = re.sub('RSA Animate', '', title)
        # Remove white space
        title = title.lstrip(' ')

        # Get the dates
        date = post.find('p', 'postmetadata').find('span', 'alignleft')
        # Get the Youtube URLs
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
            final_title = title + ' (' + date.string + ')'
            output.append(
                {'title': final_title, 'url': url})

    return output

if __name__ == '__main__':
    contents = open_page(base_url + '1')
    print scrape_site(contents)
