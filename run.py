from Robot import Robot
import tkinter as tk
import time
import random

class App():
    def __init__(self):
        self.robot = Robot.Robot(secondes=5)
        self.root = tk.Tk()
        #self.label = tk.Label(text="")
        #self.label.pack()
        self.canvas = tk.Canvas(width = 500, height = 200)
        self.canvas.pack()
        self.update_clock()
        self.update_robot()
        self.root.mainloop()

    def update_clock(self):
        now = time.strftime("%H:%M:%S")
        #self.label.configure(text=now)
        self.canvas.create_text(random.randrange(500), random.randrange(200), text = "Bonjour")
        self.root.after(1000, self.update_clock)


    def update_robot(self):
        print("update robot")
        self.robot.run()
        self.root.after(self.robot.secondes * 1000, self.update_robot)


if __name__ == "__main__":
    #robot = Robot.Robot(secondes=5)
    # Robot(secondes=1)
    #robot.run()
    app = App()
