import tkinter as tk
import threading

class CaroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Caro AI Pro | 3 Thuật Toán")
        self.root.geometry("450x680")
        self.root.configure(bg="#2c3e50")
        
        self.board = [' '] * 9
        self.buttons = []
        self.score_x = 0
        self.score_o = 0
        self.game_active = True
        
        # --- UI Control ---
        ctrl = tk.Frame(root, bg="#2c3e50")
        ctrl.pack(pady=10)
        tk.Label(ctrl, text="Chọn AI:", fg="white", bg="#2c3e50").pack(side=tk.LEFT)
        self.algo = tk.StringVar(value="Alpha-Beta")
        tk.OptionMenu(ctrl, self.algo, "Minimax", "Alpha-Beta", "Expectimax").pack(side=tk.LEFT, padx=5)
        tk.Button(ctrl, text="Reset Ván", command=self.reset_board, bg="#f1c40f").pack(side=tk.LEFT, padx=5)
        
        # --- Scoreboard ---
        self.lbl_score = tk.Label(root, text=f"Người: 0 | AI: 0", font=('Arial', 14, 'bold'), fg="#ecf0f1", bg="#2c3e50")
        self.lbl_score.pack(pady=5)

        # --- Bàn cờ ---
        self.board_frame = tk.Frame(root, bg="#34495e", bd=5)
        self.board_frame.pack(pady=10)
        for i in range(9):
            btn = tk.Button(self.board_frame, width=4, height=2, font=('Arial', 24, 'bold'),
                            bg="#ecf0f1", relief="flat", command=lambda i=i: self.on_click(i))
            btn.grid(row=i//3, column=i%3, padx=2, pady=2)
            self.buttons.append(btn)
            
        self.status = tk.Label(root, text="Lượt bạn (X)", font=('Arial', 12), bg="#2c3e50", fg="#f1c40f")
        self.status.pack(pady=10)

    def reset_board(self):
        self.board = [' '] * 9
        self.game_active = True
        for btn in self.buttons:
            btn.config(text=' ', bg="#ecf0f1", state="normal")
        self.status.config(text="Lượt bạn (X)", fg="#f1c40f")

    def on_click(self, i):
        if self.game_active and self.board[i] == ' ':
            self.board[i] = 'X'
            self.buttons[i].config(text='X', fg='#3498db')
            if not self.check_end():
                self.game_active = False
                self.status.config(text="AI đang suy nghĩ...", fg="#e74c3c")
                threading.Thread(target=self.ai_turn).start()

    def ai_turn(self):
        algo = self.algo.get()
        best_val = float('inf')
        move = -1
        
        for i in range(9):
            if self.board[i] == ' ':
                self.board[i] = 'O'
                if algo == "Minimax": val = self.minimax(0, False)
                elif algo == "Alpha-Beta": val = self.alphabeta(0, -99, 99, False)
                else: val = self.expectimax(0, False)
                self.board[i] = ' '
                if val < best_val:
                    best_val, move = val, i
        
        if move != -1:
            self.board[move] = 'O'
            self.buttons[move].config(text='O', fg='#e74c3c')
            self.game_active = True
            self.check_end()
            if self.game_active: self.status.config(text="Lượt bạn (X)", fg="#f1c40f")

    def check_end(self):
        w = self.check_win()
        if w or ' ' not in self.board:
            self.game_active = False
            if w == 'X': self.score_x += 1
            elif w == 'O': self.score_o += 1
            self.lbl_score.config(text=f"Người: {self.score_x} | AI: {self.score_o}")
            self.status.config(text=f"Kết thúc: {'Hòa' if not w else w + ' thắng!'}", fg="#2ecc71")
            return True
        return False

    def check_win(self):
        for a,b,c in [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]:
            if self.board[a]==self.board[b]==self.board[c] and self.board[a]!=' ': return self.board[a]
        return None

    # --- THUẬT TOÁN MINIMAX ---
    def minimax(self, d, is_max):
        w = self.check_win()
        if w: return (10-d) if w=='X' else (d-10)
        if ' ' not in self.board: return 0
        if is_max:
            v = -99
            for i in range(9):
                if self.board[i]==' ': self.board[i]='X'; v=max(v, self.minimax(d+1, False)); self.board[i]=' '
            return v
        else:
            v = 99
            for i in range(9):
                if self.board[i]==' ': self.board[i]='O'; v=min(v, self.minimax(d+1, True)); self.board[i]=' '
            return v

    # --- THUẬT TOÁN ALPHA-BETA ---
    def alphabeta(self, d, a, b, is_max):
        w = self.check_win()
        if w: return (10-d) if w=='X' else (d-10)
        if ' ' not in self.board: return 0
        if is_max:
            v = -99
            for i in range(9):
                if self.board[i]==' ': 
                    self.board[i]='X'; v=max(v, self.alphabeta(d+1, a, b, False)); self.board[i]=' '; a=max(a, v)
                    if b<=a: break
            return v
        else:
            v = 99
            for i in range(9):
                if self.board[i]==' ': 
                    self.board[i]='O'; v=min(v, self.alphabeta(d+1, a, b, True)); self.board[i]=' '; b=min(b, v)
                    if b<=a: break
            return v

    # --- THUẬT TOÁN EXPECTIMAX ---
    def expectimax(self, d, is_max):
        w = self.check_win()
        if w: return (10-d) if w=='X' else (d-10)
        empty = [i for i, v in enumerate(self.board) if v == ' ']
        if not empty: return 0
        if is_max:
            v = -99
            for i in empty: self.board[i]='X'; v=max(v, self.expectimax(d+1, False)); self.board[i]=' '
            return v
        else:
            total = sum(self.expectimax(d+1, True) for i in empty)
            return total / len(empty)

if __name__ == "__main__":
    root = tk.Tk()
    app = CaroApp(root)
    root.mainloop()