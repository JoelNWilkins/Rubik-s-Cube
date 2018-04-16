import tkinter as tk
import numpy as np
from virtualCube import *

class Cube3D(tk.Canvas):
    colours = {"w": "#FFFFFF", "y": "#FFFF00", "r": "#FF0000",
               "o": "#FF8C00", "g": "#00FF00", "b": "#0000FF"}
    
    def __init__(self, parent, cube, *args, **kwargs):
        if "command" in kwargs.keys():
            self.command = kwargs.pop("command")
        else:
            self.command = None
        if "invert" in kwargs.keys():
            self.invert = kwargs.pop("invert")
        else:
            self.invert = False
            
        tk.Canvas.__init__(self, *args, master=parent, **kwargs)
        self.cube = cube

        self.phi = np.pi/4
        self.theta = np.pi/4

        self.bind("<Configure>", self.draw)
        self.master.bind("<Left>", self.callback)
        self.master.bind("<Right>", self.callback)
        self.master.bind("<Up>", self.callback)
        self.master.bind("<Down>", self.callback)

        self.master.bind("<Button-1>", self.press)
        self.master.bind("<ButtonRelease-1>", self.release)
        self.master.bind("<B1-Motion>", self.drag)
        
        self.draw()

    def press(self, event):
        self.click = True
        self.x = event.x
        self.y = event.y

    def release(self, event):
        self.click = False

    def drag(self, event):
        if self.click:
            self.phi += (event.y - self.y) / (7.5*self.winfo_height())
            self.theta -= (event.x - self.x) / (7.5*self.winfo_width())

        self.phi %= 2*np.pi
        self.theta %= 2*np.pi

        self.draw()

    def callback(self, event):
        if event.keysym == "Left":
            if self.invert:
                self.theta -= np.pi/32
            else:
                self.theta += np.pi/32
        elif event.keysym == "Right":
            if self.invert:
                self.theta += np.pi/32
            else:
                self.theta -= np.pi/32
        elif event.keysym == "Up":
            if self.invert:
                self.phi += np.pi/32
            else:
                self.phi -= np.pi/32
        elif event.keysym == "Down":
            if self.invert:
                self.phi -= np.pi/32
            else:
                self.phi += np.pi/32

        self.phi %= 2*np.pi
        self.theta %= 2*np.pi

        self.draw()

        if self.command != None:
            self.command(event)

    def transform(self, point, phi, theta):
        alpha = np.arctan2(point[2], point[0])
        l = np.sqrt(point[0]**2 + point[2]**2)
        x = l * np.cos(alpha + theta)
        z = l * np.sin(alpha + theta)

        beta = np.arctan2(point[1], z)
        l = np.sqrt(point[1]**2 + z**2)
        y = l * np.sin(beta + phi)
        z = -l * np.cos(beta + phi)
        
        return (round(x, 10), round(y, 10), round(z, 10))

    def draw(self, *args, **kwargs):
        self.delete("all")

        width = self.winfo_width()
        height = self.winfo_height()
        
        x = width/2
        y = height/2
        
        if width < height:
            l = width/6
        else:
            l = height/6

        if (self.transform((0, -1, 0), self.phi, self.theta)[2]
            < self.transform((0, 1, 0), self.phi, self.theta)[2]):
            for r in range(3):
                for c in range(3):
                    point1 = self.transform((l*(c-1.5), l*(-1.5), l*(r-1.5)),
                                            self.phi, self.theta)
                    point2 = self.transform((l*(c-1.5), l*(-1.5), l*(r-0.5)),
                                            self.phi, self.theta)
                    point3 = self.transform((l*(c-0.5), l*(-1.5), l*(r-0.5)),
                                            self.phi, self.theta)
                    point4 = self.transform((l*(c-0.5), l*(-1.5), l*(r-1.5)),
                                            self.phi, self.theta)
                    points = [point1[0]+x, point1[1]+y,
                              point2[0]+x, point2[1]+y,
                              point3[0]+x, point3[1]+y,
                              point4[0]+x, point4[1]+y]
                    colour = self.colours[self.cube.tiles[0][0][r][c]]
                    self.create_polygon(points, outline="black", fill=colour,
                                        width=2)
        else:
            for r in range(3):
                for c in range(3):
                    point1 = self.transform((l*(c-1.5), l*1.5, l*(r-1.5)),
                                            self.phi, self.theta)
                    point2 = self.transform((l*(c-1.5), l*1.5, l*(r-0.5)),
                                            self.phi, self.theta)
                    point3 = self.transform((l*(c-0.5), l*1.5, l*(r-0.5)),
                                            self.phi, self.theta)
                    point4 = self.transform((l*(c-0.5), l*1.5, l*(r-1.5)),
                                            self.phi, self.theta)
                    points = [point1[0]+x, point1[1]+y,
                              point2[0]+x, point2[1]+y,
                              point3[0]+x, point3[1]+y,
                              point4[0]+x, point4[1]+y]
                    colour = self.colours[self.cube.tiles[0][1][r][c]]
                    self.create_polygon(points, outline="black", fill=colour,
                                        width=2)

        if (self.transform((0, 0, 1), self.phi, self.theta)[2]
            < self.transform((0, 0, -1), self.phi, self.theta)[2]):
            for r in range(3):
                for c in range(3):
                    point1 = self.transform((l*(c-1.5), l*(r-1.5), l*1.5),
                                            self.phi, self.theta)
                    point2 = self.transform((l*(c-1.5), l*(r-0.5), l*1.5),
                                            self.phi, self.theta)
                    point3 = self.transform((l*(c-0.5), l*(r-0.5), l*1.5),
                                            self.phi, self.theta)
                    point4 = self.transform((l*(c-0.5), l*(r-1.5), l*1.5),
                                            self.phi, self.theta)
                    points = [point1[0]+x, point1[1]+y,
                              point2[0]+x, point2[1]+y,
                              point3[0]+x, point3[1]+y,
                              point4[0]+x, point4[1]+y]
                    colour = self.colours[self.cube.tiles[1][0][r][c]]
                    self.create_polygon(points, outline="black", fill=colour,
                                        width=2)
        else:
            for r in range(3):
                for c in range(3):
                    point1 = self.transform((l*(1.5-c), l*(r-1.5), l*(-1.5)),
                                            self.phi, self.theta)
                    point2 = self.transform((l*(1.5-c), l*(r-0.5), l*(-1.5)),
                                            self.phi, self.theta)
                    point3 = self.transform((l*(0.5-c), l*(r-0.5), l*(-1.5)),
                                            self.phi, self.theta)
                    point4 = self.transform((l*(0.5-c), l*(r-1.5), l*(-1.5)),
                                            self.phi, self.theta)
                    points = [point1[0]+x, point1[1]+y,
                              point2[0]+x, point2[1]+y,
                              point3[0]+x, point3[1]+y,
                              point4[0]+x, point4[1]+y]
                    colour = self.colours[self.cube.tiles[1][1][r][c]]
                    self.create_polygon(points, outline="black", fill=colour,
                                        width=2)

        if (self.transform((-1, 0, 0), self.phi, self.theta)[2]
            < self.transform((1, 0, 0), self.phi, self.theta)[2]):
            for r in range(3):
                for c in range(3):
                    point1 = self.transform((l*(-1.5), l*(r-1.5), l*(c-1.5)),
                                            self.phi, self.theta)
                    point2 = self.transform((l*(-1.5), l*(r-1.5), l*(c-0.5)),
                                            self.phi, self.theta)
                    point3 = self.transform((l*(-1.5), l*(r-0.5), l*(c-0.5)),
                                            self.phi, self.theta)
                    point4 = self.transform((l*(-1.5), l*(r-0.5), l*(c-1.5)),
                                            self.phi, self.theta)
                    points = [point1[0]+x, point1[1]+y,
                              point2[0]+x, point2[1]+y,
                              point3[0]+x, point3[1]+y,
                              point4[0]+x, point4[1]+y]
                    colour = self.colours[self.cube.tiles[2][0][r][c]]
                    self.create_polygon(points, outline="black", fill=colour,
                                        width=2)
        else:
            for r in range(3):
                for c in range(3):
                    point1 = self.transform((l*1.5, l*(r-1.5), l*(1.5-c)),
                                            self.phi, self.theta)
                    point2 = self.transform((l*1.5, l*(r-1.5), l*(0.5-c)),
                                            self.phi, self.theta)
                    point3 = self.transform((l*1.5, l*(r-0.5), l*(0.5-c)),
                                            self.phi, self.theta)
                    point4 = self.transform((l*1.5, l*(r-0.5), l*(1.5-c)),
                                            self.phi, self.theta)
                    points = [point1[0]+x, point1[1]+y,
                              point2[0]+x, point2[1]+y,
                              point3[0]+x, point3[1]+y,
                              point4[0]+x, point4[1]+y]
                    colour = self.colours[self.cube.tiles[2][1][r][c]]
                    self.create_polygon(points, outline="black", fill=colour,
                                        width=2)

if __name__ == "__main__":
    def algorithm(self, *args, **kwargs):
        alg = entry.get().upper()
        if "RESET" in alg:
            cube.reset()
        elif "SCRAMBLE" in alg:
            cube.scramble()
        else:
            cube.algorithm(alg)
        entry.delete(0, tk.END)
        cube3D.draw()

    root = tk.Tk()
    root.title("3D Cube")

    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    cube = VirtualCube()
    cube3D = Cube3D(root, cube)
    cube3D.grid(row=0, column=0, sticky="nsew")

    entry = tk.Entry(root)
    entry.grid(row=1, column=0, sticky="nsew")
    entry.bind("<Return>", algorithm)
    entry.focus_force()

    root.mainloop()
