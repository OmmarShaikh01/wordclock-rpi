import board
import neopixel


class MatrixController:
    def __init__(self):
        self.pixels = neopixel.NeoPixel(board.D18, 256, brightness = 0.9, auto_write = False)

    def clear(self):
        self.pixels[0] = (0, 0, 0)
        self.pixels.show()

    def populateBoolean(self, matrix, color):
        self.clear()
        for index, item in enumerate(matrix):
            if item == 1:
                self.pixels[index] = color
            else:
                self.pixels[index] = (0, 0, 0)
        self.pixels.show()

    def populateRGB(self, matrix):
        self.clear()
        for index, item in enumerate(matrix):
            self.pixels[index] = item
        self.pixels.show()

    def populateMapped(self, matrix, RGB_map):
        self.clear()
        for index, item in enumerate(matrix):
            self.pixels[index] = RGB_map[item]
        self.pixels.show()
