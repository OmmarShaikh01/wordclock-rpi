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
    ONCOMEING = 2
    PAVEMENT = 3
    DIVIDER = 3

    def __init__(self, mqueue):
        self.matrix = np.zeros((16, 16))
        self.mqueue = mqueue
        self.oncar = []
        self.main_car = None
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
            if item == self.ONCOMEING_1:
                matrix[index] = (random.randint(0, 200), random.randint(0, 255), random.randint(0, 255))
            if item == self.PAVEMENT:
                matrix[index] = (0, 200, 200)
            if item == self.DIVIDER:
                matrix[index] = (0, 200, 0)
        return np.asarray(matrix).tolist()

    def clear(self):
        self.matrix = np.zeros((16, 16))
        self.generate_background()

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
        self.oncar = []
        self.main_car = None
        self.game_over = False
        self.clear()
        self.generate_car()
        self.generate_on_car()

    def generate_background(self):
        self.matrix = np.asarray(
                (
                    (3, 3, 0, 0, 0, 4, 0, 0, 0, 0, 4, 0, 0, 0, 3, 3),
                    (3, 3, 0, 0, 0, 4, 0, 0, 0, 0, 4, 0, 0, 0, 3, 3),
                    (3, 3, 0, 0, 0, 4, 0, 0, 0, 0, 4, 0, 0, 0, 3, 3),
                    (3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3),
                    (3, 3, 0, 0, 0, 4, 0, 0, 0, 0, 4, 0, 0, 0, 3, 3),
                    (3, 3, 0, 0, 0, 4, 0, 0, 0, 0, 4, 0, 0, 0, 3, 3),
                    (3, 3, 0, 0, 0, 4, 0, 0, 0, 0, 4, 0, 0, 0, 3, 3),
                    (3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3),
                    (3, 3, 0, 0, 0, 4, 0, 0, 0, 0, 4, 0, 0, 0, 3, 3),
                    (3, 3, 0, 0, 0, 4, 0, 0, 0, 0, 4, 0, 0, 0, 3, 3),
                    (3, 3, 0, 0, 0, 4, 0, 0, 0, 0, 4, 0, 0, 0, 3, 3),
                    (3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3),
                    (3, 3, 0, 0, 0, 4, 0, 0, 0, 0, 4, 0, 0, 0, 3, 3),
                    (3, 3, 0, 0, 0, 4, 0, 0, 0, 0, 4, 0, 0, 0, 3, 3),
                    (3, 3, 0, 0, 0, 4, 0, 0, 0, 0, 4, 0, 0, 0, 3, 3),
                    (3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3)
                ),
                dtype = float
        )

    def generate_car(self):
        if self.main_car is None:
            col = random.choice((2, 3, 4, 6, 7, 8, 9, 11, 12, 13))
            cord = ((14, col), (15, col))
            self.main_car = cord

    def move_car(self, direction):
        if self.main_car is None:
            return None
        val_col = (2, 3, 4, 6, 7, 8, 9, 11, 12, 13)
        col = val_col.index(self.main_car[0][1])
        if direction == "LEFT" and ((col - 1) in range(len(val_col))):
            col -= 1
            self.main_car = ((14, val_col[col]), (15, val_col[col]))
        elif direction == "RIGHT" and ((col + 1) in range(len(val_col))):
            col += 1
            self.main_car = ((14, val_col[col]), (15, val_col[col]))

    def generate_on_car(self):
        row = random.randint(0, 8)
        if len(self.oncar) == 0:
            val_col = random.choice((2, 3, 4, 6, 7, 8, 9, 11, 12, 13))
            self.oncar = [((row, val_col), (row + 1, val_col))]
        elif 0 < len(self.oncar) < 3:
            cars_in = [(2, 3, 4), (6, 7, 8, 9), (11, 12, 13)]
            for car in self.oncar:
                for index, item in enumerate(cars_in):
                    if car[0][1] in item:
                        cars_in.pop(index)
            val_col = random.choice(cars_in[0])
            self.oncar.insert(len(self.oncar), ((row, val_col), (row + 1, val_col)))

    def move_on_car(self):
        for index, car in enumerate(self.oncar):
            row, col = car[1][0], car[1][1]
            cord = ((row, col), (row + 1, col))
            if (row + 1) < 16:
                self.oncar[index] = cord
            else:
                self.oncar.pop(index)

    def populate_car(self, cord, value):
        if cord is not None:
            for item in cord:
                self.matrix[item[0]][item[1]] = value

    def check_game_over(self):
        if self.game_over:
            return self.end()

        for car in self.oncar:
            for item in self.main_car:
                if item in car:
                    return self.end()

    def run(self, callable):
        counter = 0
        self.restart()
        while True:
            if not self.game_over:
                self.clear()
                self.generate_car()
                self.generate_on_car()

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

            self.move_on_car()
            self.move_on_car()
            [self.populate_car(car, self.ONCOMEING) for car in self.oncar]
            self.populate_car(self.main_car, self.CAR)

            self.check_game_over()
            callable(self.matrix)
            time.sleep(1)
