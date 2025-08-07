# LENGTH = EJE X
# WIDTH = EJE Y
CROP_LENGTH = 345  # mm
CROP_WIDTH = 220  # mm
RESOLUTION = 0.16  # mm/step
PROJ_LENGTH = int(CROP_LENGTH/RESOLUTION)  # steps
PROJ_WIDTH = int(CROP_WIDTH/RESOLUTION)  # steps
EXP_TIME = 50e3  # ns
STEPPER_T_MIN = 1000/25_000  # ns
MAX_STEP_X = 2156
MAX_STEP_Y = 1375

PWM_THRESHOLD = 150

ARDUINO_COM = "COM5"
ARDUINO_BAUDRATE = 115200
ARDUINO_TIMEOUT = 0  # None: waitforever | 0: non block

ENCODE = "utf-8"

if __name__ == "__main__":
    print(-3 % 3 + 1)
