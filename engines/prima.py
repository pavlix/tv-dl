#!/usr/bin/env python3
#
__author__ = "Jakub Lužný"
__desc__ = "TV Prima Videoarchiv"
__url__ = r"http://(www.)?iprima\.cz/videoarchiv.*"

import re,os.path,random,math
import xml.etree.ElementTree as ElementTree
from urllib.request import urlopen, Request

class PrimaEngine:

    def __init__(self, url):
        self.url = url
        self.page = urlopen(url).read().decode('utf-8')

    def movies(self):        
        return [ ('0', re.findall(r'<meta property="og:title" content="(.+?)" />', self.page)[0]) ]
  
    def qualities(self):
        return [ ('high', 'Vysoká'), ('low', 'Nízká')]

    def download(self, quality, movie):
        reg = r"LiveboxPlayer\.init\('embed_here.*?','\d+','\d+', '(.+\.mp4)', '(.+\.mp4)'"
        r = re.findall(reg, self.page)
        if not r:
            r = re.findall( reg.replace('mp4', 'flv') , self.page)
        hq, lq = r[0]
        
        playpath = ""
        if quality == "low":
            playpath = lq
        else:
            playpath = hq

        playerUrl = 'http://embed.livebox.cz/iprima/player-1.js?__tok{}__={}'.format(
                         math.floor(random.random()*1073741824),
                         math.floor(random.random()*1073741824))
        
        req = Request(playerUrl, None, {'Referer' : self.url} )
        player = urlopen(req).read().decode('utf-8')
        
        baseUrl = re.findall( r"stream: '(.+?)'", player)[0]

        return ("rtmp", playpath[:-3]+'flv' , { 'url' : baseUrl+'/'+playpath,
                                     'rtmpdump_args' : '--live'})
