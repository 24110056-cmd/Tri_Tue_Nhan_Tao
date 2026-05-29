import tkinter as tk
from tkinter import messagebox, scrolledtext
from collections import deque
import copy
import time
import heapq
import random
MAX_SIZE = 10
class VacuumCleanerAI:
    def __init__(self, root):
        self.root = root
        self.root.title("HỆ THỐNG MÔ PHỎNG MÁY HÚT BỤI AI")
        self.root.geometry("1600x900")
        self.root.configure(bg="#0b132b")
        self.rows = 5
        self.cols = 5
        self.default_room = [
            [0, 1, 0, 1, 0],
            [0, 0, 1, 0, 0],
            [1, 0, 0, 1, 0],
            [0, 1, 0, 0, 1],
            [0, 0, 1, 0, 0]
        ]
        self.room = copy.deepcopy(self.default_room)
        self.robot_position = (0, 0)
        self.step_timer = None
        self.path_arrows = []
        self.canvas_width = 850
        self.canvas_height = 580
        self.cell_size = 75
        self.start_x = 0
        self.start_y = 0
        self.build_ui()
        self.draw_room()
    def build_ui(self):
        self.left_panel = tk.Frame(self.root, bg="#1c2541", bd=0)
        self.left_panel.place(x=0, y=0, width=320, relheight=1.0)
        self.menu_btn = tk.Button(
            self.left_panel, text="  ☰   THUẬT TOÁN", font=("Segoe UI", 16, "bold"), 
            bg="#1c2541", fg="#4cc9f0", activebackground="#4cc9f0", activeforeground="#0b132b",
            bd=0, relief="flat", cursor="hand2", anchor="w", padx=20, command=self.open_algorithm_menu
        )
        self.menu_btn.pack(fill="x", pady=(20, 5))
        tk.Label(
            self.left_panel, text="THÔNG TIN", 
            bg="#1c2541", fg="#4cc9f0", font=("Segoe UI", 14, "bold")
        ).pack(pady=(20, 5))
        self.info_frame = tk.Frame(self.left_panel, bg="#0b132b", highlightthickness=1, highlightbackground="#3a506b")
        self.info_frame.pack(padx=15, pady=5, fill="both", expand=True)
        self.info_label = tk.Label(
            self.info_frame, text="Hệ thống sẵn sàng.",
            bg="#0b132b", fg="#e0e1dd", font=("Consolas", 13), justify="left", anchor="nw", padx=10, pady=10
        )
        self.info_label.pack(fill="both", expand=True)
        tk.Label(
            self.left_panel, text="LỘ TRÌNH ĐƯỜNG ĐI CHI TIẾT", 
            bg="#1c2541", fg="#4cc9f0", font=("Segoe UI", 14, "bold")
        ).pack(pady=(20, 5))
        self.summary_text_box = scrolledtext.ScrolledText(
            self.left_panel, bg="#0b132b", fg="#00f5d4", font=("Consolas", 12, "bold"),
            wrap=tk.WORD, bd=0, highlightthickness=1, highlightbackground="#3a506b"
        )
        self.summary_text_box.pack(padx=15, pady=(0, 20), fill="both", expand=True)
        self.update_summary_box("Chưa thực hiện lộ trình.")
        self.right_control_panel = tk.Frame(self.root, bg="#1c2541")
        self.right_control_panel.place(relx=1.0, y=0, x=0, width=320, relheight=1.0, anchor="ne")
        tk.Label(
            self.right_control_panel, text="BẢNG ĐIỀU KHIỂN", 
            bg="#1c2541", fg="#4cc9f0", font=("Segoe UI", 15, "bold")
        ).pack(pady=(30, 10))
        self.create_right_button(self.right_control_panel, "Nhập Ma Trận", self.input_matrix, "#7209b7")
        self.create_right_button(self.right_control_panel, "Reset", self.reset_room, "#f72585")
        tk.Label(
            self.right_control_panel, text="CHI TIẾT CÁC BƯỚC", 
            bg="#1c2541", fg="#4cc9f0", font=("Segoe UI", 15, "bold")
        ).pack(pady=(25, 5))
        self.path_text_box = scrolledtext.ScrolledText(
            self.right_control_panel, bg="#0b132b", fg="#4cc9f0", font=("Consolas", 11),
            wrap=tk.WORD, bd=0, highlightthickness=1, highlightbackground="#3a506b"
        )
        self.path_text_box.pack(padx=15, pady=(0, 20), fill="both", expand=True)
        self.top_header_panel = tk.Frame(self.root, bg="#1c2541", bd=0)
        self.top_header_panel.place(x=320, y=0, relwidth=1.0, width=-640, height=135)
        tk.Label(
            self.top_header_panel, text="MÁY HÚT BỤI THÔNG MINH - AI SIMULATOR", 
            bg="#1c2541", fg="#ffffff", font=("Segoe UI", 24, "bold")
        ).pack(pady=(15, 2))
        legend_frame = tk.Frame(self.top_header_panel, bg="#1c2541")
        legend_frame.pack(pady=5)
        self.legend_item(legend_frame, "#ffffff", "Ô sạch")
        self.legend_item(legend_frame, "#ffb703", "Ô bẩn (Bụi)")
        self.legend_item(legend_frame, "#3a506b", "Vật cản")
        self.legend_item(legend_frame, "#4cc9f0", "Vị trí Robot")
        self.legend_item(legend_frame, "#00CC66", "Đường đi")
        self.bottom_footer_panel = tk.Frame(self.root, bg="#1c2541", bd=0)
        self.bottom_footer_panel.place(x=320, rely=1.0, y=-50, relwidth=1.0, width=-640, height=50)
        self.center_display_frame = tk.Frame(self.root, bg="#0b132b")
        self.center_display_frame.place(x=320, y=135, relwidth=1.0, width=-640, relheight=1.0, height=-185)
        self.canvas = tk.Canvas(
            self.center_display_frame, width=self.canvas_width, height=self.canvas_height, 
            bg="#0b132b", highlightthickness=0, bd=0
        )
        self.canvas.pack(expand=True)
        self.algorithm_drawer = tk.Frame(self.root, bg="#131a30", bd=0)
        self.close_btn = tk.Button(
            self.algorithm_drawer, text="  🗙   ĐÓNG MENU", font=("Segoe UI", 16, "bold"), 
            bg="#131a30", fg="#f72585", activebackground="#f72585", activeforeground="#0b132b",
            bd=0, relief="flat", cursor="hand2", anchor="w", padx=20, command=self.close_algorithm_menu
        )
        self.close_btn.pack(fill="x", pady=(20, 0))
        tk.Label(
            self.algorithm_drawer, text="CHỌN THUẬT TOÁN", 
            bg="#131a30", fg="#ffffff", font=("Segoe UI", 14, "bold")
        ).pack(pady=(15, 15))
        self.buttons_container = tk.Frame(self.algorithm_drawer, bg="#131a30")
        self.buttons_container.pack(fill="x", padx=0)
        self.create_drawer_button("BFS QUEUE", self.run_bfs_queue)
        self.create_drawer_button("BFS RECURSIVE", self.run_bfs_recursive)
        self.create_drawer_button("DFS STACK", self.run_dfs_stack)
        self.create_drawer_button("DFS RECURSIVE", self.run_dfs_recursive)
        self.create_drawer_button("UCS", self.run_ucs)
        self.create_drawer_button("IDS STACK", self.run_ids_stack)
        self.create_drawer_button("IDS RECURSIVE", self.run_ids_recursive)
        self.create_drawer_button("GREEDY", self.run_greedy)
        self.create_drawer_button("A-STAR", self.run_astar)
        self.create_drawer_button("IDA-STAR", self.run_idastar)
        self.create_drawer_button("SIMPLE HILL CLIMBING", self.run_simple_hill_climbing)
        self.create_drawer_button("STEEPEST ASCENT HILL CLIMBING", self.run_steepest_ascent_hill_climbing)
        self.create_drawer_button("STOCHASTIC HILL CLIMBING", self.run_stochastic_hill_climbing)
    def open_algorithm_menu(self):
        self.algorithm_drawer.place(x=0, y=0, width=320, relheight=1.0)
    def close_algorithm_menu(self):
        self.algorithm_drawer.place_forget()
    def create_drawer_button(self, text, command):
        btn_frame = tk.Frame(self.buttons_container, bg="#131a30", highlightthickness=1, highlightbackground="#222b45")
        btn_frame.pack(fill="x", ipady=0, ipadx=0)
        btn = tk.Button(
            btn_frame, text=text, command=lambda: [self.close_algorithm_menu(), command()],
            font=("Segoe UI", 12, "bold"), bg="#131a30", fg="#e0e1dd", activebackground="#4cc9f0", activeforeground="#0b132b",
            relief="flat", bd=0, height=2, cursor="hand2", anchor="w", padx=25
        )
        btn.pack(fill="x")
    def create_right_button(self, parent, text, command, bg_color):
        tk.Button(
            parent, text=text, command=command, height=2,
            bg=bg_color, fg="white", activebackground="#ffffff", activeforeground=bg_color,
            relief="flat", bd=0, cursor="hand2", font=("Segoe UI", 12, "bold")
        ).pack(pady=8, padx=25, fill="x")
    def legend_item(self, parent, color, text):
        frame = tk.Frame(parent, bg="#1c2541")
        frame.pack(side="left", padx=15)
        canvas = tk.Canvas(frame, width=20, height=20, bg=color, highlightthickness=1, highlightbackground="#3a506b")
        canvas.pack(side="left")
        tk.Label(frame, text=text, bg="#1c2541", fg="#e0e1dd", font=("Segoe UI", 11)).pack(side="left", padx=6)
    def clear_path_box(self):
        self.path_text_box.config(state=tk.NORMAL)
        self.path_text_box.delete("1.0", tk.END)
        self.path_text_box.config(state=tk.DISABLED)
    def append_path_log(self, text_line):
        self.path_text_box.config(state=tk.NORMAL)
        self.path_text_box.insert(tk.END, text_line)
        self.path_text_box.see(tk.END)
        self.path_text_box.config(state=tk.DISABLED)
    def update_info_box(self, text_content):
        self.info_label.config(text=text_content)
    def update_summary_box(self, text_content):
        self.summary_text_box.config(state=tk.NORMAL)
        self.summary_text_box.delete("1.0", tk.END)
        self.summary_text_box.insert(tk.END, text_content)
        self.summary_text_box.see(tk.END)
        self.summary_text_box.config(state=tk.DISABLED)
    def input_matrix(self):
        popup = tk.Toplevel(self.root)
        popup.title("Cấu hình kích thước phòng mới")
        popup.geometry("650x650")
        popup.configure(bg="#1c2541")
        popup.grab_set()
        tk.Label(popup, text="NHẬP SỐ HÀNG & SỐ CỘT", bg="#1c2541", fg="white", font=("Segoe UI", 16, "bold")).pack(pady=15)
        top_frame = tk.Frame(popup, bg="#1c2541")
        top_frame.pack()
        tk.Label(top_frame, text="Hàng (Max 10):", bg="#1c2541", fg="#4cc9f0", font=("Segoe UI", 12)).grid(row=0, column=0, padx=8)
        row_entry = tk.Entry(top_frame, width=5, font=("Segoe UI", 12), justify="center")
        row_entry.grid(row=0, column=1)
        row_entry.insert(0, str(self.rows))
        tk.Label(top_frame, text="Cột (Max 10):", bg="#1c2541", fg="#4cc9f0", font=("Segoe UI", 12)).grid(row=0, column=2, padx=8)
        col_entry = tk.Entry(top_frame, width=5, font=("Segoe UI", 12), justify="center")
        col_entry.grid(row=0, column=3)
        col_entry.insert(0, str(self.cols))
        matrix_frame = tk.Frame(popup, bg="#0b132b", padx=10, pady=10)
        matrix_frame.pack(pady=15)
        entries = []
        def create_matrix():
            for widget in matrix_frame.winfo_children():
                widget.destroy()
            entries.clear()
            try:
                r = int(row_entry.get())
                c = int(col_entry.get())
            except ValueError:
                messagebox.showerror("Lỗi dữ liệu", "Vui lòng nhập định dạng số nguyên!")
                return
            if r <= 0 or c <= 0 or r > MAX_SIZE or c > MAX_SIZE:
                messagebox.showerror("Giới hạn lỗi", f"Chỉ hỗ trợ kích thước từ 1 đến {MAX_SIZE}")
                return
            for i in range(r):
                row_data = []
                for j in range(c):
                    e = tk.Entry(matrix_frame, width=4, justify="center", font=("Consolas", 14), bg="#1c2541", fg="white", bd=1)
                    e.grid(row=i, column=j, padx=4, pady=4)
                    e.insert(0, "0")
                    row_data.append(e)
                entries.append(row_data)
        def save_matrix():
            try:
                r = int(row_entry.get())
                c = int(col_entry.get())
            except ValueError:
                return
            new_room = []
            for i in range(r):
                row_data = []
                for j in range(c):
                    value = entries[i][j].get()
                    if value not in ["0", "1", "2"]:
                        messagebox.showerror("Lỗi giá trị", "Quy ước bắt buộc: 0=Sạch | 1=Bụi | 2=Vật cản")
                        return
                    row_data.append(int(value))
                new_room.append(row_data)
            new_room[0][0] = 0
            self.rows = r
            self.cols = c
            self.default_room = copy.deepcopy(new_room)
            self.room = copy.deepcopy(new_room)
            self.robot_position = (0, 0)
            self.path_arrows.clear()
            self.update_info_box("Hệ thống cập nhật thành công\nma trận phòng mới.")
            self.update_summary_box("Chưa thực hiện lộ trình.")
            popup.destroy()
            self.clear_path_box()
            self.draw_room()
        tk.Button(popup, text="Thiết lập lưới ô", command=create_matrix, bg="#3a506b", fg="white", font=("Segoe UI", 12, "bold")).pack(pady=5)
        tk.Label(popup, text="Quy ước nhập:  0 = Ô sạch  |  1 = Ô bụi bẩn  |  2 = Khối vật cản", bg="#1c2541", fg="#e0e1dd", font=("Segoe UI", 11)).pack()
        tk.Button(popup, text="XÁC NHẬN LƯU", command=save_matrix, bg="#4cc9f0", fg="#0b132b", font=("Segoe UI", 12, "bold"), width=15).pack(pady=15)
        create_matrix()
    def draw_room(self):
        max_w = self.canvas_width - 40
        max_h = self.canvas_height - 40
        scale_x = max_w // self.cols
        scale_y = max_h // self.rows
        self.cell_size = min(scale_x, scale_y)
        if self.cell_size > 80: self.cell_size = 80
        elif self.cell_size < 45: self.cell_size = 45
        board_width = self.cols * self.cell_size
        board_height = self.rows * self.cell_size
        self.start_x = (self.canvas_width - board_width) // 2
        self.start_y = (self.canvas_height - board_height) // 2
        self.canvas.delete("all")
        self.canvas.create_rectangle(
            self.start_x - 2, self.start_y - 2, 
            self.start_x + board_width + 2, self.start_y + board_height + 2, 
            outline="#3a506b", width=2
        )
        for i in range(self.rows):
            for j in range(self.cols):
                x1 = self.start_x + j * self.cell_size
                y1 = self.start_y + i * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                value = self.room[i][j]
                color = "#ffffff"      
                if value == 1: color = "#ffb703"  
                elif value == 2: color = "#3a506b"  
                if (i, j) == self.robot_position: 
                    color = "#4cc9f0"  
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#0b132b", width=2)
        for arrow in self.path_arrows:
            x1, y1, x2, y2 = arrow
            self.canvas.create_line(x1, y1, x2, y2, fill="#00CC66", width=5, arrow=tk.LAST)
        rx, ry = self.robot_position
        robot_x = self.start_x + ry * self.cell_size + self.cell_size // 2
        robot_y = self.start_y + rx * self.cell_size + self.cell_size // 2
        self.canvas.create_text(robot_x, robot_y, text="🤖", font=("Segoe UI", 30))
    def get_neighbors(self, x, y, room_state):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        result = []
        for dx, dy in directions:
            nx = x + dx
            ny = y + dy
            if 0 <= nx < self.rows and 0 <= ny < self.cols and room_state[nx][ny] != 2:
                result.append((nx, ny))
        return result
    def get_labeled_moves_list(self, cx, cy):
        moves = [("RIGHT", (cx, cy + 1)), ("DOWN", (cx + 1, cy)), ("LEFT", (cx, cy - 1)), ("UP", (cx - 1, cy))]
        valid_moves = []
        for label, (nx, ny) in moves:
            if 0 <= nx < self.rows and 0 <= ny < self.cols and self.default_room[nx][ny] != 2:
                valid_moves.append(f"    {label} ({nx}, {ny})")
        return "\n".join(valid_moves)
    def get_move_direction_upper(self, cx, cy, nx, ny):
        if nx == cx and ny == cy + 1: return "RIGHT"
        if nx == cx and ny == cy - 1: return "LEFT"
        if nx == cx - 1 and ny == cy: return "UP"
        if nx == cx + 1 and ny == cy: return "DOWN"
        return "START"
    def Manhattan_distance(self, p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
    def bfs_queue_algorithm(self):
        start = self.robot_position
        full_path = [start]
        temp_room = copy.deepcopy(self.room)
        current = start
        while True:
            if temp_room[current[0]][current[1]] == 1:
                temp_room[current[0]][current[1]] = 0
            frontier = deque([(current, [current])])
            reached = {current}
            target_path = None
            while frontier:
                node, path = frontier.popleft()
                if temp_room[node[0]][node[1]] == 1:
                    target_path = path
                    break
                for neighbor in self.get_neighbors(*node, temp_room):
                    if neighbor not in reached:
                        reached.add(neighbor)
                        frontier.append((neighbor, path + [neighbor]))
            if target_path is None: break
            full_path.extend(target_path[1:])
            current = target_path[-1]
            temp_room[current[0]][current[1]] = 0
        return full_path
    def bfs_recursive_algorithm(self):
        temp_room = copy.deepcopy(self.room)
        full_path = [self.robot_position]
        def find_next_dirt_bfs(current):
            if temp_room[current[0]][current[1]] == 1:
                temp_room[current[0]][current[1]] = 0
            frontier = deque([(current, [current])])
            explored = {current}
            found_path = None
            while frontier:
                node, path = frontier.popleft()
                if temp_room[node[0]][node[1]] == 1:
                    found_path = path
                    break
                for neighbor in self.get_neighbors(*node, temp_room):
                    if neighbor not in explored:
                        explored.add(neighbor)
                        frontier.append((neighbor, path + [neighbor]))
            if found_path:
                full_path.extend(found_path[1:])
                next_node = found_path[-1]
                temp_room[next_node[0]][next_node[1]] = 0
                find_next_dirt_bfs(next_node)
        find_next_dirt_bfs(self.robot_position)
        return full_path
    def dfs_stack_algorithm(self):
        start = self.robot_position
        full_path = [start]
        temp_room = copy.deepcopy(self.room)
        current = start
        while True:
            if temp_room[current[0]][current[1]] == 1:
                temp_room[current[0]][current[1]] = 0
            frontier = [(current, [current])]
            reached = {current}
            target_path = None
            while frontier:
                node, path = frontier.pop()
                if temp_room[node[0]][node[1]] == 1:
                    target_path = path
                    break
                for neighbor in self.get_neighbors(*node, temp_room):
                    if neighbor not in reached:
                        reached.add(neighbor)
                        frontier.append((neighbor, path + [neighbor]))   
            if target_path is None: break
            full_path.extend(target_path[1:])
            current = target_path[-1]
            temp_room[current[0]][current[1]] = 0
        return full_path
    def dfs_recursive_algorithm(self):
        temp_room = copy.deepcopy(self.room)
        full_path = [self.robot_position]
        def find_next_dirt_dfs_rec(node, path, explored):
            explored.add(node)
            if temp_room[node[0]][node[1]] == 1:
                return path
            for neighbor in self.get_neighbors(*node, temp_room):
                if neighbor not in explored:
                    result = find_next_dirt_dfs_rec(neighbor, path + [neighbor], explored)
                    if result is not None:
                        return result
            return None
        current = self.robot_position
        while True:
            if temp_room[current[0]][current[1]] == 1:
                temp_room[current[0]][current[1]] = 0
            explored_set = set()
            target_path = find_next_dirt_dfs_rec(current, [current], explored_set)
            if target_path is None or len(target_path) <= 1: break
            full_path.extend(target_path[1:])
            current = target_path[-1]
            temp_room[current[0]][current[1]] = 0
        return full_path
    def ucs_algorithm(self):
        start = self.robot_position
        full_path = [start]
        temp_room = copy.deepcopy(self.room)
        current = start
        while True:
            if temp_room[current[0]][current[1]] == 1:
                temp_room[current[0]][current[1]] = 0
            frontier = [(0, current, [current])]
            explored = set()
            target_path = None
            while frontier:
                cost, node, path = heapq.heappop(frontier)
                if node in explored: continue
                explored.add(node)
                if temp_room[node[0]][node[1]] == 1:
                    target_path = path
                    break
                for neighbor in self.get_neighbors(*node, temp_room):
                    if neighbor not in explored:
                        heapq.heappush(frontier, (cost + 1, neighbor, path + [neighbor]))
            if target_path is None: break
            full_path.extend(target_path[1:])
            current = target_path[-1]
            temp_room[current[0]][current[1]] = 0
        return full_path
    def ids_stack_algorithm(self):
        start = self.robot_position
        full_path = [start]
        temp_room = copy.deepcopy(self.room)
        current = start
        def dls_stack(src, max_depth):
            frontier = [(src, [src], 0)]
            while frontier:
                node, path, depth = frontier.pop()
                if temp_room[node[0]][node[1]] == 1:
                    return path
                if depth < max_depth:
                    for neighbor in self.get_neighbors(*node, temp_room):
                        if neighbor not in path:
                            frontier.append((neighbor, path + [neighbor], depth + 1))
            return None
        while True:
            if temp_room[current[0]][current[1]] == 1:
                temp_room[current[0]][current[1]] = 0
            target_path = None
            for depth in range(self.rows * self.cols):
                target_path = dls_stack(current, depth)
                if target_path: break
            if target_path is None: break
            full_path.extend(target_path[1:])
            current = target_path[-1]
            temp_room[current[0]][current[1]] = 0
        return full_path
    def ids_recursive_algorithm(self):
        start = self.robot_position
        full_path = [start]
        temp_room = copy.deepcopy(self.room)
        current = start
        def dls_recursive(node, path, depth):
            if temp_room[node[0]][node[1]] == 1:
                return path
            if depth <= 0:
                return None
            for neighbor in self.get_neighbors(*node, temp_room):
                if neighbor not in path:
                    res = dls_recursive(neighbor, path + [neighbor], depth - 1)
                    if res: return res
            return None
        while True:
            if temp_room[current[0]][current[1]] == 1:
                temp_room[current[0]][current[1]] = 0
            target_path = None
            for depth in range(self.rows * self.cols):
                target_path = dls_recursive(current, [current], depth)
                if target_path: break
            if target_path is None: break
            full_path.extend(target_path[1:])
            current = target_path[-1]
            temp_room[current[0]][current[1]] = 0
        return full_path
    def greedy_algorithm(self):
        start = self.robot_position
        full_path = [start]
        temp_room = copy.deepcopy(self.room)
        current = start
        def get_nearest_dirt_heuristic(node):
            min_dist = float('inf')
            for r in range(self.rows):
                for c in range(self.cols):
                    if temp_room[r][c] == 1:
                        dist = self.Manhattan_distance(node, (r, c))
                        if dist < min_dist: min_dist = dist
            return min_dist if min_dist != float('inf') else 0
        while True:
            if temp_room[current[0]][current[1]] == 1:
                temp_room[current[0]][current[1]] = 0
            frontier = [(get_nearest_dirt_heuristic(current), current, [current])]
            explored = set()
            target_path = None
            while frontier:
                h, node, path = heapq.heappop(frontier)
                if node in explored: continue
                explored.add(node)
                if temp_room[node[0]][node[1]] == 1:
                    target_path = path
                    break
                for neighbor in self.get_neighbors(*node, temp_room):
                    if neighbor not in explored:
                        heapq.heappush(frontier, (get_nearest_dirt_heuristic(neighbor), neighbor, path + [neighbor]))
            if target_path is None: break
            full_path.extend(target_path[1:])
            current = target_path[-1]
            temp_room[current[0]][current[1]] = 0
        return full_path
    def astar_algorithm(self):
        start = self.robot_position
        full_path = [start]
        temp_room = copy.deepcopy(self.room)
        current = start
        def get_nearest_dirt_heuristic(node):
            min_dist = float('inf')
            for r in range(self.rows):
                for c in range(self.cols):
                    if temp_room[r][c] == 1:
                        dist = self.Manhattan_distance(node, (r, c))
                        if dist < min_dist: min_dist = dist
            return min_dist if min_dist != float('inf') else 0
        while True:
            if temp_room[current[0]][current[1]] == 1:
                temp_room[current[0]][current[1]] = 0
            frontier = [(get_nearest_dirt_heuristic(current), 0, current, [current])]
            explored = set()
            target_path = None
            while frontier:
                f, g, node, path = heapq.heappop(frontier)
                if node in explored: continue
                explored.add(node)
                if temp_room[node[0]][node[1]] == 1:
                    target_path = path
                    break
                for neighbor in self.get_neighbors(*node, temp_room):
                    if neighbor not in explored:
                        new_g = g + 1
                        new_f = new_g + get_nearest_dirt_heuristic(neighbor)
                        heapq.heappush(frontier, (new_f, new_g, neighbor, path + [neighbor]))
            if target_path is None: break
            full_path.extend(target_path[1:])
            current = target_path[-1]
            temp_room[current[0]][current[1]] = 0
        return full_path
    def idastar_algorithm(self):
        start = self.robot_position
        full_path = [start]
        temp_room = copy.deepcopy(self.room)
        current = start
        def get_nearest_dirt_heuristic(node):
            min_dist = float('inf')
            for r in range(self.rows):
                for c in range(self.cols):
                    if temp_room[r][c] == 1:
                        dist = self.Manhattan_distance(node, (r, c))
                        if dist < min_dist: min_dist = dist
            return min_dist if min_dist != float('inf') else 0
        def dfs_contour(node, path, g, bound):
            f = g + get_nearest_dirt_heuristic(node)
            if f > bound: return f, None
            if temp_room[node[0]][node[1]] == 1: return f, path
            min_val = float('inf')
            for neighbor in self.get_neighbors(*node, temp_room):
                if neighbor not in path:
                    t, res = dfs_contour(neighbor, path + [neighbor], g + 1, bound)
                    if res is not None: return t, res
                    if t < min_val: min_val = t
            return min_val, None
        while True:
            if temp_room[current[0]][current[1]] == 1:
                temp_room[current[0]][current[1]] = 0
            bound = get_nearest_dirt_heuristic(current)
            target_path = None
            while True:
                t, target_path = dfs_contour(current, [current], 0, bound)
                if target_path is not None: break
                if t == float('inf'): break
                bound = t
            if target_path is None: break
            full_path.extend(target_path[1:])
            current = target_path[-1]
            temp_room[current[0]][current[1]] = 0
        return full_path
    def simple_hill_climbing_algorithm(self):
        start = self.robot_position
        full_path = [start]
        temp_room = copy.deepcopy(self.room)
        current = start
        def calculate_room_value(room_state):
            return -sum(row.count(1) for row in room_state)
        while True:
            if temp_room[current[0]][current[1]] == 1:
                temp_room[current[0]][current[1]] = 0
            current_value = calculate_room_value(temp_room)
            neighbors = self.get_neighbors(*current, temp_room)
            next_state = None
            for neighbor in neighbors:
                next_room = copy.deepcopy(temp_room)
                if next_room[neighbor[0]][neighbor[1]] == 1:
                    next_room[neighbor[0]][neighbor[1]] = 0
                if calculate_room_value(next_room) > current_value:
                    next_state = neighbor
                    break
            if next_state is None:
                dirt_cells = []
                for r in range(self.rows):
                    for c in range(self.cols):
                        if temp_room[r][c] == 1:
                            dirt_cells.append((r, c))
                if not dirt_cells: break
                nearest_dirt = min(dirt_cells, key=lambda pos: self.Manhattan_distance(current, pos))
                frontier = deque([(current, [current])])
                reached = {current}
                escape_path = None
                while frontier:
                    node, path = frontier.popleft()
                    if node == nearest_dirt:
                        escape_path = path
                        break
                    for neighbor in self.get_neighbors(*node, temp_room):
                        if neighbor not in reached:
                            reached.add(neighbor)
                            frontier.append((neighbor, path + [neighbor]))
                if escape_path is None or len(escape_path) <= 1: break
                full_path.extend(escape_path[1:])
                current = escape_path[-1]
            else:
                full_path.append(next_state)
                current = next_state
        return full_path
    def steepest_ascent_hill_climbing_algorithm(self):
        start = self.robot_position
        full_path = [start]
        temp_room = copy.deepcopy(self.room)
        current = start
        def calculate_room_value(room_state):
            return -sum(row.count(1) for row in room_state)
        while True:
            if temp_room[current[0]][current[1]] == 1:
                temp_room[current[0]][current[1]] = 0
            current_value = calculate_room_value(temp_room)
            neighbors = self.get_neighbors(*current, temp_room)
            best_neighbor = None
            best_value = current_value
            for neighbor in neighbors:
                next_room = copy.deepcopy(temp_room)
                if next_room[neighbor[0]][neighbor[1]] == 1:
                    next_room[neighbor[0]][neighbor[1]] = 0
                val = calculate_room_value(next_room)
                if val > best_value:
                    best_value = val
                    best_neighbor = neighbor
            if best_neighbor is None:
                dirt_cells = []
                for r in range(self.rows):
                    for c in range(self.cols):
                        if temp_room[r][c] == 1:
                            dirt_cells.append((r, c))
                if not dirt_cells: break
                nearest_dirt = min(dirt_cells, key=lambda pos: self.Manhattan_distance(current, pos))
                frontier = deque([(current, [current])])
                reached = {current}
                escape_path = None
                while frontier:
                    node, path = frontier.popleft()
                    if node == nearest_dirt:
                        escape_path = path
                        break
                    for neighbor in self.get_neighbors(*node, temp_room):
                        if neighbor not in reached:
                            reached.add(neighbor)
                            frontier.append((neighbor, path + [neighbor]))
                if escape_path is None or len(escape_path) <= 1: break
                full_path.extend(escape_path[1:])
                current = escape_path[-1]
            else:
                full_path.append(best_neighbor)
                current = best_neighbor
        return full_path
    def stochastic_hill_climbing_algorithm(self):
        start = self.robot_position
        full_path = [start]
        temp_room = copy.deepcopy(self.room)
        current = start
        def calculate_room_value(room_state):
            return -sum(row.count(1) for row in room_state)
        while True:
            if temp_room[current[0]][current[1]] == 1:
                temp_room[current[0]][current[1]] = 0
            current_value = calculate_room_value(temp_room)
            neighbors = self.get_neighbors(*current, temp_room)
            better_neighbors = []
            for neighbor in neighbors:
                next_room = copy.deepcopy(temp_room)
                if next_room[neighbor[0]][neighbor[1]] == 1:
                    next_room[neighbor[0]][neighbor[1]] = 0
                if calculate_room_value(next_room) > current_value:
                    better_neighbors.append(neighbor)
            if not better_neighbors:
                dirt_cells = []
                for r in range(self.rows):
                    for c in range(self.cols):
                        if temp_room[r][c] == 1:
                            dirt_cells.append((r, c))
                if not dirt_cells: break
                nearest_dirt = min(dirt_cells, key=lambda pos: self.Manhattan_distance(current, pos))
                frontier = deque([(current, [current])])
                reached = {current}
                escape_path = None
                while frontier:
                    node, path = frontier.popleft()
                    if node == nearest_dirt:
                        escape_path = path
                        break
                    for neighbor in self.get_neighbors(*node, temp_room):
                        if neighbor not in reached:
                            reached.add(neighbor)
                            frontier.append((neighbor, path + [neighbor]))
                if escape_path is None or len(escape_path) <= 1: break
                full_path.extend(escape_path[1:])
                current = escape_path[-1]
            else:
                next_state = random.choice(better_neighbors)
                full_path.append(next_state)
                current = next_state
        return full_path
    def run_bfs_queue(self): self.reset_animation(); self.animate(self.bfs_queue_algorithm(), "BFS QUEUE")
    def run_bfs_recursive(self): self.reset_animation(); self.animate(self.bfs_recursive_algorithm(), "BFS RECURSIVE")
    def run_dfs_stack(self): self.reset_animation(); self.animate(self.dfs_stack_algorithm(), "DFS STACK")
    def run_dfs_recursive(self): self.reset_animation(); self.animate(self.dfs_recursive_algorithm(), "DFS RECURSIVE")
    def run_ucs(self): self.reset_animation(); self.animate(self.ucs_algorithm(), "UCS")
    def run_ids_stack(self): self.reset_animation(); self.animate(self.ids_stack_algorithm(), "IDS STACK")
    def run_ids_recursive(self): self.reset_animation(); self.animate(self.ids_recursive_algorithm(), "IDS RECURSIVE")
    def run_greedy(self): self.reset_animation(); self.animate(self.greedy_algorithm(), "GREEDY")
    def run_astar(self): self.reset_animation(); self.animate(self.astar_algorithm(), "A-STAR")
    def run_idastar(self): self.reset_animation(); self.animate(self.idastar_algorithm(), "IDA-STAR")
    def run_simple_hill_climbing(self): self.reset_animation(); self.animate(self.simple_hill_climbing_algorithm(), "SIMPLE HILL CLIMBING")
    def run_steepest_ascent_hill_climbing(self): self.reset_animation(); self.animate(self.steepest_ascent_hill_climbing_algorithm(), "STEEPEST ASCENT HILL CLIMBING")
    def run_stochastic_hill_climbing(self): self.reset_animation(); self.animate(self.stochastic_hill_climbing_algorithm(), "STOCHASTIC HILL CLIMBING")
    def reset_animation(self):
        if self.step_timer:
            self.root.after_cancel(self.step_timer)
        self.room = copy.deepcopy(self.default_room)
        self.robot_position = (0, 0)
        self.path_arrows.clear()
        self.clear_path_box()
        self.draw_room()
    def reset_room(self):
        if self.step_timer:
            self.root.after_cancel(self.step_timer)
        self.room = copy.deepcopy(self.default_room)
        self.robot_position = (0, 0)
        self.path_arrows.clear()
        self.update_info_box("Hệ thống sẵn sàng.")
        self.update_summary_box("Chưa thực hiện lộ trình.")
        self.clear_path_box()
        self.draw_room()
    def animate(self, path, algorithm):
        if not path or len(path) <= 1:
            messagebox.showinfo("Thông báo", "Phòng sạch hoàn toàn hoặc không thể tìm thấy lộ trình!")
            return
        self.step = 0
        start_time = time.time()
        self.clear_path_box()
        self.append_path_log(f"Thuật toán: {algorithm}\nTổng bước cần đi: {len(path)}\n============================\n\n")
        visited_nodes = []
        def move():
            if self.step < len(path):
                x, y = path[self.step]
                visited_nodes.append(f"({x}, {y})")
                if self.step == len(path) - 1:
                    visited_nodes.append("END")
                self.update_summary_box(" -> ".join(visited_nodes))
                if self.step == 0:
                    log_line = f"Bước 1:\nRobot khởi hành từ vị trí ban đầu\nTọa độ hiện tại: ({x}, {y})\n--------------------------------\n"
                    self.append_path_log(log_line)
                else:
                    px, py = path[self.step - 1]
                    possible_directions = self.get_labeled_moves_list(px, py)
                    chosen_direction = self.get_move_direction_upper(px, py, x, y)
                    log_line = f"Bước {self.step + 1}:\nCác hướng có thể đi:\n{possible_directions}\nHướng đã lựa chọn: {chosen_direction} ({x}, {y})\n--------------------------------\n"
                    self.append_path_log(log_line)
                self.robot_position = (x, y)
                if self.room[x][y] == 1:
                    self.room[x][y] = 0
                if self.step > 0:
                    px, py = path[self.step - 1]
                    x1 = self.start_x + py * self.cell_size + self.cell_size // 2
                    y1 = self.start_y + px * self.cell_size + self.cell_size // 2
                    x2 = self.start_x + y * self.cell_size + self.cell_size // 2
                    y2 = self.start_y + x * self.cell_size + self.cell_size // 2
                    self.path_arrows.append((x1, y1, x2, y2))
                self.draw_room()
                dirt_left = sum(row.count(1) for row in self.room)
                info_content = (
                    f"Giải thuật: {algorithm}\n\n"
                    f"Tiến trình bước: {self.step + 1} / {len(path)}\n\n"
                    f"Tọa độ thực: ({x}, {y})\n\n"
                    f"Số lượng bụi còn lại: {dirt_left}\n\n"
                    f"Thời gian: {round(time.time() - start_time, 1)} giây"
                )
                self.update_info_box(info_content)
                self.step += 1
                self.step_timer = self.root.after(350, move)
            else:
                messagebox.showinfo("Hoàn thành dọn dẹp", f"{algorithm} kết thúc chu kỳ thành công!")
        move()
if __name__ == "__main__":
    root = tk.Tk()
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass
    app = VacuumCleanerAI(root)
    root.mainloop()