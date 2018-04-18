import tkinter as tk
from virtualCube import *

class Net(tk.Canvas):
    def __init__(self, parent, cube, *args, **kwargs):
        if "colours" in kwargs.keys():
            self.colours = kwargs.pop("colours")
        else:
            self.colours = {"w": "#FFFFFF", "y": "#FFFF00", "r": "#FF0000",
                            "o": "#FFA500", "g": "#00A000", "b": "#0000FF"}
            
        tk.Canvas.__init__(self, *args, master=parent, **kwargs)
        self.cube = cube

        self.master.bind("<Configure>", self.draw)
        self.draw()

    def draw(self, *args, **kwargs):
        self.delete("all")
        
        width = self.winfo_width()
        height = self.winfo_height()

        x = width/2
        y = height/2

        if width/3 < height/4:
            l = width/9 - height/100
        else:
            l = height/12 - height/100

        rows = str(self.cube).split("\n")

        for r in range(3):
            for c in range(3):
                points = [l*(1.5-c)+x, l*(r-6)+y,
                          l*(0.5-c)+x, l*(r-6)+y,
                          l*(0.5-c)+x, l*(r-5)+y,
                          l*(1.5-c)+x, l*(r-5)+y]
                colour = self.colours[self.cube.tiles[1][1][2-r][c]]
                self.create_polygon(points, outline="black", fill=colour,
                                    width=2)

                points = [l*(c-4.5)+x, l*(r-3)+y,
                          l*(c-3.5)+x, l*(r-3)+y,
                          l*(c-3.5)+x, l*(r-2)+y,
                          l*(c-4.5)+x, l*(r-2)+y]
                colour = self.colours[self.cube.tiles[2][0][2-c][r]]
                self.create_polygon(points, outline="black", fill=colour,
                                    width=2)

                points = [l*(c-1.5)+x, l*(r-3)+y,
                          l*(c-0.5)+x, l*(r-3)+y,
                          l*(c-0.5)+x, l*(r-2)+y,
                          l*(c-1.5)+x, l*(r-2)+y]
                colour = self.colours[self.cube.tiles[0][0][r][c]]
                self.create_polygon(points, outline="black", fill=colour,
                                    width=2)

                points = [l*(c+1.5)+x, l*(r-3)+y,
                          l*(c+2.5)+x, l*(r-3)+y,
                          l*(c+2.5)+x, l*(r-2)+y,
                          l*(c+1.5)+x, l*(r-2)+y]
                colour = self.colours[self.cube.tiles[2][1][c][2-r]]
                self.create_polygon(points, outline="black", fill=colour,
                                    width=2)

                points = [l*(c-1.5)+x, l*r+y,
                          l*(c-0.5)+x, l*r+y,
                          l*(c-0.5)+x, l*(r+1)+y,
                          l*(c-1.5)+x, l*(r+1)+y]
                colour = self.colours[self.cube.tiles[1][0][r][c]]
                self.create_polygon(points, outline="black", fill=colour,
                                    width=2)

                points = [l*(c-1.5)+x, l*(r+3)+y,
                          l*(c-0.5)+x, l*(r+3)+y,
                          l*(c-0.5)+x, l*(r+4)+y,
                          l*(c-1.5)+x, l*(r+4)+y]
                colour = self.colours[self.cube.tiles[0][1][2-r][c]]
                self.create_polygon(points, outline="black", fill=colour,
                                    width=2)

# ----------------------------------- Test -----------------------------------

if __name__ == "__main__":
    def algorithm(*args, **kwargs):
        alg = entry.get()
        algCopy = alg.upper()
        if "RESET" in algCopy:
            cube.reset()
        elif "SCRAMBLE" in algCopy:
            cube.scramble()
        else:
            try:
                cube.algorithm(alg)
            except AlgorithmError:
                entry.delete(0, tk.END)
                raise
        entry.delete(0, tk.END)
        
    root = tk.Tk()
    root.title("Net")

    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    cube = VirtualCube()
    cube.algorithm("U L F2")
    net = Net(root, cube)
    cube.config(command=net.draw)
    net.grid(row=0, column=0, sticky="nsew")

    entry = tk.Entry(root)
    entry.grid(row=1, column=0, sticky="nsew")
    entry.bind("<Return>", algorithm)
    entry.focus_force()

    root.mainloop()
