import queue
import threading

def __sub_feed(sub, q):
    for submission in sub.stream.submissions():
        q.put(submission)

def obtain(sub, buffer=0):
    all_new_queue = queue.Queue(maxsize=buffer)
    all_new_thread = threading.Thread(target=__sub_feed, args=(sub, all_new_queue,), daemon=True)
    all_new_thread.start()
    return all_new_queue
