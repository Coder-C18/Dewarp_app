import tkinter as tk
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
import cv2
from dewarping import Dewarping

x_start, y_start, x_end, y_end = 0, 0, 0, 0

def on_button_press( event):
    x_start, y_start=event.x,event.y
    canvas.create_image(0, 0, image=e1.image, anchor="nw")
    canvas.create_rectangle(  x_start, y_start, event.x+100,event.y+100, outline='red')


def on_move_press( event):
    x_end, y_end = event.x, event.y
    canvas.create_image(0, 0, image=e1.image, anchor="nw")
    print(x_start, y_start)
    canvas.create_rectangle(x_start, y_start,  x_end, y_end, outline='red')

    # w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
    # if event.x > 0.9 * w:
    #     self.canvas.xview_scroll(1, 'units')
    # elif event.x < 0.1 * w:
    #     self.canvas.xview_scroll(-1, 'units')
    # if event.y > 0.9 * h:
    #     self.canvas.yview_scroll(1, 'units')
    # elif event.y < 0.1 * h:
    #     self.canvas.yview_scroll(-1, 'units')
    #
    # # expand rectangle as you drag the mouse
    # self.canvas.coords(self.rect, self.start_x, self.start_y, curX, curY)


def upload_file(e1):
    f_types = [('Jpg Files', '*.jpg'),
               ('PNG Files', '*.png')]  # type of files to select
    filename = tk.filedialog.askopenfilename(multiple=True, filetypes=f_types)
    for f in filename:
        mylist.insert(END, f)
    scrollbar.config(command=mylist.yview)
    return 1


def load_img(event):
    cs = mylist.curselection()
    f = mylist.get(cs)
    img = Image.open(f)  # read the image file
    img2 = img.resize((992, 992))
    img2 = ImageTk.PhotoImage(img2)
    e3.config(image=img2)
    e3.image = img2
    img = img.resize((576, 818))  # new width & height
    img = ImageTk.PhotoImage(img)
    e1.config(image=img)
    e1.image = img
    # canvas.create_image(0, 0, image=img, anchor="nw")
    # a = canvas.create_rectangle(50, 0, 100, 500)


def np2imgtk(image):
    image = cv2.resize(image, (576, 818))
    red, green, blue = cv2.split(image)
    image = cv2.merge((red, green, blue))
    im = Image.fromarray(image)
    im = ImageTk.PhotoImage(image=im)
    return im


def upload_file1():
    width, height = e3.image._PhotoImage__size
    rgb = np.empty((height, width, 3))
    for j in range(height):
        for i in range(width):
            rgb[j, i, :] = e3.image._PhotoImage__photo.get(x=i, y=j)
    new_image = Image.fromarray(rgb.astype('uint8'))
    new_image = np.array(new_image)
    img_soure, img_dewarping = model.dewarp_predict(new_image)
    if CheckVar1.get()==1:
        img_soure = np2imgtk(img_soure)
        e1.config(image=img_soure)
        e1.image = img_soure
    imgtk = np2imgtk(img_dewarping)
    e2.config(image=imgtk)
    e2.image = imgtk


if __name__ == "__main__":
    model = Dewarping('wrapped_rnn.pt')

    my_w = tk.Tk()
    my_w.geometry("1900x980")  # Size of the window
    labelframe = Frame(my_w,
                       height=900,
                       width=600,
                       borderwidth=10,
                       relief="groove")
    labelframe.place(x=13, y=61)
    e1 = tk.Label(labelframe)
    e1.place(x=0, y=0)
    canvas = Canvas( labelframe, width=600, height=900)
    canvas.place(x=0, y=0)



    labelframe2 = Frame(my_w,
                        height=900,
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
                              command=lambda: upload_file1())
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
                   command=lambda: upload_file(e1))
    b1.place(x=1383, y=581)
    mylist.bind('<Double-1>', load_img)
    canvas.bind("<ButtonPress-1>", on_button_press)
    canvas.bind("<B1-Motion>", on_move_press)
    my_w.mainloop()

# import PIL.Image
# from PIL import Image, ImageTk
# from tkinter import *
#
#
# class ExampleApp(Frame):
#     def __init__(self,master):
#         Frame.__init__(self,master=None)
#         self.x = self.y = 0
#         self.canvas = Canvas(self,  cursor="cross")
#         #
#         # self.sbarv=Scrollbar(self,orient=VERTICAL)
#         # self.sbarh=Scrollbar(self,orient=HORIZONTAL)
#         # self.sbarv.config(command=self.canvas.yview)
#         # self.sbarh.config(command=self.canvas.xview)
#         #
#         # self.canvas.config(yscrollcommand=self.sbarv.set)
#         # self.canvas.config(xscrollcommand=self.sbarh.set)
#
#         self.canvas.grid(row=0,column=0,sticky=N+S+E+W)
#         # self.sbarv.grid(row=0,column=1,stick=N+S)
#         # self.sbarh.grid(row=1,column=0,sticky=E+W)
#
#         self.canvas.bind("<ButtonPress-1>", self.on_button_press)
#         self.canvas.bind("<B1-Motion>", self.on_move_press)
#         # self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
#
#         self.rect = None
#
#         self.start_x = None
#         self.start_y = None
#
#         self.im = PIL.Image.open("51_1 copy.png")
#         self.wazil,self.lard=self.im.size
#         self.canvas.config(scrollregion=(0,0,self.wazil,self.lard))
#         self.tk_im = ImageTk.PhotoImage(self.im)
#         self.canvas.create_image(0,0,anchor="nw",image=self.tk_im)
#
#
#     def on_button_press(self, event):
#         # save mouse drag start position
#         self.start_x = self.canvas.canvasx(event.x)
#         self.start_y = self.canvas.canvasy(event.y)
#
#         # create rectangle if not yet exist
#         if not self.rect:
#             self.rect = self.canvas.create_rectangle(self.x, self.y, 1, 1, outline='red')
#
#     def on_move_press(self, event):
#         curX = self.canvas.canvasx(event.x)
#         curY = self.canvas.canvasy(event.y)
#
#         w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
#         if event.x > 0.9*w:
#             self.canvas.xview_scroll(1, 'units')
#         elif event.x < 0.1*w:
#             self.canvas.xview_scroll(-1, 'units')
#         if event.y > 0.9*h:
#             self.canvas.yview_scroll(1, 'units')
#         elif event.y < 0.1*h:
#             self.canvas.yview_scroll(-1, 'units')
#
#         # expand rectangle as you drag the mouse
#         self.canvas.coords(self.rect, self.start_x, self.start_y, curX, curY)
#
#     def on_button_release(self, event):
#         pass
#
# if __name__ == "__main__":
#     root=Tk()
#     app = ExampleApp(root)
#     app.pack()
#     root.mainloop()