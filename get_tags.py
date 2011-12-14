import sys
import tables
from numpy import *

tags = open(sys.argv[1]).readlines()
tags_to_idx = dict()
for i in xrange(len(tags)):
    tags_to_idx[tags[i].strip()] = i

def foobar(s):
    return str(tags_to_idx[s])

for l in sys.stdin:
        s = tables.openFile(l.strip())
        artist = s.root.metadata.songs[0]['artist_mbid']
        tags = s.root.musicbrainz.artist_mbtags[:]
        if artist != '':
            print artist,",",", ".join(map(foobar, tags))
        s.close()

