import enum
import random
import time
import numpy as np

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


class CarGame:
    EMPTY = 0
    CAR = 1
    ONCOMEING_1 = 2
    ONCOMEING_2 = 3
    PAVEMENT = 4

    def __init__(self, mqueue):
        self.matrix = np.zeros((16, 16))
        self.oncar_1, self.oncar_2 = None, None
        self.main_car = None
        self.mqueue = mqueue
        self.game_over = False

    def getMatrix(self):
        matrix_flipped = np.flip(self.matrix, 0)
        alternate_rows, alternate_rows_flipped = matrix_flipped[0::2], np.flip(matrix_flipped[1::2], 1)
        matrix = []
        for n, f in zip(alternate_rows, alternate_rows_flipped):
            matrix.extend(n)
            matrix.extend(f)
        for index, item in enumerate(matrix):
            if item == self.EMPTY:
                matrix[index] = (0, 0, 0)
            if item == self.CAR:
                matrix[index] = (255, 0, 0)
            if item == self.ONCOMEING_1 or item == self.ONCOMEING_2:
                matrix[index] = (random.randint(0, 200), random.randint(0, 255), random.randint(0, 255))
            if item == self.PAVEMENT:
                matrix[index] = (0, 200, 200)
        return np.asarray(matrix).tolist()

    def clear(self):
        self.matrix = np.zeros((16, 16))
        self.generate_pavement()

    def end(self):
        self.game_over = True
        self.matrix = np.asarray(
            (
                (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                (0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1),
                (0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0),
                (0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1),
                (0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0),
                (0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1),
                (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                (0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1),
                (0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1),
                (0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1),
                (0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0),
                (0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1),
                (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
            ),
            dtype = float
        )
        self.main_car = None

    def restart(self):
        self.game_over = False
        self.oncar_1, self.oncar_2 = None, None
        self.main_car = None
        self.clear()
        self.generate_car()
        self.generate_on_car()

    def generate_pavement(self):
        for row in range(16):
            self.matrix[row][0] = self.PAVEMENT
            self.matrix[row][15] = self.PAVEMENT

    def generate_car(self):
        if self.main_car is None:
            cord_1, cord_2, cord_3 = (13, 7), (13 + 1, 7), (13 + 2, 7)
            self.main_car = (cord_1, cord_2, cord_3)
        self.populate_car(self.main_car, self.CAR)

    def move_car(self, direction):
        cord_1, cord_2, cord_3 = self.main_car
        row, col = cord_1[0], cord_1[1]
        if direction == "LEFT":
            if (col - 1) > 0:
                cord_1, cord_2, cord_3 = (row, col - 1), (row + 1, col - 1), (row + 2, col - 1)
                self.main_car = (cord_1, cord_2, cord_3)
        elif direction == "RIGHT":
            if (col + 1) < 14:
                cord_1, cord_2, cord_3 = (row, col + 1), (row + 1, col + 1), (row + 2, col + 1)
                self.main_car = (cord_1, cord_2, cord_3)

    def generate_on_car(self):
        if self.oncar_1 is None:
            row, col = 0, random.randint(1, 13)
            if self.oncar_2 is not None:
                temp_col = self.oncar_2[0][1]
                if temp_col + 6 < 13:
                    col = temp_col + 6
                elif temp_col - 6 > 1:
                    col = temp_col - 6

            cord_1, cord_2, cord_3 = (row, col), (row + 1, col), (row + 2, col)
            self.populate_car((cord_1, cord_2, cord_3), self.ONCOMEING_1)
            self.oncar_1 = (cord_1, cord_2, cord_3)
        else:
            self.move_on_car()
            if self.oncar_1 is not None:
                self.populate_car(self.oncar_1, self.ONCOMEING_1)

        if self.oncar_2 is None:
            row, col = 0, random.randint(1, 13)
            if self.oncar_1 is not None:
                temp_col = self.oncar_1[0][1]
                if temp_col + 6 < 13:
                    col = temp_col + 6
                elif temp_col - 6 > 1:
                    col = temp_col - 6
            cord_1, cord_2, cord_3 = (row, col), (row + 1, col), (row + 2, col)
            self.populate_car((cord_1, cord_2, cord_3), self.ONCOMEING_2)
            self.oncar_2 = (cord_1, cord_2, cord_3)
        else:
            self.move_on_car()
            if self.oncar_2 is not None:
                self.populate_car(self.oncar_2, self.ONCOMEING_2)

    def move_on_car(self):
        if self.oncar_1 is not None:
            row, col = self.oncar_1[0][0], self.oncar_1[0][1]
            if row + 4 <= 15:
                row += 2
                cord_1, cord_2, cord_3 = (row, col), (row + 1, col), (row + 2, col)
                self.oncar_1 = (cord_1, cord_2, cord_3)
            else:
                self.oncar_1 = None

        if self.oncar_2 is not None:
            row, col = self.oncar_2[0][0], self.oncar_2[0][1]
            if row + 4 <= 15:
                row += 2
                cord_1, cord_2, cord_3 = (row, col), (row + 1, col), (row + 2, col)
                self.oncar_2 = (cord_1, cord_2, cord_3)
            else:
                self.oncar_2 = None

    def populate_car(self, cord, value):
        if cord:
            cord_1, cord_2, cord_3 = cord
            self.matrix[cord_1[0]][cord_1[1]] = value
            self.matrix[cord_1[0]][cord_1[1] + 1] = value
            self.matrix[cord_2[0]][cord_2[1]] = value
            self.matrix[cord_2[0]][cord_2[1] + 1] = value
            self.matrix[cord_3[0]][cord_3[1]] = value
            self.matrix[cord_3[0]][cord_3[1] + 1] = value

    def check_game_over(self):
        if self.game_over:
            return self.end()
        else:
            cord_main_1, cord_main_2, cord_main_3 = self.main_car
            main_intersection = (
                cord_main_1,
                cord_main_2,
                cord_main_3,
                (cord_main_1[0], cord_main_1[1] + 1),
                (cord_main_2[0], cord_main_2[1] + 1),
                (cord_main_3[0], cord_main_3[1] + 1)
            )
            if self.oncar_1 is not None:
                cord_1_1, cord_1_2, cord_1_3 = self.oncar_1
                intersection = (
                    cord_1_1, (cord_1_1[0], cord_1_1[1] + 1),
                    cord_1_2, (cord_1_2[0], cord_1_2[1] + 1),
                    cord_1_3, (cord_1_3[0], cord_1_3[1] + 1)
                )
                for i in main_intersection:
                    if i in intersection:
                        self.end()

            if self.oncar_2 is not None:
                cord_1_1, cord_1_2, cord_1_3 = self.oncar_2
                intersection = (
                    cord_1_1, (cord_1_1[0], cord_1_1[1] + 1),
                    cord_1_2, (cord_1_2[0], cord_1_2[1] + 1),
                    cord_1_3, (cord_1_3[0], cord_1_3[1] + 1)
                )
                for i in main_intersection:
                    if i in intersection:
                        self.end()

    def run(self, callable):
        counter = 0
        self.restart()
        while True:
            if not self.game_over:
                self.clear()
                self.generate_car()
                if counter == 4:
                    counter = 0
                    if self.oncar_1 is None or self.oncar_2 is None:
                        self.generate_on_car()
                else:
                    if self.oncar_1 is not None:
                        self.move_on_car()
                        self.populate_car(self.oncar_1, self.ONCOMEING_1)
                    if self.oncar_2 is not None:
                        self.move_on_car()
                        self.populate_car(self.oncar_2, self.ONCOMEING_2)
                    counter += 1

            if not self.mqueue.empty():
                event = self.mqueue.get()
                if event == BUTTON_Q:
                    break
                if event == BUTTON_E:
                    self.restart()
                if event == BUTTON_A and not self.game_over:
                    self.move_car("LEFT")
                if event == BUTTON_D and not self.game_over:
                    self.move_car("RIGHT")
            else:
                pass

            self.check_game_over()
            callable(self.matrix)
            callable()
            time.sleep(1)
