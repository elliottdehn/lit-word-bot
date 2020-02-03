
from source import obtain
import secrets
import praw
from reddit_fmt import *
from webster import WebsterClient
from words import *
from queue import Queue
from praw.exceptions import APIException
import time, threading

def predictionary_variants(w):
    depre_wc = depre_cloud(w, all_vocab, pres)
    repre_wc = {pre + w for pre in pres if pre + w in all_vocab}
    desuf_wc = desuf_cloud(w, all_vocab, sufs)
    resuf_wc = {w + suf for suf in sufs if w + suf in all_vocab}
    depresuf_wc = {depre_s(desuf_s(w, suf), pre) \
        for pre in pres \
        for suf in sufs if depre_s(desuf_s(w, suf), pre) in all_vocab}
    represuf_wc = {
        pre + resuf
        for pre in pres
        for resuf in resuf_wc if pre + resuf in all_vocab}
    word_cloud = depre_wc \
        .union(repre_wc) \
        .union(desuf_wc) \
        .union(resuf_wc) \
        .union(represuf_wc) \
        .union(depresuf_wc)
    word_cloud.add(w)
    return word_cloud

word_frequencies = all_word_freqs()
all_vocab = scrabble_dictionary()

# https://en.wikipedia.org/wiki/English_prefix
pres = prefixes()
sufs = suffixes()

outComments = open("comments.txt", "a+")
outWords = open("words.txt", "a+")

done_comments = words_from_file("./comments.txt")
done_words = words_from_file("./words.txt")

infinite_feed = filter(
    lambda w_c:
        len(w_c[0]) > 3 \
        and w_c[0] in all_vocab \
        and w_c[0] not in done_words \
        and w_c[1].id not in done_comments \
        and w_c[1].author != None \
        and str(w_c[1].author) != "lit_word_bot",
    obtain(500))

c = WebsterClient()

reddit_rw = praw.Reddit(client_id=secrets.reddit_client_id, client_secret=secrets.reddit_client_secret,
                user_agent='com.local.litwordbot:Python 3.8:v0.1 (by /u/lit_word_bot)',
                username=secrets.reddit_username,
                password=secrets.reddit_password)

def delete_comments(minimum_score=1):
    # delete any downvoted comments of ours
    print("Checking deletes...")
    for bot_comment in reddit_rw.redditor('lit_word_bot').comments.new(limit=25):
        print("Checking comment, score is " + str(bot_comment.score))
        if (bot_comment.score < minimum_score):
            print("Deleting comment...")
            bot_comment.delete()
    threading.Timer(30, delete_comments).start()

delete_comments()

count = 0
for w, comment in infinite_feed:
    if (count % 10 == 0):
        print(w)
    count += 1
    done_words.add(w)



    if (w in word_frequencies and word_frequencies[w] > 60000):
        continue

    variant_cloud = predictionary_variants(w)

    for v in variant_cloud:
        done_words.add(v)

    rarity = sum([6000 for variant in variant_cloud if variant not in word_frequencies])
    rarity += sum([word_frequencies[variant] for variant in variant_cloud if variant in word_frequencies])

    if (rarity > 60000):
        continue

    print(w + " might be rare! " + str(rarity))
    print(variant_cloud)

    definition = c.define(w)

    if (not definition.exists()):
        continue

    if(definition.offensive()):
        continue  # obviously don't define offensive words

    real_variants = definition.variants().union(variant_cloud)
    print("Checking variant frequency:" + str(real_variants))

    for v in real_variants:
        done_words.add(v)

    real_freq = sum([6000 for variant in real_variants if variant not in word_frequencies])
    real_freq += sum([word_frequencies[variant] for variant in real_variants if variant in word_frequencies])
    print(w + " real frequency: " + str(real_freq))

    if (real_freq > 60000 \
        or definition.is_name() \
        or definition.is_simple_mashup(all_vocab)):
            print("Did not qualify")
            continue
    
    entries = definition.matches(comment.body)
    best_entries = definition.best_matches(entries, comment.body)

    if (len(best_entries) == 0):
        print("No matches for any entries: " + comment.body)
        continue

    to_be_replied = reddit_rw.comment(comment.id)
    bot_reply = make_response(w, comment, best_entries)
    print(bot_reply)

    forbade = False
    while True:
        try:
            # crude way to deal with comment rate limiting
            to_be_replied.reply(bot_reply)
            to_be_replied.upvote()
            to_be_replied.submission.upvote()
            break
        except APIException:
            print("retrying...")
            time.sleep(30)
        except:
            forbade = True
            print("Failed for some reason...")
            break
    
    if (forbade):
        continue

    done_comments.add(comment.id)
    outComments.write(comment.id)
    outComments.write("\n")

    for v in real_variants:
        outWords.write(v)
        outWords.write("\n")


outComments.close()
outWords.close()



