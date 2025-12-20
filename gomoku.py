import tkinter as tk
from tkinter import messagebox
import random

class GomokuGame:
    def __init__(self, root):
        self.root = root
        self.root.title("五子棋 (Gomoku)")
        self.root.resizable(False, False)
        
        # 游戏参数
        self.BOARD_SIZE = 15
        self.CELL_SIZE = 40
        self.BOARD_PADDING = 30
        
        # 游戏状态
        self.board = [[0 for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)]
        self.current_player = 1  # 1为人类(黑棋), 2为AI(白棋)
        self.game_over = False
        self.ai_enabled = True
        
        # 创建画布
        canvas_size = self.CELL_SIZE * self.BOARD_SIZE + 2 * self.BOARD_PADDING
        self.canvas = tk.Canvas(
            root, 
            width=canvas_size, 
            height=canvas_size,
            bg='#DEB887',
            cursor='cross'
        )
        self.canvas.pack(pady=10)
        self.canvas.bind('<Button-1>', self.on_canvas_click)
        
        # 信息标签
        self.info_label = tk.Label(root, text="黑棋(你)的回合 | 按'重置'开始新游戏", font=('Arial', 12))
        self.info_label.pack(pady=5)
        
        # 按钮框架
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)
        
        reset_btn = tk.Button(button_frame, text="重置游戏", command=self.reset_game, width=10)
        reset_btn.pack(side=tk.LEFT, padx=5)
        
        ai_btn = tk.Button(button_frame, text="切换AI(开)", command=self.toggle_ai, width=10)
        ai_btn.pack(side=tk.LEFT, padx=5)
        
        exit_btn = tk.Button(button_frame, text="退出", command=root.quit, width=10)
        exit_btn.pack(side=tk.LEFT, padx=5)
        
        self.draw_board()
    
    def draw_board(self):
        """绘制游戏棋盘"""
        self.canvas.delete('all')
        
        # 绘制网格
        for i in range(self.BOARD_SIZE):
            # 水平线
            x1 = self.BOARD_PADDING
            y1 = self.BOARD_PADDING + i * self.CELL_SIZE
            x2 = self.BOARD_PADDING + (self.BOARD_SIZE - 1) * self.CELL_SIZE
            y2 = y1
            self.canvas.create_line(x1, y1, x2, y2, fill='black')
            
            # 竖直线
            x1 = self.BOARD_PADDING + i * self.CELL_SIZE
            y1 = self.BOARD_PADDING
            x2 = x1
            y2 = self.BOARD_PADDING + (self.BOARD_SIZE - 1) * self.CELL_SIZE
            self.canvas.create_line(x1, y1, x2, y2, fill='black')
        
        # 绘制星位(天元和四个角的星)
        star_positions = [3, 7, 11]
        for row in star_positions:
            for col in star_positions:
                if (row == 7 and col == 7) or (row != 7 and col != 7):
                    x = self.BOARD_PADDING + col * self.CELL_SIZE
                    y = self.BOARD_PADDING + row * self.CELL_SIZE
                    self.canvas.create_oval(x-3, y-3, x+3, y+3, fill='black')
        
        # 绘制棋子
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                if self.board[row][col] != 0:
                    self.draw_piece(row, col, self.board[row][col])
    
    def draw_piece(self, row, col, player):
        """绘制棋子"""
        x = self.BOARD_PADDING + col * self.CELL_SIZE
        y = self.BOARD_PADDING + row * self.CELL_SIZE
        radius = self.CELL_SIZE // 2 - 2
        
        color = 'black' if player == 1 else 'white'
        outline = 'white' if player == 1 else 'black'
        
        self.canvas.create_oval(
            x - radius, y - radius,
            x + radius, y + radius,
            fill=color,
            outline=outline,
            width=2
        )
    
    def on_canvas_click(self, event):
        """处理棋盘点击事件"""
        if self.game_over:
            messagebox.showinfo("游戏结束", "游戏已结束，请点击'重置游戏'开始新游戏")
            return
        
        if self.current_player != 1:
            messagebox.showinfo("等待", "请等待AI的回合")
            return
        
        # 计算点击的棋盘坐标
        col = round((event.x - self.BOARD_PADDING) / self.CELL_SIZE)
        row = round((event.y - self.BOARD_PADDING) / self.CELL_SIZE)
        
        # 检查坐标有效性
        if not (0 <= row < self.BOARD_SIZE and 0 <= col < self.BOARD_SIZE):
            messagebox.showwarning("无效位置", "请点击棋盘内的位置")
            return
        
        if self.board[row][col] != 0:
            messagebox.showwarning("位置被占用", "该位置已有棋子")
            return
        
        # 放置棋子
        self.place_piece(row, col, 1)
        
        # 检查是否获胜
        if self.check_win(row, col, 1):
            self.game_over = True
            self.info_label.config(text="恭喜！你赢了！", fg='green')
            messagebox.showinfo("游戏结束", "你赢了！")
            return
        
        # AI回合
        if self.ai_enabled:
            self.root.after(500, self.ai_move)
    
    def place_piece(self, row, col, player):
        """在棋盘上放置棋子"""
        self.board[row][col] = player
        self.current_player = 2 if player == 1 else 1
        self.draw_board()
    
    def ai_move(self):
        """AI的移动"""
        if self.game_over:
            return
        
        # 寻找最佳移动
        best_move = self.find_best_move()
        
        if best_move is None:
            messagebox.showinfo("平局", "棋盘已满，游戏结束")
            self.game_over = True
            return
        
        row, col = best_move
        self.place_piece(row, col, 2)
        
        # 检查AI是否获胜
        if self.check_win(row, col, 2):
            self.game_over = True
            self.info_label.config(text="AI赢了！", fg='red')
            messagebox.showinfo("游戏结束", "AI赢了！")
            return
        
        self.info_label.config(text="黑棋(你)的回合", fg='black')
    
    def find_best_move(self):
        """使用简单的策略找到最佳移动"""
        # 首先检查AI是否能赢
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                if self.board[row][col] == 0:
                    self.board[row][col] = 2
                    if self.check_win(row, col, 2):
                        self.board[row][col] = 0
                        return (row, col)
                    self.board[row][col] = 0
        
        # 检查是否需要阻止对手获胜
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                if self.board[row][col] == 0:
                    self.board[row][col] = 1
                    if self.check_win(row, col, 1):
                        self.board[row][col] = 0
                        return (row, col)
                    self.board[row][col] = 0
        
        # 寻找靠近已有棋子的空位
        candidates = []
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                if self.board[row][col] == 0:
                    # 检查周围是否有棋子
                    if self.has_neighbor(row, col):
                        candidates.append((row, col))
        
        if candidates:
            return random.choice(candidates)
        
        # 返回随机空位
        empty_positions = [(r, c) for r in range(self.BOARD_SIZE) 
                          for c in range(self.BOARD_SIZE) 
                          if self.board[r][c] == 0]
        
        return random.choice(empty_positions) if empty_positions else None
    
    def has_neighbor(self, row, col, distance=2):
        """检查位置周围是否有棋子"""
        for r in range(max(0, row - distance), min(self.BOARD_SIZE, row + distance + 1)):
            for c in range(max(0, col - distance), min(self.BOARD_SIZE, col + distance + 1)):
                if (r, c) != (row, col) and self.board[r][c] != 0:
                    return True
        return False
    
    def check_win(self, row, col, player):
        """检查是否获胜"""
        directions = [
            (0, 1),   # 水平
            (1, 0),   # 竖直
            (1, 1),   # 对角线
            (1, -1)   # 反对角线
        ]
        
        for dr, dc in directions:
            count = 1
            
            # 向一个方向检查
            r, c = row + dr, col + dc
            while 0 <= r < self.BOARD_SIZE and 0 <= c < self.BOARD_SIZE:
                if self.board[r][c] == player:
                    count += 1
                    r += dr
                    c += dc
                else:
                    break
            
            # 向相反方向检查
            r, c = row - dr, col - dc
            while 0 <= r < self.BOARD_SIZE and 0 <= c < self.BOARD_SIZE:
                if self.board[r][c] == player:
                    count += 1
                    r -= dr
                    c -= dc
                else:
                    break
            
            if count >= 5:
                return True
        
        return False
    
    def toggle_ai(self):
        """切换AI"""
        self.ai_enabled = not self.ai_enabled
        status = "开" if self.ai_enabled else "关"
        messagebox.showinfo("AI状态", f"AI已{'启用' if self.ai_enabled else '禁用'}")
        if not self.ai_enabled:
            self.info_label.config(text="两人模式: 黑棋的回合", fg='black')
    
    def reset_game(self):
        """重置游戏"""
        self.board = [[0 for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)]
        self.current_player = 1
        self.game_over = False
        self.info_label.config(text="黑棋(你)的回合", fg='black')
        self.draw_board()


if __name__ == '__main__':
    root = tk.Tk()
    game = GomokuGame(root)
    root.mainloop()
