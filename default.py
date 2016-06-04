# Copyright 2014 cdwertmann


# ------------------------------------------------------------------------------
# 2016
# Updated By esc0rtd3w [http://github.com/esc0rtd3w]
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Notes For Old SMIL Type Parsing

# smil links end in ".smil/playlist.m3u8" and will fail on all videos that used this in the past
# smil links are replaced with "content.jwplatform.com/manifests/cRG5JPZN.m3u8"
# cRG5JPZN is the video ID for this example
# From HTML Source: <div class="videoarea"><script src="//content.jwplatform.com/players/cRG5JPZN-DKo5ucaI.js">

# Example New Parse #1 (From Page): content.jwplatform.com/players/[video_id_new]-[pid].js
# Example New Parse #2 (From JS): content.jwplatform.com/manifests/[video_id_new].m3u8

# Sample From http://content.jwplatform.com/players/cRG5JPZN-DKo5ucaI.js

# "pid": "DKo5ucaI",
# "playlist": [
# {
# "description": "",
# "image": "//content.jwplatform.com/thumbs/cRG5JPZN-720.jpg",
# "legacy_id": "Cinemassacre-245",
# "link": "//content.jwplatform.com/previews/cRG5JPZN",
# "mediaid": "cRG5JPZN",
# "property_name": "Cinemassacre",
# "pubdate": "Wed, 09 Oct 2013 04:00:00 -0000",
# "sources": [
# {
# "file": "//content.jwplatform.com/manifests/cRG5JPZN.m3u8",
# "type": "hls"
# },
# {
# "duration": 91,
# "file": "//content.jwplatform.com/videos/cRG5JPZN-QvH08cwS.mp4",
# "height": 240,
# "label": "H.264 320px",
# "type": "video/mp4",
# "width": 320
# },
# {
# "duration": 91,
# "file": "//content.jwplatform.com/videos/cRG5JPZN-TGIpRPjO.m4a",
# "height": -1,
# "label": "AAC Audio",
# "type": "audio/mp4",
# "width": -1
# }
# ],
# "tags": "",
# "thumbnail_url": "https://s3.amazonaws.com/SWMVideo/Cinemassacre-245_thumb_640x360.jpg",
# "title": "Nosferatu (1922) History of Horror",
# "tracks": [
# {
# "file": "//content.jwplatform.com/strips/cRG5JPZN-120.vtt",
# "kind": "thumbnails"
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Found Video Base URL's

# Originals By cdwertmann
# http://video1.screenwavemedia.com/Cinemassacre/smil:
# http://cdn.springboard.gorillanation.com/storage/cinemassacre/conversion/
# http://blip.tv/file/get/Cinemassacre-
# http://trailers.gametrailers.com/gt_vault/3000/
# http://www.youtube.com/watch?v=
# http://www.youtube.com/embed/

# http://206.217.201.108/Cinemassacre/smil:

# http://video2.screenwavemedia.com/vod/Cinemassacre-
# http://player.screenwavemedia.com/play/jwplayer/Cinemassacre-
# http://player.screenwavemedia.com/play/Cinemassacre-
# http://player.screenwavemedia.com/play/player.php?id=Cinemassacre-
# http://player.screenwavemedia.com/play/embed.php?id=

# http://blip.tv/play/
# http://j16.video2.blip.tv/
# http://a.blip.tv/api.swf#

# http://www.gametrailers.com/videos/

# http://media.mtvnservices.com/fb/mgid:arc:video:gametrailers.com:
# http://media.mtvnservices.com/player/prime/mediaplayerprime.2.5.7.swf?uri=mgid:arc:video:gametrailers.com:
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# POST Submission: Request All AVGN Episodes

# http://cinemassacre.com/category/avgn/avgnepisodes/
# Use "page_no=1" from "action" in header to change pages (1-6 are valid)
# __cfduid and PHPSESSID may also need changed for different request sessions

# POST /wp-admin/admin-ajax.php HTTP/1.1
# Host: cinemassacre.com
# User-Agent: XBMC/Kodi (plugin.video.cinemassacre/3.0.0)
# Accept: */*
# Accept-Language: en-US,en;q=0.5
# Accept-Encoding: gzip, deflate
# Content-Type: application/x-www-form-urlencoded; charset=UTF-8
# X-Requested-With: XMLHttpRequest
# Referer: http://cinemassacre.com/category/avgn/avgnepisodes/
# Content-Length: 56
# Cookie: __cfduid=dcaa673b3d717e0aadcfdac53e94ba7d21462682306; PHPSESSID=kg4703g2mdptsussbo408vvau5
# Connection: keep-alive
# action=infinite_scroll&page_no=1&cat=1065&loop_file=loop


# Returns HTML In The Following Format (The 1st link is the newest episode)

# <div class="archiveitem">
# 	<a href="http://cinemassacre.com/2016/05/26/avgn-paperboy/" rel="bookmark" title="Permanent Link to Paperboy (NES) Angry Video Game Nerd">
# 	<img width="190" height="140" src="http://cinemassacre.com/wp-content/uploads/2016/04/Paperboy-STILL-FINAL-190x140.jpg" class="mediumthumb wp-post-image" alt="Paperboy-STILL-FINAL" srcset="http://cinemassacre.com/wp-content/uploads/2016/04/Paperboy-STILL-FINAL-190x140.jpg 190w, http://cinemassacre.com/wp-content/uploads/2016/04/Paperboy-STILL-FINAL-90x66.jpg 90w" sizes="(max-width: 190px) 100vw, 190px" />			<div>Paperboy (NES) Angry Video Game Nerd</div></a>
# </div>
		
# <div class="archiveitem">
# 	<a href="http://cinemassacre.com/2016/04/06/mega-man-games-angry-video-game-nerd/" rel="bookmark" title="Permanent Link to MEGA MAN Games &#8211; Angry Video Game Nerd: Episode 139">
# 	<img width="190" height="140" src="http://cinemassacre.com/wp-content/uploads/2016/04/Mega-Man-title-card-190x140.jpg" class="mediumthumb wp-post-image" alt="Mega Man title card" srcset="http://cinemassacre.com/wp-content/uploads/2016/04/Mega-Man-title-card-190x140.jpg 190w, http://cinemassacre.com/wp-content/uploads/2016/04/Mega-Man-title-card-90x66.jpg 90w" sizes="(max-width: 190px) 100vw, 190px" />			<div>MEGA MAN Games &#8211; Angry Video Game Nerd: Episode 139</div></a>
# </div>

# <div class="archiveitem">
# 	<a href="http://cinemassacre.com/2015/12/22/mortal-kombat-mythologies-sub-zero-n64-angry-video-game-nerd/" rel="bookmark" title="Permanent Link to AVGN: Mortal Kombat Mythologies: Sub-Zero (N64)">
# 	<img width="190" height="140" src="http://cinemassacre.com/wp-content/uploads/2015/12/AVGN-MK-190x140.jpg" class="mediumthumb wp-post-image" alt="AVGN-MK" srcset="http://cinemassacre.com/wp-content/uploads/2015/12/AVGN-MK-190x140.jpg 190w, http://cinemassacre.com/wp-content/uploads/2015/12/AVGN-MK-90x66.jpg 90w" sizes="(max-width: 190px) 100vw, 190px" />			<div>AVGN: Mortal Kombat Mythologies: Sub-Zero (N64)</div></a>
# </div>
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# GET Request: AVGN Episodes 2015-2016

# GET /category/avgn/avgnepisodes/2015/ HTTP/1.1
# Host: cinemassacre.com
# User-Agent: XBMC/Kodi (plugin.video.cinemassacre/3.0.0)
# Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
# Accept-Language: en-US,en;q=0.5
# Accept-Encoding: gzip, deflate
# Referer: http://cinemassacre.com/category/avgn/
# Cookie: __cfduid=dcaa673b3d717e0aadcfdac53e94ba7d21462682306; PHPSESSID=kg4703g2mdptsussbo408vvau5
# Connection: keep-alive


# Returns HTML In The Following Format (The 1st link is the newest episode)

# <div id="featuredImg">
# 	<a href="http://cinemassacre.com/2016/05/26/avgn-paperboy/" rel="bookmark" title="Permanent Link to Paperboy (NES) Angry Video Game Nerd">
# 	<img width="470" height="260" src="http://cinemassacre.com/wp-content/uploads/2016/04/Paperboy-STILL-FINAL-470x260.jpg" class="largethumb wp-post-image" alt="Paperboy-STILL-FINAL" srcset="http://cinemassacre.com/wp-content/uploads/2016/04/Paperboy-STILL-FINAL-470x260.jpg 470w, http://cinemassacre.com/wp-content/uploads/2016/04/Paperboy-STILL-FINAL-150x84.jpg 150w" sizes="(max-width: 470px) 100vw, 470px" />            </a>
# 	<span id="archiveCaption"><a href="http://cinemassacre.com/2016/05/26/avgn-paperboy/" rel="bookmark" title="Permanent Link to Paperboy (NES) Angry Video Game Nerd">Paperboy (NES) Angry Video Game Nerd</a></span>
# </div>

# <div class="archiveitem">
# 	<a href="http://cinemassacre.com/2016/04/06/mega-man-games-angry-video-game-nerd/" rel="bookmark" title="Permanent Link to MEGA MAN Games &#8211; Angry Video Game Nerd: Episode 139">
# 	<img width="190" height="140" src="http://cinemassacre.com/wp-content/uploads/2016/04/Mega-Man-title-card-190x140.jpg" class="mediumthumb wp-post-image" alt="Mega Man title card" srcset="http://cinemassacre.com/wp-content/uploads/2016/04/Mega-Man-title-card-190x140.jpg 190w, http://cinemassacre.com/wp-content/uploads/2016/04/Mega-Man-title-card-90x66.jpg 90w" sizes="(max-width: 190px) 100vw, 190px" />            
# 	<div>MEGA MAN Games &#8211; Angry Video Game Nerd: Episode 139</div></a>
# </div>
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Find All AVGN Episodes (Manual URLs)
# Using same returned HTML data to parse as GET and POST methods

# http://cinemassacre.com/category/avgn/avgnepisodes/page/1/
# http://cinemassacre.com/category/avgn/avgnepisodes/page/2/
# http://cinemassacre.com/category/avgn/avgnepisodes/page/3/
# http://cinemassacre.com/category/avgn/avgnepisodes/page/4/
# http://cinemassacre.com/category/avgn/avgnepisodes/page/5/
# http://cinemassacre.com/category/avgn/avgnepisodes/page/6/
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# All Page Link URL References (Site Map)

# SHOWS

#   ANGRY VIDEO GAME NERD
#   http://cinemassacre.com/category/avgn/

#     AVGN EPISODES
#     http://cinemassacre.com/category/avgn/avgnepisodes/

#       2004 - 2006
#       http://cinemassacre.com/category/avgn/avgnepisodes/2004-2006

#       2007
#       http://cinemassacre.com/category/avgn/avgnepisodes/avgn-2007

#       2008
#       http://cinemassacre.com/category/avgn/avgnepisodes/avgn-2008

#       2009
#       http://cinemassacre.com/category/avgn/avgnepisodes/avgn-2009

#       2010
#       http://cinemassacre.com/category/avgn/avgnepisodes/avgn-2010

#       2011-2014
#       http://cinemassacre.com/category/avgn/avgnepisodes/2013

#       2015-2016
#       http://cinemassacre.com/category/avgn/avgnepisodes/2015

#     AVGN MOVIE
#     http://cinemassacre.com/category/avgn/avgn-movie-avgn/

#     AVGN Related Videos
#     http://cinemassacre.com/category/avgn/avgn-related/

# GAMES

#   MIKES GAMING VIDEOS
#   http://cinemassacre.com/category/mikevideos/

#   BOOTSY BEATS
#   http://cinemassacre.com/category/gamevideos/bootsy-beats/

#   JAMES GAMING VIDEOS
#   http://cinemassacre.com/category/jamesgamingvideos/

#   OTHER GAMING VIDEOS
#   http://cinemassacre.com/category/othergaming-videos/

#   GAME COLLECTION
#   http://cinemassacre.com/2007/03/22/game-collection/

# MOVIES

#   MOVIE REVIEWS A-Z
#   http://cinemassacre.com/category/moviereviewsatoz/

#     COMPILATION MOVIE REVIEWS
#     http://cinemassacre.com/category/compilationmoviereviews/

#   TOP 10S
#   http://cinemassacre.com/category/moviereviews/top-tens/

#   ANIMATION RELATED
#   http://cinemassacre.com/category/moviereviews/animation-moviereviews/

#   COMMENTARIES
#   http://cinemassacre.com/category/moviereviews/commentaries/

#   INTERVIEWS
#   http://cinemassacre.com/category/interviews/

#   LOCATION TOURS
#   http://cinemassacre.com/category/location-tours/

#   MONSTER MADNESS
#   http://cinemassacre.com/category/moviereviews/monstermadness/

#     2007 HISTORY OF HORROR
#     http://cinemassacre.com/category/moviereviews/monstermadness/monster-madness-2007/

#     2008 GODZILLATHON
#     http://cinemassacre.com/category/moviereviews/monstermadness/monster-madness-2008/

#     2009 MONSTER MADNESS THREE
#     http://cinemassacre.com/category/moviereviews/monstermadness/monster-madness-2009/

#     2010 CAMP CULT
#     http://cinemassacre.com/category/moviereviews/monstermadness/monster-madness-2010/

#     2011 SEQUEL-A-THON
#     http://cinemassacre.com/category/moviereviews/monstermadness/2011-monstermadness/

#     2012 80S-A-THON
#     http://cinemassacre.com/category/moviereviews/monstermadness/eighties-a-thon/

#     2013 SEQUEL-A-THON 2
#     http://cinemassacre.com/category/moviereviews/monstermadness/sequel-a-thon-2/

#     2014 MONSTER MADNESS 8
#     http://cinemassacre.com/category/moviereviews/monstermadness/2014-monster-madness-8/

#     2015 MONSTER MADNESS 9
#     http://cinemassacre.com/category/moviereviews/monstermadness/monstermadness9/

#   TRIVIA VIDEOS
#   http://cinemassacre.com/category/trivia-videos/

#   OTHER MOVIE STUFF
#   http://cinemassacre.com/category/othermovierelatedvideos/

# ORIGINAL FILMS

#   SUB1

# MUSIC

#   SUB1

# SITE

#   SUB1

# ------------------------------------------------------------------------------



import sys
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import urllib
import urllib2
import urlparse
import hmac
import hashlib
import base64
import os
import binascii
import time
import xmltodict
import re
from datetime import datetime, date
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

def video_id(value):
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?.*?(?=v=)v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')

    youtube_regex_match = re.match(youtube_regex, value)
	
    if youtube_regex_match:
        return youtube_regex_match.group(6)

    return youtube_regex_match
	
def video_id_jwp(value):
	jwplayer_regex = (
		r'(http?://)?(content\.)?'
		'(jwplatform)\.(com)/'
		'(players/)?(.*)-(.*)?(\.m3u8)')

	jwplayer_regex_match = re.match(jwplayer_regex, value)

	if jwplayer_regex_match:
		return jwplayer_regex_match.group(7)

	return jwplayer_regex_match

def get_signature(key, msg):
    return base64.b64encode(hmac.new(key, msg, hashlib.sha1).digest())

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

def log(msg):
    xbmc.log(PLUGIN_NAME + ": "+ str(msg), level=xbmc.LOGNOTICE)

def getContent():

    # devicetoken=binascii.b2a_hex(os.urandom(32))
    # deviceuid=binascii.b2a_hex(os.urandom(20)).upper()
    # signature=get_signature(os.urandom(20),os.urandom(20))
    # timestamp=datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z")
    # URL="http://cinemassacre.screenwavemedia.com/AppServer/SWMAppFeed.php?appname=Cinemassacre&appversion=1.5.8&devicetoken="+devicetoken+"&deviceuid="+deviceuid+"&lastupdateid=0&timestamp="+timestamp+"&signature="+signature
    # log(URL)
    # req = urllib2.Request(URL)
    # response = urllib2.urlopen(req)
    # xml=response.read()
    # response.close()
	
    addon = xbmcaddon.Addon()
    addon_path = addon.getAddonInfo('path')
    _path = os.path.join(addon_path,'site.xml')
    f = open(_path, 'r')
    xml = f.read()
    return xmltodict.parse(xml)['document']

def getCategories(content,id):
    items = []
    if id=="":
        listitem=xbmcgui.ListItem("- All Videos Sorted By Date -", iconImage="DefaultFolder.png")
        url = build_url({'id': "all"})
        items.append((url, listitem, True))

    if id=="all":
        xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_DATE)
    else:
        xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_LABEL)

    for cat in content['MainCategory']:
        if cat['@parent_id'] == id:
            #if cat['@activeInd'] == "N": continue
			
            listitem=xbmcgui.ListItem(cat['@name'], iconImage="DefaultFolder.png")
            url = build_url({'id': cat['@id']})
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
                #url = "plugin://plugin.video.youtube/?action=play_video&videoid="+video_id(url)
                url = "plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid="+video_id(url)
				
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
			

def getLinks(page):

	# Original Source: http://kodi.wiki/view/How-to:Write_Python_Scripts

	LinkDescription = []
	LinkURL = []
	 
	socket = urllib.urlopen(page)
	linkdump = socket.read()
	socket.close()
	 
	urltemp = re.compile('<script src=["]//content.jwplatform.com/players/(*)-(*)[.]m3u8["]>', re.IGNORECASE).findall(linkdump)
	desctemp = re.compile('<script src=["]//content.jwplatform.com/players/(*)-(*)[.]m3u8["]>(.*)</script>').findall(linkdump)
	 
	for urls, desc in zip(urltemp,desctemp):
		LinkURL.append(urls[9:-2])
		LinkDescription.append(desc)
		xbmc.executebuiltin("Notification("+LinkURL+")")
	

xbmcplugin.setContent(addon_handle, "episodes")
id = ''.join(args.get('id', ""))
content = cache.cacheFunction(getContent)
getCategories(content, id)

xbmcplugin.endOfDirectory(addon_handle)
# Media Info View
xbmc.executebuiltin('Container.SetViewMode(504)')
