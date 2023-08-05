# from builtins import function
from tkinter import *
from tkinter import messagebox
import time, os, sys
from .config import config

Yzytk_windows = []
def where_data(filename) -> str:
    import os
    basepath = os.path.abspath(__file__)
    folder = os.path.dirname(basepath)
    data_path = os.path.join(folder, filename)
    return data_path


class Imgbutton(object):
    def __init__(self, root, command, width=100, img="", text="", **arg):
        import tkinter as tk
        import PIL.Image
        import PIL.ImageTk
        self.width = width
        if type(width) == type((1, 2, 3, 4)):
            self.img = PIL.ImageTk.PhotoImage(
                PIL.Image.open(img).resize(
                    width,
                    PIL.Image.ANTIALIAS
                )
            )
        else:
            self.img = PIL.ImageTk.PhotoImage(
                PIL.Image.open(img).resize(
                    (width, width),
                    PIL.Image.ANTIALIAS
                )
            )
        self.command = command
        self.Frame = tk.Frame(root,bg='white')
        self.Label = tk.Label(self.Frame,bg='white', text=text, image=self.img, compound="top", **arg)

        self.Label.pack(fill="both", expand=True)

        self.Label.bind("<Button-1>", self.click)

    def click(self, *w):
        self.command()

    def configure(self, **arg):
        self.Label.configure(**arg)

    def pack(self, *k, **K):
        self.Frame.pack(*k, **K)

    def bind(self, k, command):
        self.Label.bind(k, command)

    def reload(self, img):
        import PIL.Image
        import PIL.ImageTk
        width = self.width
        self.img = PIL.ImageTk.PhotoImage(
            PIL.Image.open(img).resize(
                (width, width),
                PIL.Image.ANTIALIAS
            )
        )
        self.Label.configure(image=self.img)


class Yzytk(Tk):
    def geometry(self, ww, wh):
        if 1:
            self.update()
            self.attributes("-alpha", 0.01)
            self.update()

            super().geometry("%dx%d+%d+%d" % (self.ww, self.wh, self.x, self.y))
    def __none(self):
        ...
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attributes('-alpha', 0.01)
        self.wait = 0
        # 初步
        if 1:
            if os.name == "nt":
                self.flag = True
            else:
                self.flag = False
            if self.flag:
                self.attributes('-topmost', True)
            if self.flag:
                self.overrideredirect(True)

        # 绑定部分业务逻辑及移动屏幕的逻辑
        if 1:
            self.update()
            self.protocol("WM_DELETE_WINDOW", self.DELETED_WINDOW)
            self.bind('<Escape>', self.DELETED_WINDOW)
            self.update()
            self.sw = self.winfo_screenwidth()
            # 得到屏幕宽度
            self.sh = self.winfo_screenheight()
            # 得到屏幕高度
            self.ww = 800
            self.wh = 500
            # 窗口宽高为100
            self.x = (self.sw - self.ww) / 2
            self.y = (self.sh - self.wh) / 2
            super().geometry("%dx%d+%d+%d" % (self.ww, self.wh, self.x, self.y))

            # 复杂一些
        if 1:
            self.vt = Frame(self,bg='white')

            self.vt_T = Imgbutton(self.vt, self.__none, (30, 30), where_data("img/icon.png"), text="")
            self._title = Label(self.vt, text="YzyTk",bg='white')

            self.vt_x = Imgbutton(self.vt, self.DELETED_WINDOW, 25, where_data("img/xo.png"), text="")
            self.vt__ = Imgbutton(self.vt, self.HIDDEN_WINDOW, 25, where_data("img/-o.png"), text="")

            self.vt_x.bind("<Enter>", self.cx)
            self.vt_x.bind("<Leave>", self.lx)

            self.vt__.bind("<Enter>", self.c_)
            self.vt__.bind("<Leave>", self.l_)

            self.vt_x.pack(side=RIGHT)
            self.vt__.pack(side=RIGHT)
            self.vt_T.pack(side=LEFT)
            self._title.pack(fill=X, side=LEFT)

            self.vt.pack(side=TOP, fill=X)
            self.update()
        # 绑定移动逻辑
        if 1:
            self.vt.bind("<B1-Motion>", self._move_window)
            self.vt.bind("<ButtonRelease-1>", self._xiufu_move)
            self.vt.bind("<Button-1>", self._xiufu_move_2)

        # ok
        self.attributes("-alpha", 1)
        self.update()
        Yzytk_windows.append(self)

    # 开始制造
    # overs hack
    # def i(self):
    #     self.attributes("-alpha", 0.01)
    #     self.attributes('-topmost', 0)
    #     self.overrideredirect(False)
    #     self.iconify()
    #     self.bind('<Map>', self.i_2)
    #
    # # self.iconbitmap("ico.ico")
    # def i_2(self, event, *w):
    #     self.attributes('-topmost', True)
    #     self.overrideredirect(True)
    #     time.sleep(0.1)
    #     self.attributes("-alpha", 1)
    #     self.unbind('<Map>')

    def nothing(self, *w):
        pass

    def cx(self, *w):
        self.vt_x.reload(where_data("img/x-.png"))

    def c_(self, *w):
        self.vt__.reload(where_data("img/--.png"))

    def lx(self, *w):
        self.vt_x.reload(where_data("img/xo.png"))

    def l_(self, *w):
        self.vt__.reload(where_data("img/-o.png"))

    def HIDDEN_WINDOW(self, *event):
        self.attributes('-alpha', 0.1)
        if self.flag:
            self.attributes('-topmost', False)
        if self.flag:
            self.overrideredirect(False)
        self.iconify()
        self.bind("<Enter>", self.SHOW_AGAIN)
        # self.bind("<Map>", self.SHOW_AGAIN)
        self.update()

    def SHOW_AGAIN(self, *event):
        self.unbind("<Enter>")
        self.focus_get()
        if self.flag:
            self.attributes('-topmost', True)
            self.update()
        if self.flag:
            self.overrideredirect(True)
            self.update()
        self.focus_get()
        self.attributes('-alpha', 1)
        self.update()

    def DELETED_WINDOW(self, *args, **kwargs):
        if config['closetip']:
            get = messagebox.askokcancel("", "确认退出吗？")
            if not get:
                return
        sys.exit()

    def _move_window(self, *event):
        click_x, click_y = event[0].x_root, event[0].y_root
        self.nx = click_x - self.tx
        self.ny = click_y - self.ty
        super().geometry("%dx%d+%d+%d" % (self.ww, self.wh, self.nx, self.ny))

    def _xiufu_move(self, *event):
        # self.x, y, ww, wh, tx, ty
        try:
            self.x, self.y = self.nx, self.ny
        except:
            # print("err")
            pass

    def _xiufu_move_2(self, *event):

        click_x, click_y = event[0].x_root, event[0].y_root
        # print(f"click x{click_x}|click y{click_y}-ex,ey={nx}{ny}")
        self.tx = click_x - self.x
        self.ty = click_y - self.y

    def center(root):
        # root=tk.Tk()
        root.update()
        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
        ww = root.winfo_width()
        wh = root.winfo_height()
        x = (sw - ww) / 2
        y = (sh - wh) / 2
        root.geometry("%dx%d+%d+%d" % (ww, wh, x, y))

    def jitter(root, times=3):
        import time
        root.update()
        root.focus_get()
        root.attributes('-topmost', True)
        time.sleep(0.1)
        root.update()
        ww = root.winfo_width()
        wh = root.winfo_height()
        wx = root.x
        wy = root.y

        for x in range(times):
            for y in (1, 2, 3, 4):
                root.update()
                if y == 1: wx += 10
                if y == 2: wy += 10
                if y == 3: wx -= 10
                if y == 4: wy -= 10
                super().geometry("%dx%d+%d+%d" % (ww, wh, wx, wy))
                time.sleep(0.05)
        return True

    def title(self, text=""):
        super().title(text)
        self._title.config(text=text)