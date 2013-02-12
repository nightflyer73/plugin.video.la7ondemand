import urllib2
from xml.dom import minidom

class La7ondemand:
        __EPG_URL = "http://www.la7.tv/xml/epg/index.xml"
        __CULT_URL = "http://www.la7.tv/xml/cult/index.xml"
        __HTTP_VIDEO_URL = "http://videoteca1.alice.cdn.interbusiness.it/vod/"
        __RTMP_VIDEO_URL = "rtmp://videoteca1.alice.cdn.interbusiness.it:1935/vod"

        EPG = 0
        CULT = 1

        def getGrid(self, gridType):
                """
                get Program Grid
                @gridType can be EPG (0) or CULT (1)
                """
                
                if gridType == self.EPG:
                        url = self.__EPG_URL
                else:
                        url = self.__CULT_URL
                xmldata = urllib2.urlopen(url).read()
                dom = minidom.parseString(xmldata)

                startDate = dom.getElementsByTagName('epg')[0].attributes["startDate"].value
                # Format: 03/10/2012
                
                grid = []
                for node in dom.getElementsByTagName('show'):
                        show = {}
                        show["title"] = node.attributes["title"].value
                        show["channel"] = node.attributes["channel"].value
                        show["logo"] = node.getElementsByTagName('logo')[0].attributes["src"].value
                        show["logo_tv"] = node.getElementsByTagName('logo_tv')[0].attributes["src"].value
                        descrizione = node.getElementsByTagName('descrizione')[0]
                        if descrizione.hasChildNodes():
                                show["descrizione"] = descrizione.childNodes[0].data
                        else:
                                show["descrizione"] = ""
                        episodes = []
                        for itemNode in node.getElementsByTagName('item'):
                                episode = {}
                                episode["pos"] = itemNode.attributes["pos"].value
                                episode["assetID"] = itemNode.attributes["assetID"].value
                                episode["xmlURL"] = itemNode.attributes["xmlURL"].value
                                episode["title"] = itemNode.getElementsByTagName('title')[0].childNodes[0].data
                                episode["duration"] = itemNode.getElementsByTagName('duration')[0].childNodes[0].data
                                episode["img_65"] = itemNode.getElementsByTagName('img')[0].attributes["src"].value
                                episode["img_140"] = episode["img_65"].replace("_65", "_140")
                                try:
                                        episode["views"] = itemNode.getElementsByTagName('views')[0].childNodes[0].data
                                except IndexError:
                                        episode["views"] = "0"
                                episodes.append(episode)
                        show["episodes"] = episodes
                        grid.append(show)
                        
                return grid
                
        def getVideoURL(self, xmlURL, quality):
                """
                get getVideoURL URL
                @xmlURL is the URL containing episode metadata
                """
                
                xmldata = urllib2.urlopen(xmlURL).read() 
                dom = minidom.parseString(xmldata)
                for video in dom.getElementsByTagName('video'):
                        if video.getElementsByTagName('quality')[0].childNodes[0].data == '600':
                                highVideoURL = video.getElementsByTagName('fms')[0].childNodes[0].data
                        if video.getElementsByTagName('quality')[0].childNodes[0].data == '400':
                                lowVideoURL = video.getElementsByTagName('fms')[0].childNodes[0].data

                if quality == 'low':
                        videoURL = lowVideoURL
                else:
                        videoURL = highVideoURL
                
                return self.__RTMP_VIDEO_URL + " playpath=" + videoURL
