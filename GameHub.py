import tkinter as tk
from subprocess import Popen
from Pong import game as pong_main
from DodgeObstacles import game as dodge_obstacles_main
from TicTacToe import game as tic_tac_toe_main
from FlappyBird import game as flappy_bird_main

class GameLauncher:
    def __init__(self, master):
        self.master = master
        master.title("Game Hub")
        
        # Set the size of the window (width x height)
        master.state("zoomed")  # Maximize the window

        # Create buttons for each game
        self.create_button("Pong", pong_main)
        self.create_button("Dodge Obstacles", dodge_obstacles_main)
        self.create_button("Tic-Tac-Toe", tic_tac_toe_main)
        self.create_button("Flappy Bird", flappy_bird_main)

    def create_button(self, text, script):
        button = tk.Button(self.master, text=text, command=lambda: self.launch_game(script))
        button.pack(pady=10)

    def launch_game(self, game_function):
        game_function()

if __name__ == "__main__":
    root = tk.Tk()
    app = GameLauncher(root)
    root.mainloop()
