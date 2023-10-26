import sys, random, argparse
import math
import numpy as np
from PIL import Image

# grayscale level values from 
# # http://paulbourke.net/dataformats/asciiart/
# 70 levels of gray
gscale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
# 10 levels of gray
gscale2 = '@%#*+=-:. '

def getAverageL(image):
    '''
    given a PIL Image, return average value of grayscale value
    '''
    # get the image as a numpy array
    im = np.array(image)
    # get the dimensions
    w,h = im.shape
    # get the average 
    return np.average(im.reshape(w*h))

def convertImageToAscii(filename, cols, scale, moreLevels):
    '''
    given Image and dimensions(rows, cols), return an m*n lists of Image
    '''
    # declare globals
    global gscale1, gscale2
    # open image and convert to grayscale
    image = Image.open(filename).convert('L')
    # store the image dimensions
    W, H = image.size[0], image.size[1]
    print(f'input image dims: ({W}, {H})')
    # compute the tile width
    w = W/cols
    # compute the tile height based on the aspect ratio and scale of the font 
    h = w/scale
    # compute the number of rows to use in the final grid 
    rows = int(H/h)
    
    print(f'cols: {cols}, rows: {rows}')
    print(f'tile dimension: ({w}, {h})')

    # check if image size is too small
    if cols > W or rows > H:
        print('Image too small for specified cols!')
        exit(0)
    # an ascii image is a list of character strings
    aimg = []
    # generate the list of tile dimensions
    for j in range(rows):
        y1 = int(j*h)
        y2 = int((j+1)*h)
        # correct the last tile 
        if j == rows-1:
            y2 = H
        # append an empty string
        aimg.append('')
        for i in range(cols):
            # crop the image to fit the tile
            x1 = int(i*w)
            x2 = int((i+1)*w)
            # correct the last tile 
            if i == cols-1:
                x2 = W
            # crop the image to extract the tile into another Image object 
            img = image.crop((x1,y1,x2,y2))
            # get the average luminance 
            avg = int(getAverageL(img))
            # look up the ASCII character for grayscale value avg
            if moreLevels:
                gsval = gscale1[int((avg*69)/255)]
            else:
                gsval = gscale2[int((avg*9)/255)]
            # append the ASCII character to the string
            aimg[j] += gsval

    # return text image
    return aimg

def main():
    # create parser
    desc = 'This program converts an image into ASCII art.' 
    parser = argparse.ArgumentParser(description=desc)

    # add expected arguments
    parser.add_argument('--file', dest='imgFile', required=True)
    parser.add_argument('--scale', dest='scale', default=0.43, required=False)
    parser.add_argument('--out', dest='outFile',required=False)
    parser.add_argument('--cols', dest='cols', default=80, required=False)
    parser.add_argument('--moreLevels', dest='moreLevels', action='store_true')

    args = parser.parse_args()

    if not args.outFile:
        args.outFile = 'out.txt'
    
    print('generating ASCII art...')
    # convert  image to ASCII text
    aimg = convertImageToAscii(args.imgFile, int(args.cols), float(args.scale), args.moreLevels)

    # save the txt file
    with open(args.outFile, 'w') as f:
        for row in aimg:
            f.write(row+'\n')

    print(f'ASCII file written to {args.outFile}')

if __name__ == '__main__':
    main()
 
    
    
    