import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename
import pickle
from virtualCube import *
from cube3D import *
from net import *

class CubeInterface(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.cube = VirtualCube()

        self.frame = tk.Frame(self, padx=2, pady=2)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)

        self.panes = ttk.PanedWindow(self.frame, orient=tk.HORIZONTAL)
        self.panes.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

        self.left = tk.Frame(self.panes, bd=5, relief=tk.SUNKEN)
        self.panes.add(self.left, weight=1)
        
        self.cube3D = Cube3D(self.left, self.cube)
        self.cube3D.pack(fill=tk.BOTH, expand=True)

        self.right = tk.Frame(self.panes, bd=5, relief=tk.SUNKEN)
        self.panes.add(self.right, weight=1)

        self.net = Net(self.right, self.cube, colours=self.cube3D.colours)
        self.net.pack(fill=tk.BOTH, expand=True)

        self.entry = tk.Entry(self.frame)
        self.entry.grid(row=1, column=0, columnspan=2, sticky="nsew",
                        padx=2, pady=2)
        self.entry.bind("<Return>", self.algorithm)
        self.entry.focus_force()

        self.cube.config(command=self.draw)
        self.bind("<Configure>", self.draw)
        self.draw()

        self.bind("<Left>", self.cube3D.callback)
        self.bind("<Right>", self.cube3D.callback)
        self.bind("<Up>", self.cube3D.callback)
        self.bind("<Down>", self.cube3D.callback)

        self.bind("<Control-a>", self.cube3D.toggleAnimate)
        self.bind("<Control-r>", self.cube3D.resetView)

    def draw(self, *args, **kwargs):
        self.cube3D.draw()
        self.net.draw()

    def algorithm(self, alg):
        alg = self.entry.get()
        algCopy = alg.upper()
        if "RESET" in algCopy:
            self.cube.reset()
        elif "SCRAMBLE" in algCopy:
            self.cube.scramble()
        else:
            try:
                self.cube.algorithm(alg)
            except AlgorithmError:
                self.entry.delete(0, tk.END)
                raise
        self.entry.delete(0, tk.END)

    def openFile(self, *args, **kwargs):
        if "filename" in kwargs.keys():
            filename = kwargs.pop("filename")
        else:
            filename = askopenfilename(parent=self,
                                       filetypes=[("Rubik's Cube", "*.cube")],
                                       defaultextension=".cube")

        if filename != "":
            with open(filename, "rb") as f:
                self.cube.tiles = pickle.load(f)

            self.draw()

    def saveAsFile(self, *args, **kwargs):
        if "filename" in kwargs.keys():
            filename = kwargs.pop("filename")
        else:
            filename = asksaveasfilename(parent=self,
                                         filetypes=[("Rubik's Cube", "*.cube")],
                                         defaultextension=".cube")
        
        if filename != "":
            with open(filename, "wb") as f:
                pickle.dump(self.cube.tiles, f)

    def export3DCubeAsImage(self, *args, **kwargs):
        if "filename" in kwargs.keys():
            filename = kwargs.pop("filename")
        else:
            filename = asksaveasfilename(parent=self, initialdir="images",
                                         filetypes=[("PNG Image", "*.png"),
                                                    ("JPEG Image", "*.jpg")],
                                         defaultextension=".png")

        if filename != "":
            self.cube3D.draw(filename=filename)

    def exportNetAsImage(self, *args, **kwargs):
        if "filename" in kwargs.keys():
            filename = kwargs.pop("filename")
        else:
            filename = asksaveasfilename(parent=self, initialdir="images",
                                         filetypes=[("PNG Image", "*.png"),
                                                    ("JPEG Image", "*.jpg")],
                                         defaultextension=".png")

        if filename != "":
            self.net.draw(filename=filename)

class Menubar(tk.Menu):
    def __init__(self, parent, *args, **kwargs):
        tk.Menu.__init__(self, *args, master=parent, **kwargs)
        self.master.config(menu=self)

        self.exportmenu = tk.Menu(self, tearoff=False)
        self.exportmenu.add_command(label="Export 3D Cube As...",
                                    command=self.master.export3DCubeAsImage)
        self.exportmenu.add_command(label="Export Net As...",
                                    command=self.master.exportNetAsImage)

        self.filemenu = tk.Menu(self, tearoff=False)
        self.filemenu.add_command(label="Open...",
                                  command=self.master.openFile,
                                  accelerator="Ctrl+O")
        self.filemenu.add_command(label="Save As...",
                                  command=self.master.saveAsFile,
                                  accelerator="Ctrl+S")
        self.filemenu.add_cascade(label="Export As...", menu=self.exportmenu)
        self.add_cascade(label="File", menu=self.filemenu)

        self.master.bind("<Control-o>", self.master.openFile)
        self.master.bind("<Control-s>", self.master.saveAsFile)

# ----------------------------------- Test -----------------------------------

if __name__ == "__main__":
    root = CubeInterface()
    root.title("Cube Interface")

    menubar = Menubar(root)
    
    root.mainloop()
