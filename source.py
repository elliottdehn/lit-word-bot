import praw
import secrets
import queue
import threading

def __sub_feed(sub, q):
    for submission in sub.stream.submissions():
        q.put(submission)

reddit_ro = praw.Reddit(client_id=secrets.reddit_client_id, client_secret=secrets.reddit_client_secret,
                        user_agent='com.local.litwords:Python 3.8:v1.0 (by /u/lit_word_x)')

all_new_source = reddit_ro.subreddit("all")
all_new_queue = queue.Queue()
all_new_thread = threading.Thread(target=__sub_feed, args=(all_new_source, all_new_queue,), daemon=True)

all_new_thread.start()

def get(reddit, name):
    all_new_source = reddit.subreddit(name)
    all_new_queue = queue.Queue()
    all_new_thread = threading.Thread(target=__sub_feed, args=(all_new_source, all_new_queue,), daemon=True)
    all_new_thread.start()
    return all_new_queue
