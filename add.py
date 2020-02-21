from tkinter import *
import os
from PIL import Image as Img
from threading import Thread
import numpy as np
import scipy.special


class Paint(Frame):
    def __init__(self, parent, Image, net):
        Frame.__init__(self, parent)

        self.t = 0

        self.parent = parent

        self.net = net

        self.setUI()

        self.brush_size = 40
        self.brush_color = "black"

        self.canv.bind_all("<KeyPress>", self.get_shit)
        self.canv.bind("<B1-Motion>", self.draw)

        self.keys = [*map(str, range(10))]
        self.image_folder = "images"

    def get_shit(self, event):
        key = event.char

        all_files = os.listdir(os.getcwd())

        if "images" not in all_files:
            os.mkdir(self.image_folder)
            print("<<< Created 'images' folder >>>")

        if key in self.keys:
            images = all_files = os.listdir(
                os.getcwd() + "/" + self.image_folder)

            max_num = 0

            for image in images:
                if image[4] == key:
                    image_num = int(image.split("_")[2].split(".")[0])

                    if image_num > max_num:
                        max_num = image_num

            self.save_photo("num_{}_{}".format(key, max_num + 1))
        else:
            if key == "s":
                self.get_photoes_num()

            elif key == "d":
                self.canv.delete("all")

    def save_photo(self, name, del_it=True):
        self.canv.postscript(file=name + ".eps", colormode='color')

        img = Img.open(name + ".eps")

        resized_image = img.resize((24, 24))

        resized_image.save(self.image_folder + "/" + name + ".png")
        if del_it:
            print("<<< IMAGE SAVED " + self.image_folder + "/" + name + ".png >>>")

        img.close()

        os.remove(name + ".eps")
        if del_it:
            self.canv.delete("all")

    def get_photoes_num(self):
        arr = [0] * 10
        for photo_name in os.listdir(self.image_folder):
            photo_num = photo_name.split("_")[1]

            arr[int(photo_num)] += 1

        res = ""

        for i, num in enumerate(arr):
            res += str(i) + ": " + str(num) + "\t"

            if (i + 1) % 5 == 0:
                res += "\n"

        print("\n<<< PHOTOS NUMS >>>")
        print(res)
        print("\n")

    def get_weight(self):
        name = "test_img"
        self.canv.postscript(file=name + ".eps", colormode='color')

        img = Img.open(name + ".eps")

        resized_image = img.resize((24, 24))

        resized_image.save(name + ".png")

        arr = []

        img = Img.open(os.getcwd().replace("\\", "/") + "/test_img.png")

        w, h = img.size

        obj = img.load()

        for k in range(w):
            for i in range(h):
                if obj[k, i][0] == 0:
                    arr.append(0)
                else:
                    arr.append(1)

        return arr

    def setUI(self):

        self.parent.title("Pythonicway PyPaint")  # Устанавливаем название окна
        # Размещаем активные элементы на родительском окне
        self.pack(fill=BOTH, expand=1)

        # Даем седьмому столбцу возможность растягиваться, благодаря чему кнопки не будут разъезжаться при ресайзе
        self.columnconfigure(6, weight=1)
        self.rowconfigure(2, weight=1)  # То же самое для третьего ряда

        # Создаем поле для рисования, устанавливаем белый фон
        self.canv = Canvas(self, bg="white")
        self.canv.grid(row=2, column=0, columnspan=7,
                       padx=5, pady=5, sticky=E + W + S + N)

    def draw(self, event):

        self.canv.create_oval(event.x - self.brush_size,
                              event.y - self.brush_size,
                              event.x + self.brush_size,
                              event.y + self.brush_size,
                              fill=self.brush_color, outline=self.brush_color)


def run_drawer():
    root = Tk()
    root.geometry("500x500")
    app = Paint(root, Image)
    root.mainloop()
