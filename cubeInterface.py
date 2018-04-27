import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from virtualCube import *
from cube3D import *
from net import *

class CubeInterface(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Untitled - Rubik's Cube Simulator")
        self.wm_iconbitmap("images/logo.ico")
            
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

    def newFile(self, *args, **kwargs):
        self.cube.reset()
        self.draw()
        
        title = "Untitled - " + self.title().split(" - ")[1]
        self.title(title)

    def openFile(self, *args, **kwargs):
        if "filename" in kwargs.keys():
            filename = kwargs.pop("filename")
        else:
            filename = askopenfilename(parent=self, initialdir="data",
                                       filetypes=[("Rubik's Cube", "*.cube")],
                                       defaultextension=".cube")

        if filename != "":
            self.cube.load(filename)

            self.draw()

            title = self.title().split(" - ")[1]
            if "\\" in filename:
                title = "{} - {}".format(
                    filename.split("\\")[-1].replace(".cube", ""), title)
            else:
                title = "{} - {}".format(
                    filename.split("/")[-1].replace(".cube", ""), title)
            self.title(title)

    def saveAsFile(self, *args, **kwargs):
        if "filename" in kwargs.keys():
            filename = kwargs.pop("filename")
        else:
            filename = asksaveasfilename(parent=self, initialdir="data",
                                         filetypes=[("Rubik's Cube", "*.cube")],
                                         defaultextension=".cube")
        
        if filename != "":
            self.cube.dump(filename)

            title = self.title().split(" - ")[1]
            if "\\" in filename:
                title = "{} - {}".format(
                    filename.split("\\")[-1].replace(".cube", ""), title)
            else:
                title = "{} - {}".format(
                    filename.split("/")[-1].replace(".cube", ""), title)
            self.title(title)

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

    def scramble(self, *args, **kwargs):
        self.cube.scramble()

    def reset(self, *args, **kwargs):
        self.cube.reset()

    def resetView(self, *args, **kwargs):
        self.cube3D.resetView()

    def toggleAnimate(self, *args, **kwargs):
        self.cube3D.toggleAnimate()

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
        self.filemenu.add_command(label="New File", command=self.master.newFile,
                                  accelerator="Ctrl+N")
        self.filemenu.add_command(label="Open...",
                                  command=self.master.openFile,
                                  accelerator="Ctrl+O")
        self.filemenu.add_command(label="Save As...",
                                  command=self.master.saveAsFile,
                                  accelerator="Ctrl+S")
        self.filemenu.add_cascade(label="Export As...", menu=self.exportmenu)
        self.add_cascade(label="File", menu=self.filemenu)

        self.optionsmenu = tk.Menu(self, tearoff=False)
        self.optionsmenu.add_command(label="Scramble",
                                     command=self.master.scramble)
        self.optionsmenu.add_command(label="Reset", command=self.master.reset)
        self.optionsmenu.add_command(label="Reset View", accelerator="Ctrl+R",
                                     command=self.master.resetView)
        self.optionsmenu.add_command(label="Animation", accelerator="Ctrl+A",
                                     command=self.master.toggleAnimate)
        self.add_cascade(label="Options", menu=self.optionsmenu)

        self.master.bind("<Control-n>", self.master.newFile)
        self.master.bind("<Control-o>", self.master.openFile)
        self.master.bind("<Control-s>", self.master.saveAsFile)

# ----------------------------------- Test -----------------------------------

if __name__ == "__main__":
    root = CubeInterface()
    root.state("zoomed")

    menubar = Menubar(root)
    
    root.mainloop()
