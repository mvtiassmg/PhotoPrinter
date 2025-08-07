import numpy as np
import matplotlib.pyplot as plt
import parameters as p
from tqdm import tqdm
import time


class Routine:

    def __init__(self, img_map: np.ndarray, mode: int, name: str):
        self.name = name
        self.img_map = img_map.astype(int)
        self.size = self.img_map.size  # = ancho * alto
        self.rel_route = self.generate_route(threshold=p.PWM_THRESHOLD)

        if mode == 0:  # PWM variable, tiempo constante
            self.delays = p.EXP_TIME * np.ones(self.size, dtype=int)
            self.pwms = self.img_map.flatten()
        elif mode == 1:  # PWM constante, tiempo variable
            self.pwms = np.ones(self.size, dtype=int)
            self.delays = (p.EXP_TIME / 255 * self.img_map).flatten()

    @property
    def img_size(self):
        return (self.img_map.shape[1], self.img_map.shape[0])  # (ancho, alto)

    @property
    def canvas_size(self):
        return self.img_size

    @property
    def route(self):
        return self.rel_route.astype(int)

    @property
    def frame_points(self):
        x_max, y_max = self.img_size
        return np.array([
            [0, 0],
            [0, y_max],
            [x_max, y_max],
            [x_max, 0]
        ], dtype=int)

    @property
    def duration(self):
        return self.size * (p.STEPPER_T_MIN + p.EXP_TIME) / 1e9 / 60  # en minutos

    @property
    def canvas_map(self):
        # Ya no se requiere offset ni centrado
        return self.img_map

    def generate_route(self, threshold=p.PWM_THRESHOLD):
        """Recorrido zig-zag tipo impresora, línea por línea"""
        y_max, x_max = self.img_map.shape
        route = []

        for x in tqdm(range(x_max), desc="Generando ruta optimizada (pasos)"):
            y_range = range(y_max) if x % 2 == 0 else range(y_max - 1, -1, -1)
            for y in y_range:
                if self.img_map[y, x] > threshold:
                    route.append([x, y])

        return np.array(route, dtype=int)

    def show_im(self):
        plt.title(f"{self.name} - {self.img_size}")
        plt.xlabel("x [pix]")
        plt.ylabel("y [pix]")
        plt.imshow(self.img_map, cmap="gray")
        plt.show()

    def show_canvas(self):
        plt.title(f"{self.name} - {self.canvas_size}")
        plt.xlabel("x [pix]")
        plt.ylabel("y [pix]")
        plt.imshow(self.canvas_map, cmap="gray")
        plt.show()

    def simulate_route(self):
        original = self.canvas_map.copy()
        canvas = np.zeros_like(original)

        fig, ax = plt.subplots(figsize=(8, 6))
        im = ax.imshow(canvas, cmap='gray', vmin=0, vmax=255)
        txt = ax.text(10, 10, '', color='red', fontsize=10, bbox=dict(facecolor='white', alpha=0.8))
        ax.set_title("Simulación de impresión en pasos")
        ax.set_xlabel("X [pasos]")
        ax.set_ylabel("Y [pasos]")

        skip = 200  # actualiza cada N pasos

        for i, (x, y) in enumerate(self.route):
            if 0 <= y < canvas.shape[0] and 0 <= x < canvas.shape[1]:
                pwm = self.pwms[i] if i < len(self.pwms) else 0
                canvas[y, x] = original[y, x]

            if i % skip == 0 or i == len(self.route) - 1:
                im.set_data(canvas)
                txt.set_text(f"Paso {i+1}/{len(self.route)}\nPWM={pwm}")
                txt.set_position((x + 10, y + 10))
                plt.pause(0.001)

        plt.ioff()
        plt.show()


if __name__ == "__main__":
    from Image import Image
    img = Image(rotation=1, adjust=1)
    routine = img.generate_routine(0)
    routine.show_im()
    routine.show_canvas()
    routine.simulate_route()