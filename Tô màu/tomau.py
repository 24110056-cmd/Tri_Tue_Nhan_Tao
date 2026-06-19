import cv2
import numpy as np
import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import colorchooser

ctk.set_appearance_mode("Dark")  
ctk.set_default_color_theme("blue") 

class MapColoringApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("HCMC Ward Coloring Tool - 4 Solvers System")
        self.geometry("1420x920")

        # 1. Đọc dữ liệu ảnh gốc
        self.image_path = "bando.jpg"
        self.cv_img = cv2.imread(self.image_path)
        
        if self.cv_img is None:
            print("LỖI: Không tìm thấy file ảnh bando.jpg!")
            self.destroy()
            return
            
        self.cv_img_colored = self.cv_img.copy()
        self.is_running_auto = False

        # DANH SÁCH TÊN PHƯỜNG / XÃ THỰC TẾ TẠI TP.HCM
        self.hcmc_wards_pool = [
            "Phường Bến Nghé (Q1)", "Phường Bến Thành (Q1)", "Phường Cô Giang (Q1)", "Phường Cầu Kho (Q1)",
            "Phường Cầu Ông Lãnh (Q1)", "Phường Đa Kao (Q1)", "Phường Nguyễn Cư Trinh (Q1)", "Phường Nguyễn Thái Bình (Q1)",
            "Phường Phạm Ngũ Lão (Q1)", "Phường Tân Định (Q1)", "Phường Võ Thị Sáu (Q3)", "Phường 1 (Q3)",
            "Phường 2 (Q3)", "Phường 3 (Q3)", "Phường 4 (Q3)", "Phường 5 (Q3)",
            "Phường 9 (Q3)", "Phường 10 (Q3)", "Phường 11 (Q3)", "Phường 12 (Q3)",
            "Phường 13 (Q3)", "Phường 14 (Q3)", "Phường 1 (Q4)", "Phường 2 (Q4)",
            "Phường 3 (Q4)", "Phường 4 (Q4)", "Phường 6 (Q4)", "Phường 8 (Q4)",
            "Phường 9 (Q4)", "Phường 10 (Q4)", "Phường 13 (Q4)", "Phường 14 (Q4)",
            "Phường 15 (Q4)", "Phường 16 (Q4)", "Phường 1 (Q5)", "Phường 2 (Q5)",
            "Phường 3 (Q5)", "Phường 4 (Q5)", "Phường 5 (Q5)", "Phường 6 (Q5)",
            "Phường 7 (Q5)", "Phường 8 (Q5)", "Phường 9 (Q5)", "Phường 10 (Q5)",
            "Phường 11 (Q5)", "Phường 12 (Q5)", "Phường 13 (Q5)", "Phường 14 (Q5)",
            "Phường 1 (Q6)", "Phường 2 (Q6)", "Phường 3 (Q6)", "Phường 4 (Q6)",
            "Phường 5 (Q6)", "Phường 6 (Q6)", "Phường 7 (Q6)", "Phường 8 (Q6)",
            "Phường 9 (Q6)", "Phường 10 (Q6)", "Phường 11 (Q6)", "Phường 12 (Q6)",
            "Phường 13 (Q6)", "Phường 14 (Q6)", "Phường 1 (Q7)", "Phường 2 (Q7)",
            "Phường Tân Kiểng (Q7)", "Phường Tân Phong (Q7)", "Phường Tân Phú (Q7)", "Phường Tân Quy (Q7)",
            "Phường Tân Thuận Đông (Q7)", "Phường Tân Thuận Tây (Q7)", "Phường Phú Mỹ (Q7)", "Phường Phú Thuận (Q7)",
            "Phường 1 (Q8)", "Phường 2 (Q8)", "Phường 3 (Q8)", "Phường 4 (Q8)",
            "Phường 5 (Q8)", "Phường 6 (Q8)", "Phường 7 (Q8)", "Phường 8 (Q8)",
            "Phường 9 (Q8)", "Phường 10 (Q8)", "Phường 11 (Q8)", "Phường 12 (Q8)",
            "Phường 13 (Q8)", "Phường 14 (Q8)", "Phường 15 (Q8)", "Phường 16 (Q8)",
            "Phường 1 (Q10)", "Phường 2 (Q10)", "Phường 4 (Q10)", "Phường 5 (Q10)",
            "Phường 6 (Q10)", "Phường 7 (Q10)", "Phường 8 (Q10)", "Phường 9 (Q10)",
            "Phường 11 (Q10)", "Phường 12 (Q10)", "Phường 13 (Q10)", "Phường 14 (Q10)",
            "Phường 15 (Q10)", "Phường 1 (Q11)", "Phường 2 (Q11)", "Phường 3 (Q11)",
            "Phường 4 (Q11)", "Phường 5 (Q11)", "Phường 6 (Q11)", "Phường 7 (Q11)",
            "Phường 8 (Q11)", "Phường 9 (Q11)", "Phường 10 (Q11)", "Phường 11 (Q11)",
            "Phường 12 (Q11)", "Phường 13 (Q11)", "Phường 14 (Q11)", "Phường 15 (Q11)",
            "Phường 16 (Q11)", "Phường Thạnh Xuân (Q12)", "Phường Thạnh Lộc (Q12)", "Phường Hiệp Thành (Q12)",
            "Phường Thới An (Q12)", "Phường Tân Chánh Hiệp (Q12)", "Phường Tân Thới Hiệp (Q12)", "Phường Tân Thới Nhất (Q12)",
            "Phường Tân Hưng Thuận (Q12)", "Phường Đông Hưng Thuận (Q12)", "Phường Trung Mỹ Tây (Q12)", "Phường An Phú Đông (Q12)",
            "Phường Linh Đông (Thủ Đức)", "Phường Linh Tây (Thủ Đức)", "Phường Linh Chiểu (Thủ Đức)", "Phường Linh Trung (Thủ Đức)",
            "Phường Linh Xuân (Thủ Đức)", "Phường Hiệp Bình Chánh (Thủ Đức)", "Phường Hiệp Bình Phước (Thủ Đức)", "Phường Tam Bình (Thủ Đức)",
            "Phường Tam Phú (Thủ Đức)", "Phường Bình Chiểu (Thủ Đức)", "Phường Trường Thọ (Thủ Đức)", "Phường Bình Thọ (Thủ Đức)",
            "Phường Long Bình (Q9 cũ)", "Phường Long Thạnh Mỹ (Q9 cũ)", "Phường Tân Phú (Q9 cũ)", "Phường Hiệp Phú (Q9 cũ)",
            "Phường Tăng Nhơn Phú A (Q9 cũ)", "Phường Tăng Nhơn Phú B (Q9 cũ)", "Phường Phước Long A (Q9 cũ)", "Phường Phước Long B (Q9 cũ)",
            "Phường Phước Bình (Q9 cũ)", "Phường Long Trường (Q9 cũ)", "Phường Trường Thạnh (Q9 cũ)", "Phường Long Phước (Q9 cũ)",
            "Phường Phú Hữu (Q9 cũ)", "Phường An Khánh (Q2 cũ)", "Phường An Lợi Đông (Q2 cũ)", "Phường An Phú (Q2 cũ)",
            "Phường Bình An (Q2 cũ)", "Phường Bình Khánh (Q2 cũ)", "Phường Bình Trưng Đông (Q2 cũ)", "Phường Bình Trưng Tây (Q2 cũ)",
            "Phường Cát Lái (Q2 cũ)", "Phường Thạnh Mỹ Lợi (Q2 cũ)", "Phường Thảo Điền (Q2 cũ)", "Phường Thủ Thiêm (Q2 cũ)"
        ]

        self.selected_panel_color_bgr = (34, 126, 230) 
        self.contours = []  
        self.color_assignment = {} 

        self.detect_all_wards()

        self.wards_data = []
        for i in range(len(self.contours)):
            name = self.hcmc_wards_pool[i] if i < len(self.hcmc_wards_pool) else f"Phường dự phòng {i + 1}"
            self.wards_data.append({"name": name, "color": [255, 255, 255]})

        # Bảng màu Palette đa dạng hỗ trợ tốt cho đồ thị lớn
        self.color_palette = [
            (76, 204, 46),   # Xanh lá
            (219, 152, 52),  # Cam
            (182, 89, 155),  # Tím
            (15, 196, 241),  # Xanh lam
            (60, 76, 231),   # Đỏ hồng
            (156, 188, 26),  # Mạ non
            (120, 40, 200)   # Tím sẫm
        ]

        # Layout chính
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ---- SIDEBAR ĐIỀU KHIỂN ----
        self.sidebar = ctk.CTkFrame(self, width=320, corner_radius=0, fg_color="#f1f5f9")
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        self.lbl_control = ctk.CTkLabel(self.sidebar, text="CONTROL PANEL", text_color="#000000", font=ctk.CTkFont(weight="bold", size=13))
        self.lbl_control.pack(anchor="w", padx=15, pady=(15, 5))
        
        self.lbl_algo = ctk.CTkLabel(self.sidebar, text="Select Algorithm:", text_color="#475569", font=ctk.CTkFont(size=12))
        self.lbl_algo.pack(anchor="w", padx=15, pady=(2, 2))
        
        # Menu đổ xuống gồm 4 thuật toán độc lập rõ ràng
        self.algo_option = ctk.CTkOptionMenu(
            self.sidebar, 
            values=[
                "1. Sequential Color", 
                "2. Pure Backtracking", 
                "3. Min-Conflicts", 
                "4. Backtracking + AC-3 Filter"
            ],
            fg_color="#ffffff", text_color="#0f172a", button_color="#cbd5e1",
            button_hover_color="#94a3b8", dropdown_fg_color="#ffffff", 
            dropdown_text_color="#0f172a", corner_radius=6
        )
        self.algo_option.pack(fill="x", padx=15, pady=(0, 10))

        self.btn_run = ctk.CTkButton(self.sidebar, text="RUN ALGORITHM", fg_color="#23a95d", hover_color="#1b8549", text_color="#ffffff", font=ctk.CTkFont(weight="bold"), corner_radius=6, command=self.start_auto_coloring)
        self.btn_run.pack(fill="x", padx=15, pady=5)

        self.lbl_manual = ctk.CTkLabel(self.sidebar, text="MANUAL COLORING", text_color="#000000", font=ctk.CTkFont(weight="bold", size=13))
        self.lbl_manual.pack(anchor="w", padx=15, pady=(15, 5))

        self.wards_list_frame = ctk.CTkScrollableFrame(self.sidebar, height=350, fg_color="#ffffff", corner_radius=4, border_width=1, border_color="#cbd5e1")
        self.wards_list_frame.pack(fill="x", padx=15, pady=5)
        
        self.ward_buttons_map = {} 
        self.render_wards_panel()

        self.btn_reset = ctk.CTkButton(self.sidebar, text="Reset Map", fg_color="#e0f2fe", text_color="#0369a1", hover_color="#bae6fd", font=ctk.CTkFont(weight="bold"), corner_radius=6, command=self.reset_map)
        self.btn_reset.pack(fill="x", padx=15, pady=5)

        self.sidebar_stats = ctk.CTkFrame(self.sidebar, fg_color="#f8fafc", corner_radius=6, border_width=1, border_color="#cbd5e1")
        self.sidebar_stats.pack(fill="x", padx=15, pady=15)
        
        self.lbl_stats_title = ctk.CTkLabel(self.sidebar_stats, text="STATISTICS", text_color="#000000", font=ctk.CTkFont(weight="bold", size=13))
        self.lbl_stats_title.pack(anchor="w", padx=10, pady=(5, 2))
        
        self.lbl_total_wards = ctk.CTkLabel(self.sidebar_stats, text=f"Total Wards Found: {len(self.contours)}", text_color="#334155", font=ctk.CTkFont(size=12))
        self.lbl_total_wards.pack(anchor="w", padx=10)
        
        self.lbl_colored_count = ctk.CTkLabel(self.sidebar_stats, text="Colored Wards: 0", text_color="#2563eb", font=ctk.CTkFont(size=12))
        self.lbl_colored_count.pack(anchor="w", padx=10, pady=(0, 5))

        # ---- KHU VỰC HIỂN THỊ BẢN ĐỒ ----
        self.map_container = ctk.CTkScrollableFrame(self, fg_color="#64748b", corner_radius=0)
        self.map_container.grid(row=0, column=1, sticky="nsew")

        self.map_label = ctk.CTkLabel(self.map_container, text="")
        self.map_label.pack(padx=10, pady=10, expand=True)
        self.map_label.bind("<Button-1>", self.on_map_click)

        self.update_map_display()

    def detect_all_wards(self):
        gray = cv2.cvtColor(self.cv_img, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        
        h_img, w_img = self.cv_img.shape[:2]
        total_image_area = h_img * w_img

        valid_contours = []
        for c in contours:
            area = cv2.contourArea(c)
            x, y, w, h = cv2.boundingRect(c)
            if y > int(h_img * 0.88) or area < 150 or area > (total_image_area * 0.65):
                continue
            valid_contours.append(c)
            
        self.contours = sorted(valid_contours, key=lambda ctr: (cv2.boundingRect(ctr)[1], cv2.boundingRect(ctr)[0]))

    def build_strict_adjacency_matrix(self):
        n = len(self.contours)
        adj_matrix = np.zeros((n, n), dtype=bool)
        masks = []
        img_shape = self.cv_img.shape[:2]
        
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (6, 6))
        for c in self.contours:
            m = np.zeros(img_shape, dtype=np.uint8)
            cv2.drawContours(m, [c], -1, 255, -1)
            m_dilated = cv2.dilate(m, kernel)
            masks.append(m_dilated)

        for i in range(n):
            for j in range(i + 1, n):
                overlap = cv2.bitwise_and(masks[i], masks[j])
                if np.any(overlap > 0):
                    adj_matrix[i][j] = True
                    adj_matrix[j][i] = True
        return adj_matrix

    # ==================== 1. THUẬT TOÁN SEQUENTIAL COLOR ====================
    def run_sequential_coloring(self, adj_matrix):
        n = len(self.contours)
        color_res = {}
        for i in range(n):
            available_colors = [True] * len(self.color_palette)
            for neighbor in range(n):
                if adj_matrix[i][neighbor] and neighbor in color_res:
                    neighbor_color = color_res[neighbor]
                    available_colors[neighbor_color] = False
            
            chosen_idx = 0
            for idx, allowed in enumerate(available_colors):
                if allowed:
                    chosen_idx = idx
                    break
            color_res[i] = chosen_idx
        return color_res

    # ==================== 2. THUẬT TOÁN PURE BACKTRACKING ====================
    def run_pure_backtracking(self, adj_matrix):
        n = len(self.contours)
        color_res = {}

        def backtrack(node):
            if node == n: return True
            for c_idx in range(len(self.color_palette)):
                if any(adj_matrix[node][nb] and color_res.get(nb) == c_idx for nb in range(n)):
                    continue
                color_res[node] = c_idx
                if backtrack(node + 1): return True
                color_res.pop(node, None)
            return False

        backtrack(0)
        return color_res

    # ==================== 3. THUẬT TOÁN MIN-CONFLICTS ====================
    def run_min_conflicts(self, adj_matrix, max_steps=5000):
        n = len(self.contours)
        
        # 1. TÔ MÀU NGẪU NHIÊN TOÀN BỘ BẢN ĐỒ NGAY TỪ ĐẦU
        # Đây là trạng thái "có sẵn màu" trước khi sửa lỗi
        assignment = {i: np.random.randint(0, 5) for i in range(n)}
        
        # Vẽ trạng thái này lên map 1 lần duy nhất
        for i in range(n):
            self.draw_perfect_contour(self.contours[i], self.color_palette[assignment[i]])
        self.update_map_display()
        
        # Hàm đếm xung đột
        def get_conflicts(node, current_assignment):
            return [nb for nb in range(n) if adj_matrix[node][nb] and current_assignment.get(nb) == current_assignment.get(node)]

        # 2. VÒNG LẶP SỬA LỖI (Min-Conflicts chính hiệu)
        for step in range(max_steps):
            # Tìm tất cả các node đang bị xung đột
            conflicted_vars = [v for v in range(n) if len(get_conflicts(v, assignment)) > 0]
            
            # Nếu không còn lỗi thì dừng
            if not conflicted_vars:
                break

            # Chọn ngẫu nhiên 1 node đang bị xung đột
            var = np.random.choice(conflicted_vars)

            # Tìm màu trong 5 màu sao cho node này ít xung đột nhất với hàng xóm
            best_val = assignment[var]
            min_c = len(get_conflicts(var, assignment))
            
            for val in range(5):
                temp_assignment = assignment.copy()
                temp_assignment[var] = val
                c = len(get_conflicts(var, temp_assignment))
                if c < min_c:
                    min_c = c
                    best_val = val
            
            # Cập nhật màu mới
            assignment[var] = best_val
            
            # Chỉ cập nhật lên UI mỗi khi có sự thay đổi màu để bạn thấy nó "tự sửa"
            self.draw_perfect_contour(self.contours[var], self.color_palette[best_val])
            if step % 20 == 0: # Cập nhật màn hình 20 bước 1 lần cho mượt
                self.update_map_display()
            
        self.update_map_display()
        return assignment

    # ==================== 4. THUẬT TOÁN BACKTRACKING + AC-3 FILTER ====================
    def run_backtracking_ac3(self, adj_matrix):
        n = len(self.contours)
        domains = {i: list(range(len(self.color_palette))) for i in range(n)}

        def rm_inconsistent_values(X_i, X_j):
            removed = False
            for x in domains[X_i][:]:
                if not any(x != y for y in domains[X_j]):
                    domains[X_i].remove(x)
                    removed = True
            return removed

        def ac3_filter(node):
            queue = []
            for i in range(n):
                if adj_matrix[node][i]:
                    queue.append((i, node))
            while queue:
                (X_i, X_j) = queue.pop(0)
                if rm_inconsistent_values(X_i, X_j):
                    if not domains[X_i]: return False
                    for k in range(n):
                        if adj_matrix[k][X_i] and k != X_j:
                            queue.append((k, X_i))
            return True

        color_res = {}
        def backtrack(node):
            if node == n: return True
            old_domains = {k: list(v) for k, v in domains.items()}
            
            for c_idx in list(domains[node]):
                if any(adj_matrix[node][nb] and color_res.get(nb) == c_idx for nb in range(n)):
                    continue
                
                color_res[node] = c_idx
                domains[node] = [c_idx]
                
                if ac3_filter(node):
                    if backtrack(node + 1): return True
                
                color_res.pop(node, None)
                for k in old_domains: domains[k] = list(old_domains[k])
            return False

        backtrack(0)
        return color_res

    def start_auto_coloring(self):
        if self.is_running_auto or not self.contours: return
        
        selected_algo = self.algo_option.get()
        self.reset_map()
        self.is_running_auto = True
        self.btn_run.configure(state="disabled", text="RUNNING...")

        # Chạy thuật toán trong luồng riêng để không bị treo giao diện
        import threading
        def process():
            adj_matrix = self.build_strict_adjacency_matrix()

            if "3. Min-Conflicts" in selected_algo:
                # 1. TÔ MÀU NGẪU NHIÊN TOÀN BỘ (Dùng vòng lặp draw_perfect_contour của bạn)
                self.color_assignment = {i: np.random.randint(0, len(self.color_palette)) for i in range(len(self.contours))}
                for i in range(len(self.contours)):
                    self.draw_perfect_contour(self.contours[i], self.color_palette[self.color_assignment[i]])
                self.update_map_display()
                
                # 2. CHẠY ANIMATION SỬA LỖI
                self.after(500, lambda: self.animate_min_conflicts(adj_matrix, 0))
            
            else:
                # Giữ nguyên logic cũ cho các thuật toán khác
                if "1. Sequential" in selected_algo:
                    self.color_assignment = self.run_sequential_coloring(adj_matrix)
                elif "2. Pure Backtracking" in selected_algo:
                    self.color_assignment = self.run_pure_backtracking(adj_matrix)
                else:
                    self.color_assignment = self.run_backtracking_ac3(adj_matrix)
                self.after(0, lambda: self.animate_contour_step(0))

        threading.Thread(target=process, daemon=True).start()
    def animate_min_conflicts(self, adj_matrix, step):
        # Giới hạn 2000 bước để tránh vòng lặp treo
        if step >= 2000:
            self.is_running_auto = False
            self.btn_run.configure(state="normal", text="RUN ALGORITHM")
            return

        n = len(self.contours)
        # Tìm các node đang bị xung đột
        conflicts = [v for v in range(n) if any(adj_matrix[v][nb] and self.color_assignment.get(nb) == self.color_assignment.get(v) for nb in range(n))]
        
        if not conflicts:
            self.is_running_auto = False
            self.btn_run.configure(state="normal", text="RUN ALGORITHM")
            return

        var = np.random.choice(conflicts)
        best_val = self.color_assignment[var]
        min_c = sum(1 for nb in range(n) if adj_matrix[var][nb] and self.color_assignment.get(nb) == best_val)
        
        # Tìm màu tối ưu nhất
        for val in range(len(self.color_palette)):
            c = sum(1 for nb in range(n) if adj_matrix[var][nb] and self.color_assignment.get(nb) == val)
            if c < min_c:
                min_c = c
                best_val = val
        
        # Cập nhật và vẽ lại
        self.color_assignment[var] = best_val
        self.draw_perfect_contour(self.contours[var], self.color_palette[best_val])
        self.update_map_display()
        
        # Tiếp tục bước tiếp theo
        self.after(500, lambda: self.animate_min_conflicts(adj_matrix, step + 1))

    def animate_contour_step(self, current_idx):
        if not self.is_running_auto or current_idx >= len(self.contours):
            self.is_running_auto = False
            self.btn_run.configure(state="normal", text="RUN ALGORITHM")
            return

        contour = self.contours[current_idx]
        palette_idx = self.color_assignment.get(current_idx, 0)
        chosen_color = self.color_palette[palette_idx]

        self.draw_perfect_contour(contour, chosen_color)

        if current_idx < len(self.wards_data):
            self.wards_data[current_idx]["color"] = list(chosen_color)
            hex_color = f"#{chosen_color[2]:02x}{chosen_color[1]:02x}{chosen_color[0]:02x}"
            if current_idx in self.ward_buttons_map:
                self.ward_buttons_map[current_idx].configure(fg_color=hex_color)

        self.lbl_colored_count.configure(text=f"Colored Wards: {current_idx + 1}")
        self.update_map_display()

        self.after(300, lambda: self.animate_contour_step(current_idx + 1))

    def render_wards_panel(self):
        for widget in self.wards_list_frame.winfo_children():
            widget.destroy()
        for idx in range(len(self.contours)):
            if idx >= len(self.wards_data): break
            ward = self.wards_data[idx]
            row_frame = ctk.CTkFrame(self.wards_list_frame, fg_color="transparent", height=32)
            row_frame.pack(fill="x", pady=2)
            row_frame.pack_propagate(False)

            lbl_name = ctk.CTkLabel(row_frame, text=ward["name"], text_color="#334155", font=ctk.CTkFont(size=12), anchor="w")
            lbl_name.pack(side="left", padx=5, expand=True, fill="x")

            b, g, r = ward["color"]
            hex_color = f"#{r:02x}{g:02x}{b:02x}" if [b,g,r] != [255,255,255] else "#ffffff"

            color_btn = ctk.CTkButton(
                row_frame, width=22, height=22, text="", 
                fg_color=hex_color, border_width=1, border_color="#94a3b8",
                hover_color="#cbd5e1", corner_radius=4,
                command=lambda i=idx: self.pick_color_for_ward(i)
            )
            color_btn.pack(side="right", padx=10)
            self.ward_buttons_map[idx] = color_btn

    def pick_color_for_ward(self, ward_idx):
        if ward_idx >= len(self.wards_data): return
        color_code = colorchooser.askcolor(title=f"Chọn màu cho {self.wards_data[ward_idx]['name']}", parent=self)
        if color_code and color_code[0]:
            rgb = color_code[0]
            bgr_color = [int(rgb[2]), int(rgb[1]), int(rgb[0])]
            self.wards_data[ward_idx]["color"] = bgr_color
            self.selected_panel_color_bgr = tuple(bgr_color)
            self.ward_buttons_map[ward_idx].configure(fg_color=color_code[1])

    def update_map_display(self):
        rgb_img = cv2.cvtColor(self.cv_img_colored, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(rgb_img)
        max_width, max_height = 980, 840
        pil_img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
        self.actual_display_w = pil_img.width
        self.actual_display_h = pil_img.height
        self.tk_img = ImageTk.PhotoImage(pil_img)
        self.map_label.configure(image=self.tk_img)

    def draw_perfect_contour(self, contour, color):
        mask = np.zeros(self.cv_img.shape[:2], dtype=np.uint8)
        cv2.drawContours(mask, [contour], -1, 255, -1)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        mask_dilated = cv2.dilate(mask, kernel)
        self.cv_img_colored[mask_dilated > 0] = color

    def on_map_click(self, event):
        if self.is_running_auto: return
        img_w, img_h = self.cv_img.shape[1], self.cv_img.shape[0]
        actual_x = int(event.x * (img_w / self.actual_display_w))
        actual_y = int(event.y * (img_h / self.actual_display_h))

        for idx, contour in enumerate(self.contours):
            if cv2.pointPolygonTest(contour, (actual_x, actual_y), False) >= 0:
                self.draw_perfect_contour(contour, self.selected_panel_color_bgr)
                if idx < len(self.wards_data):
                    self.wards_data[idx]["color"] = list(self.selected_panel_color_bgr)
                    hex_color = f"#{self.selected_panel_color_bgr[2]:02x}{self.selected_panel_color_bgr[1]:02x}{self.selected_panel_color_bgr[0]:02x}"
                    self.ward_buttons_map[idx].configure(fg_color=hex_color)
                self.update_map_display()
                break

    def reset_map(self):
        self.is_running_auto = False
        self.cv_img_colored = self.cv_img.copy()
        for idx in range(len(self.wards_data)):
            self.wards_data[idx]["color"] = [255, 255, 255]
            if idx in self.ward_buttons_map:
                self.ward_buttons_map[idx].configure(fg_color="#ffffff")
        self.lbl_colored_count.configure(text="Colored Wards: 0")
        self.update_map_display()
        self.btn_run.configure(state="normal", text="RUN ALGORITHM")

if __name__ == "__main__":
    app = MapColoringApp()
    app.mainloop()