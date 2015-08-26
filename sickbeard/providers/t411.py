# -*- coding: latin-1 -*-
# Author: Guillaume Serre <guillaume.serre@gmail.com>
# URL: http://code.google.com/p/sickbeard/
#
# This file is part of Sick Beard.
#
# Sick Beard is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Sick Beard is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Sick Beard.  If not, see <http://www.gnu.org/licenses/>.

from bs4 import BeautifulSoup
from sickbeard import classes, show_name_helpers, logger
from sickbeard.common import Quality
import generic
import cookielib
import sickbeard
import urllib
import urllib2


class T411Provider(generic.TorrentProvider):

    def __init__(self):
        
        generic.TorrentProvider.__init__(self, "T411")

        self.supportsBacklog = True
        
        self.cj = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        self.opener.addheaders = [('Content-Type', 'application/x-www-form-urlencoded'),('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7 (.NET CLR 3.5.30729)')]
        
        self.url = "http://www.t411.io"
        
        self.login_done = False
        
    def isEnabled(self):
        return sickbeard.T411
    
    def getSearchParams(self, searchString, audio_lang, subcat, french=None):
        if audio_lang == "en" and french==None:
            return urllib.urlencode( {'search': searchString, 'cat' : 210, 'submit' : 'Recherche', 'subcat': subcat } ) + "&term%5B17%5D%5B%5D=721"
        elif audio_lang == "fr" or french:
            return urllib.urlencode( {'search': searchString, 'cat' : 210, 'submit' : 'Recherche', 'subcat': subcat } ) + "&term%5B17%5D%5B%5D=541&term%5B17%5D%5B%5D=542"
        else:
            return urllib.urlencode( {'search': searchString, 'cat' : 210, 'submit' : 'Recherche', 'subcat': subcat } )

    def seasonValue(self, season):
        values = [968, 969, 970, 971, 972, 973, 974, 975, 976, 977, 978, 979, 980, 981, 982, 983, 984, 985, 986, 987, 988, 989, 990, 991, 994, 992, 993, 995, 996, 997]
        return values[int(season) -1]

    def episodeValue(self, episode):
        values = [937, 938, 939, 940, 941, 942, 943, 944, 946, 947, 948, 949, 950, 951, 952, 954, 953, 955, 956, 957, 958, 959, 960, 961, 962, 963, 964, 965, 966, 967, 1088, 1089, 1090, 1091, 1092, 1093, 1094, 1095, 1096, 1097, 1098, 1099, 1100, 1101, 1102, 1103, 1104, 1105, 1106, 1107, 1108, 1109, 1110, 1110, 1111, 1112, 1113, 1114, 1115, 1116, 1117]
        return values[int(episode) - 1]
        
    def _get_season_search_strings(self, show, season):

        showNam = show_name_helpers.allPossibleShowNames(show)
        showNames = list(set(showNam))
        results = []
        for showName in showNames:
            if (int(season) < 31):
                results.append( self.getSearchParams(showName, show.audio_lang, 433 ) + "&" + urllib.urlencode({'term[46][]': 936, 'term[45][]': self.seasonValue(season)}))
                results.append( self.getSearchParams(showName, show.audio_lang, 637 ) + "&" + urllib.urlencode({'term[46][]': 936, 'term[45][]': self.seasonValue(season)}))
            #results.append( self.getSearchParams(showName + " S%02d" % season, show.audio_lang, 433 )) TOO MANY ERRORS
            #results.append( self.getSearchParams(showName + " S%02d" % season, show.audio_lang, 637 ))
            #results.append( self.getSearchParams(showName + " S%02d" % season, show.audio_lang, 634 ))
            #results.append( self.getSearchParams(showName + " saison %02d" % season, show.audio_lang, 433 ))
            #results.append( self.getSearchParams(showName + " saison %02d" % season, show.audio_lang, 637 ))
            results.append( self.getSearchParams(showName + " saison %02d" % season, show.audio_lang, 634 ))
        return results

    def _get_episode_search_strings(self, ep_obj, french=None):

        showNam = show_name_helpers.allPossibleShowNames(ep_obj.show)
        showNames = list(set(showNam))
        results = []
        for showName in showNames:
            results.append( self.getSearchParams( "%s S%02dE%02d" % ( showName, ep_obj.scene_season, ep_obj.scene_episode), ep_obj.show.audio_lang, 433, french ))
            if (int(ep_obj.scene_season) < 31 and int(ep_obj.scene_episode) < 61):
                results.append( self.getSearchParams( showName, ep_obj.show.audio_lang, 433, french)+ "&" + urllib.urlencode({'term[46][]': self.episodeValue(ep_obj.scene_episode), 'term[45][]': self.seasonValue(ep_obj.scene_season)}))
            #results.append( self.getSearchParams( "%s %dx%d" % ( showName, ep_obj.season, ep_obj.episode ), ep_obj.show.audio_lang , 433 )) MAY RETURN 1x12 WHEN SEARCHING 1x1
            results.append( self.getSearchParams( "%s %dx%02d" % ( showName, ep_obj.scene_season, ep_obj.scene_episode ), ep_obj.show.audio_lang, 433, french ))
            results.append( self.getSearchParams( "%s S%02dE%02d" % ( showName, ep_obj.scene_season, ep_obj.scene_episode), ep_obj.show.audio_lang, 637, french ))
            if (int(ep_obj.scene_season) < 31 and int(ep_obj.scene_episode) < 61):
                results.append( self.getSearchParams( showName, ep_obj.show.audio_lang, 637, french)+ "&" + urllib.urlencode({'term[46][]': self.episodeValue(ep_obj.scene_episode), 'term[45][]': self.seasonValue(ep_obj.scene_season)}))
            #results.append( self.getSearchParams( "%s %dx%d" % ( showName, ep_obj.season, ep_obj.episode ), ep_obj.show.audio_lang, 637 ))
            results.append( self.getSearchParams( "%s %dx%02d" % ( showName, ep_obj.scene_season, ep_obj.scene_episode ), ep_obj.show.audio_lang, 637, french ))
            results.append( self.getSearchParams( "%s S%02dE%02d" % ( showName, ep_obj.scene_season, ep_obj.scene_episode), ep_obj.show.audio_lang, 634, french))
            #results.append( self.getSearchParams( "%s %dx%d" % ( showName, ep_obj.season, ep_obj.episode ), ep_obj.show.audio_lang, 634 ))
            results.append( self.getSearchParams( "%s %dx%02d" % ( showName, ep_obj.scene_season, ep_obj.scene_episode ), ep_obj.show.audio_lang, 634, french ))
            results.append( self.getSearchParams( "%s S%02dE%02d" % ( showName, ep_obj.scene_season, ep_obj.scene_episode), ep_obj.show.audio_lang, 639, french))
            #results.append( self.getSearchParams( "%s %dx%d" % ( showName, ep_obj.season, ep_obj.episode ), ep_obj.show.audio_lang, 634 ))
            results.append( self.getSearchParams( "%s %dx%02d" % ( showName, ep_obj.scene_season, ep_obj.scene_episode ), ep_obj.show.audio_lang, 639, french ))
        return results
    
    def _get_title_and_url(self, item):
        return (item.title, item.url)
    
    def getQuality(self, item):
        return item.getQuality()
    
    def _doLogin(self, login, password):

        data = urllib.urlencode({'login': login, 'password' : password, 'submit' : 'Connexion', 'remember': 1, 'url' : '/'})
        self.opener.open(self.url + '/users/login', data)
    
    def _doSearch(self, searchString, show=None, season=None, french=None):
        
        if not self.login_done:
            self._doLogin( sickbeard.T411_USERNAME, sickbeard.T411_PASSWORD )

        results = []
        searchUrl = self.url + '/torrents/search/?' + searchString.replace('!','')
        logger.log(u"Search string: " + searchUrl, logger.DEBUG)
        
        r = self.opener.open( searchUrl )
        soup = BeautifulSoup( r, "html.parser" )
        resultsTable = soup.find("table", { "class" : "results" })
        if resultsTable:
            rows = resultsTable.find("tbody").findAll("tr")
    
            for row in rows:
                link = row.find("a", title=True)
                title = link['title']
                id = row.find_all('td')[2].find_all('a')[0]['href'][1:].replace('torrents/nfo/?id=','')
                downloadURL = ('http://www.t411.io/torrents/download/?id=%s' % id)
                
                quality = Quality.nameQuality( title )
                if quality==Quality.UNKNOWN and title:
                    if '720p' not in title.lower() and '1080p' not in title.lower():
                        quality=Quality.SDTV
                if show and french==None:
                    results.append( T411SearchResult( self.opener, link['title'], downloadURL, quality, str(show.audio_lang) ) )
                elif show and french:
                    results.append( T411SearchResult( self.opener, link['title'], downloadURL, quality, 'fr' ) )
                else:
                    results.append( T411SearchResult( self.opener, link['title'], downloadURL, quality ) )
                
        return results
    
    def getResult(self, episodes):
        """
        Returns a result of the correct type for this provider
        """
        result = classes.TorrentDataSearchResult(episodes)
        result.provider = self

        return result    
    
class T411SearchResult:
    
    def __init__(self, opener, title, url, quality, audio_langs=None):
        self.opener = opener
        self.title = title
        self.url = url
        self.quality = quality
        self.audio_langs=audio_langs
        
    def getNZB(self):
        return self.opener.open( self.url , 'wb').read()

    def getQuality(self):
        return self.quality

provider = T411Provider()
