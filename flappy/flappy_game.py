import copy
import enum
import itertools
import os
import random
import time
import sys

import numpy as np
from colorsys import hsv_to_rgb
from PIL import Image, ImageDraw, ImageFont

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

PARENT = os.path.dirname(__file__)


class FlappyBird:
    EMPTY = 0

    BIRD_EYE = 1
    BIRD_HEAD = 2
    BIRD_BEAK = 3
    BIRD_BODY = 4
    PIPE = 5
    PAVEMENT = 6

    GAME_OVER = 7
    SCORE = 8
    CLOUD_BLUE = 9
    CLOUD_WHITE = 10

    def __init__(self, mqueue):
        self.matrix = np.zeros((16, 16))
        self.mqueue = mqueue
        self.game_over = False
        self.bird_cord = [4, 0]
        self.pipe_cord = [[13, 5, 3]]
        self.score = 0
        self.back_matrix = itertools.cycle((
            os.path.join(PARENT, "images", "1.png"),
            os.path.join(PARENT, "images", "2.png"),
            os.path.join(PARENT, "images", "3.png"),
            os.path.join(PARENT, "images", "4.png"),
            os.path.join(PARENT, "images", "5.png"),
            os.path.join(PARENT, "images", "6.png"),
            os.path.join(PARENT, "images", "7.png"),
            os.path.join(PARENT, "images", "8.png"),
            os.path.join(PARENT, "images", "9.png"),
            os.path.join(PARENT, "images", "10.png"),
            os.path.join(PARENT, "images", "11.png"),
            os.path.join(PARENT, "images", "12.png"),
            os.path.join(PARENT, "images", "13.png"),
            os.path.join(PARENT, "images", "14.png"),
            os.path.join(PARENT, "images", "15.png"),
            os.path.join(PARENT, "images", "16.png"),
            os.path.join(PARENT, "images", "17.png"),
            os.path.join(PARENT, "images", "18.png"),
            os.path.join(PARENT, "images", "19.png"),
            os.path.join(PARENT, "images", "20.png"),
            os.path.join(PARENT, "images", "21.png"),
            os.path.join(PARENT, "images", "22.png"),
            os.path.join(PARENT, "images", "23.png"),
            os.path.join(PARENT, "images", "24.png"),
        ))
        self.bird_matrix = itertools.cycle((
            np.asarray(
                    [
                        [self.EMPTY, self.BIRD_HEAD, self.BIRD_HEAD, self.EMPTY],
                        [self.EMPTY, self.BIRD_HEAD, self.BIRD_EYE, self.BIRD_BEAK],
                        [self.BIRD_BODY, self.BIRD_BODY, self.BIRD_BODY, self.EMPTY],
                        [self.BIRD_BODY, self.BIRD_BODY, self.EMPTY, self.EMPTY]
                    ]
            ),
            np.asarray(
                    [
                        [self.EMPTY, self.BIRD_HEAD, self.BIRD_HEAD, self.EMPTY],
                        [self.EMPTY, self.BIRD_HEAD, self.EMPTY, self.BIRD_BEAK],
                        [self.BIRD_BODY, self.BIRD_BODY, self.BIRD_BODY, self.EMPTY],
                        [self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY]
                    ]
            )))

    def getMatrix(self):
        matrix_flipped = np.flip(self.matrix, 0)
        alternate_rows, alternate_rows_flipped = matrix_flipped[0::2], np.flip(matrix_flipped[1::2], 1)
        matrix = []
        for n, f in zip(alternate_rows, alternate_rows_flipped):
            matrix.extend(n)
            matrix.extend(f)

        color_map = {
            self.EMPTY: (0, 0, 0),
            self.BIRD_EYE: (230, 230, 250),
            self.BIRD_HEAD: (0, 0, 0),
            self.BIRD_BEAK: (255, 0, 0),
            self.BIRD_BODY: (255, 255, 0),
            self.PIPE: (102, 255, 51),
            self.PAVEMENT: (102, 255, 51),
            self.GAME_OVER: (255, 0, 102),
            self.SCORE: (255, 200, 102),
            self.CLOUD_BLUE: (0, 130, 255),
            self.CLOUD_WHITE: (255, 255, 255),
        }
        for index, item in enumerate(matrix):
            matrix[index] = color_map.get(item, (0, 0, 0))
        return np.asarray(matrix, dtype = int).tolist()

    def clear(self):
        self.matrix = np.zeros((16, 16))
        link = os.path.normpath(next(self.back_matrix))
        ext = os.path.splitext(link)[1]
        if os.path.isfile(link) and ext in [".jpeg", ".png"]:
            image = Image.open(link)
            image = image.convert('RGB')
            image = image.resize((16, 16))
            for r_i, r in enumerate(np.array(image)):
                for c_i, c in enumerate(r):
                    if (c[0], c[1], c[2]) == (0, 130, 255):
                        self.matrix[r_i][c_i] = self.CLOUD_BLUE
                    else:
                        self.matrix[r_i][c_i] = self.CLOUD_WHITE

    def end(self):
        self.game_over = True
        if not hasattr(self, "game_over_matrix"):
            self.game_over_matrix = itertools.cycle((
                np.asarray(
                        (
                            (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                            (0, 7, 7, 7, 0, 7, 7, 7, 0, 7, 0, 7, 0, 7, 7, 7),
                            (0, 7, 0, 0, 0, 7, 0, 7, 0, 7, 7, 7, 0, 7, 0, 0),
                            (0, 7, 0, 7, 0, 7, 0, 7, 0, 7, 0, 7, 0, 7, 7, 7),
                            (0, 7, 0, 7, 0, 7, 7, 7, 0, 7, 0, 7, 0, 7, 0, 0),
                            (0, 7, 7, 7, 0, 7, 0, 7, 0, 7, 0, 7, 0, 7, 7, 7),
                            (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                            (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                            (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                            (0, 7, 7, 7, 0, 7, 0, 7, 0, 7, 7, 7, 0, 7, 7, 7),
                            (0, 7, 0, 7, 0, 7, 0, 7, 0, 7, 0, 0, 0, 7, 0, 7),
                            (0, 7, 0, 7, 0, 7, 0, 7, 0, 7, 7, 7, 0, 7, 7, 7),
                            (0, 7, 0, 7, 0, 0, 7, 0, 0, 7, 0, 0, 0, 7, 7, 0),
                            (0, 7, 7, 7, 0, 0, 7, 0, 0, 7, 7, 7, 0, 7, 0, 7),
                            (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                            (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
                        ),
                        dtype = float
                ),
                np.zeros((16, 16))
            ))
        self.matrix = copy.deepcopy(next(self.game_over_matrix))

    def drawBird(self):
        bird = copy.deepcopy(next(self.bird_matrix))
        row_C = self.bird_cord[0]
        for row in bird:
            col_C = self.bird_cord[1]
            for col in row:
                self.matrix[row_C][col_C] = col
                col_C += 1
            row_C += 1

    def moveBird(self, direction):
        row = self.bird_cord[0]
        if direction == "DOWN" and (row + 4) <= 14:
            self.bird_cord[0] = row + 1
        elif direction == "UP" and (row - 1) >= 0:
            self.bird_cord[0] = row - 1

    def movePipe(self):
        interval = 9
        row = self.pipe_cord[0][0] + interval
        width = 3
        if (0 < len(self.pipe_cord) < 2) and (11 <= row <= 13):
            height = random.randint(0, 5)
            self.pipe_cord.append([row, height, width])
        else:
            for index, col_cord in enumerate(self.pipe_cord):
                (col, h1, width) = col_cord
                if col - 1 >= 0:
                    self.pipe_cord[index] = [col - 1, h1, width]
                else:
                    width = ((col - 1) + 3)
                    if (col - 1) >= -3:
                        self.pipe_cord[index] = [col - 1, h1, width]
                    else:
                        self.pipe_cord.pop(0)
                        self.score += 1
        self.drawPipe(width)

    def drawPipe(self, width = 3):
        for col_cord in self.pipe_cord:
            (col, h1, w) = col_cord
            if col < 0:
                col = 0
            for col_inx in range(col, col + w):
                for row in range(h1):
                    self.matrix[row][col_inx] = self.PIPE
                for row in range(h1 + 8, 16):
                    self.matrix[row][col_inx] = self.PIPE

    def restart(self):
        self.game_over = False
        self.bird_cord = [4, 0]
        self.score = 0
        self.clear()

    def check_game_over(self):
        if self.game_over:
            return self.end()

        col_collis = False
        row_collis = False
        col = self.bird_cord[1]
        row = self.bird_cord[0]
        pipe_col = self.pipe_cord[0][0]
        pipe_h = self.pipe_cord[0][1]
        for c in range(col, col + 4):
            if c in range(pipe_col, pipe_col + 3):
                col_collis = True
        for r in range(row, row + 4):
            if (r in range(0, pipe_h)) or (r in range(pipe_h + 8, 15)):
                row_collis = True

        if row_collis and col_collis:
            self.end()

    def scrollText(self, text):
        text = list(str(text))
        renderscore_matrix = np.zeros((5, 6))
        scorematrix = {
            0: ((8, 8, 8), (8, 0, 8), (8, 8, 8), (8, 0, 8), (8, 8, 8)),
            1: ((8, 8, 8), (8, 0, 8), (8, 8, 8), (8, 0, 8), (8, 8, 8)),
            2: ((8, 8, 8), (8, 0, 8), (8, 8, 8), (8, 0, 8), (8, 8, 8)),
            3: ((8, 8, 8), (8, 0, 8), (8, 8, 8), (8, 0, 8), (8, 8, 8)),
            4: ((8, 8, 8), (8, 0, 8), (8, 8, 8), (8, 0, 8), (8, 8, 8)),
            5: ((8, 8, 8), (8, 0, 8), (8, 8, 8), (8, 0, 8), (8, 8, 8)),
            6: ((8, 8, 8), (8, 0, 8), (8, 8, 8), (8, 0, 8), (8, 8, 8)),
            7: ((8, 8, 8), (8, 0, 8), (8, 8, 8), (8, 0, 8), (8, 8, 8)),
            8: ((8, 8, 8), (8, 0, 8), (8, 8, 8), (8, 0, 8), (8, 8, 8)),
            9: ((8, 8, 8), (8, 0, 8), (8, 8, 8), (8, 0, 8), (8, 8, 8)),
        }

        number = scorematrix.get(int(text[0]), scorematrix.get(0))
        matrix_x = 11
        for row in (number):
            matrix_y = 10
            for col in (row):
                self.matrix[matrix_x][matrix_y] = col
                matrix_y += 1
            matrix_x += 1

        if 1 < len(text) <= 2:
            number = scorematrix.get(int(text[1]), scorematrix.get(0))
            matrix_x = 11
            for row in (number):
                matrix_y = 13
                for col in (row):
                    self.matrix[matrix_x][matrix_y] = col
                    matrix_y += 1
                matrix_x += 1

    def run(self, callable):
        self.restart()
        while True:
            self.clear()
            bird_moved = False

            if not self.mqueue.empty():
                event = self.mqueue.get()
                if event == BUTTON_Q:
                    break
                if event == BUTTON_E:
                    self.restart()
                if event == BUTTON_W and not self.game_over:
                    bird_moved = True
                    self.moveBird("UP")
            else:
                pass

            if not bird_moved:
                self.moveBird("DOWN")

            self.drawBird()
            self.movePipe()
            self.scrollText(self.score)
            self.check_game_over()
            callable(self.matrix)
            time.sleep(1)
