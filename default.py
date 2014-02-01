import os
import sys
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import urllib
import urlparse
import datetime
from resources.lib.libLa7 import La7ondemand

# plugin constants
__plugin__ = "plugin.video.la7ondemand"
__author__ = "Nightflyer"

Addon = xbmcaddon.Addon(id=__plugin__)

# plugin handle
handle = int(sys.argv[1])

# utility functions
def parameters_string_to_dict(parameters):
    ''' Convert parameters encoded in a URL to a dict. '''
    paramDict = dict(urlparse.parse_qsl(parameters[1:]))
    return paramDict
 
def addDirectoryItem(parameters, li):
    url = sys.argv[0] + '?' + urllib.urlencode(parameters)
    return xbmcplugin.addDirectoryItem(handle=handle, url=url, 
        listitem=li, isFolder=True)

def addLinkItem(url, li):
    return xbmcplugin.addDirectoryItem(handle=handle, url=url, 
        listitem=li, isFolder=False)

# UI builder functions
def show_root_menu():
    ''' Show the plugin root menu '''
    liStyle = xbmcgui.ListItem("LA SETTIMANA")
    addDirectoryItem({"mode": "epg"}, liStyle)
    liStyle = xbmcgui.ListItem("ARCHIVIO CULT")
    addDirectoryItem({"mode": "cult"}, liStyle)
    xbmcplugin.endOfDirectory(handle=handle, succeeded=True)

def show_last_week():
    xbmcplugin.setContent(handle, 'tvshows')
    
    ond = La7ondemand()
    grid = ond.getGrid(ond.EPG)
    for show in grid:
        title = show["title"]
        liStyle = xbmcgui.ListItem(title.upper(), thumbnailImage=show["logo"])
        addDirectoryItem({"mode": "epg", "name": show["title"]}, liStyle)

    # force thumbnail view
    #xbmc.executebuiltin("Container.SetViewMode(500)")
    xbmcplugin.endOfDirectory(handle=handle, succeeded=True)

def show_cult():
    xbmcplugin.setContent(handle, 'tvshows')
    
    ond = La7ondemand()
    grid = ond.getGrid(ond.CULT)
    for show in grid:
        title = show["title"]
        liStyle = xbmcgui.ListItem(title.upper(), thumbnailImage=show["logo"])
        addDirectoryItem({"mode": "cult", "name": show["title"]}, liStyle)

    # force thumbnail view
    #xbmc.executebuiltin("Container.SetViewMode(500)")    
    xbmcplugin.endOfDirectory(handle=handle, succeeded=True)

def show_episodes(mode, name):
    xbmcplugin.setContent(handle, 'episodes')
    
    ond = La7ondemand()
    if mode == "epg":
        grid = ond.getGrid(ond.EPG)
    else:
        grid = ond.getGrid(ond.CULT)

    # [TODO] get this value from the xml file
    epgstartdate = datetime.date.today() - datetime.timedelta(days=6)
        
    for show in grid:
        if show["title"] == name:
            for episode in show["episodes"]:
                labels = {"title": episode["title"], 
                        "tvshowtitle": episode["title"],
                        "duration": int(episode["duration"][:-6]) * 60 + int(episode["duration"][-5:-3])}
                
                if mode == "epg":
                    airdate = epgstartdate + datetime.timedelta(days = int(episode["pos"]))
                    labels["date"] = airdate.strftime("%d.%m.%Y")
                    labels["airdate"] = airdate.strftime("%Y-%m-%d")
                
                liStyle=xbmcgui.ListItem(episode["title"], thumbnailImage=episode["img_140"])
                liStyle.setInfo(type="Video", infoLabels=labels)

                addLinkItem(episode["videoUrl"], liStyle)
    if mode == "epg":
        xbmcplugin.addSortMethod(handle, xbmcplugin.SORT_METHOD_DATE)
    xbmcplugin.endOfDirectory(handle=handle, succeeded=True)


# parameter values
params = parameters_string_to_dict(sys.argv[2])
mode = str(params.get("mode", ""))
name = str(params.get("name", ""))

if mode == "epg":
    if name == "":
        show_last_week()
    else:
        show_episodes(mode, name)
elif mode == "cult":
    if name == "":
        show_cult()
    else:
        show_episodes(mode, name)
else:
    show_root_menu()

