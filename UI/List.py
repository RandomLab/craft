import tkinter as tk



class List(tk.Frame):
    def __init__(self, player_name, score):
        tk.Frame.__init__(self)
        self.player = player_name
        self.score = score
        self.player_label = tk.Label(text = player_name)
        self.score_label = tk.Label(text = score)

        self.player_label.pack(side="left")
        self.score_label.pack(side="right")

    def configure(self, score = 0):
        self.score_label.configure(text = score)
