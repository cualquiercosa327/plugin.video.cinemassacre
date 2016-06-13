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
		

def getPageLinks(web_url, page_num):
	
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
	
    #links = {}
    links=[]
    counter = 0
    for element in episodes:
        #links[element.a.get_text()] = {}
        #links[element.a.get_text()]["href"] = element.a["href"]
        #links[element.a.get_text()]["title"] = element.a["title"]
        
        if counter < 50:
            link = episodes[counter].a["href"]
            counter += 1
            links.append(link)
		
    return links
	
	
def processLinks(page_base, page_max):

    page_counter = 1
    links = []
    while page_counter <= page_max:
        link = getPageLinks(site_base + page_base, str(page_counter))
        page_counter += 1
        links.append(link)
	
    return links
	
	
def processLinksAlt(page_base, page_start, page_max):

    page_counter = page_start
    links = []
    while page_counter <= page_max:
        link = getPageLinks(site_base + page_base, str(page_counter))
        page_counter += 1
        links.append(link)
	
    return links
	

def dumpPageByDate():
    
    more_data = "0"
    #cur_page = "0"
    #max_page = "20"
	
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
	
	
def dumpPageShows():
	
    # Angry Video Game Nerd
    links_avgn = processLinks("category/avgn/avgnepisodes", 6)
    #logPlus(links_avgn, "Links (SHOWS -> Angry Video Game Nerd): ")
	
    # James and Mike Mondays
    links_jmm = processLinks("category/jamesandmike", 7)
    #logPlus(links_jmm, "Links (SHOWS -> James and Mike Mondays): ")
	
    # Mike and Ryan
    links_mr = processLinks("category/mikeryantalkaboutgames", 1)
    #logPlus(links_mr, "Links (SHOWS -> Mike and Ryan): ")
	
    # Mike and Bootsy
    links_mb = processLinks("category/mike-bootsy", 1)
    #logPlus(links_mb, "Links (SHOWS -> Mike and Bootsy): ")
	
    # Board James
    links_bj = processLinks("category/boardjames", 1)
    #logPlus(links_bj, "Links (SHOWS -> Board James): ")
	
    # You Know Whats Bullshit
    links_ykwb = processLinks("category/ykwb", 2)
    #logPlus(links_ykwb, "Links (SHOWS -> You Know Whats Bullshit): ")
	
	
def dumpPageGames():
	
    # Mikes Gaming Videos
    links_mgv = processLinks("category/mikevideos", 3)
    #logPlus(links_mgv, "Links (GAMES -> Mikes Gaming Videos): ")
	
    # Bootsy Beats
    links_bb = processLinks("category/bootsy-beats", 1)
    #logPlus(links_bb, "Links (GAMES -> Bootsy Beats): ")
	
    # James Gaming Videos
    links_jgv = processLinks("category/jamesgamingvideos", 1)
    #logPlus(links_jgv, "Links (GAMES -> James Gaming Videos): ")
	
    # Other Gaming Videos
    links_ogv = processLinks("category/othergaming-videos", 1)
    #logPlus(links_ogv, "Links (GAMES -> Other Gaming Videos): ")
	
	
def dumpPageMovies():
	
    # Movie Reviews A-Z
    links_mraz = processLinks("category/moviereviewsatoz", 13)
    #logPlus(links_mraz, "Links (MOVIES -> Movie Reviews A-Z): ")
	
    # Top Tens
    links_mrtt = processLinks("category/moviereviews/top-tens", 1)
    #logPlus(links_mrtt, "Links (MOVIES -> Top Tens): ")
	
    # Animation Related
    links_mrar = processLinks("category/moviereviews/animation-moviereviews", 1)
    #logPlus(links_mrar, "Links (MOVIES -> Animation Related): ")
	
    # Commentaries
    links_mrc = processLinks("category/moviereviews/commentaries", 1)
    #logPlus(links_mrc, "Links (MOVIES -> Commentaries): ")
	
    # Interviews
    links_mri = processLinks("category/moviereviews/interviews", 1)
    #logPlus(links_mri, "Links (MOVIES -> Interviews): ")
	
    # Location Tours
    links_mrlt = processLinks("category/moviereviews/location-tours", 1)
    #logPlus(links_mrlt, "Links (MOVIES -> Location Tours): ")
	
    # Monster Madness
    links_mrmm = processLinks("category/moviereviews/monstermadness", 12)
    #logPlus(links_mrmm, "Links (MOVIES -> Monster Madness): ")
	
    # Trivia Videos
    links_mrtv = processLinks("category/moviereviews/trivia-videos", 1)
    #logPlus(links_mrtv, "Links (MOVIES -> Trivia Videos): ")
	
    # Other Movie Related Videos
    links_mromrv = processLinks("category/moviereviews/othermovierelatedvideos", 1)
    #logPlus(links_mromrv, "Links (MOVIES -> Other Movie Related Videos): ")
	
	
def dumpPageFilm():
	
    # Original Films Main
    links_film = processLinks("category/films", 4)
    #logPlus(links_film, "Links (ORIGINAL FILMS -> Main): ")
	
    # Favorites
    links_filmfav = processLinks("category/films/favorites", 1)
    #logPlus(links_filmfav, "Links (ORIGINAL FILMS -> Favorites): ")
	
    # Animation
    links_filmani = processLinks("category/films/animation", 1)
    #logPlus(links_filmani, "Links (ORIGINAL FILMS -> Animation): ")
	
    # Horror Films
    links_filmhorror = processLinks("category/films/horror-films", 2)
    #logPlus(links_filmhorror, "Links (ORIGINAL FILMS -> Horror Films): ")
	
    # Comedy
    links_filmcomedy = processLinks("category/films/comedy", 1)
    #logPlus(links_filmcomedy, "Links (ORIGINAL FILMS -> Comedy): ")
	
    # 48-Hour Films
    links_film48 = processLinks("category/films/48-hour-films", 1)
    #logPlus(links_film48, "Links (ORIGINAL FILMS -> 48 Hour Films): ")
	
    # Other
    links_filmother = processLinks("category/films/other", 1)
    #logPlus(links_filmother, "Links (ORIGINAL FILMS -> Other): ")
	

def dumpPageMusic():
	
    # Music Main
    links_mus = processLinks("category/music-2", 1)
    #logPlus(links_mus, "Links (MUSIC -> Main): ")
	
    # Audio Slaughter
    links_musas = processLinks("category/music-2/audio-slaughter", 1)
    #logPlus(links_musas, "Links (MUSIC -> Audio Slaughter): ")
	
    # Kyle Justin
    links_muskj = processLinks("category/music-2/kylejustin", 1)
    #logPlus(links_muskj, "Links (MUSIC -> Kyle Justin): ")
	
    # Name That Tune
    links_musntt = processLinks("category/music-2/namethattune", 1)
    #logPlus(links_musntt, "Links (MUSIC -> Name That Tune): ")
	

def dumpPageSite():
    
    # Site Main
    links_site = processLinks("category/site-2", 1)
    #logPlus(links_site, "Links (SITE -> Main): ")
	
    # Articles
    links_sitearticles = processLinks("category/site-2/featuredarticles", 1)
    #logPlus(links_sitearticles, "Links (SITE -> Articles): ")
	
    # Appearances
    links_siteappear = processLinks("category/site-2/appearances", 1)
    #logPlus(links_siteappear, "Links (SITE -> Appearances): ")
	
    # Misc Videos
    links_sitemisc = processLinks("category/site-2/misc-videos", 1)
    #logPlus(links_sitemisc, "Links (SITE -> Misc Videos): ")
	
	
def dumpPageAll():

    dumpPageShows()
    dumpPageGames()
    dumpPageMovies()
    dumpPageFilm()
    dumpPageMusic()
    dumpPageSite()


try:
    dumpPageAll()
except:
    doNothing()

xbmcplugin.setContent(addon_handle, "episodes")
id = ''.join(args.get('id', ""))
content = cache.cacheFunction(getContentFromXML)
getCategoriesFromXML(content, id)

xbmcplugin.endOfDirectory(addon_handle)

# Media Info View
xbmc.executebuiltin('Container.SetViewMode(504)')
