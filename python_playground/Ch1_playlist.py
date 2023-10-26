import re, argparse
import sys
from matplotlib import pyplot as plt
import plistlib
import numpy as np


def findDuplicates(fileName):
    print(f'Finding duplicate tracks in {fileName}')
    # get xml file
    with open(fileName, 'rb') as f:
        pl = plistlib.load(f)
    tracks = pl['Tracks']
    # create a track name dictionary
    # trackNames: key--> track name, value-->(duration, count)
    trackNames = {}
    for trackId, track in tracks.items():
        try:
            name = track['Name']
            duration = track['Total Time']
            if name in trackNames:
                if duration//1000 == trackNames[name][0]//1000:
                    count = trackNames[name][1]
                    trackNames[name] = (duration,count+1)
            else:
                trackNames[name] =(duration,1)
        except:
            pass
    # store duplicates as (name,count) tuples
    dups = []
    for k,v in trackNames.items():
        if v[1] > 1:
            dups.append((v[1], k))
    
    #save duplicates to a file
    if len(dups) > 0:
        print(f'Found {len(dups)} duplicates. Track names saved to dup.txt')
    else:
        print('No duplicate tracks found.')
        return 
        
    with open('dups.txt', 'w') as f:
        for val in dups:
            f.write('[%d] %s\n' % (val[0],val[1]))
    


def findCommonTracks(fileNames):
    trackNameSets = []
    for filename in fileNames:
        trackNames = set()
        # read the playlist
        with open(filename,'rb') as f:
            pl = plistlib.load(f)
        tracks = pl['Tracks']
        for trackId, track in tracks.items():
            try:
                trackNames.add(track['Name'])
            except:
                pass
        trackNameSets.append(trackNames)
    commonTracks = set.intersection(*trackNameSets)
    # write to file
    if len(commonTracks) > 0:
        with open('./common.txt', 'w') as f:
#             f.writelines(commonTracks)
            for val in commonTracks:
                f.write(val+'\n')
        print(f'{len(commonTracks)} common tracks found\nTrack names written to common.txt')
    else:
        print('No common tracks')
                

# thers is no Album Rating 
def plotStats(fileName):
    with open(fileName, 'rb') as f:
        pl= plistlib.load(f)
    tracks = pl['Tracks']
    years= []
    durations =[]
    for trackId, track in tracks.items():
        try:
            years.append(track['Year'])
            durations.append(track['Total Time'])
        except:
            pass
    if years == [] or durations == []:
        print(f'No valid album year/total time in {fileName}')
        return
    
    # plot data 
    x= np.array(durations, np.int32)
    x = x/ 60000.0
    y = np.array(years, np.int16)
    plt.figure(figsize=(16,18))
    plt.subplot(2,1,1)
    plt.plot(x,y,'o')
    plt.axis([0,10,1950,np.max(y)+2])
    plt.yticks(np.arange(1950,2030,5))
    plt.xlabel('Track Duration')
    plt.ylabel('Track Year')

    # plot histgram
    plt.subplot(2,1,2)
    plt.hist(x, bins=20)
    plt.xlabel('Track Duration')
    plt.ylabel('Count')

    plt.show()


def main():
    # create parser
    descStr = '''This program analyzes playlist files(.xml) exported from iTunes'''
    parser = argparse.ArgumentParser(description=descStr)

    # add a manually exclusive group of arguments
    group = parser.add_mutually_exclusive_group()

    # add expected arguments
    group.add_argument('--common', nargs='*', dest='plFiles', required=False)
    group.add_argument('--stats', dest='plFile', required=False)
    group.add_argument('--dup',dest='plFileD', required=False)

    # parse args
    args = parser.parse_args()

    if args.plFiles:
        # find common tracks
        findCommonTracks(args.plFiles)
    elif args.plFile:
        plotStats(args.plFile)
    elif args.plFileD:
        findDuplicates(args.plFileD)
    else:
        print('These are not the tracks you are looking for')

if __name__ =='__main__':
    main()