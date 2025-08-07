from Image import Image
from Head import Head
import time
from easygui import indexbox, integerbox, ccbox, msgbox
from threading import Event
from ArduinoPort import ArduinoPort


class CPU:

    def __init__(self):
        self.img = None
        self.routine = None
        self.head = Head()
        self.close_event = Event()
        # self.arduino = ArduinoPort()

    def init_serial(self):
        print("inicainzo arduino")
        self.arduino.init_threads()

    def init(self):
        try:
            # self.init_serial()
            choice = indexbox("WELCOME TO PHOTOPRINTER", "Photo-printer",
                              choices=("Exit", "Load Image"),
                              default_choice="Load Image",
                              cancel_choice="Exit")
            while choice != 0 and choice != None:

                if choice == 1:  # Load Image
                    img = Image()

                    while choice != 0:
                        choice = indexbox(f"IMAGE UPLOADED: {img.file_name}", "Photo-printer",
                                          choices=("Exit", "Load New Image",
                                                   "Show Image", "Edit Image", "Calculate Routine"),
                                          cancel_choice="Exit")
                        if choice == 0:
                            break

                        if choice == 1:  # Load New Image
                            img = Image()

                        if choice == 2:  # Show Image
                            img.show()

                        if choice == 3:  # Edit Image
                            choice = indexbox("choose", "Photo-printer",
                                              choices=("Return", "Rotate", "Adjust"))
                            if choice == 0:  # Return
                                choice = None
                            if choice == 1:  # Rotate
                                rotation = integerbox("Enter the number of rotations of 90°(>0 counterclockwise / <0 clockwise )",
                                                      "Photo-printer",
                                                      lowerbound=-99, upperbound=99)
                                img.rotate(rotation)
                            if choice == 2:  # Adjust
                                img.adjust_undersize()

                        if choice == 4:  # Calculate Routine
                            routine = img.generate_routine(0)
                            while choice != 0:
                                choice = indexbox("choose", "Photo-printer",
                                                  choices=("Return", "Show Canvas", "Set Offset", "Print"))
                                if choice == 0:  # Return
                                    pass
                                if choice == 1:  # Show Canvas
                                    routine.show_canvas()
                                if choice == 2:  # Set Offset
                                    pass
                                if choice == 3:  # Print
                                    choice = ccbox("Continue?")
                                    if choice:
                                        t_init = time.time()
                                        self.head.set_routine(routine)
                                        self.head.init_routine()
                                        t_fin = time.time()
                                        msgbox(
                                            f"Routine completed in {t_fin-t_init} s")
                                    else:
                                        pass
                            choice = None

                if choice == 2:
                    pass
                if choice == 3:
                    print("exit")

                if choice == 0:
                    break
                choice = indexbox("WELCOME", "Photo-printer",
                                  choices=("Exit", "Load Image"),
                                  default_choice="Load Image",
                                  cancel_choice="Exit")
        except Exception as e:
            self.arduino.close()


if __name__ == "__main__":
    # integerbox()
    cpu = CPU()
    cpu.init()
    print("init")
