import sys
import os
import xbmcgui
import xbmcplugin
import xbmcaddon
import urllib
import re

#addon name
__addonname__ = 'plugin.video.myvideo'

#get path the default.py is in.
__addonpath__ = xbmcaddon.Addon(id=__addonname__).getAddonInfo('path')

#datapath
__datapath__ = xbmc.translatePath('special://profile/addon_data/'+__addonname__)

#append lib directory
sys.path.append( os.path.join( __addonpath__, 'resources', 'lib' ) )


import gethtml


def get_html(url):
    return gethtml.get(url, __datapath__)

addon_handle = int(sys.argv[1])

xbmcplugin.setContent(addon_handle, 'movies')

#urls = ["http://www.xvideos.com/video11036330/0/splendid_mom_ariella_ferrera_gets_nailed_on_the_couch",
#        "http://www.xvideos.com/video14481755/0/asian_hottie_cindy_starfall_fucks_and_gets_a_creampie",]
        #"http://www.xvideos.com/video8991790/beata_and_vanessa_sweet_punishment",
        #"http://www.xvideos.com/video10455445/vanessa_sky_was_all_set_and_ready_to_hit",
        #"http://www.xvideos.com/video6912062/sweet_exgf_swallow",
        #"http://www.xvideos.com/video7792032/big_juggs_teen_august_ames_gets_her_pussy_railed_by_big_cock",
        #"http://www.xvideos.com/video9688257/august_ames_gets_fucked_in_the_bathroom",
        #"http://www.xvideos.com/video9472632/busty_amateur_girlfriend_pleasing_dude",
        #"http://www.xvideos.com/video4312598/passionate_love_making_for_this_lustfilled_couple",
        #"http://www.xvideos.com/video10639164/mia_khalifa_interracial_threesome",
        #]"""

def getItems(url):
    print "Opening", url
    html = get_html(url)
    match = re.compile('flv_url=(.+?)&amp').findall(html)
    fetchurl = urllib.unquote(match[0])
    print 'fetchurl: %s' % fetchurl
    tit = re.compile('<h2>(.+?)<span class="duration">').findall(html)
    img = re.compile('url_bigthumb=(.+?)&amp').findall(html)
    print 'title: %s' % tit[0]
    print 'image: %s' % img[0]
    return tit[0], fetchurl, img[0]

r = get_html("http://xvideos.com")

ptn = re.compile("<a href=\"(/video.+?)\"><img")
urls = ["http://xvideos.com/%s" % i.strip() for i in ptn.findall(r)]


for u in urls:
    t,f,i = getItems(u)

    li = xbmcgui.ListItem(t, iconImage=i, path=f)
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=f, listitem=li)


xbmcplugin.endOfDirectory(addon_handle)
