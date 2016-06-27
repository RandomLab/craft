from Robot import Robot
import tkinter as tk
import time
import random
from UI.List import *
from Robot.classes import *
from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import osc_message_builder

from pythonosc import udp_client

import threading
import socket

from Entite.Base import Base

# Mise à jour du robit (en secondes)
ROBOT_UPDATE_TIME = 5
WIDTH = 200
HEIGHT = 500

player = os.getenv("USERNAME")
my_ip = socket.gethostbyname(socket.gethostname())
class App():
    def __init__(self):
        self.registered = False
        self.robot = Robot.Robot(secondes=ROBOT_UPDATE_TIME)
        #self.update_robot()
        self.dispatcher = dispatcher.Dispatcher()
        self.dispatcher.map("/clock", self.update_robot, "TEST")
        self.dispatcher.map("/hack", self.server_hack, "Hack")
        self.dispatcher.map("/player", self.get_player, "Player")

        self.server = osc_server.ThreadingOSCUDPServer(("0.0.0.0", 5005), self.dispatcher)
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.start()
        self.client = udp_client.UDPClient("255.255.255.255", 5006)
        if hasattr(socket,'SO_BROADCAST'):
            self.client._sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        print("Registering to server...")
        msg = osc_message_builder.OscMessageBuilder(address="/register")
        msg.add_arg(player)
        msg.add_arg(my_ip) #
        msg = msg.build()
        self.client.send(msg)
        print("Waiting for server")
        self.root = tk.Tk()

        self.root.geometry('{}x{}'.format(200, 500))
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        #self.canvas = tk.Canvas(width = WIDTH, height = HEIGHT)
        #self.canvas.pack()
        #i = tk.PhotoImage(file = "ressources/Ingenieur.png")
        #logo = tk.Label(image = i)
        #logo.image = i
        #logo.pack(side="top")

        #self.label = List(player, 0)
        #self.label.pack()
        self.players_label = []
        self.playerListBox = tk.Listbox()
        self.playerListBox.pack()
        self.playerListBox.insert(tk.END, player + " 0")
        self.root.mainloop()
    def get_player(self, unused_addr, args, player, score):
        print("Got player msg")
        if player not in self.players_label:
            self.playerListBox.insert(tk.END, player + " " + str(score))
            #tmp = List(player, score)
            #tmp.pack()
            self.players_label[player].append(tmp)

    def server_hack(self, unused_addr, args, user_name, bob):
        print("Got hack from server")
    def on_closing(self):
        print("Closing")
        self.server.shutdown()
        self.root.destroy()
    def update_robot(self, unused_addr, args):
        print("update robot")
        self.robot.run()
        score = Robot.count("Soja")
        self.playerListBox.delete(0, tk.END)
        self.playerListBox.insert(tk.END, player + " " + str(0))



        msg = osc_message_builder.OscMessageBuilder(address="/player")
        msg.add_arg(player)
        msg.add_arg(score) #
        msg = msg.build()
        self.client.send(msg)
        #self.root.after(self.robot.secondes * 1000, self.update_robot)


if __name__ == "__main__":
    #robot = Robot.Robot(secondes=5)
    # Robot(secondes=1)
    #robot.run()
    app = App()
