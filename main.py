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
from flappy.flappy_game import FlappyBird
from scroll_clock import TextRendererClock

menu_scroll = 0
message_queue = queue.Queue()

clock = Clock(message_queue)
image_renderer = ImageRenderer(message_queue)
gif_renderer = GifImageRenderer(message_queue)
text_renderer = TextRenderer(message_queue)
weather = Weather(message_queue)
snake = SnakeGame(message_queue)
clock_renderer = TextRendererClock(message_queue)
car_game = CarGame(message_queue)
flappy_game = FlappyBird(message_queue)

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
        0: (2, 2, 8),
        1: (3, 2, 8),
        2: (4, 2, 8),
        3: (5, 2, 8),
        4: (6, 2, 8),
        5: (7, 2, 8),
        6: (8, 2, 8),
        7: (9, 2, 8),
        8: (10, 2, 8),
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
    rows = len(Menu.ROWS)
    if (menu_scroll + direction) > rows:
        menu_scroll = 0
    elif 0 <= (menu_scroll + direction) <= rows:
        menu_scroll += direction
    elif (menu_scroll + direction) < 0:
        menu_scroll = rows
    print("main", menu_scroll)


def listner():
    keyboard.add_hotkey(BUTTON_Q, lambda: message_queue.put(BUTTON_Q))
    keyboard.add_hotkey(BUTTON_W, lambda: message_queue.put(BUTTON_W))
    keyboard.add_hotkey(BUTTON_E, lambda: message_queue.put(BUTTON_E))
    keyboard.add_hotkey(BUTTON_A, lambda: message_queue.put(BUTTON_A))
    keyboard.add_hotkey(BUTTON_S, lambda: message_queue.put(BUTTON_S))
    keyboard.add_hotkey(BUTTON_D, lambda: message_queue.put(BUTTON_D))
    keyboard.add_hotkey(BUTTON_Z, lambda: message_queue.put(BUTTON_Z))
    keyboard.add_hotkey(BUTTON_X, lambda: message_queue.put(BUTTON_X))
    keyboard.add_hotkey(BUTTON_C, lambda: message_queue.put(BUTTON_C))
    keyboard.add_hotkey(BUTTON_V, lambda: message_queue.put(BUTTON_V))
    keyboard.wait()


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
                    elif menu_scroll == 8:
                        flappy_game.run(print)
                elif event == (BUTTON_S):
                    scroll_menu(1)
                    menu.renderMenu(menu_scroll, print)
                else:
                    continue
            time.sleep(1 / 8)
    except KeyboardInterrupt:
        pass


def mainloop_matrix():
    from pixel import MatrixController
    controller = MatrixController()

    try:
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
                        snake.run(
                            lambda mat: controller.populateMapped(mat, {0: (0, 0, 0), 1: (255, 0, 0), 2: (0, 255, 0)}))
                    elif menu_scroll == 6:
                        clock_renderer.render(lambda mat: controller.populateBoolean(mat, (255, 255, 0)))
                    elif menu_scroll == 7:
                        car_game.run(controller.populateRGB)
                    elif menu_scroll == 8:
                        flappy_game.run(controller.populateRGB)
                elif event == (BUTTON_S):
                    scroll_menu(1)
                    menu.renderMenu(menu_scroll, (
                        lambda mat: controller.populateMapped(mat, {0: (0, 0, 0), 1: (255, 255, 255), 2: (0, 255, 0)})
                    ))
                else:
                    continue
            time.sleep(1 / 8)
    except KeyboardInterrupt:
        controller.clear()
        pass


if __name__ == '__main__':
    mainloop()
    sys.exit()
