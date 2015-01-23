# GLCD Font Extractor for Adafruit GFX LED Matrix Library

*Allows you to use different fonts for a matrix LED display*

The [Adafruit-GFX-Library](https://github.com/adafruit/Adafruit-GFX-Library) only comes with one font. This script takes a TTF "Bitmap Font" and rasterizes it into a C++ array format suitable for use with the [Adafruit-GFX-Library](https://github.com/adafruit/Adafruit-GFX-Library) for use and tested on
MAX7219 dot matrix LED modules.

 > For more information on the format of the font and how the `glcdfont.c` works and is constructed, see Smart Interaction Lab's article on [Customizing Adafruit’s 32×32 LED Matrix](http://smartinteractionlab.com/customizing-adafruits-32x32-led-matrix/).

### Caveats and Notes
1. You may need licensing permission to do this to a font you don't own.
1. It will not work on non-bitmap, anti-aliased fonts e.g. Times New Roman, as it won't be able to detect clean edges of the font.
1. Mono-spaced fonts will also give you better, more even spacing/kerning.
1. **Alternative:** This UI-based font creator might work for you instead - [GLCD Font Creator](http://www.mikroe.com/glcd-font-creator/).


## Installation

 1. Clone repo or download zip.
 1. Install dependencies via ```requirements.txt``` e.g. ```pip install -r requirements.txt```

## Usage


To create a pixel font array out of `gameboy.ttf` and write it to a file, run:
```shell
font-extractor/font-extractor.py test/fonts/gameboy.ttf --output=glcdfont.c --default-array-size
```

This example will output a _partial_ `glcdfont.c` whose contents can be copied and pasted into array section of you `glcdfont.c` file in your Adafruit-GFX-Library location e.g. `~/Documents/Arduino/libraries/Adafruit-GFX-Library-master`

You can run `font-extractor.py` for a list of all arguments.
