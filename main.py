#!/usr/bin/python3
# @File: daka.py
# --coding: utf-8--
# @Author: 昊昊反思
# @Time: 2022年 03月 30日 11:55
"""
说明:
"""
import tkinter as tk
from PIL import ImageTk,Image
import daka_chrome

class Menu():
    def __init__(self,root):
        self.root = root
        tk.Label(self.root,text="账户").place(relx=0,rely=0)
        tk.Label(self.root,text="密码").place(relx=0,rely=0.2)
        self.name = tk.Entry(self.root)
        self.name.place(relx=0.15,rely=0)
        self.pwd = tk.Entry(self.root,show="*")
        self.pwd.place(relx=0.15,rely=0.2)
        tk.Button(root,text="打卡",command=self.daka).place(relx=0.5,rely=0.5)

    def daka(self):
        name = self.name.get()
        pwd = self.pwd.get()
        daka_chrome.Daka(name,pwd)


if __name__ == '__main__':
    root = tk.Tk()
    root.resizable(0,0)
    root.geometry("200x100")
    root.title("江苏大学打卡系统")
    Menu(root)
    root.mainloop()
