'''问题： 
+ piano模式有错误
+ 展示波形和播放乐符的功能耦合在一起了，并且视听不同步'''
import sys, os 
import time, random
import wave, argparse, pygame
import numpy as np
from collections import deque
from matplotlib import pyplot as plt


# show plot of algorithm in action? 
gShowPlot = False

# notes of a Pentatonic Minor scale
# piano C4-E(b)-F-G-B(b)-C5
pmNotes = {'C4':262, 'Eb':311, 'F':349, 'G':391, 'Bb':466}

# write out WAV file
def writeWAVE(fname, data):
    # open file
    file = wave.open(fname, 'wb')
    # WAV file params
    nChannels = 1
    sampleWidth = 2
    frameRate = 44100
    nFrames = 44100
    # set params
    file.setparams((nChannels, sampleWidth, frameRate, nFrames, 'NONE', 'noncompressed'))
    file.writeframes(data)
    file.close()

# generate note of given frequency
def generateNote(freq):
    '''
    freq: 音符本身的频率
    samleRate: 采样的频率
    N:　环形缓冲区的长度
    buf: 在[-0.5, 0.5]范围内的随机初始的长度为N的环形缓冲区
    samples: 初始化为全0的长度为nSamples的样本缓冲区
    '''
    nSamples = 44100
    sampleRate = 44100
    N = int(sampleRate/freq)
    # initialize ring buffer
    buf = deque([random.random() - 0.5 for i in range(N)])
    
    # plot of flag set
    if gShowPlot:
        axline, = plt.plot(buf)

    # initialze samples buffer
    samples = np.array([0]*nSamples, 'float32')
    # implement KS by loop
    for i in range(nSamples):
        samples[i] = buf[0]
        avg = 0.996 * 0.5*(buf[0]+buf[1])
        buf.append(avg)
        buf.popleft()
        if gShowPlot:
            if i % 1000 ==0:
                axline.set_ydata(buf)
                plt.pause(0.001)
                plt.draw()

    # convert samples to 16-bit values and then to a string
    # the maximum value is 32767 for 16 bit
    samples = np.array(samples*32767, 'int16')
    return samples.tobytes()

# play a wav file
class NotePlayer:
    # constructor
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 1, 2048)
        pygame.init()
        # directory of notes
        self.notes = {}
    
    # add a note
    def add(self, fileName):
        self.notes[fileName] = pygame.mixer.Sound(fileName)

    # play a note
    def play(self, fileName):
        try:
            self.notes[fileName].play()
        except:
            print(f'{fileName} not found!')
    
    def playRandom(self):
        index = random.randint(0, len(self.notes)-1)
        note = list(self.notes.values())[index]
        note.play()


def main():
    # declare global var
    global gShowPlot

    parser = argparse.ArgumentParser(description='Generate sound with Karplus-Strong algorithm')
    # add arguments
    parser.add_argument('--display', action='store_true', required=False)
    parser.add_argument('--play', action='store_true', required=False)
    parser.add_argument('--piano', action='store_true', required=False)

    args = parser.parse_args()

    # show plot if flag set
    if args.display:
        gShowPlot = True
        plt.ion()

    # create note player
    nPlayer = NotePlayer()
    
    print('creating notes...')
    for name, freq in list(pmNotes.items()):
        fileName = name + '.wav'
        if not os.path.exists(fileName) or args.display:
            data = generateNote(freq)
            print(f'creating {fileName}...')
            writeWAVE(fileName, data)
        else:
            print(f'{fileName} already created, skipping...')
        
        nPlayer.add(fileName)

        if args.display:
            nPlayer.play(fileName)
            time.sleep(0.5)

    # play a random tune
    if args.play:
        while True:
            try:
                nPlayer.playRandom()
                # rest -1 to 8 beats
                rest = np.random.choice([1,2,4,8], 1, p=[0.15,0.7,0.1,0.05])
                time.sleep(0.25*rest[0])
            except KeyboardInterrupt:
                exit()


    if args.piano:
        while True:
            for event in pygame.event.get():
                if (event.type == pygame.KEYUP):
                    print('key pressed')
                    nPlayer.playRandom()
                    time.sleep(0.5)


if __name__ == '__main__':
    main()