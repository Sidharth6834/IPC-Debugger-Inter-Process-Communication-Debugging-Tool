import tkinter as tk
import threading
import time
import random


THINKING = "thinking"
HUNGRY   = "hungry"
EATING   = "eating"
DEADLOCK = "deadlock"


class DiningPhilosophersGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Deadlock Visualizer (Dining Philosophers)")
        self.root.geometry("900x600")
        self.root.configure(bg="white")

        self.title = tk.Label(
            self.root,
            text="Dining Philosophers - Deadlock Visualizer",
            bg="white", font=("Arial", 18, "bold")
        )
        self.title.pack(pady=15)

       
        self.canvas = tk.Canvas(self.root, width=850, height=450, bg="white")
        self.canvas.pack()

       
        self.positions = [
            (425, 100),
            (200, 200),
            (300, 380),
            (550, 380),
            (650, 200),
        ]

        self.philosophers = []
        for x, y in self.positions:
            p = self.canvas.create_oval(
                x-40, y-40, x+40, y+40,
                fill="lightgray", outline="black", width=2
            )
            self.philosophers.append(p)

       
        self.state_labels = []
        for i, (x, y) in enumerate(self.positions):
            t = self.canvas.create_text(
                x, y+65, text=f"P{i} - thinking", font=("Arial", 11))
            self.state_labels.append(t)

     
        button_frame = tk.Frame(self.root, bg="white")
        button_frame.pack(pady=15)

        tk.Button(
            button_frame, text="Simulate Deadlock", bg="#FF5722", fg="white",
            width=20, height=2, command=self.simulate_deadlock
        ).grid(row=0, column=0, padx=15)

        tk.Button(
            button_frame, text="Resolve Deadlock", bg="#4CAF50", fg="white",
            width=20, height=2, command=self.resolve_deadlock
        ).grid(row=0, column=1, padx=15)

        self.running = False
        self.deadlock_detected = False
        self.root.mainloop()

    def simulate_deadlock(self):
        if self.running:
            return

        self.running = True
        self.deadlock_detected = False
        threading.Thread(target=self._deadlock_sequence).start()

    def _deadlock_sequence(self):
       
        for i in range(5):
            self._set_state(i, HUNGRY)
            time.sleep(0.7)

      
        self._show_cycle()

       
        for i in range(5):
            self._set_state(i, DEADLOCK)

        self.deadlock_detected = True
        self.running = False

    def resolve_deadlock(self):
        if not self.deadlock_detected:
            return

     
        chosen = random.randint(0, 4)
        self._set_state(chosen, EATING)
        time.sleep(0.5)

     
        for i in range(5):
            if i != chosen:
                self._set_state(i, THINKING)

        self.deadlock_detected = False

   
    def _set_state(self, idx, state):
        colors = {
            THINKING: "lightgray",
            HUNGRY: "yellow",
            EATING: "lightgreen",
            DEADLOCK: "red"
        }

        texts = {
            THINKING: "thinking",
            HUNGRY: "waiting",
            EATING: "eating",
            DEADLOCK: "deadlocked"
        }

        self.canvas.itemconfig(self.philosophers[idx], fill=colors[state])
        self.canvas.itemconfig(self.state_labels[idx], text=f"P{idx} - {texts[state]}")
        self.canvas.update()

    def _show_cycle(self):
        arrows = []
        for i in range(5):
            x1, y1 = self.positions[i]
            x2, y2 = self.positions[(i+1) % 5]

            a = self.canvas.create_line(
                x1, y1, x2, y2, arrow=tk.LAST, width=3, fill="orange"
            )
            arrows.append(a)
            self.canvas.update()
            time.sleep(0.4)

       
        for _ in range(3):
            for a in arrows:
                self.canvas.itemconfig(a, fill="red")
            self.canvas.update()
            time.sleep(0.3)

            for a in arrows:
                self.canvas.itemconfig(a, fill="orange")
            self.canvas.update()
            time.sleep(0.3)


if __name__ == "__main__":
    DiningPhilosophersGUI()
