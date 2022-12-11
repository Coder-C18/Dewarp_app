import os.path
import tkinter as tk
from tkinter import *
from tkinter import filedialog

from PIL import Image, ImageTk
import numpy as np
import cv2
from dewarping import Dewarping

out_image = None


class ExampleApp(Frame):
    def __init__(self, master):
        Frame.__init__(self, master=None)
        self.x = self.y = 0
        self.x_end = self.y_end = 0
        self.canvas = Canvas(master, height=800, width=580, cursor="cross")

        self.canvas.place(x=0, y=0)

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        self.rect = None

        self.start_x = None
        self.start_y = None

        self.tk_im = None
        self.img_source = None

        self.out_image= None
        # self.canvas.create_image(0, 0, anchor="nw", image=self.tk_im)

    def on_button_press(self, event):
        self.canvas.delete(self.rect)
        # save mouse drag start position
        self.start_x = event.x
        self.start_y = event.y

        self.rect = self.canvas.create_rectangle(self.x, self.y, 1, 1, fill='', outline='red')

    def on_move_press(self, event):
        self.x_end, self.y_end = (event.x, event.y)

        # expand rectangle as you drag the mouse
        self.canvas.coords(self.rect, self.start_x, self.start_y, self.x_end, self.y_end)

    def on_button_release(self, event):
        print('heel')
        pass

def save():
   path = filedialog.asksaveasfile(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")),defaultextension='.jpg')
   img = app.out_image
   print(path)

   red, green, blue = cv2.split(img)
   image = cv2.merge((red, green, blue))
   img = Image.fromarray(image)

   img.save(path)

   print(path)


def upload_file(app):
    f_types = [('Jpg Files', '*.jpg'),
               ('PNG Files', '*.png')]  # type of files to select
    filename = tk.filedialog.askopenfilename(multiple=True, filetypes=f_types)
    for f in filename:
        mylist.insert(END, f)
    first_image = filename[0]

    img = Image.open(first_image)  # read the image file

    app.img_source = img

    img2 = img.resize((576, 818))
    img2 = ImageTk.PhotoImage(img2)
    app.tk_im = img2
    app.canvas.create_image(0, 0, anchor="nw", image=app.tk_im)

    scrollbar.config(command=mylist.yview)
    return 1


def load_img(event):
    cs = mylist.curselection()
    f = mylist.get(cs)
    img = Image.open(f)  # read the image file
    app.img_source = img
    img = img.resize((576, 818))  # new width & height
    img = ImageTk.PhotoImage(img)
    app.tk_im = img
    app.canvas.create_image(0, 0, anchor="nw", image=app.tk_im)


def crop():
    left, upper, right, lower = app.start_x, app.start_y, app.x_end, app.y_end
    w,h=app.img_source.size

    app.img_source.save("geeks0.jpg")
    app.img_source = app.img_source.crop(((left/576)*w, (upper/818)*h, (right/576)*w, (lower/818)*h))
    app.img_source = app.img_source.resize((576, 818))
    app.img_source.save("geeks.jpg")

    img = ImageTk.PhotoImage(app.img_source)
    app.tk_im = img
    app.canvas.create_image(0, 0, anchor="nw", image=app.tk_im)




def np2imgtk(image):
    image = cv2.resize(image, (576, 818))
    red, green, blue = cv2.split(image)
    image = cv2.merge((red, green, blue))
    im = Image.fromarray(image)
    im = ImageTk.PhotoImage(image=im)
    return im


def dewarp():
    image = ImageTk.PhotoImage(app.img_source)
    width, height = image._PhotoImage__size
    rgb = np.empty((height, width, 3))
    for j in range(height):
        for i in range(width):
            rgb[j, i, :] = image._PhotoImage__photo.get(x=i, y=j)
    new_image = Image.fromarray(rgb.astype('uint8'))
    new_image = np.array(new_image)
    img_soure, img_dewarping = model.dewarp_predict(new_image)

    app.out_image = img_dewarping
    if CheckVar1.get() == 1:
        img_soure = np2imgtk(img_soure)
        app.tk_im = img_soure
        app.canvas.create_image(0, 0, anchor="nw", image=app.tk_im)
    imgtk = np2imgtk(img_dewarping)
    e2.config(image=imgtk)
    e2.image = imgtk


if __name__ == "__main__":
    model = Dewarping('wrapped_rnn.pt')

    my_w = tk.Tk()
    my_w.geometry("1900x980")  # Size of the window
    labelframe = Frame(my_w,
                       height=830,
                       width=600,
                       borderwidth=10,
                       relief="groove")
    labelframe.place(x=13, y=61)

    app = ExampleApp(labelframe)
    app.place(x=0, y=0)

    labelframe2 = Frame(my_w,
                        height=830,
                        width=600,
                        borderwidth=10,
                        relief="groove")
    labelframe2.place(x=698, y=61)

    e2 = tk.Label(labelframe2)
    e2.place(x=0, y=0)
    e3 = tk.Label(my_w)

    labelframe3 = Frame(my_w,
                        height=500,
                        width=428,
                        borderwidth=5,
                        relief="groove")
    labelframe3.place(x=1383, y=61)
    scrollbar = Scrollbar(labelframe3)
    scrollbar.pack(side=RIGHT, fill=Y)
    mylist = Listbox(labelframe3,
                     yscrollcommand=scrollbar.set,
                     width=70,
                     height=30)
    mylist.pack(side=LEFT)

    dewarp_button = tk.Button(my_w,
                              text='Dewarping',
                              background="red",
                              height=5,
                              width=65,
                              command=lambda: dewarp())
    dewarp_button.place(x=1383, y=789)

    CheckVar1 = IntVar()
    check_button = Checkbutton(my_w,
                               text="Visual control point",
                               variable=CheckVar1,
                               onvalue=1,
                               offvalue=0,
                               height=5,
                               width=20)
    check_button.place(x=1383, y=677)

    b1 = tk.Button(my_w,
                   text='Upload Files',
                   # background="purple",
                   height=2,
                   width=65,
                   command=lambda: upload_file(app))
    b1.place(x=1383, y=581)

    b2 = tk.Button(my_w,
                   text='crop',
                   height=2,
                   width=5,
                   command=lambda : crop()
                   )
    b2.place(x=1383, y=630)


    save_button = tk.Button(my_w,
                   text='save',
                   height=2,
                   width=5,
                   command=lambda : save()
                   )

    save_button.place(x=1453, y=630)
    mylist.bind('<Double-1>', load_img)
    my_w.mainloop()
