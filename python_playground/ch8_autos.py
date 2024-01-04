import sys, random, argparse
from PIL import Image, ImageDraw

# create spacing/depth example
def createSpacingDepthExample():
    tiles = [Image.open(r'D:\浏览器下载\a.png'), Image.open(r'D:\浏览器下载\b.png'),
             Image.open(r'D:\浏览器下载\c.png')]
    img = Image.new('RGB', (600,400), (0,0,0))
    spacing = [10,20,40]
    for j, tile in enumerate(tiles):
        for i in range(8):
            img.paste(tile, (10+i*(100+j*10), 10+j*100))
    img.save('sdepth.png')

# 若用户不提供平铺图像,用随机圆创建一张平铺图象
def createRandomTile(dims):
    # create image
    img = Image.new('RGB', dims)
    draw = ImageDraw.Draw(img)
    # set the radius of a random circle to 1% of 
    # width or height, whichever is smaller
    r= int(min(*dims)/100)
    # number of circles
    n = 1000
    # draw random circles
    for i in range(n):
        # - r makes sure that the circles stay inside and aren't cut off
        # at the edge of the image so that they'll look better when tiled 
        x,y = random.randint(0,dims[0]-r), random.randint(0,dims[1]-r)
        fill = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        draw.ellipse((x-r,y-r,x+r,y+r), fill)
    return img

# 重复给定的平铺图像
def createTiledImage(tile, dims):
    # create the new image
    img = Image.new('RGB', dims)
    W, H = dims
    w, h =tile.size
    # calculate the number of tiles needed
    cols= int(W/w)+1
    rows = int(H/h)+1
    # paste the tile into the image
    for i in range(rows):
        for j in range(cols):
            img.paste(tile,(j*w,i*h))
    # output the image
    return img

# creata a depth map for testing
def createDepthMap(dims):
    dmap = Image.new('L',dims)
    dmap.paste(10,(200,25,300,125))
    dmap.paste(30,(200,150,300,250))
    dmap.paste(20,(200,275,300,375))
    return dmap

# given a detph map image and an input image,
# create a new iamge wiwth pixels shifted according to detph
def createDepthShiftedImage(dmap, img):
    # size check
    assert dmap.size == img.size 
    sImg = img.copy()
    # get pixel access
    pixD = dmap.load()
    pixS = sImg.load()
    # shift pixels output based on depth map
    cols, rows = sImg.size
    for j in range(rows):
        for i in range(cols):
            xshift = pixD[i, j]/10
            xpos = i - 140 + xshift
            if xpos > 0 and xpos < cols:
                pixS[i, j] = pixS[xpos, j]
    # return shifted image
    return sImg

def createAutostereogram(dmap, tile):
    # convert the depth map to a single channel if needed
    if dmap.mode != 'L':
        dmap = dmap.convert('L')
    # if no image is specified for a tile, create a random circles tile
    if not tile:
        tile = createRandomTile((100,100))
    # create an image by tiling
    img = createTiledImage(tile,dmap.size)
    # create a shifted image using depth map values
    sImg = img.copy()
    # get access to image pixels by loading the Image object first 
    pixD = dmap.load()
    pixS = sImg.load()
    # shift pixels horizontally based on depth map  
    cols, rows = sImg.size 
    for j in range(rows):
        for i in range(cols): 
            xshift = pixD[i,j]/10
            xpos = i - tile.size[0] + xshift
            if xpos > 0 and xpos < cols:
                pixS[i,j] = pixS[xpos, j]
    return sImg

def main():
    print('creating autostereogram...')
    # create parser
    parser = argparse.ArgumentParser(description='Autostereograms...')
    # add expected arguments
    parser.add_argument('--depth', dest='dmFile', required=True)
    parser.add_argument('--tile', dest='tileFile', required=False)
    parser.add_argument('--out', dest='outFile', required=False)

    # parse args
    args = parser.parse_args()
    
    # set the output file
    if args.outFile:
        outFile = args.outFile
    else:
        outFile = 'as.png'
    
    # set tile 
    tileFile = False
    if args.tileFile:
        tileFile = Image.open(args.tileFile)
    
    # open depth map
    dmImg = Image.open(args.dmFile)
    # create stereogram
    asImg = createAutostereogram(dmImg, tileFile)
    # write out
    asImg.save(outFile)

if __name__ == '__main__':
    main()

