# import board
# import neopixel
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


class Clock():
    w_it = (0, 0, 2)
    w_is = (0, 3, 2)
    w_half = (7, 0, 4)
    w_to = (7, 14, 2)
    w_past = (8, 0, 4)
    w_oclock = (11, 10, 6)
    w_in = (12, 0, 2)
    w_the = (12, 3, 3)
    w_afternoon = (12, 7, 9)
    w_noon = (12, 12, 4)
    w_midnight = (4, 8, 8)
    w_morning = (13, 0, 7)
    w_at = (13, 8, 2)
    w_night = (13, 11, 5)
    w_evening = (14, 0, 7)
    w_and = (14, 8, 3)
    w_cool = (15, 0, 4)
    w_warm = (15, 6, 4)

    w_cold = (14, 12, 4)
    w_hot = (15, 12, 3)

    w_weeks = {
        'sun': (14, 12, 1),
        'mon': (14, 13, 1),
        'tue': (14, 14, 1),
        'wed': (14, 15, 1),
        'thu': (15, 12, 1),
        'fri': (15, 13, 1),
        'sat': (15, 14, 1),
    }

    w_el = (9, 2, 2)
    w_minutes = {
        'one': (0, 13, 3),
        'two': (1, 0, 3),
        'three': (3, 0, 5),
        'four': (2, 12, 4),
        'five': (2, 0, 4),
        'six': (5, 0, 3),
        'seven': (6, 0, 5),
        'eight': (5, 8, 5),
        'nine': (3, 6, 4),
        'ten': (1, 4, 3),
        'eleven': (2, 5, 6),
        'twelve': (6, 10, 6),
        'thirteen': (1, 8, 8),
        'fourteen': (4, 0, 8),
        'quarter': (7, 6, 7),
        'sixteen': (5, 0, 7),
        'seventeen': (6, 0, 9),
        'eighteen': (5, 8, 8),
        'nineteen': (3, 6, 8),
        'twenty': (0, 6, 6)
    }
    w_hours = {
        'one': (8, 5, 3),
        'two': (8, 9, 3),
        'three': (11, 4, 5),
        'four': (9, 7, 4),
        'five': (9, 12, 4),
        'six': (8, 13, 3),
        'seven': (10, 0, 5),
        'eight': (10, 6, 5),
        'nine': (10, 12, 4),
        'ten': (11, 0, 3),
        'even': (10, 1, 4),
        'twelve': (9, 0, 6)
    }

    def __init__(self, mqueue) -> None:
        self.matrix = np.zeros((16, 16))
        self.mqueue = mqueue
        self.pulse = False

    def clear(self):
        self.matrix = np.zeros((16, 16))

    def populate(self, co_ords):
        for value in range(0, co_ords[2]):
            self.matrix[co_ords[0]][co_ords[1] + value] = 1

    def debug(self):
        TEST_MATRIX = [i for i in
                       'ITLISOTWENTYRONETWOETENMTHIRTEENFIVEMELEVENIFOURTHREEPNINETEENSUFOURTEENMIDNIGHTSIXTEENDEIGHTEENSEVENTEENOTWELVEHALFELQUARTEROTOPASTRONESTWOISIXTWELVETFOURAFIVESEVENMEIGHTENINETENTTHREECOCLOCKINOTHENAFTERNOONMORNINGSATENIGHTEVENINGCANDTCOLDSMTWETWARMURTFSA']
        array = [i for i, j in zip(TEST_MATRIX, self.matrix.flatten()) if j == 1]
        return "".join(array)

    def getMatrix(self):
        matrix_flipped = np.flip(self.matrix, 0)
        alternate_rows, alternate_rows_flipped = matrix_flipped[0::2], np.flip(matrix_flipped[1::2], 1)
        matrix = []
        for n, f in zip(alternate_rows, alternate_rows_flipped):
            matrix.extend(n)
            matrix.extend(f)
        return np.asarray(matrix).tolist()

    def clockPulseing(self, callback = None):
        while self.pulse:
            if not self.mqueue.empty():
                event = self.mqueue.get()
                if event == BUTTON_Q:
                    self.stop_clock()
                    break
            self.clear()
            cur_time = time.localtime()
            hour = cur_time.tm_hour
            minute = cur_time.tm_min
            week = cur_time.tm_wday
            self.clear()
            self.setTime((hour, minute, week))
            print(self.debug())
            if callback is not None:
                callback(self.getMatrix())
            time.sleep(1)

    def stop_clock(self):
        self.pulse = False

    def start_clock(self):
        self.pulse = True

    def setTime(self, _time):
        hour, min, week = _time
        self.populate(self.w_it)
        self.populate(self.w_is)
        self.populate(self.w_and)

        if week == 0:
            self.populate(self.w_weeks['mon'])
        if week == 1:
            self.populate(self.w_weeks['tue'])
        if week == 2:
            self.populate(self.w_weeks['wed'])
        if week == 3:
            self.populate(self.w_weeks['thu'])
        if week == 4:
            self.populate(self.w_weeks['fri'])
        if week == 5:
            self.populate(self.w_weeks['sat'])
        if week == 6:
            self.populate(self.w_weeks['sun'])

        if 0 <= min <= 30:
            self.set0to30Minute(hour, min)
        if 30 < min <= 59:
            self.set30to59Minute(hour, min)
            if 0 <= hour < 23:
                hour += 1
            else:
                hour = 0
        if 0 <= hour < 12:
            if hour in range(0, 6):
                self.populate(self.w_at)
                self.populate(self.w_night)
                self.populate(self.w_warm)
            if hour in range(6, 12):
                self.populate(self.w_in)
                self.populate(self.w_the)
                self.populate(self.w_morning)
                self.populate(self.w_warm)
            if hour == 0:
                self.populate(self.w_hours["twelve"])
            if hour == 1:
                self.populate(self.w_hours["one"])
            if hour == 2:
                self.populate(self.w_hours["two"])
            if hour == 3:
                self.populate(self.w_hours["three"])
            if hour == 4:
                self.populate(self.w_hours["four"])
            if hour == 5:
                self.populate(self.w_hours["five"])
            if hour == 6:
                self.populate(self.w_hours["six"])
            if hour == 7:
                self.populate(self.w_hours["seven"])
            if hour == 8:
                self.populate(self.w_hours["eight"])
            if hour == 9:
                self.populate(self.w_hours["nine"])
            if hour == 10:
                self.populate(self.w_hours["ten"])
            if hour == 11:
                self.populate(self.w_hours["even"])
                self.populate(self.w_el)
        if 12 <= hour <= 23:
            if hour in range(12, 18):
                self.populate(self.w_in)
                self.populate(self.w_the)
                self.populate(self.w_afternoon)
                self.populate(self.w_warm)
            if hour in range(18, 21):
                self.populate(self.w_in)
                self.populate(self.w_the)
                self.populate(self.w_evening)
                self.populate(self.w_warm)
            if hour in range(21, 24):
                self.populate(self.w_at)
                self.populate(self.w_night)
                self.populate(self.w_warm)
            if hour == 12:
                self.populate(self.w_hours["twelve"])
            if hour == 13:
                self.populate(self.w_hours["one"])
            if hour == 14:
                self.populate(self.w_hours["two"])
            if hour == 15:
                self.populate(self.w_hours["three"])
            if hour == 16:
                self.populate(self.w_hours["four"])
            if hour == 17:
                self.populate(self.w_hours["five"])
            if hour == 18:
                self.populate(self.w_hours["six"])
            if hour == 19:
                self.populate(self.w_hours["seven"])
            if hour == 20:
                self.populate(self.w_hours["eight"])
            if hour == 21:
                self.populate(self.w_hours["nine"])
            if hour == 22:
                self.populate(self.w_hours["ten"])
            if hour == 23:
                self.populate(self.w_el)
                self.populate(self.w_hours["even"])

    def set0to30Minute(self, hour, min):
        if min == 0:
            self.populate(self.w_oclock)
        if 1 <= min <= 20:
            self.populate(self.w_past)
            if min == 1: self.populate(self.w_minutes['one'])
            if min == 2: self.populate(self.w_minutes['two'])
            if min == 3: self.populate(self.w_minutes['three'])
            if min == 4: self.populate(self.w_minutes['four'])
            if min == 5: self.populate(self.w_minutes['five'])
            if min == 6: self.populate(self.w_minutes['six'])
            if min == 7: self.populate(self.w_minutes['seven'])
            if min == 8: self.populate(self.w_minutes['eight'])
            if min == 9: self.populate(self.w_minutes['nine'])
            if min == 10: self.populate(self.w_minutes['ten'])
            if min == 11: self.populate(self.w_minutes['eleven'])
            if min == 12: self.populate(self.w_minutes['twelve'])
            if min == 13: self.populate(self.w_minutes['thirteen'])
            if min == 14: self.populate(self.w_minutes['fourteen'])
            if min == 15: self.populate(self.w_minutes['quarter'])
            if min == 16: self.populate(self.w_minutes['sixteen'])
            if min == 17: self.populate(self.w_minutes['seventeen'])
            if min == 18: self.populate(self.w_minutes['eighteen'])
            if min == 19: self.populate(self.w_minutes['nineteen'])
            if min == 20: self.populate(self.w_minutes['twenty'])
        if 20 < min < 30:
            self.populate(self.w_past)
            self.populate(self.w_minutes['twenty'])
            if (min - 20) == 1: self.populate(self.w_minutes['one'])
            if (min - 20) == 2: self.populate(self.w_minutes['two'])
            if (min - 20) == 3: self.populate(self.w_minutes['three'])
            if (min - 20) == 4: self.populate(self.w_minutes['four'])
            if (min - 20) == 5: self.populate(self.w_minutes['five'])
            if (min - 20) == 6: self.populate(self.w_minutes['six'])
            if (min - 20) == 7: self.populate(self.w_minutes['seven'])
            if (min - 20) == 8: self.populate(self.w_minutes['eight'])
            if (min - 20) == 9: self.populate(self.w_minutes['nine'])
        if min == 30:
            self.populate(self.w_past)
            self.populate(self.w_half)

    def set30to59Minute(self, hour, min):
        min = 60 - min
        if 1 <= min <= 20:
            self.populate(self.w_to)
            if min == 1: self.populate(self.w_minutes['one'])
            if min == 2: self.populate(self.w_minutes['two'])
            if min == 3: self.populate(self.w_minutes['three'])
            if min == 4: self.populate(self.w_minutes['four'])
            if min == 5: self.populate(self.w_minutes['five'])
            if min == 6: self.populate(self.w_minutes['six'])
            if min == 7: self.populate(self.w_minutes['seven'])
            if min == 8: self.populate(self.w_minutes['eight'])
            if min == 9: self.populate(self.w_minutes['nine'])
            if min == 10: self.populate(self.w_minutes['ten'])
            if min == 11: self.populate(self.w_minutes['eleven'])
            if min == 12: self.populate(self.w_minutes['twelve'])
            if min == 13: self.populate(self.w_minutes['thirteen'])
            if min == 14: self.populate(self.w_minutes['fourteen'])
            if min == 15: self.populate(self.w_minutes['quarter'])
            if min == 16: self.populate(self.w_minutes['sixteen'])
            if min == 17: self.populate(self.w_minutes['seventeen'])
            if min == 18: self.populate(self.w_minutes['eighteen'])
            if min == 19: self.populate(self.w_minutes['nineteen'])
            if min == 20: self.populate(self.w_minutes['twenty'])
        if 20 < min < 29:
            self.populate(self.w_to)
            self.populate(self.w_minutes['twenty'])
            if (min - 20) == 1: self.populate(self.w_minutes['one'])
            if (min - 20) == 2: self.populate(self.w_minutes['two'])
            if (min - 20) == 3: self.populate(self.w_minutes['three'])
            if (min - 20) == 4: self.populate(self.w_minutes['four'])
            if (min - 20) == 5: self.populate(self.w_minutes['five'])
            if (min - 20) == 6: self.populate(self.w_minutes['six'])
            if (min - 20) == 7: self.populate(self.w_minutes['seven'])
            if (min - 20) == 8: self.populate(self.w_minutes['eight'])
            if (min - 20) == 9: self.populate(self.w_minutes['nine'])
        if min == 29:
            self.populate(self.w_to)
            self.populate(self.w_half)
