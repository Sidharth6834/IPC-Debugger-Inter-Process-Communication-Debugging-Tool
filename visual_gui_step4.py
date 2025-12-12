import tkinter as tk
from tkinter import scrolledtext
import subprocess
import threading
import sys
import time



def animate_arrows(canvas, arrow1, arrow2, color):
    # A → IPC
    canvas.itemconfig(arrow1, fill=color, width=3)
    canvas.update()
    time.sleep(0.20)

    # IPC → B
    canvas.itemconfig(arrow2, fill=color, width=3)
    canvas.update()
    time.sleep(0.20)

    # Reset arrows
    canvas.itemconfig(arrow1, fill="black", width=2)
    canvas.itemconfig(arrow2, fill="black", width=2)
    canvas.update()



def run_ipc_process(command, output_box, status_label, canvas, arrow1, arrow2, ipc_label_widget):

    def task():
        status_label.config(text="Running...", fg="blue")
        output_box.delete("1.0", tk.END)

        # Run command
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        for line in process.stdout:
            output_box.insert(tk.END, line)
            output_box.see(tk.END)

            l = line.lower()

            if "bottleneck" in l:
                animate_arrows(canvas, arrow1, arrow2, "yellow")

            elif "race" in l or "overwrite" in l or "no lock" in l:
                animate_arrows(canvas, arrow1, arrow2, "red")

            else:
                animate_arrows(canvas, arrow1, arrow2, "green")

        process.wait()
        status_label.config(text="Finished", fg="green")

    threading.Thread(target=task).start()



def main_gui():
    root = tk.Tk()
    root.title("IPC Debugger - Visual GUI (Step 4)")
    root.geometry("1050x780")
    root.configure(bg="white")

    # Title
    tk.Label(
        root,
        text="IPC Debugger - Visual Simulation (Step 4: Full Animation)",
        font=("Arial", 18, "bold"),
        bg="white"
    ).pack(pady=15)

    
    canvas = tk.Canvas(root, width=1000, height=250, bg="white", highlightthickness=0)
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

    # Arrows
    arrow1 = canvas.create_line(240, 120, 380, 120, arrow=tk.LAST, width=2)  # A → IPC
    arrow2 = canvas.create_line(560, 120, 700, 120, arrow=tk.LAST, width=2)  # IPC → B

 
    output_box = scrolledtext.ScrolledText(root, height=18, width=115)
    output_box.pack(pady=10)

    # Status bar
    status_label = tk.Label(root, text="Idle", fg="black", bg="white", font=("Arial", 13))
    status_label.pack(pady=5)

    # -------------------------------------
    # BUTTONS (ALL 4 IN ONE ROW)
    # -------------------------------------
    button_frame = tk.Frame(root, bg="white")
    button_frame.pack(pady=25)

    # Simulate Pipe
    tk.Button(
        button_frame, text="Simulate Pipe", width=18, height=2,
        bg="#4CAF50", fg="white",
        command=lambda: [
            canvas.itemconfig(ipc_label, text="Pipe"),
            run_ipc_process(
                [sys.executable, "step1_demo.py", "--pipe"],
                output_box, status_label, canvas, arrow1, arrow2, ipc_label
            )
        ]
    ).grid(row=0, column=0, padx=18, pady=10)

    # Simulate Queue
    tk.Button(
        button_frame, text="Simulate Queue", width=18, height=2,
        bg="#2196F3", fg="white",
        command=lambda: [
            canvas.itemconfig(ipc_label, text="Queue"),
            run_ipc_process(
                [sys.executable, "step1_demo.py", "--queue"],
                output_box, status_label, canvas, arrow1, arrow2, ipc_label
            )
        ]
    ).grid(row=0, column=1, padx=18, pady=10)

    # Shared Memory (Lock)
    tk.Button(
        button_frame, text="Shared Memory (Lock)", width=22, height=2,
        bg="#FF9800", fg="white",
        command=lambda: [
            canvas.itemconfig(ipc_label, text="Shared Memory (Lock)"),
            run_ipc_process(
                [sys.executable, "step1_demo.py", "--shm"],
                output_box, status_label, canvas, arrow1, arrow2, ipc_label
            )
        ]
    ).grid(row=0, column=2, padx=18, pady=10)

    # Shared Memory (No Lock)
    tk.Button(
        button_frame, text="Shared Memory (No Lock)", width=22, height=2,
        bg="#F44336", fg="white",
        command=lambda: [
            canvas.itemconfig(ipc_label, text="Shared Memory (No Lock)"),
            run_ipc_process(
                [sys.executable, "step1_demo.py", "--shm-nolock"],
                output_box, status_label, canvas, arrow1, arrow2, ipc_label
            )
        ]
    ).grid(row=0, column=3, padx=18, pady=10)

    root.mainloop()


if __name__ == "__main__":
    main_gui()
