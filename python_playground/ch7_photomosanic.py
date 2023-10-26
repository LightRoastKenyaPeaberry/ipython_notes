import sys, os, random, argparse
from PIL import Image
import imghdr
import numpy as np


def getImages(imageDir):
    '''
    given a directory of images, return a list of Images
    '''
    files = os.listdir(imageDir)
    imgs  = []
    for file in files:
        if file.split('.')[-1] in ['jpg', 'jpeg', 'png']:
            file_path = os.path.join(imageDir,file)
            try:
                # explicit load so we dont run into a resource crunch
                fp = open(file_path, 'rb')
                im = Image.open(fp)
                imgs.append(im)
                # force loading the image data from file
                im.load()
                # close the file
                fp.close()
            except:
                # skip 
                print(f'Invalid image: {file_path}')
    return imgs
    
def getAverageRGB(image):
    '''
    return the average color value as (r,g,b) for each input image
    '''
    # get each tile image as numpy array
    im = np.array(image)
    # get the shape of each input image
    w,h,d = im.shape
    # get the average RGB value
    return tuple(np.average(im.reshape(w*h,d), axis = 0))

def splitImage(image,size):
    '''
    given the image and dimensions (rows, cols), return a m*n list of images
    '''
    W, H = image.size[0], image.size[1]
    m, n = size
    w, h = int(W/n), int(H/m)
    # image list
    imgs = []
    # gemerate a list of dimensions
    for j in range(m):
        for i in range(n):
            # append cropped image
            imgs.append(image.crop((i*w, j*h, (i+1)*w, (j+1)*h)))
    return imgs

def getBestMatchIndex(input_avg, avgs):
    '''
    return index of the best image match based on average RGB value distance
    '''
    # input image average
    avg = input_avg
    # get the closest RGB value to input, based on RGB distance
    index = 0 
    min_index = 0
    min_dist = float('inf')
    for val in avgs:
        dist = (val[0] - avg[0])**2 + (val[1] - avg[1])**2 + \
        (val[2] - avg[2])**2
        if dist < min_dist:
            min_dist = dist
            min_index = index 
        index +=1
    return min_index

def createImageGrid(images, dims):
    '''
    given a list of images and a grid size (m,n), create a grid of iamges'''
    m, n = dims

    # sanity check
    assert m*n == len(images)

    # get the maximun height and width of the images
    # dont assume they're all equal
    width = max([img.size[0] for img in images])
    height = max([img.size[1] for img in images])

    # create the target image
    grid_img = Image.new('RGB', (n*width,m*height))

    # paste the tile images into the image grid
    for index in range(len(images)):
        row = int(index/n)
        col = index - n*row
        grid_img.paste(images[index], (col*width, row*height))
    
    return grid_img

def createPhotomosiac(target_image, input_images, grid_size,  reuse_images=True):
    '''
    create photomosaic given target and input images
    '''

    print('splitting input image...')
    # split the target image into tiles
    target_images = splitImage(target_image, grid_size)

    print('finding image matches...')
    # for each tile, pick one matching input image
    output_images = []
    # for user feedback
    count = 0
    batch_size = int(len(target_images)/10)

    # calculate the average of the input image
    avgs = []
    for img in input_images:
        avgs.append(getAverageRGB(img))

    for img in target_images:
        # compute the average RGB value of the image
        avg = getAverageRGB(img)
        # find the matching index of closest RGB value
        # from a list of average RGB values
        match_index = getBestMatchIndex(avg, avgs)
        output_images.append(input_images[match_index])
        if count > 0 and batch_size > 10 and count % batch_size == 0:
            print(f'processed {count} of {len(target_images)}')
        count +=1
        # remove the selected image from input if flag set
        if not reuse_images:
            input_images.pop(match_index)
            avgs.pop(match_index)

    print('creating mosaic...')
    mosaic_image = createImageGrid(output_images,grid_size)

    # display the mosaic
    return mosaic_image


# gather our code in a main() function
def main():
    parser = argparse.ArgumentParser(description='Create a photomosaic from input images')
    # add arguments
    parser.add_argument('--target-image', dest='target_image', required=True)
    parser.add_argument('--input-folder', dest='input_folder', required=True)
    parser.add_argument('--grid-size', nargs=2, dest='grid_size', required=True)
    parser.add_argument('--output-file', dest='outfile', required=False)

    args = parser.parse_args()
    
    #####  INPUTS  #####

    # target images
    target_image = Image.open(args.target_image)

    # input images
    print('reading input folder...')
    input_images = getImages(args.input_folder)

    # check if any valid input iamges found
    if len(input_images) == 0:
        print(f'No input images found in {args.input_folder}')
        exit()

    # shuffle list to get a more varies output?
    random.shuffle(input_images)

    # size of the grid
    grid_size = (int(args.grid_size[0]), int(args.grid_size[1]))

    # output
    if args.outfile:
        output_filename = args.outfile
    else:
        output_filename = 'mosaic.png'
    
    # reuse any image in input
    reuse_images = True

    # resize the input to fit the original image size?
    resize_input = True

    ##### END INPUTS #####


    print('starting photomosaic creation...')
    # if not reuse photo, ensure m*n <= num of images
    if not reuse_images:
        if grid_size[0]*grid_size[1] > len(input_images):
            print('grid size lesser than number of iamges')
            exit()
    # resizing input
    if resize_input:
        print('resizing images...')
        # for given grid size, compute the maximun width and height for the tiles
        dims = (int(target_image.size[0]/grid_size[1]), 
            int(target_image.size[1]/grid_size[0])) 
        print(f'max tile dims: {dims}')
        # resize
        for img in input_images:
            img.thumbnail(dims)

    # create photomosaic 
    mosaic_image = createPhotomosiac(target_image, input_images, grid_size, reuse_images)
    # write out mosaic
    mosaic_image.save(output_filename, 'PNG')

    print("saved output to %s" % (output_filename,))
    print('done.')

# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
  main()
     
    


