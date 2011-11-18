import sys
import tables
from numpy import *

def avg(x):
    return sum(x)/len(x)

for l in sys.stdin:
    try:
        features = dict()
        t = tables.openFile(l.strip())

        features['artistID'] = t.root.metadata.songs[0]['artist_mbid']
        features['songID'] = t.root.metadata.songs[0]['song_id']

        duration = t.root.analysis.songs[0]["duration"]
        features['duration'] = int(round(duration))
        segment_starts = t.root.analysis.segments_start
        segment_lengths = list(segment_starts[1:] - segment_starts[:-1])

        segment_lengths.append(duration - segment_starts[-1])
        features['meanSegmentLength'] = round(avg(segment_lengths),3)
        features['varSegmentLength'] = round(var(segment_lengths),4)
        
        max_loudness_times = t.root.analysis.segments_loudness_max_time
        features['meanTimeToMaxLoudnessInSegment'] = round(avg(max_loudness_times),4)
        
        max_loudness = t.root.analysis.segments_loudness_max
        features['meanMaxSegmentLoudness'] = int(round(avg(max_loudness)))
        features['varMaxSegmentLoudness'] = round(var(max_loudness),1)
        sortedMaxLoudness = sort(max_loudness)
        features['lowerMaxSegmentLoudness'] = round(sortedMaxLoudness[len(max_loudness)/4],1)
        features['upperMaxSegmentLoudness'] = round(sortedMaxLoudness[3*len(max_loudness)/4],1)

        begin_loudness = t.root.analysis.segments_loudness_start
        features['meanBeginSegmentLoudness'] = int(round(avg(begin_loudness)))
        features['varBeginSegmentLoudness'] = round(var(begin_loudness),1)

        features['loudness']  = int(round(t.root.analysis.songs[0]['loudness']))
        features['tempo']  = int(round(t.root.analysis.songs[0]['tempo']))
        
        beats = t.root.analysis.beats_start
        beat_intervals = list(beats[1:] - beats[:-1])
        beat_intervals.append(duration - beats[-1])
        features['varBeat'] = round(var(beat_intervals),4)

        features['tatumConf'] = round(avg(t.root.analysis.tatums_confidence),3)
        tatums = t.root.analysis.tatums_start
        tatum_intervals = list(tatums[1:] - tatums[:-1])
        tatum_intervals.append(duration - tatums[-1])
        features['meanTatumLength'] = round(avg(tatum_intervals),3)

        features['tatumsPerBeat'] = int(len(tatums) / float(len(beats)))
        
        features['timeSignature'] = t.root.analysis.songs[0]['time_signature']
        features['timeSignatureConf'] = round(t.root.analysis.songs[0]['time_signature_confidence'],3)


        features['mode'] = t.root.analysis.songs[0]['mode']
        features['modeConf'] = round(t.root.analysis.songs[0]['mode_confidence'],3)

        pitches = t.root.analysis.segments_pitches
        features['pitchCov'] = cov(transpose(pitches))
        features['pitchWeights'] = (dot(transpose(pitches),pitches))
        header = ['songID', 'artistID','duration', 'meanSegmentLength', 'varSegmentLength', 'meanTimeToMaxLoudnessInSegment', 'meanMaxSegmentLoudness','varMaxSegmentLoudness','lowerMaxSegmentLoudness', 'upperMaxSegmentLoudness','meanBeginSegmentLoudness','varBeginSegmentLoudness','loudness','tempo','varBeat', 'tatumConf', 'meanTatumLength', 'tatumsPerBeat', 'timeSignature', 'timeSignatureConf','mode', 'modeConf']
        for h in header:
            print features[h],
        for r in features['pitchCov']:
            for v in r:
                print round(v,3),
        for r in features['pitchWeights']:
            for v in r:
                print int(round(v)),
        print
        t.close()
    except:
        sys.stderr.write("Error on " + l + " - " + str(sys.exc_info()[0]))
