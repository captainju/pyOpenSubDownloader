#!/usr/bin/python2
# -*- coding: iso-8859-1 -*-

# see http://api.opensubtitles.org/xml-rpc


from xmlrpclib import ServerProxy
from conf import Configuration


class OpenSubDownloader():

    def __init__(self):
        self.xmlrpc = ServerProxy(Configuration.OPEN_SUBTITLES_URL)
        self.token = None

    def login(self, username="", password=""):
        result = self.xmlrpc.LogIn(username, password, "", Configuration.OPEN_SUBTITLES_USER_AGENT)
        if result["status"] == "200 OK":
            self.token = result['token']
        else:
            print "Can't connect!"

    def find(self, queryDict):
        result = self.xmlrpc.SearchSubtitles(self.token, [queryDict])
        if result["status"] == "200 OK":
            print result["data"]

if __name__ == "__main__":
    osd = OpenSubDownloader()
    osd.login()
    osd.find({'sublanguageid': 'fre', 'query': 'Person.of.Interest.S02E04.720p.HDTV.X264-DIMENSION.mkv'})
