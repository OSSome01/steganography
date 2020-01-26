import os
from PIL import Image
import sys
from math import sqrt
from random import randrange

def convert_to_binary(string_):
    binary = []
    for i in string_:
        binary.append(format(ord(i),'08b'))

    return binary

def convert_to_ascii(data):
    ascii = []

    for i in data:
        ascii.append(ord(i))

    return ascii

def modify_pixels(pixels, string):
    binary = convert_to_binary(string)
    length = len(binary)
    pixdata = iter(pixels)
    modified_pixels = []

    for i in range(0,length):
        pix = [pixls for pixls in pixdata.__next__()[:3]+
                                    pixdata.__next__()[:3]+
                                        pixdata.__next__()[:3]]

        for j in range(0,8):
            if binary[i][j] == '0' and pix[j]%2 != 0:
                pix[j] = pix[j] - 1

            elif binary[i][j] == '1' and pix[j]%2 == 0:
                if pix[j] != 0:
                    pix[j] = pix[j] - 1
                elif pix[j] == 0:
                    pix[j] = pix[j] + 1

        if i == length - 1:
            if pix[-1]%2 == 0:
                pix[-1] = pix[-1] - 1
        else:
            if pix[-1]%2 != 0:
                pix[-1] = pix[-1] -1
        pix = tuple(pix)
        modified_pixels.append(pix[0:3])
        modified_pixels.append(pix[3:6])
        modified_pixels.append(pix[6:9])
    
    return modified_pixels

def modify_pixels_ascii(im, data):
    ascii_list = convert_to_ascii(data)
    pixels = iter(im.getdata())
    length = len(ascii_list)
    modifed_pixels = []
    counter = 0

    for j in pixels:
        if counter > length - 1:
            break
        
        i = [int(k) for k in j]
        i[0] = ascii_list[counter]
        counter = counter + 1
        i = tuple(i)
        modifed_pixels.append(i)

    return modifed_pixels    

def encode(pixels, text):
    w = pixels.size[0]
    (x, y) = (0, 0)

    for pxls in modify_pixels(pixels.getdata(), text):
        pixels.putpixel((x,y),pxls)

        if x == w - 1:
            x = 0
            y = y + 1
        else:
            x = x + 1

def encode_ascii(im,data):
    w = im.size[0]
    (x, y) = (0, 0)

    for pxls in modify_pixels_ascii(im, data):
        im.putpixel((x,y),pxls)
        
        if x == w - 1:
            x = 0
            y = y + 1
        else:
            x = x + 1

def decode(pixels):
    pixdata = iter(pixels.getdata())
    str_data = ''
    while 1:
        pix = [pxls for pxls in pixdata.__next__()[:3]+
                                    pixdata.__next__()[:3]+
                                        pixdata.__next__()[:3]]

        binstr = ''

        for i in pix[:8]:
            if i%2 == 0:
                binstr = binstr + '0'
            else:
                binstr = binstr + '1'
        
        str_data = str_data + chr(int(binstr,2))

        if pix[-1]%2 != 0:
            return str_data

def decode_ascii(im):
    pixels = iter(im.getdata())

    decoded_string = ''

    for i in pixels:
        if i[0] > 130:
            break
        decoded_string = decoded_string + chr(i[0])
    return decoded_string

def main():
    if sys.argv[1] == '-e':
        im = Image.open(sys.argv[2])
        output_name = sys.argv[3]
        string = sys.argv[4]
        
        if sys.argv[4].find('.') >=0:
            if sys.argv[4].split('.')[1] == 'txt':
                file = open(sys.argv[4],'r')
                string = file.read()
                file.close()
                print("read from file: ", sys.argv[4])

        encode(im,string)
        im.save(output_name)

    elif sys.argv[1] == '-ea':
        imgdim = int(sqrt(len(sys.argv[3]))+1)

        if imgdim**2 < 1000*1000:
            imgdim = 1000

        im = Image.new(mode = "RGB", size = (imgdim, imgdim))
        output_name = sys.argv[2]
        string = sys.argv[3]
        px = im.load()

        for i in range(0,randrange(im.size[0]-1)):
            for j in range(0,randrange(im.size[1]-1)):
                px[j,i] = (randrange(140,250), randrange(140,250), randrange(140,250))

        if sys.argv[3].find('.') >=0:
            if sys.argv[3].split('.')[1] == 'txt':
                file = open(sys.argv[3],'r')
                string = file.read()
                file.close()
                print("read from file:", sys.argv[3])
        
        encode_ascii(im,string)
        im.save(output_name)

    elif sys.argv[1] == '-d':
        im = Image.open(sys.argv[2])
        if len(sys.argv) > 3:
            if sys.argv[3] == '-f':
                file = open(sys.argv[4],'a+')
                file.truncate(0)
                file.write(decode(im))
                file.close()
        else:
            print(decode(im))

    elif sys.argv[1] == '-da':
        im = Image.open(sys.argv[2])
        if len(sys.argv) > 3:
            if sys.argv[3] == '-f':
                file = open(sys.argv[4],'a+')
                file.truncate(0)
                file.write(decode_ascii(im))
                file.close()
        else:
            print(decode_ascii(im))
    
    else:
        print('usage: -e  [input_filename] [output_filename] [string]')
        print('       -e  [input_filename] [output_filename] [data_input_filename]')
        print('       -ea [output_filename] [string]')
        print('       -ea [output_filename] [data_input_filename]')
        print('       -d  [input_filename]')
        print('       -d  [input_filename] -f [output_filename]')
        print('       -da [input_filename]')
        print('       -da [input_filename] -f [output_filename]')

if __name__ == '__main__':
    main()