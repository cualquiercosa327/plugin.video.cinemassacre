# Copyright 2014 cdwertmann


# ------------------------------------------------------------------------------
# 2016
# Updated By esc0rtd3w [http://github.com/esc0rtd3w]
# ------------------------------------------------------------------------------

# fanart.jpg source: http://the-great-pipmax.deviantart.com/art/cinemassacre-chainsaw-camera-386865336


import base64
import binascii
import hashlib
import hmac
import os
import re
import sys
import time
import urllib
import urllib2
import urlparse
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import xmltodict

from datetime import datetime, date
from types import *

# Importing BeautifulSoup
from bs4 import *

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])
PLUGIN_NAME = "plugin.video.cinemassacre"

site_base = "http://cinemassacre.com/"

try:
    import StorageServer
except:
    import storageserverdummy as StorageServer

# cache for one hour
cache = StorageServer.StorageServer(PLUGIN_NAME, 1)

cache.table_name = PLUGIN_NAME
#cache.set("some_string", "string")
#save_data = { "some_string": "string", "some_int": 1234, "some_dict": repr({ "our": { "dictionary": [] } }) }
#cache.setMulti("pre-", save_data)

# Youtube Video ID (MOSTLY OBSOLETE AS OF 2016)
def videoIdYoutube(value):
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?.*?(?=v=)v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')

    youtube_regex_match = re.match(youtube_regex, value)
	
    if youtube_regex_match:
        return youtube_regex_match.group(6)

    return youtube_regex_match

def getSignature(key, msg):
    return base64.b64encode(hmac.new(key, msg, hashlib.sha1).digest())

def buildUrl(query):
    return base_url + '?' + urllib.urlencode(query)

# Default Log
def log(msg):
    xbmc.log(PLUGIN_NAME + ": "+ str(msg), level=xbmc.LOGNOTICE)

# Log With Additional Text Display
def logPlus(msg, label):
    xbmc.log(PLUGIN_NAME + ": "+ str(label) + str(msg), level=xbmc.LOGNOTICE)


# Read Content From XML
def getContentFromXML():

    # devicetoken=binascii.b2a_hex(os.urandom(32))
    # deviceuid=binascii.b2a_hex(os.urandom(20)).upper()
    # signature=getSignature(os.urandom(20),os.urandom(20))
    # timestamp=datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z")
    #URL="http://cinemassacre.screenwavemedia.com/AppServer/SWMAppFeed.php?appname=Cinemassacre&appversion=1.5.8&devicetoken="+devicetoken+"&deviceuid="+deviceuid+"&lastupdateid=0&timestamp="+timestamp+"&signature="+signature
    #req = urllib2.Request(URL)
    #response = urllib2.urlopen(req)
    #xml = response.read()
    #response.close()
	
    addon = xbmcaddon.Addon()
    addon_path = addon.getAddonInfo('path')
    _path = os.path.join(addon_path,'site.xml')
    f = open(_path, 'r')
    xml = f.read()
    return xmltodict.parse(xml)['document']


def getCategoriesFromXML(content,id):

    #logPlus(content, "content: ")
    #logPlus(id, "id: ")
	
    items = []
	
    #if id=="":
    #    listitem=xbmcgui.ListItem("- All Videos Sorted By Date -", iconImage="DefaultFolder.png")
    #    url = buildUrl({'id': "all"})
    #    items.append((url, listitem, True))

    if id=="all":
        xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_DATE)
    else:
        xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_LABEL)

    for cat in content['MainCategory']:
        if cat['@parent_id'] == id:
            #if cat['@activeInd'] == "N": continue
			
            listitem=xbmcgui.ListItem(cat['@name'], iconImage="DefaultFolder.png")
            url = buildUrl({'id': cat['@id']})
            items.append((url, listitem, True))
    
    if id!="" or id=="all":
        count=0
        for clip in content['item']:
            if clip['movieURL']=="" or clip['@activeInd'] == "N": continue
            cat_tag=clip['categories']['category']
            cat=None
            if type(cat_tag)==DictType:
                if cat_tag['@id']==id: cat=[cat_tag['@id']]
            elif type(cat_tag)==ListType:
                for c in cat_tag:
                    if c['@id']==id: cat=c['@id']

            if not cat and id!="all": continue
            url = clip['movieURL']
			
            if not "http" in url:
                #url = "http://video1.screenwavemedia.com/Cinemassacre/smil:"+url+".smil/playlist.m3u8"
                url = "http://content.jwplatform.com/manifests/"+url+".m3u8"
				
            elif "youtu" in url:
                #url = "plugin://plugin.video.youtube/?action=play_video&videoid="+videoIdYoutube(url)
                url = "plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid="+videoIdYoutube(url)
				
            date=None
            airdate=None
            if clip['pubDate']:
                # python bug http://stackoverflow.com/questions/2609259/converting-string-to-datetime-object-in-python
                d=clip['pubDate'][:-6]
				
                # python bug http://forum.xbmc.org/showthread.php?tid=112916
                try:
                    d=datetime.strptime(d, '%a, %d %b %Y %H:%M:%S')
                except TypeError:
                    d=datetime(*(time.strptime(d, '%a, %d %b %Y %H:%M:%S')[0:6]))

                date=d.strftime('%d.%m.%Y')
                airdate=d.strftime('%Y-%m-%d')
            count+=1
            listitem=xbmcgui.ListItem (clip['title'], thumbnailImage=clip['smallThumbnail'], iconImage='DefaultVideo.png')
            listitem.setInfo( type="Video", infoLabels={ "title": clip['title'], "plot": clip['description'], "aired": airdate, "date": date, "count": count})
            listitem.setProperty('IsPlayable', 'true')
            listitem.addStreamInfo('video', {'duration': clip['duration']})
            items.append((url, listitem, False))

    xbmcplugin.addDirectoryItems(addon_handle,items)
	

def pageDump(web_url, page_num):
	
    req = urllib2.Request(web_url + "/page/" + page_num, headers={ 'User-Agent': 'CasperTheFriendlyGhost/v1.0' })
    html = urllib2.urlopen(req).read()

    soup = BeautifulSoup(html, "html.parser")

    for html in soup.find_all("div", {"class": "archiveitem"}):
        temp_grab = (html.get('Permanent'))
        #tempGrab = findSections(html)
		
        #logPlus(web_url, "web_url: ")
        #logPlus(html, "html: ")
        #logPlus(temp_grab, "temp_grab: ")
		
    # Get "link" for XML Output
    for temp_grab in soup.find_all('a'):
        temp_link = (temp_grab.get('href'))
        logPlus(temp_link, "temp_link: ")
		
    # Get "smallThumbnail" for XML Output
    for temp_grab in soup.find_all('img'):
        temp_small_thumbnail = (temp_grab.get('src'))
        logPlus(temp_small_thumbnail, "temp_small_thumbnail: ")
	
	
def findSections(source, text):
    soup = BeautifulSoup(source, "html.parser")
    sections = soup.find_all("div", {"class": "archiveitem"})
    for sec in sections:
        fr = sec.find("Permanent")
        url, img = fr["href"], fr.find("img")["src"]
        name, size =  sec.select("h3.title a")[0].text, sec.select("span.details")[0].text.split(None,1)[-1]
        yield url, name, img,size


		
pageDump(site_base + "category/avgn/avgnepisodes", "1")
pageDump(site_base + "category/avgn/avgnepisodes", "2")
pageDump(site_base + "category/avgn/avgnepisodes", "3")
pageDump(site_base + "category/avgn/avgnepisodes", "4")
pageDump(site_base + "category/avgn/avgnepisodes", "5")
pageDump(site_base + "category/avgn/avgnepisodes", "6")


xbmcplugin.setContent(addon_handle, "episodes")
id = ''.join(args.get('id', ""))
content = cache.cacheFunction(getContentFromXML)
getCategoriesFromXML(content, id)

xbmcplugin.endOfDirectory(addon_handle)

# Media Info View
xbmc.executebuiltin('Container.SetViewMode(504)')
