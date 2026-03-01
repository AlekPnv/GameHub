import tkinter as tk
from tkinter import messagebox
import subprocess
import random
import sys
import os

_DIR = os.path.dirname(os.path.abspath(__file__))

class GameHub(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Game Hub")
        self.geometry("420x400")

        button_font = ("Helvetica", 14)
        button_fg   = "#FFFFFF"

        tk.Button(self, text="Connect 4",      command=self.connect_4,      font=button_font, bg="blue",    fg=button_fg).place(x=50,  y=50,  width=150, height=50)
        tk.Button(self, text="Cookie Clicker", command=self.cookie_clicker, font=button_font, bg="#9C661F", fg=button_fg).place(x=220, y=50,  width=150, height=50)
        tk.Button(self, text="Flappy Bird",    command=self.flappy_bird,    font=button_font, bg="#DFFF00", fg="black")  .place(x=50,  y=110, width=150, height=50)
        tk.Button(self, text="2048",           command=self.game_2048,      font=button_font, bg="#FCE6C9", fg="black")  .place(x=220, y=110, width=150, height=50)
        tk.Button(self, text="Ping Pong",      command=self.ping_pong,      font=button_font, bg="black",   fg=button_fg).place(x=50,  y=170, width=150, height=50)
        tk.Button(self, text="RPS",            command=self.RPS,            font=button_font, bg="#808080", fg=button_fg).place(x=220, y=170, width=150, height=50)
        tk.Button(self, text="Snake",          command=self.snake,          font=button_font, bg="#00FF00", fg="black")  .place(x=50,  y=230, width=150, height=50)
        tk.Button(self, text="Tic Tac Toe",    command=self.tic_tac_toe,    font=button_font, bg="#E3CF57", fg="black")  .place(x=220, y=230, width=150, height=50)
        tk.Button(self, text="Random Game",    command=self.random_game,    font=button_font, bg="purple",  fg=button_fg).place(x=50,  y=290, width=150, height=50)
        tk.Button(self, text="Quit",           command=self.quit,           font=button_font, bg="red",     fg=button_fg).place(x=220, y=290, width=150, height=50)

    def _run(self, script):
        subprocess.call([sys.executable, os.path.join(_DIR, script)])

    def connect_4(self):      self._run(os.path.join("Connect_4",   "Connect_4.py"))
    def cookie_clicker(self): self._run(os.path.join("Cookie_Clicker","Cookie_Clicker.py"))
    def flappy_bird(self):    self._run(os.path.join("Flappy_Bird",  "Flappy_Bird.py"))
    def game_2048(self):      self._run(os.path.join("Game_2048",    "Game_2048.py"))
    def ping_pong(self):      self._run(os.path.join("Ping_Pong",    "Ping_Pong.py"))
    def RPS(self):            self._run(os.path.join("RPS",          "Rock_Paper_Scissors.py"))
    def snake(self):          self._run(os.path.join("Snake",        "Snake.py"))
    def tic_tac_toe(self):    self._run(os.path.join("Tic_Tac_Toe",  "Tic_Tac_Toe.py"))

    def random_game(self):
        random.choice([
            self.connect_4, self.cookie_clicker, self.flappy_bird, self.game_2048,
            self.ping_pong, self.RPS, self.snake, self.tic_tac_toe
        ])()

    def quit(self):
        if messagebox.askokcancel("Quit", "Are you sure you want to quit?"):
            self.destroy()

if __name__ == "__main__":
    GameHub().mainloop()
