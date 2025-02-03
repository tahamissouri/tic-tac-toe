# Filepath: C:\Users\taham\OneDrive\Documents\Ingescape\sandbox\engine\src\engine.py
import ingescape as igs

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Engine(metaclass=Singleton):
    def __init__(self):
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.current_turn = "X"
        self.x_ready=False
        self.o_ready=False
        self.winning_boxes = []
        igs.input_create("x_move", igs.STRING_T, None)
        igs.input_create("o_move", igs.STRING_T, None)
        igs.output_create("grille",igs.STRING_T,None)
        igs.observe_input("x_move", self.x_move_input_callback, self)
        igs.observe_input("o_move", self.o_move_input_callback, self)
        igs.output_create("last_move", igs.STRING_T, None)
        igs.output_create("game_result",igs.STRING_T,None)
        igs.input_create("ready",igs.STRING_T,None)
        igs.observe_input("ready",self.ready,self)
        igs.output_create("restart", igs.IMPULSION_T, None)
    def ready(self, iop_type, name, value_type, value, my_data):
        if value=='x' :
            self.x_ready=True
        elif value=='o':
            self.o_ready=True
        if(self.x_ready and self.o_ready):
            self.x_ready=False
            self.o_ready=False
            igs.service_call("Whiteboard","clear",(),"")
            igs.output_set_impulsion("restart")
            
             
    def is_valid_move(self, row, col):
        return 0 <= row < 3 and 0 <= col < 3 and self.board[row][col] == ""

    def make_move(self, player_symbol, row, col):
        if self.is_valid_move(row, col):
            self.board[row][col] = player_symbol
            move = f"{player_symbol},{row},{col}"
            igs.output_set_string("last_move", move)
            self.update_clients()
            return True
        return False

    def update_clients(self):
        winner = self.check_winner()
        board_state =   [1 if cell == "X" else 0 if cell == "O" else -1 for row in self.board for cell in row]
        
        igs.output_set_string("grille",f"{board_state},{[]}")
        if winner:
            self.board = [["" for _ in range(3)] for _ in range(3)]
            igs.output_set_string("grille",f"{board_state},{self.winning_boxes}")
            igs.output_set_string("game_result", f"{winner} wins!" if winner != "Draw" else "It's a draw!")


    def x_move_input_callback(self, iop_type, name, value_type, value, my_data):
        if self.current_turn == "X":
            row, col = map(int, value.split(","))
            if self.make_move("X", row, col):
                self.current_turn = "O"

    def o_move_input_callback(self, iop_type, name, value_type, value, my_data):
        if self.current_turn == "O":
            row, col = map(int, value.split(","))
            if self.make_move("O", row, col):
                self.current_turn = "X"
    def check_winner(self):
        # Reset winning boxes before each check
        self.winning_boxes = []

        # Check rows and columns
        for i in range(3):
            # Check rows
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != "":
                self.winning_boxes = [(i, 0), (i, 1), (i, 2)]
                return self.board[i][0]
            
            # Check columns
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != "":
                self.winning_boxes = [(0, i), (1, i), (2, i)]
                return self.board[0][i]

        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != "":
            self.winning_boxes = [(0, 0), (1, 1), (2, 2)]
            return self.board[0][0]
        
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != "":
            self.winning_boxes = [(0, 2), (1, 1), (2, 0)]
            return self.board[0][2]

        # Check for a draw (no empty spaces left)
        if all(self.board[row][col] != "" for row in range(3) for col in range(3)):
            return "Draw"

        return None  # No winner yet

