import os
from datetime import datetime
from time import sleep
# from pyfiglet import Figlet
from art import *


class SwcProcessor:
    def __init__(self):
        pass

    def start(self, type):
        start = datetime.now()
        while True:
            now = datetime.now()
            time = str(now - start)[0:-3]
            if type == 1:
                self.display_type_1(time)
            else:
                self.display_type_2(time)

            sleep(0.2)

    def display_type_1(self, time):
        print("\r" + time, end="")

    def display_type_2(self, time):
        os.system('clear')
        # tprint(time, font="dotmatrix")
        # tprint(time, font="univers")
        # tprint(time, font="doh")
        # tprint(time, font="roman")
        # tprint(time, font="georgia11")
        # tprint(time, font="xhelvi")
        # tprint(time, font="utopiai")
        # tprint(time, font="rev")
        # tprint(time, font="larry3d")
        # tprint(time, font="nancyj")
        # tprint(time, font="nancyj-underlined")
        # tprint(time, font="block2")
        # tprint(time, font="soft")
        # tprint(time, font="4max")
        # tprint(time, font="5x7")
        # tprint(time, font="stampate")
        # tprint(time, font="o8")
        tprint(time, font="standard")
        # tprint(time, font="alphabet")
        # tprint(time, font="computer")
        # tprint(time, font="shadow")
        # tprint(time, font="speed")
        # tprint(time, font="rounded")
        # tprint(time, font="chartri")
