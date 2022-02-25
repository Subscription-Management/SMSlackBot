import pprint
import time

class Util:

    @staticmethod
    def pprint(val):
        pprint.pprint(val)

    @staticmethod
    def current_milli_time():
        return round(time.time() * 1000)
