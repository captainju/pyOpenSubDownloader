#!/usr/bin/python2
# -*- coding: iso-8859-1 -*-

# see http://api.opensubtitles.org/xml-rpc


from xmlrpclib import ServerProxy
import os
import mimetypes
import argparse
import urllib2
import tempfile
import gzip


class Configuration(object):
    OPEN_SUBTITLES_URL = "http://api.opensubtitles.org/xml-rpc"
    OPEN_SUBTITLES_USER_AGENT = "OS Test User Agent"


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
                except:
                    None
        else:
            print "wtf iz " + args.path + "?"


def hasSubtitles(videoPath):
    return os.path.isfile(os.path.splitext(videoPath)[0] + ".srt")


def downloadUrlFile(url, path, name):
    u = urllib2.urlopen(url)
    tempFile = tempfile.mkstemp()[1]
    f = open(tempFile, 'wb')

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break
        file_size_dl += len(buffer)
        f.write(buffer)
    f.close()
    f = gzip.open(tempFile, 'rb')
    file_content = f.read()
    f.close()
    f = open(path + os.sep + name + ".srt", 'wb')
    f.write(file_content)
    f.close()
    print "Subtitles downloaded for %s" % (name)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Download subs from opensubtitles.org')
    parser.add_argument('path', help='path of the video file or folder containing videos')
    parser.add_argument('--hash', help='using hash instead of filename', action='store_const', const=True)
    parser.add_argument('--force', help='replace existing subtitles', action='store_const', const=True)
    parser.add_argument('-l', '--language', help='subtitles language code like eng or fre', nargs="?", const="fre")
    args = parser.parse_args()

    mimetypes.init()
    osd = OpenSubDownloader()
    osd.login()

    if args.language is None:
        #default french
        args.language = 'fre'

    vf = VideoFiles(args.path)

    for videoFile in vf.filenames:
        if not hasSubtitles(vf.path + os.sep + videoFile) or args.force:
            if args.hash:
                raise NotImplementedError
            else:
                osresult = osd.find({'sublanguageid': args.language, 'query': videoFile})
                if osresult is not None and osresult is not False:
                    # for subEntry in osresult:
                    #     print subEntry["SubDownloadLink"]
                    #get first one
                    subUrl = osresult[0]["SubDownloadLink"]
                    downloadUrlFile(subUrl, vf.path, os.path.splitext(videoFile)[0])
                else:
                    print "no sub found for " + videoFile
