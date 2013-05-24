pyOpenSubDownloader
===================

Simple subtitle downloader from OpenSubtitles.org

usage:
<pre>pyOpenSubDownloader.py [-h] [--hash] [--force] [-l [LANGUAGE]] path

positional arguments:
  path                  path of the video file or folder containing videos

optional arguments:
  -h, --help            show this help message and exit
  --hash                using hash instead of filename
  --force               replace existing subtitles
  -l [LANGUAGE], --language [LANGUAGE]
                        subtitles language code like eng or fre
</pre>


example:
<pre>
$python pyOpenSubDownloader.py -l eng /home/pi/Person.of.Interest.S01.720p.HDTV.x264
checking for : /home/pi/Person.of.Interest.S01.720p.HDTV.x264
Subtitles downloaded for Person.of.Interest.S01E23.720p.HDTV.x264-DIMENSION
Subtitles downloaded for Person.of.Interest.S01E04.720p.HDTV.x264-ORENJI
...

$ls /home/pi/Person.of.Interest.S01.720p.HDTV.x264
Person.of.Interest.S01E01.720p.HDTV.x264-IMMERSE.mkv
Person.of.Interest.S01E01.720p.HDTV.x264-IMMERSE.srt
Person.of.Interest.S01E02.720p.HDTV.x264-IMMERSE.mkv
Person.of.Interest.S01E02.720p.HDTV.x264-IMMERSE.srt
Person.of.Interest.S01E03.720p.HDTV.x264-IMMERSE.mkv
Person.of.Interest.S01E03.720p.HDTV.x264-IMMERSE.srt
...
</pre>
