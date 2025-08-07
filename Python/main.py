from CPU import CPU
import easygui


if __name__ == "__main__":
    try:
        cpu = CPU()
        cpu.init()
        # cpu.load_img()
        # cpu.generate_routine(0)
        # print(cpu.routine.secuence)
    except Exception as e:
        print("error de init")
        pass
