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

site_xml = 'site.xml'

try:
    import StorageServer
except:
    import storageserverdummy as StorageServer

# cache for one hour
cache = StorageServer.StorageServer(PLUGIN_NAME, 1)


# cache.table_name = PLUGIN_NAME
# cache.set("some_string", "string")
# save_data = { "some_string": "string", "some_int": 1234, "some_dict": repr({ "our": { "dictionary": [] } }) }
# cache.setMulti("pre-", save_data)

def doNothing():
    nothing = ""


# Default Log
def log(msg):
    xbmc.log(PLUGIN_NAME + ": " + str(msg), level=xbmc.LOGNOTICE)


# Log With Additional Text Display
def logPlus(msg, label):
    xbmc.log(PLUGIN_NAME + ": " + str(label) + str(msg), level=xbmc.LOGNOTICE)


def getPageLinks(web_url, page_num):
    request = urllib2.Request(web_url + "/page/" + str(page_num), headers={'User-Agent': 'CasperTheFriendlyGhost/v1.0'})
    response = urllib2.urlopen(request)
    output = response.read()
    response.close()
    soup = BeautifulSoup(output, "html.parser")
    episodes = soup.findAll("div", class_="archiveitem")

    links = []
    counter = 0
    for element in episodes:
        if counter < 50:
            link = episodes[counter].a["href"]
            counter += 1
            links.append(link)

    return links


def CATEGORIES():
    addDir('Latest Videos', 'http://cinemassacre.com/2016/', 1, '')
    addDir('Shows', '', 1, '')
    addDir('Angry Video Game Nerd', 'http://cinemassacre.com/category/avgn/', 1, '')
    addDir('Games', '', 1, '')
    addDir('Movies', '', 1, '')
    addDir('Original Films', '', 1, '')
    addDir('Music', '', 1, '')
    addDir('Site', '', 1, '')


def INDEX(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'CasperTheFriendlyGhost/v1.0')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    # match=re.compile('').findall(link)
    match = re.compile('(.?)http:\/\/cinemassacre.com\/[0-9][0-9][0-9][0-9]\/[0-9][0-9]\/[0-9][0-9](.*?)"').findall(
        link)
    logPlus(match, "match: ")
    for thumbnail, url, name in match:
        addDir(name, url, 2, thumbnail)


def getJsConfigFile(url_js):
    req = urllib2.Request(url_js)
    req.add_header('User-Agent', 'CasperTheFriendlyGhost/v1.0')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    # match=re.compile('').findall(link)
    match = re.compile('content.jwplatform.com\/players\/(.*?)js').find(link)
    match = "http:\\" + match
    return match


def parseJsFile(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'CasperTheFriendlyGhost/v1.0')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    # match=re.compile('').findall(link)
    playlist = re.compile('content.jwplatform.com\/manifests\/(.*?)m3u8').findall(link)
    videos_mp4 = re.compile('content.jwplatform.com\/videos\/(.*?)mp4').findall(link)
    audio_aac = re.compile('content.jwplatform.com\/videos\/(.*?)m4a').findall(link)
    vtt = re.compile('content.jwplatform.com\/strips\/(.*?)vtt').findall(link)

    logPlus(playlist, "playlist: ")
    logPlus(videos_mp4, "videos_mp4: ")
    logPlus(audio_aac, "audio_aac: ")
    logPlus(vtt, "vtt: ")

    video = ""

    return playlist


def VIDEOLINKS(url, name):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'CasperTheFriendlyGhost/v1.0')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    # match=re.compile('').findall(link)
    for url in match:
        addLink(name, url, '')


def get_params():
    param = []
    paramstring = sys.argv[2]
    if len(paramstring) >= 2:
        params = sys.argv[2]
        cleanedparams = params.replace('?', '')
        if (params[len(params) - 1] == '/'):
            params = params[0:len(params) - 2]
        pairsofparams = cleanedparams.split('&')
        param = {}
        for i in range(len(pairsofparams)):
            splitparams = {}
            splitparams = pairsofparams[i].split('=')
            if (len(splitparams)) == 2:
                param[splitparams[0]] = splitparams[1]

    return param


def addLink(name, url, iconimage):
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"Title": name})
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=liz)
    return ok


def addDir(name, url, mode, iconimage):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"Title": name})
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    return ok


params = get_params()
url = None
name = None
mode = None

try:
    url = urllib.unquote_plus(params["url"])
except:
    pass
try:
    name = urllib.unquote_plus(params["name"])
except:
    pass
try:
    mode = int(params["mode"])
except:
    pass

# print
# "Mode: " + str(mode)
# print
# "URL: " + str(url)
# print
# "Name: " + str(name)

if mode == None or url == None or len(url) < 1:
    # print
    # ""
    CATEGORIES()

elif mode == 1:
    # print
    # "" + url
    INDEX(url)

elif mode == 2:
    # print
    # "" + url
    url_js = getJsConfigFile(url)
    video = parseJsFile(getJsConfigFile(url_js))
    VIDEOLINKS(video, name)

xbmcplugin.endOfDirectory(int(sys.argv[1]))

# Media Info View
xbmc.executebuiltin('Container.SetViewMode(504)')
