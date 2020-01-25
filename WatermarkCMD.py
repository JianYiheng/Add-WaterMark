import argparse
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw


def checkArgs():
    args = argparse.ArgumentParser(description='Watermark Program')
    args.add_argument('-i', '--images', type=str, dest='imagePaths', help='path of image file', nargs='*')
    args.add_argument('-w', '--words', type=str, dest='markWord', help='watermark word')
    return args.parse_args()


def waterMark(imagePath: str, markWord: str):
    imageFile = Image.open(imagePath)
    if imageFile.mode != 'RGBA':
        imageFile = imageFile.convert('RGBA')

    textLayer = Image.new('RGBA', imageFile.size, (0, 0, 0, 0))
    textLayerDraw = ImageDraw.Draw(textLayer)

    textSize = int(imageFile.size[0]/20)
    textLayerFont = ImageFont.truetype('simfang.ttf', textSize)
    textLayerFontSize = textLayerFont.getsize(markWord)

    textPosW, textPosH = 0, 0
    flag: bool = True
    while 1:
        textLayerDraw.text([textPosW, textPosH], str(markWord), font=textLayerFont, fill=(128, 138, 135,
                                                                                          128))
        if textPosW < imageFile.size[0]:
            textPosW += 2 * textLayerFontSize[0]
        else:
            textPosW = textLayerFontSize[0] * flag
            textPosH += 3 * textLayerFontSize[1]
            flag = not flag

        if textPosH > imageFile.size[1]:
            break
    textLayer = textLayer.rotate(45)

    outputImage = Image.composite(textLayer, imageFile, textLayer)
    outputImage.save('revised.png')


def main():
    inputArgs = checkArgs()
    waterMark(inputArgs.imagePaths[0], inputArgs.markWord)


if __name__ == '__main__':
    main()
