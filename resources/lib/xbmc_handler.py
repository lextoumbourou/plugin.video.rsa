import sys
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin

# Add on info
__addon__ = xbmcaddon.Addon()
__addon_id__ = __addon__.getAddonInfo('id')
__addon_id_int__ = int(sys.argv[1])
__addon_dir__ = xbmc.translatePath(__addon__.getAddonInfo('path'))


def get_params():
    params = {}
    # The plugin will be called with arguments,
    # we want to get the second argument with is the parameters
    paramstring = sys.argv[2]
    # Check params exist
    if len(paramstring) >= 2:
        all_params = sys.argv[2]
        if (all_params[len(all_params)-1] == '/'):
                all_params = all_params[0:len(all_params)-2]
        # Remove the '?'
        all_params = all_params.replace('?', '')
        # split param string into individual params
        pair_params = all_params.split('&')

        for p in pair_params:
            split = p.split('=')
            # Set dictionary mapping of key : value
            params[split[0]] = split[1]

    return params


def add_video_link(title, url):
    # The Youtube ID is the 4th value with array split
    id = url.split('/')[4]
    # URL to call the Youtube plugin
    youtube_url = (
        'plugin://plugin.video.youtube?action=play_video&videoid=%s' % (id))

    # Create a new XBMC List Item and provide the title
    list_item = xbmcgui.ListItem(title)
    list_item.setProperty('IsPlayable', 'true')

    return xbmcplugin.addDirectoryItem(
        __addon_id_int__, youtube_url, list_item)


def add_next_page(page_no):
    page_no = str(page_no)
    list_item = xbmcgui.ListItem('Next Page')
    url = sys.argv[0] + '?page_no=' + page_no

    return xbmcplugin.addDirectoryItem(
        __addon_id_int__, url=url,
        listitem=list_item, isFolder=True, totalItems=5)


def end_directory():
    return xbmcplugin.endOfDirectory(__addon_id_int__)
