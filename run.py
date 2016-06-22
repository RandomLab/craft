from Robot import Robot
import tkinter as tk
import time
import random
from UI.List import *
from Robot.classes import *
# Mise à jour du robit (en secondes)
ROBOT_UPDATE_TIME = 5
WIDTH = 200
HEIGHT = 500

player = os.getenv("USERNAME")

class App():
    def __init__(self):
        self.robot = Robot.Robot(secondes=ROBOT_UPDATE_TIME)
        self.root = tk.Tk()
        #self.canvas = tk.Canvas(width = WIDTH, height = HEIGHT)
        #self.canvas.pack()
        i = tk.PhotoImage(file = "ressources/Ingenieur.png")
        logo = tk.Label(image = i)
        logo.image = i
        logo.pack(side="top")

        self.label = List(player, 0)
        self.label.pack()
        self.update_clock()
        self.update_robot()
        self.root.mainloop()

    def update_clock(self):
        now = time.strftime("%H:%M:%S")
        #self.canvas.create_text(random.randrange(WIDTH), random.randrange(HEIGHT), text = "Bonjour")
        self.root.after(1000, self.update_clock)


    def update_robot(self):
        print("update robot")
        self.robot.run()
        print(len(Robot.find(Arme)))

        self.label.configure(score = len(Robot.find(Arme)))


        self.root.after(self.robot.secondes * 1000, self.update_robot)


if __name__ == "__main__":
    #robot = Robot.Robot(secondes=5)
    # Robot(secondes=1)
    #robot.run()
    app = App()
