import requests, json, time
from scroll_text import TextRenderer
from time import gmtime, strftime

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


class TextRendererClock(TextRenderer):

    def __init__(self, mqueue) -> None:
        super().__init__(mqueue, 1)

    def render(self, callback = None):
        while True:
            if not self.mqueue.empty():
                event = self.mqueue.get()
                if event == BUTTON_Q:
                    break
                if event == BUTTON_E:
                    self.clear()
                    if callback is not None:
                        self.scrollText(strftime("%I:%M:%S", time.localtime()), (lambda: callback(self.getMatrix())))
            time.sleep(1 / 8)
