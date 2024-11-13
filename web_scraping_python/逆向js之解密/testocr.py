import ddddocr 
from PIL import Image


ocr = ddddocr.DdddOcr()
img =  Image.open('./captcha.jpg')
text = ocr.classification(img) 
print(text.split('NSwk7i')[-1].strip())