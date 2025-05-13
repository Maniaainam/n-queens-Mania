import tkinter as tk
from tkinter import ttk
from turtle import width
from solvers.genetic_algorithm_solver import GeneticAlgorithmSolver
from solvers.backtracking_solver import BacktrackingSolver

try:
    from solvers.csp_solver import CSPSolver
    csp_available = True
except ImportError:
    csp_available = False

class MainWindow:
    def __init__(self, master):
        self.master = master
        master.title("N-Queens Solver")

 
        self.bg_color = "#fbf8cc"
        self.label_color = "#000000"
        self.button_bg_color = "#3f37c9"
        self.button_fg_color = "#FFFFFF"
        self.frame_bg_color = "#fbf8cc"
        self.frame_fg_color = "#000000"
        self.board_color_light = "#fef9ef"   
        self.board_color_dark = "#7b2cbf"    
        self.solution_text_color = "#000000"

 
        self.style = ttk.Style()
        self.style.theme_use('clam')


        self.style.configure("Solve.TButton",
                             background=self.button_bg_color,
                             foreground=self.button_fg_color,
                             font=("Arial", 11, "bold"),
                             padding=5,
                             borderwidth=1,
                             relief="raised"
                            )
                             
        self.style.map("Solve.TButton",
                       background=[("active", "#00bbf9"),
                                   ("disabled", self.button_bg_color)],
                       foreground=[("disabled", self.button_fg_color)])


        self.style.configure("Solution.TLabelframe.Label",
                             foreground=self.frame_fg_color,
                             font=("Segoe UI", 12, "bold"))
        self.style.configure("Solution.TLabelframe",
                             background=self.frame_bg_color,
                             padding=15,
                             borderwidth=2,
                             relief="groove")

        master.config(bg=self.bg_color, padx=10, pady=10)

        master.columnconfigure(0, weight=0)
        master.columnconfigure(1, weight=1)
        master.rowconfigure(3, weight=1)

        # عناصر ورودی
        self.n_label = ttk.Label(master, text="Board Size (N):", foreground=self.label_color)
        self.n_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')

        self.n_entry = ttk.Entry(master, foreground="black", width=10)
        self.n_entry.insert(0, "8")
        self.n_entry.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

        self.algorithm_label = ttk.Label(master, text="Algorithm:", foreground=self.label_color)
        self.algorithm_label.grid(row=1, column=0, padx=10, pady=10, sticky='w')

        algorithms = ["Genetic Algorithm", "Backtracking"]
        if csp_available:
            algorithms.append("CSP")
        self.algorithm_combo = ttk.Combobox(master, values=algorithms, foreground="black", width=20, state="readonly")
        self.algorithm_combo.set("Backtracking")
        self.algorithm_combo.grid(row=1, column=1, padx=10, pady=10, sticky='ew')

        # دکمه حل
        self.solve_button = ttk.Button(master, text="Solve", command=self.solve, style="Solve.TButton")
        self.solve_button.grid(row=2, column=0, columnspan=2, pady=15, sticky='')

        # نمایش نتیجه در یک LabelFrame
        self.result_frame = ttk.LabelFrame(master, text="Solution", style="Solution.TLabelframe")
        self.result_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

        self.board_canvas = tk.Canvas(self.result_frame, width=300, height=300, borderwidth=2, relief="groove", bg="white")
        self.board_canvas.pack(padx=10, pady=10, fill='both', expand='true')

        try:
            self.queen_image = tk.PhotoImage(file="queen_icon.png")
        except tk.TclError:
            self.queen_image = None
            print("Could not load queen icon.")

        self.result_label = ttk.Label(self.result_frame,
                                      text="",
                                      foreground=self.solution_text_color,
                                      background=self.frame_bg_color,
                                      font=("Arial", 10))
        self.result_label.pack(padx=10, pady=10, fill='x')

    def display_solution_graphic(self, solution):
        self.board_canvas.delete("all")
        n = len(solution)
        cell_size = self.board_canvas.winfo_width() / n
        for col in range(n):
            for row in range(n):
                x1 = col * cell_size
                y1 = row * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                color = self.board_color_light if (row + col) % 2 == 0 else self.board_color_dark
                self.board_canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")
                if solution[col] == row:
                    if self.queen_image:
                        img_x = x1 + cell_size / 2
                        img_y = y1 + cell_size / 2
                        self.board_canvas.create_image(img_x, img_y, image=self.queen_image)
                    else:
                        self.board_canvas.create_text(x1 + cell_size / 2, y1 + cell_size / 2, text="Q",
                                                      font=("Arial", int(cell_size / 2), "bold"), fill="black")

    def solve(self):
        n = int(self.n_entry.get())
        algorithm = self.algorithm_combo.get()
        self.result_label.config(text="Solving...")
        self.master.update()

        solution = None
        if algorithm == "Genetic Algorithm":
            solver = GeneticAlgorithmSolver(n)
            solution = solver.solve()
        elif algorithm == "Backtracking":
            solver = BacktrackingSolver(n)
            solution = solver.solve()
        elif algorithm == "CSP" and csp_available:
            solver = CSPSolver(n)
            solution = solver.solve()
        else:
            self.result_label.config(text="Algorithm not selected or implemented.")
            return

        if solution:
            self.display_solution_graphic(solution)
            self.result_label.config(text=f"Solution: {solution}")
        else:
            self.result_label.config(text="No solution found.")

def main():
    root = tk.Tk()
    app = MainWindow(root)
    try:
        root.iconbitmap("n_queens_icon.ico")
    except tk.TclError:
        print("Could not load icon.")
    root.mainloop()

if __name__ == "__main__":
    main()
