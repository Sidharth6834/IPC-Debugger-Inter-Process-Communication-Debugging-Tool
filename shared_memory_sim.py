# shared_memory_sim.py
from multiprocessing import Process, Lock
from multiprocessing import shared_memory
import time
import struct

SHM_SIZE = 8  # 64-bit integer

def writer_no_lock(name, iterations, write_delay, start_value=0):
    shm = shared_memory.SharedMemory(name=name)
    for i in range(iterations):
        val = start_value + i
        shm.buf[:8] = struct.pack('q', val)
        print(f"[Writer-NoLock] wrote {val}")
        time.sleep(write_delay)
    shm.close()
    print("[Writer-NoLock] done.")

def reader_no_lock(name, iterations, read_delay):
    shm = shared_memory.SharedMemory(name=name)
    for _ in range(iterations):
        raw = bytes(shm.buf[:8])
        val = struct.unpack('q', raw)[0]
        print(f"[Reader-NoLock] read {val}")
        time.sleep(read_delay)
    shm.close()
    print("[Reader-NoLock] done.")

def writer_with_lock(name, lock, iterations, write_delay, start_value=1000):
    shm = shared_memory.SharedMemory(name=name)
    for i in range(iterations):
        with lock:
            val = start_value + i
            shm.buf[:8] = struct.pack('q', val)
            print(f"[Writer-Lock] wrote {val}")
        time.sleep(write_delay)
    shm.close()
    print("[Writer-Lock] done.")

def reader_with_lock(name, lock, iterations, read_delay):
    shm = shared_memory.SharedMemory(name=name)
    for _ in range(iterations):
        with lock:
            raw = bytes(shm.buf[:8])
            val = struct.unpack('q', raw)[0]
            print(f"[Reader-Lock] read {val}")
        time.sleep(read_delay)
    shm.close()
    print("[Reader-Lock] done.")

def run_demo(iterations=6, rw_delay=0.5, use_lock_demo=True):
    shm = shared_memory.SharedMemory(create=True, size=SHM_SIZE)
    shm.buf[:8] = struct.pack('q', 0)
    print(f"[Main] created shared memory name={shm.name}")

    if use_lock_demo:
        lock = Lock()
        w = Process(target=writer_with_lock, args=(shm.name, lock, iterations, rw_delay))
        r = Process(target=reader_with_lock, args=(shm.name, lock, iterations, rw_delay))
    else:
        w = Process(target=writer_no_lock, args=(shm.name, iterations, rw_delay))
        r = Process(target=reader_no_lock, args=(shm.name, iterations, rw_delay))

    r.start()
    w.start()
    w.join()
    r.join()

    shm.close()
    shm.unlink()
    print("[Shared Memory Demo] finished. (unlinked shared memory)")
