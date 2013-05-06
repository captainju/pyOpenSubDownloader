#!/usr/bin/python2
# -*- coding: iso-8859-1 -*-

# see http://api.opensubtitles.org/xml-rpc


from xmlrpclib import ServerProxy
from conf import Configuration
import os
import mimetypes
import argparse


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
            return result["data"]
        else:
            return None


class VideoFiles():

    def __init__(self, path=None):
        if path is None or not os.path.exists(path):
            print "plz enter video file path or video path containing videos"
            exit()
        else:
            print "checking for : "+path
            self.listVideosInPath(path)

    def listVideosInPath(self, path):
        self.filenames = []
        self.path = ""

        if os.path.isfile(path):
            try:
                if mimetypes.guess_type(path)[0].split('/')[0] == 'video':
                    self.filenames.append(path)
                    self.path = os.path.dirname(os.path.abspath(path))
                else:
                    print path + " iz not a video file"
            except:
                None
        elif os.path.isdir(args.path):
            for filePath in os.listdir(path):
                try:
                    if mimetypes.guess_type(path+os.sep+filePath)[0].split('/')[0] == 'video':
                        self.filenames.append(filePath)
                        self.path = os.path.dirname(os.path.abspath(path+os.sep+filePath))
                    else:
                        print filePath + " iz not a video file"
                except:
                    None
        else:
            print "wtf iz " + args.path + "?"

    def hasSubtitles(self, videoPath):
        os.path.splitext(filename)[0]


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Download subs from opensubtitles.org')
    parser.add_argument('path', help='path of the video file or folder containing videos')
    parser.add_argument('--hash', help='using hash instead of filename', action='store_const', const=True)
    parser.add_argument('--force', help='replace existing subtitles', action='store_const', const=True)
    args = parser.parse_args()

    mimetypes.init()
    osd = OpenSubDownloader()
    osd.login()

    vf = VideoFiles(args.path)

    for videoFile in vf.filenames:
        print videoFile
        if args.hash:
            raise NotImplementedError
        else:
            osresult = osd.find({'sublanguageid': 'fre', 'query': videoFile})
            if osresult is not None and osresult is not False:
                for subEntry in osresult:
                    print subEntry["SubDownloadLink"]
            else:
                print "no sub found for " + videoFile
    print vf.path

