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


class ImageRenderer():

    def __init__(self, mqueue) -> None:
        self.matrix = np.zeros((16, 16))
        self.mqueue = mqueue
        self.loaded_files = None
        self.menu_scroll = 0

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
        print("ImageRenderer", menu_scroll)

    def getMatrix(self):
        matrix_flipped = np.flip(self.matrix, 0)
        alternate_rows, alternate_rows_flipped = matrix_flipped[0::2], np.flip(matrix_flipped[1::2], 1)
        matrix = []
        for n, f in zip(alternate_rows, alternate_rows_flipped):
            matrix.extend(n)
            matrix.extend(f)
        return np.asarray(matrix).tolist()

    def render(self, callback = None):
        self.loaded_files = os.listdir(os.path.join(ROOT, "images"))
        link = ""
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
                    link = os.path.join(ROOT, "images", self.loaded_files[self.menu_scroll])
                    ext = os.path.splitext(link)[1]
                    if os.path.isfile(link) and ext in [".jpeg", ".png"]:
                        self.clear()
                        image = Image.open(link)
                        image = image.convert('RGB')
                        image = image.resize((16, 16))
                        self.matrix = np.array(image)
                        if callback is not None:
                            callback(self.getMatrix())
            time.sleep(1 / 8)
