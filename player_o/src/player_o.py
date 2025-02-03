import ingescape as igs
import tkinter as tk
from tkinter import messagebox

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class PlayerO(metaclass=Singleton):
    def __init__(self, player_symbol="O"):
        self.player_symbol = player_symbol
        self.root = tk.Tk()
        self.root.title(f"Tic-Tac-Toe: Player {self.player_symbol}")
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        
        for row in range(3):
            for col in range(3):
                btn = tk.Button(self.root, text="", font=("Arial", 24), height=2, width=4,
                                command=lambda r=row, c=col: self.make_move(r, c))
                btn.grid(row=row, column=col)
                self.buttons[row][col] = btn

        self.restart_btn = None  # Store the restart button reference

        igs.output_create("restart_request", igs.STRING_T, None)
        igs.input_create("restart", igs.IMPULSION_T, None)
        igs.observe_input("restart", self.restart_game, None)

        igs.input_create("game_result", igs.STRING_T, None)
        igs.input_create("last_move", igs.STRING_T, None)
        igs.observe_input("game_result", self.game_finished, None)
        igs.observe_input("last_move", self.on_last_move, None)
        igs.output_create("o_move", igs.STRING_T, None)

    def make_move(self, row, col):
        if self.buttons[row][col]["text"] == "":
            move = f"{row},{col}"
            igs.output_set_string("o_move", move)

    def on_last_move(self, iop_type, name, value_type, value, my_data):
        player, row, col = value.split(",")
        row, col = int(row), int(col)
        self.buttons[row][col]["text"] = player
        self.buttons[row][col].config(state="disabled")

    def game_finished(self, iop_type, name, value_type, value, my_data):
        messagebox.showinfo("Game Over", value)
        
        for row in self.buttons:
            for btn in row:
                btn.config(state="disabled")  # Disable all buttons to prevent further moves

        # Add and store the restart button
        self.restart_btn = tk.Button(self.root, text="Restart", font=("Arial", 16), command=self.request_restart)
        self.restart_btn.grid(row=3, column=1)  # Positioning the restart button

    def request_restart(self):
        igs.output_set_string("restart_request",'o')


    def restart_game(self, iop_type=None, name=None, value_type=None, value=None, my_data=None):
        # Reset the game logic and clear all buttons
        for row in self.buttons:
            for btn in row:
                btn.config(state="normal", text="")  # Enable buttons and clear text

        # Remove restart button if it exists
        if self.restart_btn:
            self.restart_btn.destroy()
            self.restart_btn = None  # Reset reference

        # Remove restart button if it exists
        if self.restart_btn:
            self.restart_btn.destroy()
            self.restart_btn = None  # Reset reference

    def run(self):
        self.root.mainloop()
