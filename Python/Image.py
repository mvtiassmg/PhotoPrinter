import cv2
from os import path
import numpy as np
import easygui
import matplotlib.pyplot as plt
from Routine import Routine
import parameters as p

# img[0] -> vertical imagen
# img[1] -> horizontal de imagen


class Image:

    def __init__(self, rotation=0, adjust=0):
        self.file = easygui.fileopenbox(
            title="Selecciona una imagen",
            default="*.jpg",
            filetypes=[["*.jpg", "*.png", "Image files"]]
        )

        self.file_name = path.basename(self.file)
        self.arr = np.fromfile(self.file, np.uint8)
        self.full_cmap = cv2.imdecode(self.arr, cv2.IMREAD_COLOR)
        self.rotate(rotation)

        if adjust == 1:
            self.adjust_undersize()
        self.adjust_to_max_steps()

    def rotate(self, rotation: int):
        if rotation >= 0:
            self.full_cmap = np.rot90(self.full_cmap, rotation % 3)
        else:
            self.full_cmap = np.rot90(self.full_cmap, rotation % 3 + 1)

    def adjust_to_max_steps(self):
        self.full_cmap = cv2.resize(
            self.full_cmap,
            (p.MAX_STEP_X, p.MAX_STEP_Y),
            interpolation=cv2.INTER_AREA
        )

    def adjust_undersize(self):
        ratio_x = self.size[0] / p.PROJ_LENGTH
        ratio_y = self.size[1] / p.PROJ_WIDTH
        if ratio_x > ratio_y and self.size[0] < p.PROJ_LENGTH:
            new_width = p.PROJ_LENGTH
            new_height = int(self.size[1] / self.size[0] * p.PROJ_LENGTH)
        else:
            new_height = p.PROJ_WIDTH
            new_width = int(self.size[0] / self.size[1] * p.PROJ_WIDTH)
        self.full_cmap = cv2.resize(self.full_cmap, (new_width, new_height))

    @property
    def cmap(self):
        """Canal rojo como imagen en escala de grises (para láser)"""
        return self.full_cmap[:, :, 2]  # canal R

    @property
    def cmap_norm(self):
        return self.cmap.astype(np.float32) / 255.0

    @property
    def size(self):
        return (self.full_cmap.shape[1], self.full_cmap.shape[0])

    @property
    def ratio(self):
        """Relación de aspecto: ancho / alto"""
        return self.size[0] / self.size[1]

    def show(self):
        """Muestra la imagen RGB original"""
        plt.title(f"{self.file_name} - {self.size}")
        plt.xlabel("x [pix]")
        plt.ylabel("y [pix]")
        plt.imshow(self.full_cmap)
        plt.show()

    def generate_routine(self, mode: int):
        return Routine(self.cmap, mode, self.file_name)


if __name__ == "__main__":
    img = Image(rotation=1, adjust=1)
    print("Tamaño final:", img.size)
    img.show()