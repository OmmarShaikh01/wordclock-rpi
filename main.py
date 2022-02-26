import queue
import sys
import threading
import time
import numpy as np
import keyboard
from clock import Clock
from image_renderer.renderer import ImageRenderer
from gif_renderer.renderer import GifImageRenderer
from scroll_text import TextRenderer
from weather import Weather
from snake_game import SnakeGame
from car_game import CarGame
from scroll_clock import TextRendererClock

menu_scroll = 7
message_queue = queue.Queue()

clock = Clock(message_queue)
image_renderer = ImageRenderer(message_queue)
gif_renderer = GifImageRenderer(message_queue)
text_renderer = TextRenderer(message_queue)
weather = Weather(message_queue)
snake = SnakeGame(message_queue)
clock_renderer = TextRendererClock(message_queue)
car_game = CarGame(message_queue)

development = True

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


class Menu:
    ROWS = {
        0: (1, 2, 8),
        1: (3, 2, 8),
        2: (5, 2, 8),
        3: (7, 2, 8),
        4: (9, 2, 8),
        5: (11, 2, 8),
        6: (13, 2, 8),
        7: (15, 2, 8),
    }

    def __init__(self) -> None:
        self.matrix = np.zeros((16, 16))

    def clear(self):
        self.matrix = np.zeros((16, 16))

    def populate(self, co_ords, value):
        for item in range(0, co_ords[2]):
            self.matrix[co_ords[0]][co_ords[1] + item] = value

    def getMatrix(self):
        matrix_flipped = np.flip(self.matrix, 0)
        alternate_rows, alternate_rows_flipped = matrix_flipped[0::2], np.flip(matrix_flipped[1::2], 1)
        matrix = []
        for n, f in zip(alternate_rows, alternate_rows_flipped):
            matrix.extend(n)
            matrix.extend(f)
        return np.asarray(matrix).tolist()

    def renderMenu(self, sel_index, callback):
        for index, row in enumerate(self.ROWS.values()):
            if sel_index == index:
                self.populate(row, 2)
            else:
                self.populate(row, 1)
        callback(self.getMatrix())


def scroll_menu(direction):
    global menu_scroll
    rows = 7
    if (menu_scroll + direction) > rows:
        menu_scroll = 0
    elif 0 <= (menu_scroll + direction) <= rows:
        menu_scroll += direction
    elif (menu_scroll + direction) < 0:
        menu_scroll = rows
    print("main", menu_scroll)


def listner():
    while True:
        if keyboard.is_pressed(BUTTON_Q):
            message_queue.put(BUTTON_Q)
        elif keyboard.is_pressed(BUTTON_W):
            message_queue.put(BUTTON_W)
        elif keyboard.is_pressed(BUTTON_E):
            message_queue.put(BUTTON_E)
        elif keyboard.is_pressed(BUTTON_A):
            message_queue.put(BUTTON_A)
        elif keyboard.is_pressed(BUTTON_S):
            message_queue.put(BUTTON_S)
        elif keyboard.is_pressed(BUTTON_D):
            message_queue.put(BUTTON_D)
        elif keyboard.is_pressed(BUTTON_Z):
            message_queue.put(BUTTON_Z)
        elif keyboard.is_pressed(BUTTON_X):
            message_queue.put(BUTTON_X)
        elif keyboard.is_pressed(BUTTON_C):
            message_queue.put(BUTTON_C)
        elif keyboard.is_pressed(BUTTON_V):
            message_queue.put(BUTTON_V)
        else:
            continue
        time.sleep(1 / 8)


def mainloop():
    try:
        menu = Menu()
        activity_thread = threading.Thread(target = listner, daemon = False)
        activity_thread.start()
        while True:
            menu.renderMenu(menu_scroll, print)
            while not message_queue.empty():
                event = message_queue.get()
                if event == (BUTTON_W):
                    scroll_menu(-1)
                    menu.renderMenu(menu_scroll, print)
                elif event == (BUTTON_E):
                    if menu_scroll == 0:
                        clock.start_clock()
                        clock.clockPulseing(print)
                    elif menu_scroll == 1:
                        gif_renderer.render(print)
                    elif menu_scroll == 2:
                        image_renderer.render(print)
                    elif menu_scroll == 3:
                        text_renderer.render(print)
                    elif menu_scroll == 4:
                        weather.render(print)
                    elif menu_scroll == 5:
                        snake.run(print)
                    elif menu_scroll == 6:
                        clock_renderer.render(print)
                    elif menu_scroll == 7:
                        car_game.run(print)
                elif event == (BUTTON_S):
                    scroll_menu(1)
                    menu.renderMenu(menu_scroll, print)
                else:
                    continue
            time.sleep(1 / 8)
    except KeyboardInterrupt:
        pass


def mainloop_matrix():
    try:
        from pixel import MatrixController
        controller = MatrixController()

        menu = Menu()
        activity_thread = threading.Thread(target = listner, daemon = False)
        activity_thread.start()
        while True:
            while not message_queue.empty():
                menu.renderMenu(menu_scroll, (
                    lambda mat: controller.populateMapped(mat, {0: (0, 0, 0), 1: (255, 255, 255), 2: (0, 255, 0)})
                ))
                event = message_queue.get()
                if event == (BUTTON_W):
                    scroll_menu(-1)
                    menu.renderMenu(menu_scroll, (
                        lambda mat: controller.populateMapped(mat, {0: (0, 0, 0), 1: (255, 255, 255), 2: (0, 255, 0)})
                    ))
                elif event == (BUTTON_E):
                    if menu_scroll == 0:
                        clock.start_clock()
                        clock.clockPulseing(lambda mat: controller.populateBoolean(mat, (255, 0, 0)))
                    elif menu_scroll == 1:
                        gif_renderer.render(controller.populateRGB)
                    elif menu_scroll == 2:
                        image_renderer.render(controller.populateRGB)
                    elif menu_scroll == 3:
                        text_renderer.render(lambda mat: controller.populateBoolean(mat, (255, 255, 0)))
                    elif menu_scroll == 4:
                        weather.render(lambda mat: controller.populateBoolean(mat, (255, 255, 0)))
                    elif menu_scroll == 5:
                        snake.run(lambda mat: controller.populateMapped(mat, {0: (0, 0, 0), 1: (255, 0, 0), 2: (0, 255, 0)}))
                    elif menu_scroll == 6:
                        clock_renderer.render(lambda mat: controller.populateBoolean(mat, (255, 255, 0)))
                    elif menu_scroll == 7:
                        car_game.run(controller.populateRGB)
                elif event == (BUTTON_S):
                    scroll_menu(1)
                    menu.renderMenu(menu_scroll, (
                        lambda mat: controller.populateMapped(mat, {0: (0, 0, 0), 1: (255, 255, 255), 2: (0, 255, 0)})
                    ))
                else:
                    continue
            time.sleep(1 / 8)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    mainloop()
    sys.exit()
