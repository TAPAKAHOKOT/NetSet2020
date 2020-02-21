from add import run_drawer
from PIL import Image as Img
import os
from netset import NetSet
import keyboard as kb
from add import *
import os
from threading import Thread
from time import sleep

# run_drawer()


def pretty_bytes(fpath, delim=''):
    arr = []

    img = Img.open(os.getcwd().replace("\\", "/") + fpath)

    w, h = img.size

    obj = img.load()

    for k in range(w):
        for i in range(h):
            if obj[k, i][0] == 0:
                arr.append(0)
            else:
                arr.append(1)

    return arr


bytes_photos = {}
for photo_name in os.listdir("images"):
    num = photo_name.split("_")[1]

    if num in bytes_photos:
        bytes_photos[num].append(pretty_bytes("/images/" + photo_name))
    else:
        bytes_photos[num] = [pretty_bytes("/images/" + photo_name)]

# print(bytes_photos)


net = NetSet(576, 200, 10, 0.1)

epochs = 500
for k in range(epochs):
    if k % (epochs // 100) == 0:
        os.system("cls")
        print(round(k / epochs * 100), "%")

    for i in range(10):
        net.train(bytes_photos[str(i)], i)


def get_w():
    root_text = Tk()
    root_text.geometry("100x200")

    lab = Label(width=20, height=10, text="")
    lab.pack()

    lab2 = Label(text="", font=("Comic Sans MS", 24, "bold"))
    lab2.pack()

    # root_text.mainloop()

    while True:

        arr = app.get_weight()

        res = net.query(arr)

        line = "\n\n"

        os.system("cls")

        for i in range(10):

            line += str(i) + " - " + str(round(res[i, 0] * 100, 1)) + "%\n"

        line += "\n"
        lab["text"] = line

        lab2["text"] = str(list(res).index(max(res)))

        sleep(0.03)
        root_text.update()


kb.add_hotkey('t', get_w)


th = Thread(target=get_w)
th.start()

root = Tk()
root.geometry("500x500")
app = Paint(root, Image, net)

root.mainloop()


th.join()
