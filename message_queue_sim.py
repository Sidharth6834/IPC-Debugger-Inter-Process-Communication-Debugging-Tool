# message_queue_sim.py
# Demonstrates a Queue (FIFO) with maxsize to simulate buffer-full bottleneck.
from multiprocessing import Process, Queue
import time

def producer(q: Queue, items, produce_delay, put_timeout=1.0):
    for item in items:
        try:
            q.put(item, timeout=put_timeout)
            print(f"[Producer] put: {item}")
        except Exception:
            print(f"⚠️ [Producer] Queue full! couldn't put '{item}' within {put_timeout}s")
        time.sleep(produce_delay)
    print("[Producer] done.")
    # indicate end (special token)
    q.put(None)

def consumer(q: Queue, consume_delay):
    while True:
        item = q.get()  # blocks until an item appears
        if item is None:
            print("[Consumer] received termination token. Exiting.")
            break
        time.sleep(consume_delay)  # simulate slow consumer -> possible queue growth
        print(f"[Consumer] got: {item}")
    print("[Consumer] done.")

def run_demo(items=None, queue_maxsize=3, produce_delay=0.2, consume_delay=1.0):
    if items is None:
        items = [f"msg{i}" for i in range(1, 8)]
    q = Queue(maxsize=queue_maxsize)
    p = Process(target=producer, args=(q, items, produce_delay))
    c = Process(target=consumer, args=(q, consume_delay))
    c.start()
    p.start()
    p.join()
    c.join()
    print("[Queue Demo] finished.")
