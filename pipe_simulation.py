# pipe_simulation.py
# Demonstrates a simple Pipe-based IPC with delay detection (bottleneck).
from multiprocessing import Process, Pipe
import time

DELAY_THRESHOLD = 2.0  # seconds: if receiving takes longer, flag bottleneck

def sender(conn, messages, send_delay):
    """Send messages through a pipe, with optional delay between sends."""
    for msg in messages:
        time.sleep(send_delay)  # simulate sender doing work / slow production
        timestamp = time.time()
        conn.send((msg, timestamp))
        print(f"[Sender] sent: {msg} (t={timestamp:.3f})")
    conn.close()
    print("[Sender] done and closed pipe.")

def receiver(conn, expect_count):
    """Receive messages. If delay between send timestamp and now exceeds threshold, warn."""
    received = 0
    while received < expect_count:
        try:
            msg, ts = conn.recv()
        except EOFError:
            break
        now = time.time()
        latency = now - ts
        if latency > DELAY_THRESHOLD:
            print(f"⚠️ [Receiver] Bottleneck detected! latency={latency:.3f}s for message '{msg}'")
        else:
            print(f"[Receiver] received: {msg} (latency={latency:.3f}s)")
        received += 1
    conn.close()
    print("[Receiver] done and closed pipe.")

def run_demo(messages=None, sender_delay=0.5):
    if messages is None:
        messages = ["hello", "world", "IPC", "pipe", "end"]
    parent_conn, child_conn = Pipe()
    p_send = Process(target=sender, args=(parent_conn, messages, sender_delay))
    p_recv = Process(target=receiver, args=(child_conn, len(messages)))
    p_recv.start()
    p_send.start()
    p_send.join()
    p_recv.join()
    print("[Pipe Demo] finished.")
