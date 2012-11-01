#!/usr/bin/python
import xml
import logging
import sys,os,urllib2
import logging.handlers
import xml.etree.ElementTree as ET
from logging.handlers import RotatingFileHandler

logpath = "/var/log/sitemap_aggregator.log"
#5 Megabytes log file
logfilesize = 1024*1024*5

urls = ["http://openite.com/ru/sitemap.xml",
        "http://openite.com/en/sitemap.xml"]

savepath = "./sitemap.xml"

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler = logging.handlers.RotatingFileHandler(filename=logpath,maxBytes=logfilesize)
handler.setFormatter(formatter)
logger.addHandler(handler)


def process():
    firstTree = None
    tree = None
    for url in urls:
        response = urllib2.urlopen(url)
        data = response.read()
        
        if data:
            if firstTree == None:
                #Registering namespace
                ET.register_namespace("","http://www.sitemaps.org/schemas/sitemap/0.9")

                try:
                    firstTree = ET.XML(data)
                except Exception as e:
                    logger.error(e)
                    
            else:
                try:
                    tree = ET.XML(data)
                except Exception as e:
                    logger.error(e)
                
                if tree!=None:
                    for child in list(tree):
                        firstTree.append(child)
                    

    if firstTree!=None:
        ET.ElementTree(firstTree).write(savepath)
        
if __name__ == "__main__":
    process()
