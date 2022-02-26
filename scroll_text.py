import time
import sys
from colorsys import hsv_to_rgb
from PIL import Image, ImageDraw, ImageFont

import os.path
import time
import numpy as np
from PIL import Image
import copy


BUTTON_W = 'w'
BUTTON_S = 's'
BUTTON_A = 'a'
BUTTON_D = 'd'
BUTTON_Z = 'z'
BUTTON_X = 'x'
BUTTON_C = 'c'
BUTTON_V = 'v'
BUTTON_Q = 'q'
BUTTON_E = 'e'
ROOT = os.path.split(__file__)[0]


class TextRenderer():

    def __init__(self, mqueue, repeat = 2) -> None:
        self.matrix = np.zeros((16, 16))
        self.mqueue = mqueue
        self.loaded_files = None
        self.menu_scroll = 0
        self.repeat = repeat

    def clear(self):
        self.matrix = np.zeros((16, 16))

    def scroll_menu(self, direction):
        menu_scroll = self.menu_scroll
        if (menu_scroll + direction) >= len(self.loaded_files):
            self.menu_scroll = 0
        elif 0 <= (menu_scroll + direction) < len(self.loaded_files):
            self.menu_scroll += direction
        elif (menu_scroll + direction) < 0:
            self.menu_scroll = len(self.loaded_files) - 1
        print("TextRenderer", menu_scroll)

    def getMatrix(self):
        matrix_flipped = np.flip(self.matrix, 0)
        alternate_rows, alternate_rows_flipped = matrix_flipped[0::2], np.flip(matrix_flipped[1::2], 1)
        matrix = []
        for n, f in zip(alternate_rows, alternate_rows_flipped):
            matrix.extend(n)
            matrix.extend(f)
        return np.asarray(matrix).tolist()

    def render(self, callback = None):
        self.loaded_files = [
            "hello", "1", "2"
        ]
        while True:
            if not self.mqueue.empty():
                event = self.mqueue.get()
                if event == BUTTON_Q:
                    break
                if event == BUTTON_W:
                    self.scroll_menu(-1)
                if event == BUTTON_S:
                    self.scroll_menu(1)
                if event == BUTTON_E:
                    self.clear()
                    text = self.loaded_files[self.menu_scroll]
                    if callback is not None:
                        self.scrollText(text, (lambda: callback(self.getMatrix())))
            time.sleep(1 / 8)

    def scrollText(self, text, callback):
        display_width = 16
        display_height = 16
        font = ImageFont.truetype("LiberationMono-Regular.ttf", 18)
        # Measure the size of our text, we only really care about the width for the moment
        # but we could do line-by-line scroll if we used the height
        text_width, text_height = font.getsize(text)

        # Create a new PIL image big enough to fit the text
        image = Image.new('P', (text_width + display_width + display_width, display_height), 0)
        draw = ImageDraw.Draw(image)

        # Draw the text into the image
        draw.text((display_width, -1), text, font=font, fill=255)
        image.save("img.png", "PNG")
        offset_x = 0
        for i in range(self.repeat):
            while True:
                if not self.mqueue.empty():
                    event = self.mqueue.get()
                    if event == BUTTON_Q:
                        break

                for x in range(display_width):
                    for y in range(display_height):
                        if image.getpixel((x + offset_x, y)) == 255:
                            self.matrix[y][x] = 1
                        else:
                            self.matrix[y][x] = 0
                offset_x += 1
                if offset_x + display_width > image.size[0]:
                    offset_x = 0
                    break
                time.sleep(0.09) #scrolling text speed
                callback()
