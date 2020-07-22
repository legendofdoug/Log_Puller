#!/usr/bin/python

import tkinter as tk
import fai
import menu
import config

# class log_gui(tk.Frame):
#    def __init__(self, master = None):
class log_gui():

    def __init__(self, root):
        self.root = root
        self.root.title("Log Puller")
        self.root.config(bg="#111111")
        self.log_frame = tk.Frame(master=self.root)
        self.log_frame.config(bg="#111111")
        self.log_frame.grid(row=0, column=2, columnspan=8)
        self.info_frame = tk.Frame(master=self.root)
        self.info_frame.config(bg="#111111")
        self.info_frame.grid(row=0, column=0, columnspan=2, rowspan=2)
        self.lbl_infoside = tk.Label(self.info_frame, text="Insert Details Below")
        self.lbl_infoside.config(bg="#111111", fg="white", font=("Helvetica", 16))
        self.lbl_infoside.grid(row=0, column=0, columnspan=2)
        self.lbl_rackSN = tk.Label(self.info_frame, text="RACK  SN", width=10, height=1)
        self.lbl_rackSN.config(bg="#111111", fg="white", font=("Helvetica", 12))
        self.lbl_rackSN.grid(row=1, column=0, columnspan=1)

        self.ent_rackSN = tk.Entry(self.info_frame, width=25, borderwidth=2)
        self.ent_rackSN.grid(row=1, column=1, columnspan=1, padx=10, pady=10)

        self.lbl_pxe = tk.Label(self.info_frame, text="PXE IP")
        self.lbl_pxe.config(bg="#111111", fg="white", font=("Helvetica", 12))
        self.lbl_pxe.grid(row=2, column=0, columnspan=1, padx=10, pady=0)

        self.ent_pxe = tk.Entry(self.info_frame, width=50, borderwidth=2)
        self.ent_pxe.grid(row=3, column=1, columnspan=1, padx=10, pady=10)
        self.ent_pxe.insert(0, "Enter Custom IP Here only if you selected custom PXE")

        self.lbl_log_area = tk.Label(master=self.log_frame, text="Log Output")
        self.lbl_log_area.config(font=("Helvetica", 16))
        self.lbl_log_area.grid(row=0, column=3)
        self.txt_log_area = tk.Text(master=self.log_frame, bg="black", fg="white", height=50, width=75)
        # self.txt_log_area.config(state=DISABLED)
        self.txt_log_area.grid(row=1, column=3, rowspan=10, sticky="nsew")
        S = tk.Scrollbar(self.log_frame)
        S.grid(row=1, column=4, rowspan=10)
        S.config(command=self.txt_log_area.yview)
        self.txt_log_area.config(yscrollcommand=S.set)

        self.txt_log_area.columnconfigure(3, weight=1, minsize=75)
        self.txt_log_area.rowconfigure(3, weight=1, minsize=70)

        choices = config.choices

        self.variable = tk.StringVar(self.root)
        self.variable.set(choices[0])

        self.opt = tk.OptionMenu(self.info_frame, self.variable, *choices)
        self.opt.config(width=17, bg="white")
        self.opt.grid(row=2, column=1, padx=10, pady=10)

        self.lbl_gitPW = tk.Label(master=self.info_frame, text="GIT Password", width=10, height=1)
        self.lbl_gitPW.config(bg="#111111", fg="white", font=("Helvetica", 12))
        self.lbl_gitPW.grid(row=4, column=0, padx=10, pady=10)
        self.ent_gitPW = tk.Entry(master=self.info_frame, show="*", width=20, borderwidth=2)
        self.ent_gitPW.grid(row=4, column=1, padx=10, pady=10)
        self.lbl_pxePW = tk.Label(master=self.info_frame, text="PXE Password", width=10, height=1)
        self.lbl_pxePW.config(bg="#111111", fg="white", font=("Helvetica", 12))
        self.lbl_pxePW.grid(row=5, column=0, padx=10, pady=10)
        self.ent_pxePW = tk.Entry(master=self.info_frame, show="*", width=20, borderwidth=2)
        self.ent_pxePW.grid(row=5, column=1, padx=10, pady=10)
        self.zip = tk.IntVar()
        self.chkbox_zip = tk.Checkbutton(master=self.info_frame, text="Zip Results", variable=self.zip)
        self.chkbox_zip.config(bg="#111111", fg="white", font=("Helvetica", 12))
        self.chkbox_zip.grid(row=6, column=1)

        self.btn_submit = tk.Button(self.info_frame, text="Start!", width=15, height=2, command=self.submit_click)
        self.btn_submit.grid(row=7, column=0, columnspan=2, pady=5)

    def submit_click(self):
        self.important_info = {}
        if self.variable.get() == "Custom":
            self.important_info["pxe"] = self.ent_pxe.get()
        else:
            self.important_info["pxe"] = self.variable.get()
        self.important_info["rack_SN"] = self.ent_rackSN.get()
        self.important_info["gitpw"] = self.ent_gitPW.get()
        self.important_info["pxepw"] = self.ent_pxePW.get()
        self.important_info["zip"]=self.zip.get()
        self.txt_log_area.insert(tk.END, self.important_info)
        #fai.fai(self.important_info)

    # def custom_pxe(self):


root = tk.Tk()
log_gui(root)
root.mainloop()
