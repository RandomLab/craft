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
from pymsgbox import alert

from Entite.Base import Base

from config import player_name

# Mise à jour du robit (en secondes)
ROBOT_UPDATE_TIME = 5
WIDTH = 200
HEIGHT = 500


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

        self.server = osc_server.ThreadingOSCUDPServer(("0.0.0.0", 5006), self.dispatcher)
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.start()
        self.to_server_client = udp_client.UDPClient("255.255.255.255", 5005)
        self.to_client_client = udp_client.UDPClient("255.255.255.255", 5006)

        if hasattr(socket,'SO_BROADCAST'):
            self.to_server_client._sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        if hasattr(socket,'SO_BROADCAST'):
            self.to_client_client._sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        print("Registering to server...")
        msg = osc_message_builder.OscMessageBuilder(address="/register")
        msg.add_arg(player_name)
        msg.add_arg(my_ip) #
        msg = msg.build()
        self.to_server_client.send(msg)
        print("Waiting for server")
        self.root = tk.Tk()

        self.root.geometry('{}x{}'.format(200, 500))
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.players_list = {}
        self.playerListBox = tk.Listbox()
        self.playerListBox.pack()
        self.playerListBox.insert(tk.END, player_name + " 0")
        self.root.mainloop()
    def get_player(self, unused_addr, args, player, score):
        print("Got player msg")
        if player not in self.players_list and player != player_name:
            self.playerListBox.insert(tk.END, player + " " + str(score))
            self.players_list[player] = score

    def server_hack(self, unused_addr, args):
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
        self.playerListBox.insert(tk.END, player_name + " " + str(score))
        for p in self.players_list:
            self.playerListBox.insert(tk.END, p + " " + str(self.players_list[p]))

        msg = osc_message_builder.OscMessageBuilder(address="/player")
        msg.add_arg(player_name)
        msg.add_arg(score) #
        msg = msg.build()
        self.to_client_client.send(msg)

        if self.robot.win:
            # I am the winner
            # lets tel that to ohters
            msg = osc_message_builder.OscMessageBuilder(address="/winner")
            msg.add_arg(player_name)
            msg.add_arg(score)
            msg = msg.build()
            #self.to_client_client.send(msg)
            self.to_server_client.send(msg)
            rep = alert(text = "Vous avez gagné la partie !")
            self.on_closing()

        #self.root.after(self.robot.secondes * 1000, self.update_robot)


if __name__ == "__main__":
    #robot = Robot.Robot(secondes=5)
    # Robot(secondes=1)
    #robot.run()
    app = App()
