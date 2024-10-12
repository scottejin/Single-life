import tkinter as tk
from tkinter import messagebox
import random
#trial

def generate_sudoku(size=9):
    def pattern(r, c): return (size//3*(r % (size//3)) + r//(size//3) + c) % size
    def shuffle(s): return random.sample(s, len(s))

    rBase = range(size//3)
    rows  = [g*size//3 + r for g in shuffle(rBase) for r in shuffle(rBase)]
    cols  = [g*size//3 + c for g in shuffle(rBase) for c in shuffle(rBase)]
    nums  = shuffle(range(1, size + 1))

    board = [[nums[pattern(r, c)] for c in cols] for r in rows]

    squares = size * size
    empties = squares * 3//4
    for p in random.sample(range(squares), empties):
        board[p//size][p%size] = 0

    return board

def is_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False
    return True

def solve_sudoku(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve_sudoku(board):
                            return True
                        board[row][col] = 0
                return False
    return True

class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku")
        self.board = generate_sudoku()
        self.entries = [[None for _ in range(9)] for _ in range(9)]
        self.create_widgets()

    def create_widgets(self):
        for i in range(9):
            for j in range(9):
                entry = tk.Entry(self.root, width=2, font=('Arial', 18), justify='center')
                entry.grid(row=i, column=j, padx=5, pady=5)
                if self.board[i][j] != 0:
                    entry.insert(0, str(self.board[i][j]))
                    entry.config(state='disabled')
                self.entries[i][j] = entry

        submit_button = tk.Button(self.root, text="Submit", command=self.submit)
        submit_button.grid(row=9, column=4, pady=10)

        brute_force_button = tk.Button(self.root, text="Brute Force", command=self.brute_force)
        brute_force_button.grid(row=10, column=4, pady=10)

    def submit(self):
        try:
            for i in range(9):
                for j in range(9):
                    if self.entries[i][j].get() != '':
                        self.board[i][j] = int(self.entries[i][j].get())
            messagebox.showinfo("Sudoku", "Board submitted successfully!")
        except ValueError:
            messagebox.showerror("Error", "Invalid input! Please enter numbers only.")

    def brute_force(self):
        if solve_sudoku(self.board):
            for i in range(9):
                for j in range(9):
                    self.entries[i][j].delete(0, tk.END)
                    self.entries[i][j].insert(0, str(self.board[i][j]))
                    self.entries[i][j].config(state='disabled')
            messagebox.showinfo("Sudoku", "Board solved successfully!")
        else:
            messagebox.showerror("Error", "No solution exists for the given board.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()