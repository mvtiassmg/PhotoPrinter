from serial import Serial
import parameters as p
from threading import Thread, Event


class ArduinoPort:

    def __init__(self):
        self.ser = Serial(p.ARDUINO_COM, p.ARDUINO_BAUDRATE,
                          timeout=p.ARDUINO_TIMEOUT)
        self.close_event = Event()
        self.read_thread = Thread(target=self.read, daemon=False)
        self.data_received_event = Event()
        self.read_cb_thread = Thread(target=self.read_cb, daemon=True)
        self.data_processed_event = Event()
        self.data_read = None
        # self.init_threads()

    def init_threads(self):
        self.read_thread.start()
        self.read_cb_thread.start()

    def close(self):
        print("Cerrando puerto serial...")
        self.close_event.set()
        if self.ser.is_open:
            self.ser.close()

    def send(self, data_str: str, mandatory=False):
        if not mandatory:
            if self.ser.writable():
                self.ser.write(data_str.encode(p.ENCODE))
        else:
            while not self.ser.writable():
                pass
            self.ser.write(data_str.encode(p.ENCODE))

    def read(self):
        print("READING THREAD STARTED")
        try:
            while not self.close_event.is_set():
                if not self.data_received_event.is_set():
                    data = self.ser.readline().decode(p.ENCODE)
                if data and data is not None:
                    self.data_read = data.strip()
                    print("Serial data read:", self.data_read)
                    self.data_received_event.set()
                    self.data_processed_event.wait()
                    self.data_processed_event.clear()
        except Exception as error:
            pass
        finally:
            print("READING THREAD ENDED")

    def read_cb(self):
        while True:
            self.data_received_event.wait()
            self.data_received_event.clear()
            print("Processing data...")
            if self.data_read == "hola":
                pass
            self.data_read = None
            print("Data processed")
            self.data_processed_event.set()


if __name__ == "__main__":
    ev = Event()
    ar = ArduinoPort()
    try:
        while True:
            input_ = input("")
            ar.send(input)
    except KeyboardInterrupt:
        print("Cierre por teclado")
        ar.close()
