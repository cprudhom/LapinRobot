# coding: utf-8
import enum

'''
file to init global variables in every files imported as glob
'''


# Using enum class create enumerations
class State(enum.Enum):
    Rest = 0
    Adrenaline = 1
    Acetylcholine = 2


class Observation(enum.Enum):
    FR = 0
    FC = 1
    # DI = 2


IN_NS = 1e9  # for duration in nanoseconds
FREQUENCY = 0.005  # one line every 5 ms
NUMBER_OF_LINES = 20  # bunch of lines
TIME_TO_WAIT = FREQUENCY * NUMBER_OF_LINES * IN_NS

debug = True

port = 'COM7'
baudrate = 2000000

rest_file_name = None
running = False

tdata = []
ydata = []

molecules = [str(State.Adrenaline.name), str(State.Acetylcholine.name)]
state = State.Rest

observations = [str(Observation.FR.name), str(Observation.FC.name)]

need_change_file = False
