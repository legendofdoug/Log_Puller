#!/usr/bin/python

import tkinter as tk

root = tk.Tk()
root.title("Simple Calculator")

frame_a = tk.Frame()
frame_b = tk.Frame()

label_a = tk.Label(master=frame_a, text="I'm in Frame A.")
label_a.pack()

label_b = tk.Label(master=frame_b, text="I'm in Frame B.")
label_b.pack()

frame_a.pack()
frame_b.pack()

# Widgets here
# Creating a Label Widget


# shoves onto the screen


root.mainloop()
