import tkinter as tk
from tkinter import ttk, scrolledtext
import subprocess
import threading
import sys
import time


# ---------------------------------------------------------
# ARROW ANIMATION (IPC TAB)
# ---------------------------------------------------------
def animate_arrows(canvas, arrow1, arrow2, color):
    canvas.itemconfig(arrow1, fill=color, width=3)
    canvas.update()
    time.sleep(0.20)

    canvas.itemconfig(arrow2, fill=color, width=3)
    canvas.update()
    time.sleep(0.20)

    canvas.itemconfig(arrow1, fill="black", width=2)
    canvas.itemconfig(arrow2, fill="black", width=2)
    canvas.update()


# ---------------------------------------------------------
# IPC BACKEND PROCESS
# ---------------------------------------------------------
def run_ipc_process(command, output_box, status_label, canvas, arrow1, arrow2, ipc_label_widget):

    ipc_mode = command[-1]   # last argument → --pipe / --queue / --shm / --shm-nolock

    def task():
        status_label.config(text="Running...", fg="blue")
        output_box.delete("1.0", tk.END)

        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        for line in process.stdout:
            output_box.insert(tk.END, line)
            output_box.see(tk.END)

            # --------------------------------------
            # FIXED COLOR LOGIC BASED ON IPC MODE
            # --------------------------------------
            if ipc_mode == "--pipe":
                animate_arrows(canvas, arrow1, arrow2, "yellow")   # bottleneck demo

            elif ipc_mode == "--queue":
                animate_arrows(canvas, arrow1, arrow2, "green")

            elif ipc_mode == "--shm":
                animate_arrows(canvas, arrow1, arrow2, "green")    # safe with lock

            elif ipc_mode == "--shm-nolock":
                animate_arrows(canvas, arrow1, arrow2, "red")      # race condition

        process.wait()
        status_label.config(text="Finished", fg="green")

    threading.Thread(target=task).start()


# ---------------------------------------------------------
# DEADLOCK VISUALIZER TAB (Dining Philosophers)
# ---------------------------------------------------------
class DeadlockTab:
    THINKING = "thinking"
    HUNGRY = "hungry"
    EATING = "eating"
    DEADLOCK = "deadlock"

    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill="both", expand=True)

        tk.Label(
            self.frame,
            text="Deadlock Visualizer - Dining Philosophers",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        self.canvas = tk.Canvas(self.frame, width=900, height=450, bg="white")
        self.canvas.pack(pady=10)

        # Philosopher positions
        self.positions = [
            (450, 100),
            (220, 200),
            (320, 380),
            (580, 380),
            (680, 200),
        ]

        # Circles (philosophers)
        self.philosophers = []
        for x, y in self.positions:
            p = self.canvas.create_oval(x - 40, y - 40, x + 40, y + 40,
                                        fill="lightgray", outline="black", width=2)
            self.philosophers.append(p)

        # State labels under philosophers
        self.state_labels = []
        for i, (x, y) in enumerate(self.positions):
            t = self.canvas.create_text(
                x, y + 65, text=f"P{i} - thinking", font=("Arial", 11)
            )
            self.state_labels.append(t)

        # Buttons
        btn_frame = tk.Frame(self.frame)
        btn_frame.pack(pady=15)

        tk.Button(
            btn_frame, text="Simulate Deadlock", width=20, height=2,
            bg="#FF5722", fg="white", command=self.simulate_deadlock
        ).grid(row=0, column=0, padx=20)

        tk.Button(
            btn_frame, text="Resolve Deadlock", width=20, height=2,
            bg="#4CAF50", fg="white", command=self.resolve_deadlock
        ).grid(row=0, column=1, padx=20)

        self.running = False
        self.deadlock_detected = False

        # NEW: store cycle arrows so we can delete after resolve
        self.cycle_arrows = []

    # -------------------------------------------------
    # UPDATE PHILOSOPHER STATE
    # -------------------------------------------------
    def _set_state(self, idx, state):
        colors = {
            self.THINKING: "lightgray",
            self.HUNGRY: "yellow",
            self.EATING: "lightgreen",
            self.DEADLOCK: "red"
        }
        texts = {
            self.THINKING: "thinking",
            self.HUNGRY: "waiting",
            self.EATING: "eating",
            self.DEADLOCK: "deadlocked"
        }

        self.canvas.itemconfig(self.philosophers[idx], fill=colors[state])
        self.canvas.itemconfig(self.state_labels[idx], text=f"P{idx} - {texts[state]}")
        self.canvas.update()

    # -------------------------------------------------
    # SIMULATE DEADLOCK
    # -------------------------------------------------
    def simulate_deadlock(self):
        if self.running:
            return
        self.running = True
        threading.Thread(target=self._simulate_sequence).start()

    def _simulate_sequence(self):
        # All become hungry → circular wait
        for i in range(5):
            self._set_state(i, self.HUNGRY)
            time.sleep(0.6)

        # Show circular arrows
        self._show_cycle()

        # All deadlocked
        for i in range(5):
            self._set_state(i, self.DEADLOCK)

        self.deadlock_detected = True
        self.running = False

    # -------------------------------------------------
    # RESOLVE DEADLOCK
    # -------------------------------------------------
    def resolve_deadlock(self):
        if not self.deadlock_detected:
            return

        import random
        chosen = random.randint(0, 4)

        # One philosopher eats (break cycle)
        self._set_state(chosen, self.EATING)
        time.sleep(0.5)

        # Others go back to thinking
        for i in range(5):
            if i != chosen:
                self._set_state(i, self.THINKING)

        # NEW: remove all cycle arrows
        for a in self.cycle_arrows:
            self.canvas.delete(a)

        self.cycle_arrows = []
        self.canvas.update()

        self.deadlock_detected = False

    # -------------------------------------------------
    # DRAW CIRCULAR WAIT ARROWS
    # -------------------------------------------------
    def _show_cycle(self):
        self.cycle_arrows = []

        # create cycle arrows one by one
        for i in range(5):
            x1, y1 = self.positions[i]
            x2, y2 = self.positions[(i + 1) % 5]

            arrow = self.canvas.create_line(
                x1, y1, x2, y2, arrow=tk.LAST, width=3, fill="orange"
            )
            self.cycle_arrows.append(arrow)

            self.canvas.update()
            time.sleep(0.25)

        # Flash cycle red/orange
        for _ in range(2):
            for a in self.cycle_arrows:
                self.canvas.itemconfig(a, fill="red")
            self.canvas.update()
            time.sleep(0.3)

            for a in self.cycle_arrows:
                self.canvas.itemconfig(a, fill="orange")
            self.canvas.update()
            time.sleep(0.3)


# ---------------------------------------------------------
# MAIN APPLICATION WITH TABS
# ---------------------------------------------------------
def main():
    root = tk.Tk()
    root.title("IPC Debugger + Deadlock Visualizer")
    root.geometry("1200x900")

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)

    # =====================================================
    # TAB 1 — IPC DEBUGGER
    # =====================================================
    ipc_tab = ttk.Frame(notebook)
    notebook.add(ipc_tab, text="IPC Debugger")

    canvas = tk.Canvas(ipc_tab, width=1100, height=250, bg="white")
    canvas.pack(pady=10)

    # Process A
    canvas.create_rectangle(70, 80, 240, 160, fill="#BDE0FE", outline="black", width=2)
    canvas.create_text(155, 120, text="Process A", font=("Arial", 12, "bold"))

    # IPC Box
    ipc_box = canvas.create_rectangle(380, 80, 560, 160, fill="#FFF3B0", outline="black", width=2)
    ipc_label = canvas.create_text(470, 120, text="IPC", font=("Arial", 12, "bold"))

    # Process B
    canvas.create_rectangle(700, 80, 870, 160, fill="#C4F7C3", outline="black", width=2)
    canvas.create_text(785, 120, text="Process B", font=("Arial", 12, "bold"))

    # Arrows A→IPC and IPC→B
    arrow1 = canvas.create_line(240, 120, 380, 120, arrow=tk.LAST, width=2)
    arrow2 = canvas.create_line(560, 120, 700, 120, arrow=tk.LAST, width=2)

    # Output area
    output_box = scrolledtext.ScrolledText(ipc_tab, height=20, width=125)
    output_box.pack(pady=10)

    status_label = tk.Label(ipc_tab, text="Idle", font=("Arial", 12))
    status_label.pack()

    # Buttons
    btn_frame = tk.Frame(ipc_tab)
    btn_frame.pack(pady=15)

    buttons = [
        ("Pipe", "--pipe", "#4CAF50", "Pipe"),
        ("Queue", "--queue", "#2196F3", "Queue"),
        ("SHM (Lock)", "--shm", "#FF9800", "SHM (Lock)"),
        ("SHM (No Lock)", "--shm-nolock", "#F44336", "SHM (No Lock)"),
    ]

    for idx, (btn_text, cmd, color, ipc_text) in enumerate(buttons):
        tk.Button(
            btn_frame, text=btn_text, width=22, height=2,
            bg=color, fg="white",
            command=lambda c=cmd, it=ipc_text: [
                canvas.itemconfig(ipc_label, text=it),
                run_ipc_process(
                    [sys.executable, "step1_demo.py", c],
                    output_box, status_label, canvas, arrow1, arrow2, ipc_label
                )
            ]
        ).grid(row=0, column=idx, padx=15)

    # =====================================================
    # TAB 2 — DEADLOCK VISUALIZER
    # =====================================================
    deadlock_tab = DeadlockTab(notebook)
    notebook.add(deadlock_tab.frame, text="Deadlock Visualizer")

    root.mainloop()


if __name__ == "__main__":
    main()
