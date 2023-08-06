# -*- coding: utf-8 -*-
import curses

from dataclasses import dataclass

from PIL import Image

from vindauga.types.draw_buffer import DrawBuffer
from vindauga.types.rect import Rect

COLOR_STEPS = (0, 0x5f, 0x87, 0xaf, 0xd7, 0xff)
FLAG_FG = 1
FLAG_BG = 2
GRAYSCALE_STEPS = (
    0x08, 0x12, 0x1c, 0x26, 0x30, 0x3a, 0x44, 0x4e, 0x58, 0x62, 0x6c, 0x76,
    0x80, 0x8a, 0x94, 0x9e, 0xa8, 0xb2, 0xbc, 0xc6, 0xd0, 0xda, 0xe4, 0xee
)


@dataclass
class BitMap:
    pattern: int
    charOrd: int
    char: str
    
BLOCK = BitMap(0x0000ffff, 0x2584, '▄')  # lower 1/2


@dataclass
class Color:
    r: int
    g: int
    b: int

    def __floordiv__(self, other):
        self.r //= other
        self.g //= other
        self.b //= other
        return self

    def __add__(self, other):
        self.r += other[0]
        self.g += other[1]
        self.b += other[2]


@dataclass
class CharData:
    fgColor: Color = Color(0, 0, 0)
    bgColor: Color = Color(0, 0, 0)
    char: str = '▄'


@dataclass
class Size:
    width: int
    height: int

    def scaled(self, scale):
        return Size(int(self.width * scale), int(self.height * scale))

    def fittedWithin(self, container):
        scale = min(container.width / self.width, container.height / self.height)
        return self.scaled(scale)

def openFile(filename):
    im = Image.open(filename)
    im.draft("RGB", im.size)
    return im

def getBitmapCharData(bitmap: BitMap, input_image, x0: int, y0: int):
    result = CharData()
    result.char = bitmap.char

    fgCount = 0
    bgCount = 0
    mask = 0x80000000

    for y in range(y0, y0 + 8):
        for x in range(x0, x0 + 4):
            if bitmap.pattern & mask:
                avg = result.fgColor
                fgCount += 1
            else:
                avg = result.bgColor
                bgCount += 1

            avg += input_image[x, y]
            mask >>= 1

    if bgCount:
        result.bgColor //= bgCount

    if fgCount:
        result.fgColor //= fgCount
    return result

def clampByte(value):
    return min(max(0, value), 255)


def sqr(n):
    return n * n


def bestIndex(value, data):
    diffs = ((i, abs(d - value)) for i, d in enumerate(data))
    diffs = sorted(diffs, key=lambda x: x[1])
    return diffs[0][0]


def emitColor(r, g, b):
    r = clampByte(r)
    g = clampByte(g)
    b = clampByte(b)

    ri = bestIndex(r, COLOR_STEPS)
    bi = bestIndex(b, COLOR_STEPS)
    gi = bestIndex(g, COLOR_STEPS)

    rq = COLOR_STEPS[ri]
    gq = COLOR_STEPS[gi]
    bq = COLOR_STEPS[bi]

    gray = int(round(r * 0.2989 + g * 0.5870 + b * 0.1140))
    gri = bestIndex(gray, GRAYSCALE_STEPS)
    grq = GRAYSCALE_STEPS[gri]

    if (0.3 * sqr(rq - r) + 0.59 * sqr(gq - g) + 0.11 * sqr(bq - b) <
            0.3 * sqr(grq - r) + 0.59 * sqr(grq - g) + 0.11 * sqr(grq - b)):
        colorIndex = 16 + 36 * ri + 6 * gi + bi
    else:
        colorIndex = 232 + gri

    return colorIndex


def emitImage(image):
    w, h = image.size
    pixels = image.load()
    lines = []
    for y in range(0, h - 8, 8):
        buffer = DrawBuffer()
        for i, x in enumerate(range(0, w - 4, 4)):
            charData = getBitmapCharData(BLOCK, pixels, x, y)
            bg = emitColor(charData.bgColor.r, charData.bgColor.g, charData.bgColor.b)
            fg = emitColor(charData.fgColor.r, charData.fgColor.g, charData.fgColor.b)
            buffer.moveCStr(i, charData.char, )
        lines.append(buffer)
    return lines

def wallpaper(filename, bounds: Rect):
    maxWidth = bounds.width * 4
    maxHeight = bounds.height * 8

    img = openFile(filename).convert('RGB')
    iw, ih = img.size
    size = Size(iw, ih)
    if iw > maxWidth or ih > maxHeight:
        size = size.fittedWithin(Size(maxWidth, maxHeight))
        img = img.resize((size.width, size.height))
    return size.width//4, size.height//8, emitImage(img)
