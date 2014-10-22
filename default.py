# -*- coding: utf-8 -*-
# Copyright 2014 cdwertmann

import sys
import xbmcgui
import xbmcplugin
import urllib
import urllib2
import urlparse
import hmac
import hashlib
import base64
import os
import binascii
import time
from datetime import datetime, date
from resources.xmltodict import xmltodict
from types import *

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])
PLUGIN_NAME = "plugin.video.cinemassacre"

try:
    import StorageServer
except:
    import storageserverdummy as StorageServer

# cache for one hour
cache = StorageServer.StorageServer(PLUGIN_NAME, 1)

def get_signature(key, msg):
    return base64.b64encode(hmac.new(key, msg, hashlib.sha1).digest())

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

def log(msg):
    xbmc.log(PLUGIN_NAME + ": "+ str(msg), level=xbmc.LOGNOTICE)

def getContent():
    devicetoken=binascii.b2a_hex(os.urandom(32))
    deviceuid=binascii.b2a_hex(os.urandom(20)).upper()
    signature=get_signature(os.urandom(10),os.urandom(20))
    timestamp=datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z")
    URL="http://cinemassacre.screenwavemedia.com/AppServer/SWMAppFeed.php?appname=Cinemassacre&appversion=1.5.8&devicetoken="+devicetoken+"&deviceuid="+deviceuid+"&lastupdateid=0&timestamp="+timestamp+"&signature="+signature
    log(URL)
    req = urllib2.Request(URL)
    response = urllib2.urlopen(req)
    xml=response.read()
    response.close()
    return xmltodict.parse(xml)['document']

def getCategories(content,id):
    items = []
    for cat in content['MainCategory']:
        if cat['@parent_id'] == id:
            if cat['@activeInd'] == "N": continue
            listitem=xbmcgui.ListItem(cat['@name'], iconImage="DefaultFolder.png")
            url = build_url({'id': cat['@id']})
            items.append((url, listitem, True))
    
    xbmcplugin.addDirectoryItems(addon_handle,items)
    items = []
    # no videos in root category
    if cat=="": return

    for clip in content['item']:
        for cat in clip['categories']['category']:
            if type(cat) != DictType: continue # FIX ME
            if cat['@activeInd'] == "N": continue
            if cat['@id']==id:
                url = clip['movieURL']
                if not "http" in url:
                    url = "http://video1.screenwavemedia.com/Cinemassacre/smil:"+clip['movieURL']+".smil/playlist.m3u8"
                date=None
                if clip['pubDate']:
                    # python bug http://stackoverflow.com/questions/2609259/converting-string-to-datetime-object-in-python
                    date=clip['pubDate'][:-6]
                    # python bug http://forum.xbmc.org/showthread.php?tid=112916
                    try:
                        date=datetime.strptime(date, '%a, %d %b %Y %H:%M:%S')
                    except TypeError:
                        date=datetime(*(time.strptime(date, '%a, %d %b %Y %H:%M:%S')[0:6]))

                    date=date.strftime('%Y-%m-%d')
                listitem=xbmcgui.ListItem (clip['title'], thumbnailImage=clip['smallThumbnail'], iconImage='DefaultVideo.png')
                listitem.setInfo( type="Video", infoLabels={ "Title": clip['title'], "plot": clip['description'], "aired": date})
                listitem.addStreamInfo('video', {'duration': clip['duration']})
                items.append((url, listitem, False))

    xbmcplugin.addDirectoryItems(addon_handle,items)


xbmcplugin.setContent(addon_handle, "episodes")
xbmc.executebuiltin('Container.SetViewMode(504)')
id = ''.join(args.get('id', ""))
content = cache.cacheFunction(getContent)
getCategories(content, id)

xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_LABEL)
xbmcplugin.endOfDirectory(addon_handle)
