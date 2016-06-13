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

#cache.table_name = PLUGIN_NAME
#cache.set("some_string", "string")
#save_data = { "some_string": "string", "some_int": 1234, "some_dict": repr({ "our": { "dictionary": [] } }) }
#cache.setMulti("pre-", save_data)

def doNothing():
    nothing=""

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
	
	
def findValidLinks(blob, type):
    
    # Get "Dated" URLs
    get_dated = (r'(\/\d\d\d\d\/\d\d\/\d\d\/)')
    #get_dated = (r'(\/\d\d\d\d\/\d\d\/\d\d\/)[^\d]')
	
    temp = re.compile(get_dated, re.DOTALL + re.MULTILINE + re.UNICODE)
    temp_link = temp.findall(blob)
    logPlus(temp, "temp: ")
    logPlus(temp_link, "temp_link: ")

    return temp_link
	

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
	
    addon = xbmcaddon.Addon()
    addon_path = addon.getAddonInfo('path')
    _path = os.path.join(addon_path, site_xml)
    f = open(_path, 'r')
    xml = f.read()
    return xmltodict.parse(xml)['document']


def getCategoriesFromXML(content, id):
	
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
	
	
def getTitle(data):

    try:
        #request = urllib2.Request(web_url + "/page/" + page_num, headers={ 'User-Agent': 'CasperTheFriendlyGhost/v1.0' })
        #html = urllib2.urlopen(request).read()
        #soup = BeautifulSoup(data, "html.parser")
        #link = soup.find('a', 'title')
        #value = link['href']
        #logPlus(value, "value: ")

        return {data}
		

    except:
        error_msg = xbmcgui.Dialog()
        error_msg.ok("Error!", "Could Not Get Title From HTML Source")
		

def pageDump(web_url, page_num):
	
    request = urllib2.Request(web_url + "/page/" + page_num, headers={ 'User-Agent': 'CasperTheFriendlyGhost/v1.0' })
    #blob = urllib2.urlopen(request).read()
    #soup = BeautifulSoup(blob, "html.parser")
	
    response = urllib2.urlopen(request)
    output = response.read()
    #logPlus(output, "output: ")
    response.close()

    soup = BeautifulSoup(output, "html.parser")
    #episodes = soup.findAll("div", {"class": "archiveitem"})
    episodes = soup.findAll("div", class_="archiveitem")
	
    list = {}
    for element in episodes:
        list[element.a["href"]] = {}
	
    #episodes[0].a["href"]
    #episodes[0].find(href="")
		
    return list
	

def getPageLinks(page_dump):

    #links = []
    #html = page_dump
    #logPlus(page_dump, "page_dump: ")
    #soup = BeautifulSoup(page_dump, "html.parser")
    #episode = soup.find("div", "archiveitem")
    #logPlus(episode, "episode: ")
    #links = [site_base + div.a["href"] for div in soup.findAll("div")]
    #logPlus(links, "links: ")
    #links = page_dump
    return page_dump
    #for link in links:
      #return link


def dumpSite():
    
    # more_data = "0"
    # cur_page = "0"
    # max_page = "20"
	
    # # By Date
    # cur_day = "0"
    # max_day = "31"
    # cur_month = "0"
    # max_month = "12"
    # cur_year = "2005"
    # max_year = "2016"
    # cur_date = "0"
    # max_date = max_year + "/" + max_month + "/" + max_day
	
    # while cur_year <= max_year:
	
        # cur_day = cur_day + 1
	
        # cur_date = cur_year + "/" + cur_month + "/" + cur_day
        # cur_link = site_base + "/" + cur_date + "/"
		
        # if cur_day == max_day:
            # cur_month += 1
            # #break
		
        # if cur_month == max_month:
            # cur_year += 1
            # #break
		
        # if cur_year == max_year:
            # more_data = "1"
        # break
			
        # # Advance Page Forward
        # cur_page += 1
		
        # pageDump(site_base + "/" + cur_year + "/", cur_page)
        # pageDump(site_base + "/" + cur_year + "/" + cur_month + "/", cur_page)
        # pageDump(site_base + "/" + cur_year + "/" + cur_month + "/" + cur_day + "/", cur_page)
	
        # logPlus(cur_date, "cur_date: ")
        # logPlus(cur_link, "cur_link: ")
        # logPlus(cur_page, "cur_page: ")
        # logPlus(cur_day, "cur_day: ")
        # logPlus(cur_month, "cur_month: ")
        # logPlus(cur_year, "cur_year: ")
	
	
	
	
    # Angry Video Game Nerd
    #pageDump(site_base + "category/avgn/avgnepisodes", "1")
    test1 = getPageLinks(pageDump(site_base + "category/avgn/avgnepisodes", "1"))
    #test1 = pageDump(site_base + "category/avgn/avgnepisodes", "1")
    logPlus(test1, "test1: ")
    
    #pageDump(site_base + "category/avgn/avgnepisodes", "2")
    #pageDump(site_base + "category/avgn/avgnepisodes", "3")
    #pageDump(site_base + "category/avgn/avgnepisodes", "4")
    #pageDump(site_base + "category/avgn/avgnepisodes", "5")
    #pageDump(site_base + "category/avgn/avgnepisodes", "6")
	
    # James and Mike Mondays
    #pageDump(site_base + "category/jamesandmike", "1")
    #pageDump(site_base + "category/jamesandmike", "2")
    #pageDump(site_base + "category/jamesandmike", "3")
    #pageDump(site_base + "category/jamesandmike", "4")
    #pageDump(site_base + "category/jamesandmike", "5")
    #pageDump(site_base + "category/jamesandmike", "6")
    #pageDump(site_base + "category/jamesandmike", "7")
	
    # Mike and Ryan
    #pageDump(site_base + "category/mikeryantalkaboutgames", "1")
	
    # Mike and Bootsy
    #pageDump(site_base + "category/mike-bootsy", "1")
	
    # Board James
    #pageDump(site_base + "category/boardjames", "1")
    #pageDump(site_base + "category/boardjames", "2")
	
    # You Know Whats Bullshit
    #pageDump(site_base + "category/ykwb", "1")
    #pageDump(site_base + "category/ykwb", "2")
	
    # Mikes Gaming Videos
    #pageDump(site_base + "category/mikevideos", "1")
    #pageDump(site_base + "category/mikevideos", "2")
    #pageDump(site_base + "category/mikevideos", "3")
	
    # Bootsy Beats
    #pageDump(site_base + "category/bootsy-beats", "1")
	
    # James Gaming Videos
    #pageDump(site_base + "category/jamesgamingvideos", "1")
	
    # Other Gaming Videos
    #pageDump(site_base + "category/othergaming-videos", "1")
	
    # Game Collection
    #pageDump(site_base + "2007/03/22/game-collection", "1")
	
    # Movie Reviews A-Z
    #pageDump(site_base + "category/moviereviewsatoz", "1")
    #pageDump(site_base + "category/moviereviewsatoz", "2")
    #pageDump(site_base + "category/moviereviewsatoz", "3")
    #pageDump(site_base + "category/moviereviewsatoz", "4")
    #pageDump(site_base + "category/moviereviewsatoz", "5")
    #pageDump(site_base + "category/moviereviewsatoz", "6")
    #pageDump(site_base + "category/moviereviewsatoz", "7")
    #pageDump(site_base + "category/moviereviewsatoz", "8")
    #pageDump(site_base + "category/moviereviewsatoz", "9")
    #pageDump(site_base + "category/moviereviewsatoz", "10")
    #pageDump(site_base + "category/moviereviewsatoz", "11")
    #pageDump(site_base + "category/moviereviewsatoz", "12")
    #pageDump(site_base + "category/moviereviewsatoz", "13")
    #pageDump(site_base + "category/moviereviewsatoz", "14")
    #pageDump(site_base + "category/moviereviewsatoz", "15")
	
    # Top Tens
    #pageDump(site_base + "category/moviereviews/top-tens", "1")
	
    # Animation Related
    #pageDump(site_base + "category/moviereviews/animation-moviereviews", "1")
	
    # Commentaries
    #pageDump(site_base + "category/moviereviews/commentaries", "1")
	
    # Interviews
    #pageDump(site_base + "category/moviereviews/interviews", "1")
	
    # Location Tours
    #pageDump(site_base + "category/location-tours", "1")
	
    # Monster Madness
    #pageDump(site_base + "category/moviereviews/monstermadness", "1")
	
    # Trivia Videos
    #pageDump(site_base + "category/trivia-videos", "1")
	
    # Other Movie Related Videos
    #pageDump(site_base + "category/othermovierelatedvideos", "1")
	
    # Original Films Main
    #pageDump(site_base + "category/films", "1")
    #pageDump(site_base + "category/films", "2")
    #pageDump(site_base + "category/films", "3")
    #pageDump(site_base + "category/films", "4")
	
    # Favorites
    #pageDump(site_base + "category/films/favorites", "1")
	
    # Animation
    #pageDump(site_base + "category/films/animation", "1")
	
    # Horror Films
    #pageDump(site_base + "category/films/horror-films", "1")
    #pageDump(site_base + "category/films/horror-films", "2")
	
    # Comedy
    #pageDump(site_base + "category/films/comedy", "1")
	
    # 48-Hour Films
    #pageDump(site_base + "category/films/48-hour-films", "1")
	
    # Other
    #pageDump(site_base + "category/films/other", "1")
	
    # Music Main
    #pageDump(site_base + "category/music-2", "1")
	
    # Audio Slaughter
    #pageDump(site_base + "category/music-2/audio-slaughter", "1")
	
    # Kyle Justin
    #pageDump(site_base + "category/music-2/kylejustin", "1")
	
    # Name That Tune
    #pageDump(site_base + "category/music-2/namethattune", "1")
	
    # Site Main
    #pageDump(site_base + "category/site-2", "1")
	
    # Articles
    #pageDump(site_base + "category/site-2/featuredarticles", "1")
	
    # Appearances
    #pageDump(site_base + "category/site-2/appearances", "1")
	
    # Misc Videos
    #pageDump(site_base + "category/site-2/misc-videos", "1")


try:
    dumpSite()
except:
    doNothing()

xbmcplugin.setContent(addon_handle, "episodes")
id = ''.join(args.get('id', ""))
content = cache.cacheFunction(getContentFromXML)
getCategoriesFromXML(content, id)

xbmcplugin.endOfDirectory(addon_handle)

# Media Info View
xbmc.executebuiltin('Container.SetViewMode(504)')
