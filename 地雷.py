# -*- coding: utf-8 -*-
"""
簡易 Tkinter 踩地雷遊戲
左鍵揭示、右鍵標記旗子。可設定列/欄/地雷數並重新開始。

執行：
python "Corel Content\地雷.py"
"""
import tkinter as tk
from tkinter import messagebox
import random
import time

class Cell:
    def __init__(self):
        self.is_mine = False
        self.adj = 0
        self.revealed = False
        self.flagged = False

class MinesweeperApp:
    def __init__(self, master):
        self.master = master
        master.title('踩地雷')
        self.top_frame = tk.Frame(master)
        self.top_frame.pack(padx=8, pady=8)

        tk.Label(self.top_frame, text='列').grid(row=0, column=0)
        self.rows_var = tk.IntVar(value=9)
        tk.Entry(self.top_frame, width=4, textvariable=self.rows_var).grid(row=0, column=1)
        tk.Label(self.top_frame, text='欄').grid(row=0, column=2)
        self.cols_var = tk.IntVar(value=9)
        tk.Entry(self.top_frame, width=4, textvariable=self.cols_var).grid(row=0, column=3)
        tk.Label(self.top_frame, text='地雷').grid(row=0, column=4)
        self.mines_var = tk.IntVar(value=10)
        tk.Entry(self.top_frame, width=5, textvariable=self.mines_var).grid(row=0, column=5)

        self.new_btn = tk.Button(self.top_frame, text='重新開始', command=self.new_game)
        self.new_btn.grid(row=0, column=6, padx=6)
        self.timer_label = tk.Label(self.top_frame, text='時間: 0')
        self.timer_label.grid(row=0, column=7, padx=6)

        self.board_frame = tk.Frame(master)
        self.board_frame.pack(padx=8, pady=(0,8))

        self.status = tk.Label(master, text='準備中')
        self.status.pack()

        self.buttons = []
        self.grid = []
        self.rows = 9
        self.cols = 9
        self.mines = 10
        self.start_time = None
        self.timer_running = False
        self.new_game()

    def new_game(self):
        try:
            rows = max(3, int(self.rows_var.get()))
            cols = max(3, int(self.cols_var.get()))
            mines = int(self.mines_var.get())
        except Exception:
            messagebox.showerror('錯誤', '請輸入有效數字')
            return
        mines = min(mines, rows*cols-1)
        self.rows, self.cols, self.mines = rows, cols, mines

        for w in self.board_frame.winfo_children():
            w.destroy()
        self.buttons = [[None for _ in range(cols)] for _ in range(rows)]
        self.grid = [[Cell() for _ in range(cols)] for _ in range(rows)]

        for r in range(rows):
            for c in range(cols):
                b = tk.Button(self.board_frame, width=3, height=1, relief='raised')
                b.grid(row=r, column=c, padx=1, pady=1)
                b.bind('<Button-1>', lambda e, rr=r, cc=c: self.on_left(rr, cc))
                b.bind('<Button-3>', lambda e, rr=r, cc=c: self.on_right(rr, cc))
                self.buttons[r][c] = b

        self.place_mines()
        self.calc_adj()
        self.revealed_count = 0
        self.game_over = False
        self.status.config(text='進行中')
        self.start_time = time.time()
        if not self.timer_running:
            self.timer_running = True
            self.master.after(200, self.update_timer)

    def place_mines(self):
        coords = [(r, c) for r in range(self.rows) for c in range(self.cols)]
        mines = random.sample(coords, self.mines)
        for r, c in mines:
            self.grid[r][c].is_mine = True

    def calc_adj(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c].is_mine:
                    self.grid[r][c].adj = -1
                    continue
                count = 0
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        if dr == 0 and dc == 0:
                            continue
                        rr, cc = r+dr, c+dc
                        if 0 <= rr < self.rows and 0 <= cc < self.cols:
                            if self.grid[rr][cc].is_mine:
                                count += 1
                self.grid[r][c].adj = count

    def on_left(self, r, c):
        if self.game_over:
            return
        cell = self.grid[r][c]
        if cell.flagged or cell.revealed:
            return
        if cell.is_mine:
            self.reveal_all(mine_hit=(r,c))
            self.game_over = True
            self.status.config(text='遊戲結束')
            messagebox.showinfo('失敗', '踩到地雷！')
            return
        self.reveal(r, c)
        if self.check_win():
            self.game_over = True
            self.status.config(text='你贏了 🎉')
            messagebox.showinfo('勝利', '恭喜，你已清除所有安全格！')

    def on_right(self, r, c):
        if self.game_over:
            return
        cell = self.grid[r][c]
        b = self.buttons[r][c]
        if cell.revealed:
            return
        cell.flagged = not cell.flagged
        b.config(text='🚩' if cell.flagged else '')

    def reveal(self, r, c):
        cell = self.grid[r][c]
        b = self.buttons[r][c]
        if cell.revealed or cell.flagged:
            return
        cell.revealed = True
        b.config(relief='sunken', state='disabled', bg='#ffffff')
        if cell.adj > 0:
            b.config(text=str(cell.adj), fg=self.color_for_num(cell.adj))
            self.revealed_count += 1
            return
        self.revealed_count += 1
        # flood fill
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                rr, cc = r+dr, c+dc
                if 0 <= rr < self.rows and 0 <= cc < self.cols:
                    if not self.grid[rr][cc].revealed:
                        self.reveal(rr, cc)

    def reveal_all(self, mine_hit=None):
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.grid[r][c]
                b = self.buttons[r][c]
                if cell.is_mine:
                    b.config(text='💣', bg='#ffb3b3')
                if mine_hit and (r, c) == mine_hit:
                    b.config(bg='#ff6666')
                b.config(state='disabled', relief='sunken')

    def check_win(self):
        total_safe = self.rows * self.cols - self.mines
        return self.revealed_count >= total_safe

    def color_for_num(self, n):
        colors = {1:'#1a73e8', 2:'#1aa34a', 3:'#e85c3b', 4:'#7b3be8'}
        return colors.get(n, '#333333')

    def update_timer(self):
        if not self.timer_running:
            return
        if self.start_time is None:
            self.timer_label.config(text='時間: 0')
        else:
            elapsed = int(time.time() - self.start_time)
            self.timer_label.config(text=f'時間: {elapsed}')
        if not self.game_over:
            self.master.after(200, self.update_timer)
        else:
            self.timer_running = False

if __name__ == '__main__':
    root = tk.Tk()
    app = MinesweeperApp(root)
    root.mainloop()
