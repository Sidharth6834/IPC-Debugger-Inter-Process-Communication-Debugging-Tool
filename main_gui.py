import tkinter as tk
from tkinter import scrolledtext
import multiprocessing
import threading
import subprocess
import sys

def run_command(command, output_box, status_label):
    def task():
        status_label.config(text="Running...", fg="blue")
        output_box.delete("1.0", tk.END)

        # Start the subprocess
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Read output live
        for line in process.stdout:
            output_box.insert(tk.END, line)
            output_box.see(tk.END)

        process.wait()
        status_label.config(text="Finished", fg="green")

    threading.Thread(target=task).start()



def main_gui():
    root = tk.Tk()
    root.title("IPC Debugger - Step 2 GUI")
    root.geometry("700x600")
    root.configure(bg="white")

    # Title
    title = tk.Label(
        root, text="IPC Debugger (Pipes, Message Queue, Shared Memory)",
        font=("Arial", 14, "bold"),
        bg="white"
    )
    title.pack(pady=10)

    # Buttons Frame
    frame = tk.Frame(root, bg="white")
    frame.pack(pady=10)

    # Output area (scrollable)
    output_box = scrolledtext.ScrolledText(root, height=20, width=80)
    output_box.pack(pady=10)

    # Status bar
    status_label = tk.Label(root, text="Idle", fg="black", bg="white", font=("Arial", 12))
    status_label.pack(pady=5)

  

    btn1 = tk.Button(
        frame, text="Run Pipe Demo",
        command=lambda: run_command([sys.executable, "step1_demo.py", "--pipe"], output_box, status_label),
        width=20, height=2, bg="#4CAF50", fg="white"
    )
    btn1.grid(row=0, column=0, padx=10, pady=5)

    btn2 = tk.Button(
        frame, text="Run Queue Demo",
        command=lambda: run_command([sys.executable, "step1_demo.py", "--queue"], output_box, status_label),
        width=20, height=2, bg="#2196F3", fg="white"
    )
    btn2.grid(row=0, column=1, padx=10, pady=5)

    btn3 = tk.Button(
        frame, text="Run Shared Memory (Lock)",
        command=lambda: run_command([sys.executable, "step1_demo.py", "--shm"], output_box, status_label),
        width=20, height=2, bg="#FF9800", fg="white"
    )
    btn3.grid(row=1, column=0, padx=10, pady=5)

    btn4 = tk.Button(
        frame, text="Run Shared Memory (No Lock)",
        command=lambda: run_command([sys.executable, "step1_demo.py", "--shm-nolock"], output_box, status_label),
        width=20, height=2, bg="#F44336", fg="white"
    )
    btn4.grid(row=1, column=1, padx=10, pady=5)

    root.mainloop()


if __name__ == "__main__":
    multiprocessing.freeze_support()  # needed for Windows
    main_gui()
