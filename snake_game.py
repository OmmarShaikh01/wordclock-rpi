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


class SnakeGame:
    EMPTY = 0
    APPLE = 1
    SNAKE = 2

    def __init__(self, mqueue):
        self.matrix = np.zeros((16, 16))
        self.mqueue = mqueue
        self.game_over = False
        x = random.randint(1, 14)
        y = random.randint(1, 14)
        self.snake = [(x, y + 1), (x, y)]

    def getMatrix(self):
        matrix_flipped = np.flip(self.matrix, 0)
        alternate_rows, alternate_rows_flipped = matrix_flipped[0::2], np.flip(matrix_flipped[1::2], 1)
        matrix = []
        for n, f in zip(alternate_rows, alternate_rows_flipped):
            matrix.extend(n)
            matrix.extend(f)
        return np.asarray(matrix).tolist()

    def clear(self):
        self.matrix = np.zeros((16, 16))

    def end(self):
        self.matrix = np.ones((16, 16))

    def restart(self):
        self.game_over = False
        x = random.randint(1, 14)
        y = random.randint(1, 14)
        self.snake = [(x, y + 1), (x, y)]
        self.clear()
        self.generate_apple()
        self.generate_snake()

    def generate_apple(self):
        head_x, head_y = self.snake[0][0], self.snake[0][1]
        x = random.randint(0, 15)
        y = random.randint(0, 15)
        self.matrix[x][y] = self.APPLE
        self.apple = (x, y)

    def generate_snake(self):
        for x, y in self.snake:
            self.matrix[x][y] = self.SNAKE

    def moveSnake(self, direction):
        head_x, head_y = self.snake[0][0], self.snake[0][1]
        head_x_1, head_y_1 = self.snake[1][0], self.snake[1][1]
        if direction == 'UP':
            if head_x == 0:
                head_x = 15
            elif 0 < head_x <= 15:
                head_x -= 1
        elif direction == 'DOWN':
            if head_x == 15:
                head_x = 0
            elif 0 <= head_x < 15:
                head_x += 1
        elif direction == 'LEFT':
            if head_y == 0:
                head_y = 15
            elif 0 < head_y <= 15:
                head_y -= 1
        elif direction == 'RIGHT':
            if head_y == 15:
                head_y = 0
            elif 0 <= head_y < 15:
                head_y += 1
        else:
            return
        if (head_x, head_y) != (head_x_1, head_y_1):
            if (head_x, head_y) not in self.snake:
                snake = [(head_x, head_y)]
                if ((head_x, head_y) != self.apple):
                    snake.extend(self.snake[:-1])
                    self.hasEaten = False
                else:
                    self.hasEaten = True
                    snake.extend(self.snake)
                self.snake = snake
            else:
                self.game_over = True
        else:
            return

    def move_FWD(self):
        head_x_0, head_y_0 = self.snake[0][0], self.snake[0][1]
        head_x_1, head_y_1 = self.snake[1][0], self.snake[1][1]
        hit_box = [
            ((head_x_0 + 1) if 0 < (head_x_0 + 1) <= 15 else 0, head_y_0),  # DOWN
            ((head_x_0 - 1) if not (head_x_0 - 1) < 0 else 15, head_y_0),  # UP
            (head_x_0, head_y_0),  # HEAD
            (head_x_0, (head_y_0 + 1) if 0 < (head_y_0 + 1) <= 15 else 0),  # RIGHT
            (head_x_0, (head_y_0 - 1) if not (head_y_0 - 1) < 0 else 15)  # LEFT
        ]

        if (head_x_1, head_y_1) == hit_box[0]:
            self.moveSnake("UP")
        elif (head_x_1, head_y_1) == hit_box[1]:
            self.moveSnake("DOWN")
        elif (head_x_1, head_y_1) == hit_box[3]:
            self.moveSnake("LEFT")
        elif (head_x_1, head_y_1) == hit_box[4]:
            self.moveSnake("RIGHT")

    def run(self, callable):
        first = True
        self.hasEaten = False
        while True:
            if not self.game_over:
                self.clear()
                self.generate_snake()
                if first:
                    self.generate_apple()
                    first = False
                if self.hasEaten:
                    self.generate_apple()
                    self.hasEaten = False
                else:
                    self.matrix[self.apple[0]][self.apple[1]] = self.APPLE

            if not self.mqueue.empty():
                event = self.mqueue.get()
                if event == BUTTON_Q:
                    break
                if event == BUTTON_E:
                    first = True
                    self.hasEaten = False
                    self.restart()
                if event == BUTTON_W:
                    self.moveSnake("UP")
                if event == BUTTON_S:
                    self.moveSnake("DOWN")
                if event == BUTTON_A:
                    self.moveSnake("LEFT")
                if event == BUTTON_D:
                    self.moveSnake("RIGHT")
            else:
                self.move_FWD()

            if not self.game_over:
                callable(self.getMatrix())
            else:
                self.end()
                callable(self.getMatrix())
            time.sleep(1)
