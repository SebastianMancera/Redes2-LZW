#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tkinter import filedialog
from tkinter import *
import os
from comprimir import algoritmolzw

ventana = Tk()


def abrir_archivo():
    mensaje = filedialog.askopenfilename(initialdir="/",
                                                 title="Seleccione archivo", filetypes=(("txt files", "*.txt"),
                                                                                        ("all files", "*.*")))
    print(mensaje)


Button(text="Abrir archivo", bg="pale green", command=abrir_archivo).place(x=10, y=10)



myList = ["a", "b", "c"]
myFrame = Frame(ventana).place(x=50, y=100)
for i in myList:
    Label(myFrame, text = i).pack()



ventana.mainloop()