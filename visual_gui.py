import tkinter as tk
from tkinter import scrolledtext
import subprocess
import sys
import threading
import time


# ------------------------------
# Function to animate arrow
# ------------------------------
def animate_arrow(canvas, arrow_id, color):
    canvas.itemconfig(arrow_id, fill=color, width=3)
    canvas.update()
    time.sleep(0.3)
    canvas.itemconfig(arrow_id, fill="black", width=2)
    canvas.update()
    time.sleep(0.3)


# ------------------------------
# Run a backend IPC command and update GUI
# ------------------------------
def run_ipc_process(command, output_box, status_label, canvas, arrow_id):

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

            # Color logic for arrow animation
            lower_line = line.lower()

            if "bottleneck" in lower_line:
                animate_arrow(canvas, arrow_id, "yellow")

            elif "race" in lower_line or "overwritten" in lower_line:
                animate_arrow(canvas, arrow_id, "red")

            else:
                animate_arrow(canvas, arrow_id, "green")

        process.wait()
        status_label.config(text="Finished", fg="green")

    threading.Thread(target=task).start()


# ------------------------------
# MAIN GUI (Visual + Buttons + Logs)
# ------------------------------
def main_gui():
    root = tk.Tk()
    root.title("IPC Debugger - Visual GUI (Step 3)")
    root.geometry("900x700")
    root.configure(bg="white")

    title = tk.Label(
        root,
        text="IPC Debugger - Visual Simulation (Pipe, Queue, Shared Memory)",
        font=("Arial", 16, "bold"),
        bg="white"
    )
    title.pack(pady=10)

    # Canvas for visual boxes
    canvas = tk.Canvas(root, width=850, height=200, bg="white", highlightthickness=0)
    canvas.pack(pady=10)

    # Process A
    canvas.create_rectangle(50, 60, 200, 140, fill="#D1E8FF", outline="black", width=2)
    canvas.create_text(125, 100, text="Process A", font=("Arial", 12, "bold"))

    # IPC middle box
    ipc_box = canvas.create_rectangle(350, 60, 500, 140, fill="#FFF1C1", outline="black", width=2)
    ipc_label = canvas.create_text(425, 100, text="IPC", font=("Arial", 12, "bold"))

    # Process B
    canvas.create_rectangle(650, 60, 800, 140, fill="#D1FFD1", outline="black", width=2)
    canvas.create_text(725, 100, text="Process B", font=("Arial", 12, "bold"))

    # Arrow between A → IPC → B
    arrow_id = canvas.create_line(200, 100, 350, 100, arrow=tk.LAST, width=2)

    # ------------------------------
    # Output log box
    # ------------------------------
    output_box = scrolledtext.ScrolledText(root, height=15, width=100)
    output_box.pack(pady=10)

    # Status label
    status_label = tk.Label(
        root, text="Idle", font=("Arial", 12),
        bg="white", fg="black"
    )
    status_label.pack(pady=5)

    # ------------------------------
    # Buttons
    # ------------------------------
    frame = tk.Frame(root, bg="white")
    frame.pack(pady=10)

    # Pipe button
    tk.Button(
        frame,
        text="Simulate Pipe",
        bg="#4CAF50",
        fg="white",
        width=20,
        height=2,
        command=lambda: [
            canvas.itemconfig(ipc_label, text="Pipe"),
            run_ipc_process(
                [sys.executable, "step1_demo.py", "--pipe"],
                output_box, status_label, canvas, arrow_id
            )
        ]
    ).grid(row=0, column=0, padx=10)

    # Queue button
    tk.Button(
        frame,
        text="Simulate Queue",
        bg="#2196F3",
        fg="white",
        width=20,
        height=2,
        command=lambda: [
            canvas.itemconfig(ipc_label, text="Queue"),
            run_ipc_process(
                [sys.executable, "step1_demo.py", "--queue"],
                output_box, status_label, canvas, arrow_id
            )
        ]
    ).grid(row=0, column=1, padx=10)

    # Shared memory with lock
    tk.Button(
        frame,
        text="Shared Memory (Lock)",
        bg="#FF9800",
        fg="white",
        width=20,
        height=2,
        command=lambda: [
            canvas.itemconfig(ipc_label, text="Shared Memory (Lock)"),
            run_ipc_process(
                [sys.executable, "step1_demo.py", "--shm"],
                output_box, status_label, canvas, arrow_id
            )
        ]
    ).grid(row=1, column=0, padx=10, pady=10)

    # Shared memory without lock
    tk.Button(
        frame,
        text="Shared Memory (No Lock)",
        bg="#F44336",
        fg="white",
        width=20,
        height=2,
        command=lambda: [
            canvas.itemconfig(ipc_label, text="Shared Memory (NO Lock)"),
            run_ipc_process(
                [sys.executable, "step1_demo.py", "--shm-nolock"],
                output_box, status_label, canvas, arrow_id
            )
        ]
    ).grid(row=1, column=1, padx=10, pady=10)

    root.mainloop()


if __name__ == "__main__":
    main_gui()
