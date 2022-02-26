import requests, json, time
from scroll_text import TextRenderer

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


class Weather(TextRenderer):

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
                    text = self.fetch()
                    if callback is not None:
                        self.scrollText(text, (lambda: callback(self.getMatrix())))
            time.sleep(1 / 8)

    def fetch(self):
        api_key = "9e196ce49b2997c42fb520914a310383"
        base_url = "https://api.openweathermap.org/data/2.5/weather?lat=19.07&lon=72.87&"
        complete_url = base_url + "appid=" + api_key
        response = requests.get(complete_url)
        api_response = response.json()
        if api_response["cod"] not in ("404", "401"):
            main = api_response["main"]
            temprature = f"Temprature: {round(round(main['temp'], 2) - 273.15, 2)} C"
            pressure = f"Pressure: {main['pressure']}"
            humidity = f"Humidity: {main['humidity']}"
            desc = f"Desc: {api_response['weather'][0]['description']}"
            return " ".join([temprature, pressure, humidity, desc])
        else:
            print(" City Not Found ")
            return None
