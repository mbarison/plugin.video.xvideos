import sys
import os
from xbmc import Keyboard
from xbmcaddon import Addon
import xbmcgui
import xbmcplugin
import xbmcaddon
import urllib
import re

from xbmcswift2 import Plugin

plugin = Plugin()

#addon name
__addonname__ = plugin.addon.getAddonInfo('id')

#get path the default.py is in.
__addonpath__ = plugin.addon.getAddonInfo('path')

#datapath
__datapath__ = xbmc.translatePath('special://profile/addon_data/'+__addonname__)

#append lib directory
sys.path.append( os.path.join( __addonpath__, 'resources', 'lib' ) )


import gethtml


def get_html(url):
    return gethtml.get(url, __datapath__)

#addon_handle = int(sys.argv[1])

#xbmcplugin.setContent(addon_handle, 'videos')


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

@plugin.route('/')
def main_menu():
    items = [{'label': "Show Latest Videos", 'path': plugin.url_for('show_latest')},
             {'label': "Show Best Videos", 'path': plugin.url_for('show_best')},
             {'label': "Search Videos", 'path': plugin.url_for('search')},
             ]
    
    return items


@plugin.route('/show_latest')
def show_latest():
    r = get_html("http://xvideos.com")

    ptn = re.compile("<a href=\"(/video.+?)\"><img")
    urls = ["http://xvideos.com/%s" % i.strip() for i in ptn.findall(r)]

    items = []
    for u in urls:
        t,f,i = getItems(u)

        items.append({'label': t, 'path': plugin.url_for("play_video",url=f), 'thumbnail' : i})
        
    return items

@plugin.route('/show_best')
def show_best():
    r = get_html("http://xvideos.com/best")

    ptn = re.compile("<a href=\"(/video.+?)\"><img")
    urls = ["http://xvideos.com/%s" % i.strip() for i in ptn.findall(r)]

    items = []
    for u in urls:
        t,f,i = getItems(u)

        items.append({'label': t, 'path': plugin.url_for("play_video",url=f), 'thumbnail' : i})
        
    return items

@plugin.route('/profiles/<nm>')
def show_profile(nm):
    print "Inside show_profile(%s)" % nm
    
    print "Opening %s" % ("http://xvideos.com/profiles/%s/videos" % nm)
    r = get_html("http://xvideos.com/profiles/%s/videos" % nm)

    ptn = re.compile('<a href="(/prof-video-click.+?)"><img')
    urls = ["http://xvideos.com/%s" % i.strip() for i in ptn.findall(r)]

    items = []
    for u in urls:
        t,f,i = getItems(u)

        items.append({'label': t, 'path': plugin.url_for("play_video",url=f), 'thumbnail' : i})
        
    return items

@plugin.route('/search')
def search():
    kb = Keyboard('', "Insert search term")
    kb.doModal()
    if (kb.isConfirmed()):
        search_item = urllib.quote(kb.getText().strip())
    else:
        return
    
    r = get_html("http://xvideos.com/?k=%s" % search_item)

    # see if there's a profile
    pro_ptn = re.compile('<img src="(http://.+?jpg)" data-videos=\'\[\]\' /></a></div><p><a href="(/profiles/.+?)">(.+?)</a>')

    items = []

    if pro_ptn.search(r):
        icon,lnk,nm = pro_ptn.findall(r)[0]
        lnk =  plugin.url_for('show_profile',nm=os.path.basename(lnk))
        nm = "[Profile] %s" % nm       
        items.append({'label': nm, 'path': lnk, 'thumbnail' : icon}) 

    ptn = re.compile("<a href=\"(/video.+?)\"><img")
    urls = ["http://xvideos.com/%s" % i.strip() for i in ptn.findall(r)]

    for u in urls:
        t,f,i = getItems(u)

        items.append({'label': t, 'path': plugin.url_for("play_video",url=f), 'thumbnail' : i})
        
    return items

@plugin.route('/play_video/<url>/')
def play_video(url):
    plugin.log.info('Playing url: %s' % url)
    plugin.set_resolved_url(url)

plugin.run()
