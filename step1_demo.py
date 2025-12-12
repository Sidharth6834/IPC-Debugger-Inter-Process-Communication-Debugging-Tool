# step1_demo.py
# Launcher to run each demo interactively from CLI.
import argparse
import time

def run_pipe():
    from pipe_simulation import run_demo as pipe_run
    print("Running Pipe demo (sender_delay=1.5 => simulates bottleneck)...")
    pipe_run(sender_delay=1.5)

def run_queue():
    from message_queue_sim import run_demo as queue_run
    print("Running Queue demo (producer fast, consumer slow => queue can fill)...")
    queue_run(queue_maxsize=3, produce_delay=0.1, consume_delay=1.0)

def run_shared(lock_demo=True):
    from shared_memory_sim import run_demo as shm_run
    print(f"Running Shared Memory demo (use_lock_demo={lock_demo})...")
    shm_run(use_lock_demo=lock_demo, iterations=6, rw_delay=0.3)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="IPC Debugger Step1 Demos")
    parser.add_argument("--pipe", action="store_true", help="Run pipe demo")
    parser.add_argument("--queue", action="store_true", help="Run queue demo")
    parser.add_argument("--shm", action="store_true", help="Run shared memory demo (with lock)")
    parser.add_argument("--shm-nolock", action="store_true", help="Run shared memory demo (no lock)")
    args = parser.parse_args()

    if args.pipe:
        run_pipe()
    elif args.queue:
        run_queue()
    elif args.shm:
        run_shared(lock_demo=True)
    elif args.shm_nolock:
        run_shared(lock_demo=False)
    else:
        print("No option provided. Running all demos one by one (pipe, queue, shm with lock, shm no lock)")
        run_pipe()
        time.sleep(1)
        run_queue()
        time.sleep(1)
        run_shared(lock_demo=True)
        time.sleep(1)
        run_shared(lock_demo=False)
