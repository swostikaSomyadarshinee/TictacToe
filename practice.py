import tkinter as tk
from tkinter import messagebox
import random

class PlayerNamesDialog:
    def __init__(self, parent, mode):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Enter Player Names")
        self.dialog.geometry("400x250")
        self.dialog.resizable(False, False)
        
        self.player1_name = tk.StringVar()
        self.player2_name = tk.StringVar()

        tk.Label(self.dialog, text="Player 1 (X):").pack(pady=5)
        self.entry1 = tk.Entry(self.dialog, textvariable=self.player1_name)
        self.entry1.pack(pady=5)
        
        if mode == "PvP":
            tk.Label(self.dialog, text="Player 2 (O):").pack(pady=5)
            self.entry2 = tk.Entry(self.dialog, textvariable=self.player2_name)
            self.entry2.pack(pady=5)
        else:
            self.player2_name.set("Computer")
            tk.Label(self.dialog, text="Player 2 (O): Computer").pack(pady=5)

        tk.Button(self.dialog, text="OK", command=self.on_ok).pack(pady=10)

        self.dialog.transient(parent)
        self.dialog.grab_set()
        parent.wait_window(self.dialog)

    def on_ok(self):
        self.dialog.destroy()

class ModeSelectionDialog:
    def __init__(self, parent):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Select Mode")
        self.dialog.geometry("300x200")
        self.dialog.resizable(False, False)

        self.mode = tk.StringVar()

        tk.Label(self.dialog, text="Select Game Mode:").pack(pady=10)
        tk.Button(self.dialog, text="Player vs Player", command=self.player_vs_player).pack(pady=5)
        tk.Button(self.dialog, text="Player vs Computer", command=self.player_vs_computer).pack(pady=5)

        self.dialog.transient(parent)
        self.dialog.grab_set()
        parent.wait_window(self.dialog)

    def player_vs_player(self):
        self.mode.set("PvP")
        self.dialog.destroy()

    def player_vs_computer(self):
        self.mode.set("PvC")
        self.dialog.destroy()

class DifficultySelectionDialog:
    def __init__(self, parent):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Select Difficulty")
        self.dialog.geometry("300x200")
        self.dialog.resizable(False, False)

        self.difficulty = tk.StringVar()

        tk.Label(self.dialog, text="Select Difficulty Level:").pack(pady=10)
        tk.Button(self.dialog, text="Easy", command=lambda: self.set_difficulty("Easy")).pack(pady=5)
        tk.Button(self.dialog, text="Medium", command=lambda: self.set_difficulty("Medium")).pack(pady=5)
        tk.Button(self.dialog, text="Hard", command=lambda: self.set_difficulty("Hard")).pack(pady=5)

        self.dialog.transient(parent)
        self.dialog.grab_set()
        parent.wait_window(self.dialog)

    def set_difficulty(self, level):
        self.difficulty.set(level)
        self.dialog.destroy()

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")

        self.mode = ''
        self.get_game_mode()

        self.difficulty = ''
        if self.mode == 'PvC':
            self.get_difficulty_level()

        self.player1_name = ''
        self.player2_name = ''
        self.get_player_names()

        self.turn = 'X'
        self.board = ['' for _ in range(9)]
        self.buttons = []
        self.create_buttons()
        self.font = ('Helvetica', 60, 'bold')
        self.blur_colors = {
            'X': ['#FF0000', '#FF3333', '#0949F8'],
            'O': ['#0000FF', '#3333FF', '#F80404']
        }

        self.root.configure(bg='black')

    def get_game_mode(self):
        dialog = ModeSelectionDialog(self.root)
        self.mode = dialog.mode.get()

    def get_difficulty_level(self):
        dialog = DifficultySelectionDialog(self.root)
        self.difficulty = dialog.difficulty.get()

    def get_player_names(self):
        dialog = PlayerNamesDialog(self.root, self.mode)
        self.player1_name = dialog.player1_name.get()
        self.player2_name = dialog.player2_name.get()
        
        if not self.player1_name:
            self.player1_name = "Player 1"
        if not self.player2_name and self.mode == 'PvP':
            self.player2_name = "Player 2"

        self.root.title(f"Tic Tac Toe - {self.player1_name} (X) vs {self.player2_name} (O)")

    def create_buttons(self):
        for i in range(3):
            row = []
            for j in range(3):
                button = tk.Button(self.root, text='', font=('Helvetica', 60, 'bold'), width=5, height=2,
                                command=lambda i=i, j=j: self.on_button_click(i, j), bg='black', fg='white')
                button.grid(row=i, column=j)
                row.append(button)
            self.buttons.append(row)

    def on_button_click(self, i, j):
        index = i * 3 + j
        if self.board[index] == '':
            self.board[index] = self.turn
            self.apply_blur_effect(self.buttons[i][j], self.turn)
            if self.check_winner():
                winner = self.player1_name if self.turn == 'X' else self.player2_name
                messagebox.showinfo("Tic Tac Toe", f"{winner} ({self.turn}) wins!")
                self.reset_game()
            elif '' not in self.board:
                messagebox.showinfo("Tic Tac Toe", "It's a tie!")
                self.reset_game()
            else:
                self.turn = 'O' if self.turn == 'X' else 'X'
                if self.turn == 'O' and self.mode == 'PvC':
                    self.ai_move()

    def ai_move(self):                       
        if self.difficulty == "Easy":
            self.random_move()
        elif self.difficulty == "Medium":
            if random.random() < 0.5:
                self.random_move()
            else:
                self.best_move()
        else:  # Hard
            self.best_move()

    def random_move(self):
        empty_spots = [i for i, spot in enumerate(self.board) if spot == '']
        if empty_spots:
            ai_index = random.choice(empty_spots)
            self.board[ai_index] = 'O'
            i, j = divmod(ai_index, 3)
            self.apply_blur_effect(self.buttons[i][j], 'O')
            if self.check_winner():
                messagebox.showinfo("Tic Tac Toe", f"{self.player2_name} (O) wins!")
                self.reset_game()
            elif '' not in self.board:
                messagebox.showinfo("Tic Tac Toe", "It's a tie!")
                self.reset_game()
            else:
                self.turn = 'X'

    def best_move(self):
        best_score = float('-inf')
        best_move = None
        for i in range(9):
            if self.board[i] == '':
                self.board[i] = 'O'
                score = self.minimax(self.board, 0, False)
                self.board[i] = ''
                if score > best_score:
                    best_score = score
                    best_move = i
        self.board[best_move] = 'O'
        i, j = divmod(best_move, 3)
        self.apply_blur_effect(self.buttons[i][j], 'O')
        if self.check_winner():
            messagebox.showinfo("Tic Tac Toe", f"{self.player2_name} (O) wins!")
            self.reset_game()
        elif '' not in self.board:
            messagebox.showinfo("Tic Tac Toe", "It's a tie!")
            self.reset_game()
        else:
            self.turn = 'X'

    def minimax(self, board, depth, is_maximizing):
        if self.check_winner_static(board):
            return 1 if not is_maximizing else -1
        elif '' not in board:
            return 0

        if is_maximizing:
            best_score = float('-inf')
            for i in range(9):
                if board[i] == '':
                    board[i] = 'O'
                    score = self.minimax(board, depth + 1, False)
                    board[i] = ''
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if board[i] == '':
                    board[i] = 'X'
                    score = self.minimax(board, depth + 1, True)
                    board[i] = ''
                    best_score = min(score, best_score)
            return best_score

    def check_winner_static(self, board):
        winning_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
            (0, 4, 8), (2, 4, 6)  # diagonals
        ]
        for combo in winning_combinations:
            if board[combo[0]] == board[combo[1]] == board[combo[2]] != '':
                return True
        return False

    def apply_blur_effect(self, button, player):
        for color in self.blur_colors[player]:
            button.config(fg=color)
            button.update()
            self.root.after(50)
        button.config(text=player, font=self.font, fg=self.blur_colors[player][-1])

    def check_winner(self):
        return self.check_winner_static(self.board)

    def reset_game(self):
        self.board = ['' for _ in range(9)]
        self.turn = 'X'
        for row in self.buttons:
            for button in row:
                button.config(text='', fg='white', bg='black')

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
