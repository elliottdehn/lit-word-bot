import queue
import threading
import criteria as it_meets
import praw
import re
import secrets
from functools import lru_cache, partial
from itertools import chain
from praw.models.reddit.more import MoreComments
from expiringdict import ExpiringDict

def __multirepl_list(repl_list, repl, tbr):
    if(len(repl_list) > 1):
        head, *tail = repl_list
        return __multirepl_list(tail, repl, tbr.replace(head, repl))
    else:
        return tbr.replace(repl_list[0], repl)


def __bag(body):
    urls = r"((http|ftp|https):\/\/)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)"
    spacify = r"([^a-zA-z]|[\\]|[\^])"
    despaced = r"[\s]+"

    replaced = re.sub(urls, ' ', body)
    replaced = __multirepl_list("-|[|]|n't|n’t".split('|'), " ", replaced)
    replaced = __multirepl_list("'|’".split('|'), " ", replaced)
    replaced = replaced.replace("_", " ")
    replaced = re.sub(spacify, ' ', replaced)
    replaced = re.sub(despaced, ' ', replaced)
    return set(replaced.strip().lower().split(" "))


def __feed(sub, q):
    sub_cache = ExpiringDict(max_len=100000, max_age_seconds=300)
    post_cache = ExpiringDict(max_len=100000, max_age_seconds=300)
    while (True):
        try:
            for new_post in sub.stream.submissions():
                if it_meets.subreddit_criteria(new_post.subreddit) and new_post.subreddit.id not in sub_cache:
                    sub_cache[new_post.subreddit.id] = True
                    for hot_post in chain(new_post.subreddit.hot(limit=25), new_post.subreddit.new(limit=25)):
                        if it_meets.submission_criteria(hot_post, comments=2, score=5, hours=3) and hot_post.id not in post_cache:
                            post_cache[hot_post.id] = True
                            [q.put((word, comment))
                            for comment in get_post_comments(hot_post)
                            if it_meets.comment_criteria(comment, score=2, hours=2)
                            for word in __bag(comment.body)]
        except:
            continue


def obtain(buffer=0):
    reddit_ro = praw.Reddit(client_id=secrets.reddit_client_id, client_secret=secrets.reddit_client_secret,
                            user_agent='com.local.litwords:Python 3.8:v1.0 (by /u/lit_word_x)')
    sub = reddit_ro.subreddit("all")
    all_new_queue = queue.LifoQueue(maxsize=buffer)
    all_new_thread = threading.Thread(target=__feed, args=(sub, all_new_queue,), daemon=True)
    all_new_thread.start()
    return iter(partial(all_new_queue.get, block=True, timeout=None), None)

def get_post_comments(post):
    return filter(lambda c: not isinstance(c, MoreComments), post.comments)
