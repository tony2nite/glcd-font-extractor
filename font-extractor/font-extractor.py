#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Extracts pixel data from a bitmap font

Usage:
  font-maker [FONT_NAME] [--verbose] [--write-debug-fontsize-files] [--default-array-size] [--output=<file>] [--font-scale=<scale>]
  font-maker (-h | --help)
  font-maker --version

Options:
  --verbose                         Write debug data to logger
  --output=<file>                   Output Adafruit encoded array to this file
  --font-scale=<scale>              A manual integer scale factor for the font. Sometimes a font can be halved.
  --write-debug-fontsize-files      Will output images of sample text at varying font sizes to check which one is clearer
  --default-array-size              Use the standard Adafruit font array height and width (5x7). Default is false, automatically detect widths, so array size in final font will not be standard
  -h --help                         Show this screen.
  --version                         Show version.

"""


from PIL import Image, ImageDraw, ImageFont
import string
import sys
import os
import codecs
import logging
import ntpath

from docopt import docopt

__version__ = '0.0.1'


# create logger
# logger = logging.getLogger('font_maker')

txt = (("\0", 0), ("", 1), ("", 2), ("", 3), ("", 4), ("", 5), ("", 6), ("\a", 7), ("\b", 8), ("  ", 9), ("\r", 10), ("\v", 11), ("\f", 12), ("\n", 13), ("", 14), ("", 15), ("", 16), ("", 17), ("", 18), ("", 19), ("", 20), ("", 21), ("", 22), ("", 23), ("", 24), ("", 25), ("", 26), ("", 27), ("", 28), ("", 29), ("", 30), ("", 31), (" ", 32), ("!", 33), ("\"", 34), ("#", 35), ("$", 36), ("%", 37), ("&", 38), ("'", 39), ("(", 40), (")", 41), ("*", 42), ("+", 43), (",", 44), ("-", 45), (".", 46), ("/", 47), ("0", 48), ("1", 49), ("2", 50), ("3", 51), ("4", 52), ("5", 53), ("6", 54), ("7", 55), ("8", 56), ("9", 57), (":", 58), (";", 59), ("<", 60), ("=", 61), (">", 62), ("?", 63), ("@", 64), ("A", 65), ("B", 66), ("C", 67), ("D", 68), ("E", 69), ("F", 70), ("G", 71), ("H", 72), ("I", 73), ("J", 74), ("K", 75), ("L", 76), ("M", 77), ("N", 78), ("O", 79), ("P", 80), ("Q", 81), ("R", 82), ("S", 83), ("T", 84), ("U", 85), ("V", 86), ("W", 87), ("X", 88), ("Y", 89), ("Z", 90), ("[", 91), ("\\", 92), ("]", 93), ("^", 94), ("_", 95), ("`", 96), ("a", 97), ("b", 98), ("c", 99), ("d", 100), ("e", 101), ("f", 102), ("g", 103), ("h", 104), ("i", 105), ("j", 106), ("k", 107), ("l", 108), ("m", 109), ("n", 110), ("o", 111), ("p", 112), ("q", 113), ("r", 114), ("s", 115), ("t", 116), ("u", 117), ("v", 118), ("w", 119), ("x", 120), ("y", 121), ("z", 122), ("{", 123), ("|", 124), ("}", 125), ("~", 126), ("", 127), ("", 128), ("", 129), ("", 130), ("", 131), (
    "", 132), ("", 133), ("", 134), ("", 135), ("", 136), ("", 137), ("", 138), ("", 139), ("", 140), ("", 141), ("", 142), ("", 143), ("", 144), ("", 145), ("", 146), ("", 147), ("", 148), ("", 149), ("", 150), ("", 151), ("", 152), ("", 153), ("", 154), ("", 155), ("", 156), ("", 157), ("", 158), ("", 159), (" ", 160), ("¡", 161), ("¢", 162), ("£", 163), ("¤", 164), ("¥", 165), ("¦", 166), ("§", 167), ("¨", 168), ("©", 169), ("ª", 170), ("«", 171), ("¬", 172), ("­", 173), ("®", 174), ("¯", 175), ("°", 176), ("±", 177), ("²", 178), ("³", 179), ("´", 180), ("µ", 181), ("¶", 182), ("·", 183), ("¸", 184), ("¹", 185), ("º", 186), ("»", 187), ("¼", 188), ("½", 189), ("¾", 190), ("¿", 191), ("À", 192), ("Á", 193), ("Â", 194), ("Ã", 195), ("Ä", 196), ("Å", 197), ("Æ", 198), ("Ç", 199), ("È", 200), ("É", 201), ("Ê", 202), ("Ë", 203), ("Ì", 204), ("Í", 205), ("Î", 206), ("Ï", 207), ("Ð", 208), ("Ñ", 209), ("Ò", 210), ("Ó", 211), ("Ô", 212), ("Õ", 213), ("Ö", 214), ("×", 215), ("Ø", 216), ("Ù", 217), ("Ú", 218), ("Û", 219), ("Ü", 220), ("Ý", 221), ("Þ", 222), ("ß", 223), ("à", 224), ("á", 225), ("â", 226), ("ã", 227), ("ä", 228), ("å", 229), ("æ", 230), ("ç", 231), ("è", 232), ("é", 233), ("ê", 234), ("ë", 235), ("ì", 236), ("í", 237), ("î", 238), ("ï", 239), ("ð", 240), ("ñ", 241), ("ò", 242), ("ó", 243), ("ô", 244), ("õ", 245), ("ö", 246), ("÷", 247), ("ø", 248), ("ù", 249), ("ú", 250), ("û", 251), ("ü", 252), ("ý", 253), ("þ", 254), ("ÿ", 255))

# The number of bits the GFX library is expecting. Not sure if this can
# change...
GFX_DEFAULT_ARRAY_WIDTH = 5
GFX_DEFAULT_ARRAY_HEIGHT = 7

MAX_LED_HEIGHT = 8

def _extract_font(fontfile, fontscale=1.0, autoscale_array=True, gldc_font_file=False, write_fontsize_files=False):
    imageheight = 20
    imagewidth = 1400
    image = Image.new("RGBA", (imagewidth, imageheight))
    draw = ImageDraw.Draw(image)

    fontsize = getoptimalfontsize(
        image, draw, fontfile, write_debug_files=write_fontsize_files)
    cropbox, cropbounds = calculatecharacterboundingbox(
        image, draw, fontfile, fontsize)

    logging.debug("cropbounds: %s", cropbounds)
    logging.debug("cropsize: %s", cropbox)
    logging.debug("fontscale: %f", fontscale)

    bytewidth = GFX_DEFAULT_ARRAY_WIDTH
    byteheight = GFX_DEFAULT_ARRAY_HEIGHT

    detectedbytewidth = int(cropbox[0] * fontscale)
    detectedbyteheight = int(cropbox[1] * fontscale)

    if autoscale_array:
        bytewidth = detectedbytewidth
        byteheight = detectedbyteheight
        logging.info(
            "Detected non-default array widths. Update GFX library with array dimensions: %dw x %dh", bytewidth, byteheight)
    elif detectedbyteheight > GFX_DEFAULT_ARRAY_HEIGHT or detectedbytewidth > GFX_DEFAULT_ARRAY_WIDTH:
        logging.warn('Font is too large for array and will crop. Detected %dx%d, AdaFruit default is %dx%d',
                     detectedbytewidth, detectedbyteheight, GFX_DEFAULT_ARRAY_WIDTH, GFX_DEFAULT_ARRAY_HEIGHT)
    # sys.exit()

    encoded = [0] * len(txt)

    font = ImageFont.truetype(fontfile, fontsize)
    # font.fontmode = "1"
    for char in txt:
        logging.debug("-------- %s %s ", char[0], char[1])

        draw.rectangle((0, 0) + image.size, (255, 255, 255, 255))
        draw.text((0, 0), char[0], (0, 0, 0, 255), font=font)
        # draw.text((0, 0), "T", (0,0,0,255), font=font)

        crop = image.crop(cropbounds)
        if fontscale is not 1:
            crop = crop.resize(
                (int(cropbox[0] * fontscale), int(cropbox[1] * fontscale)))
            # crop.save('resized.png')

        hexdata = []
        for x in range(0, bytewidth):
            line = []
            for y in reversed(range(0, min(byteheight,MAX_LED_HEIGHT))):
                try:
                    pixel = crop.getpixel((x, y))
                    if pixel[0] < 125:
                        line.append(1)
                    else:
                        line.append(0)
                except:
                    line.append(0)
            line = map(str, line)
            h = string.join(line, u'')
            h = hex(int(h, 2))
            h = h[:2] + h[2:].zfill(2)
            hexdata.append(h)
            logging.debug('%s %s', line, h)
        encoded[char[1]] = hexdata

    try:
        image.close()
    except:
        # OK. Couldn't close image
        pass
    del image
    del draw


    file = None
    header = u'// %s\nstatic const signed int FONT_WIDTH = %d;\nstatic const signed int FONT_HEIGHT = %d;\nstatic const unsigned char font[] PROGMEM = {\n' % (ntpath.basename(fontfile), bytewidth , byteheight)
    if gldc_font_file:
        file = codecs.open(gldc_font_file, 'w', 'utf-8')
        file.write(u'\ufeff')  # BOM header
        file.write(header)
        logging.info('Written font data to file: %s', gldc_font_file)
    else:
        logging.info(header)
    for index, value in enumerate(encoded):
        # output = u''
        code = u''
        letter = txt[index][0].encode('string_escape')
        letter = ''
        # if index > 161:
        #   letter = txt[index][0].decode('utf-8')
        code = code + \
            string.join(encoded[index], ', ') + ',' + \
            '\t\t// ' + str(txt[index][1]) + ', ' + letter
        if file:
            file.write(code + u'\n')
        else:
            # If you don't want a file written, write the array contents out to the console
            logging.info(code)

    if file:
        file.write('};\n')
        file.close()

# analysze font to get the best size i.e fewer colors and less aliasing


def getoptimalfontsize(image, draw, fontfile, write_debug_files=False):
    colors = []
    start = 6
    for size in range(start, 24):
        font = ImageFont.truetype(fontfile, size)
        font.fontmode = '1'
        draw.rectangle((0, 0) + image.size, (0, 0, 0, 0))
        draw.text((0, 0), 'ft' + str(size) + ':' +
                  string.ascii_letters, (0, 0, 0, 255), font=font)

        if write_debug_files:
            image.save('of-' + str(size) + '.png')
        # Getting the colors on a bitmap font gives me an apprixamation of how
        # much antialising is going on
        colors.append(len(image.getcolors()))

    logging.debug("colors", colors)
    colormin = min(colors)
    logging.debug("colormin", colormin)
    minfontsizes = [
        index for index, size in enumerate(colors) if size == colormin]
    logging.info("Optimal Font Sizes: %s", [(size + start) for size in minfontsizes])
    fontsize = start + colors.index(min(colors))
    if len(minfontsizes) > 1 and fontsize < 8:
        # don't use a tiny, tiny font
        fontsize = start + minfontsizes[1]
        logging.info(
            "Detected multiple font sizes, arbirtrarly using the second at %d", fontsize)
    logging.info("Optimal unscaled font size for rasterizing: %d", fontsize)
    return fontsize


def calculatecharacterboundingbox(image, draw, fontfile, fontsize):
    # now that we have the best font size, calculate the scaling ratio
    # ascii = string.printable[:90]
    ascii = string.ascii_letters + ''.join(str(i) for i in range(0, 10))
    # ascii = string.ascii_letters
    font = ImageFont.truetype(fontfile, fontsize)
    font.fontmode = '1'
    maxbounds = [sys.maxint, sys.maxint, 0, 0]
    tallest = ''
    widest = ''
    for char in ascii:
        draw.rectangle((0, 0) + image.size, (0, 0, 0, 0))
        draw.text((0, 0), char, (0, 0, 0), font=font)
        quantized = image.quantize(2)
        cropbounds = quantized.getbbox()

        # check this character acutally printed, maybe it's not in the font
        if len(image.getcolors()) > 1:
            if cropbounds[0] < maxbounds[0]:
                widest = char
                maxbounds[0] = cropbounds[0]
            if cropbounds[1] < maxbounds[1]:
                tallest = char
                maxbounds[1] = cropbounds[1]
            if cropbounds[2] > maxbounds[2]:
                widest = char
                maxbounds[2] = cropbounds[2]
            if cropbounds[3] > maxbounds[3]:
                tallest = char
                maxbounds[3] = cropbounds[3]
    logging.info("Tallest Character: %s", tallest)
    logging.info("Widest Character: %s", widest)
    # crop = quantized.crop(cropbounds)

    # crop.save('cropped.png')
    logging.debug("maxbounds %s", maxbounds)
    size = (maxbounds[2] - maxbounds[0], maxbounds[3] - maxbounds[1])
    logging.info("size %s", size)

    return size, maxbounds


def main():
    arguments = docopt(__doc__, version=__version__)
    format = '%(message)s'
    if (arguments['--verbose']):
        logging.basicConfig(level=logging.DEBUG, format=format)
        logging.debug('--verbose')
    else:
        logging.basicConfig(level=logging.INFO, format=format)

    if (arguments['FONT_NAME']):
        write_fontsize_files = arguments['--write-debug-fontsize-files']
        output = arguments['--output']

        user_default_font_array_widths = arguments['--default-array-size']
        autoscale = True
        if user_default_font_array_widths:
            autoscale = False

        font_scale = 1.0
        if arguments['--font-scale']:
            font_scale = float(arguments['--font-scale'])
        _extract_font(arguments['FONT_NAME'], autoscale_array=autoscale,
                      gldc_font_file=output, fontscale=font_scale, write_fontsize_files=write_fontsize_files)
    else:
        print __doc__


if __name__ == '__main__':
    main()
