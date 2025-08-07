from tqdm import tqdm
import numpy as np
import time
import parameters as p
from Routine import Routine
from numpy import ndarray


class Head:

    def __init__(self):
        self.frame_origin = None
        self.routine = None
        self.state = np.array([0, 0], dtype=int)

    def calibrate(self):
        pass

    def set_routine(self, routine: Routine):
        self.routine = routine

    def del_routine(self):
        self.routine = None

    def update_routine_offset(self):
        self.routine.frame_offset = self.state

    def do_frame(self):  # fix sleep
        print("\nRealizando marco")
        self.send_command((0, 0, 0))
        for point in tqdm(self.routine.frame_points):
            self.move_to(point)
            time.sleep(p.STEPPER_T_MIN/1000)

    def init_routine(self):
        print(f"\nStarting to print a {self.routine.img_size} pix image")
        movs_list = self.calculate_movements(self.routine.route)
        self.calibrate()
        self.move_to((0, 0))
        print(f"Estimated time: {self.routine.duration} min")
        it = list(zip(movs_list, self.routine.pwms, self.routine.delays))
        for commands, pwm, delay in tqdm(it, desc="Printing image"):
            for comm in commands:
                self.send_command((comm[0], comm[1], 0))
                t_move = time.perf_counter_ns()
                self.state += comm
                t_pwm = time.perf_counter_ns()
                if time.perf_counter_ns() - t_move < p.STEPPER_T_MIN:
                    while time.perf_counter_ns() - t_move < p.STEPPER_T_MIN:
                        pass
            # self.send_command((0, 0, pwm))
        # time.sleep(delay/1000)

    # movimientos (1/-1/0) por paso para realizar secuencia
    def calculate_movements(self, points: ndarray):
        movs_list = []
        state_aux = np.copy(self.state)
        for point in tqdm(points, desc="Calculating movements"):
            dir_ = np.sign(point - state_aux, dtype=int)
            delta_abs = np.absolute(point - state_aux, dtype=int)
            delta_fill = np.max(delta_abs) - delta_abs
            col_x = np.concatenate((np.full((delta_abs[0],), dir_[0]),
                                    np.zeros(delta_fill[0])))
            col_y = np.concatenate((np.full((delta_abs[1],), dir_[1]),
                                    np.zeros(delta_fill[1])))
            comm = np.column_stack((col_x, col_y)).astype(int)
            movs_list.append(comm)
            state_aux += np.sum(comm, axis=0)
        return movs_list

    # agregar encencido o pagado laser
    def move_to(self, point: ndarray):  # recibe de cpu
        # print(f"\nMoviendo de {self.state} a {point}")
        dir_ = np.sign(point - self.state, dtype=int)
        delta_abs = np.absolute(point - self.state, dtype=int)
        delta_fill = np.max(delta_abs) - delta_abs
        col_x = np.concatenate((np.full((delta_abs[0],), dir_[0]),
                               np.zeros(delta_fill[0])))
        col_y = np.concatenate((np.full((delta_abs[1],), dir_[1]),
                               np.zeros(delta_fill[1])))
        commands = np.column_stack((col_x, col_y)).astype(int)
        for command in commands:
            self.send_command(",".join(command.astype(str))+",0")
            self.state += command
            t_move = time.perf_counter_ns()
            if time.perf_counter_ns() - t_move < p.STEPPER_T_MIN:
                while time.perf_counter_ns() - t_move < p.STEPPER_T_MIN:
                    pass

    def send_command(self, comm: str):
        # "x,dirx,y,diry,laser"
        # x/y : {0: inactivo, 1: step}
        # dir : {0: neg, 1: pos}
        # print("...Enviando:", comm)
        pass


if __name__ == "__main__":
    from Image import Image
    img = Image()
    rout = img.generate_routine(0)
    head = Head()
    head.set_routine(rout)
    # rout.show_im()
    # rout.show_canvas()
    # head.do_frame()
    head.init_routine()
