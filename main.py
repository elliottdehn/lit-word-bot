from datetime import *
from itertools import *
# https://praw.readthedocs.io/en/latest/getting_started/quick_start.html
import praw
from nltk.stem import *
import requests
import re
import io
from os import walk
import json
import heapq
import secrets as secrets
from functools import reduce
import glob

blacklist = [
    "anime",
    "asianamerican",
    "askhistorians",
    "askscience",
    "askreddit",
    "aww",
    "chicagosuburbs",
    "cosplay",
    "cumberbitches",
    "d3gf",
    "deer",
    "depression",
    "depthhub",
    "drinkingdollars",
    "forwardsfromgrandma",
    "geckos",
    "giraffes",
    "grindsmygears",
    "indianfetish",
    "me_irl",
    "misc",
    "movies",
    "mixedbreeds",
    "news",
    "newtotf2",
    "omaha",
    "petstacking",
    "pics",
    "pigs",
    "politicaldiscussion",
    "politics",
    "programmingcirclejerk",
    "raerthdev",
    "rants",
    "runningcirclejerk",
    "salvia",
    "science",
    "seiko",
    "shoplifting",
    "sketches",
    "sociopath",
    "suicidewatch",
    "talesfromtechsupport",
    "torrent",
    "torrents",
    "trackers",
    "tr4shbros",
    "unitedkingdom",
    "crucibleplaybook",
    "cassetteculture",
    "italy_SS",
    "DimmiOuija",
    "benfrick",
    "bsa",
    "futurology",
    "graphic_design",
    "historicalwhatif",
    "lolgrindr",
    "malifaux",
    "nfl",
    "toonami",
    "trumpet",
    "ps2ceres",
    "duelingcorner",
    "medical_advice"
]


def inPastHours(ts, hs):
    difference = timedelta(hours=6)
    delta = timedelta(hours=hs)
    then = datetime.fromtimestamp(ts) + difference
    now = datetime.utcnow()
    return now-delta <= then


def scoreOver(to_score, threshhold):
    return to_score.score >= threshhold


def multirepl_list(repl_list, repl, tbr):
    if(len(repl_list) > 1):
        head, *tail = repl_list
        return multirepl_list(tail, repl, tbr.replace(head, repl))
    else:
        return tbr.replace(repl_list[0], repl)


def clean(body):
    urls = r"((http|ftp|https):\/\/)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)"
    spacify = r"([^a-zA-z]|[\\]|[\^])"
    despaced = r"[\s]+"
    no_dummies = r"\b.{1,3}\b"

    replaced = re.sub(urls, ' ', body)
    replaced = multirepl_list("-|[|]".split('|'), " ", replaced)
    replaced = multirepl_list("n't|n’t".split('|'), " ", replaced)
    replaced = multirepl_list("'|’".split('|'), " ", replaced)
    replaced = replaced.replace("_", " ")
    replaced = re.sub(spacify, ' ', replaced)
    replaced = re.sub(no_dummies, ' ', replaced)
    replaced = re.sub(despaced, ' ', replaced)
    return replaced.strip().lower()


def filter_submissions(submissions, submission_score, hours):
    submissions = filterfalse(lambda p: not scoreOver(
        p, submission_score), submissions)
    submissions = filterfalse(lambda p: not inPastHours(
        p.created_utc, hours), submissions)
    submissions = filterfalse(lambda p: p.stickied, submissions)
    submissions = filterfalse(
        lambda p: p.distinguished == "moderator", submissions)
    return submissions


def filter_posts(posts, post_score, hours):
    posts = filterfalse(lambda p: p.num_comments < 3, posts)
    posts = filter_submissions(posts, post_score, hours)
    posts = filterfalse(lambda p: p in blacklist, posts)
    posts = filterfalse(lambda p: p.locked, posts)
    return posts


def filter_comments(comments, comment_score, hours):
    return filter_submissions(comments, comment_score, hours)

# What the comment consumption algorithm boils down to:
# Comment -> Map(word -> Comment)
# Highest scoring comment wins in a word-map collision
# Algo:
# - turn each comment into a (Comment, {words}) tuple
# - map each (Comment, {words}) tuple into N (Comment, word) pairs
# - collect the pairs into (word -> {Comments}) pairs
# - select the highest scoring comment for each, resulting in (word -> Comment) mapping

# - turn each comment into a (Comment, {words}) tuple


def associate_words(comment, text):
    return (comment, set(clean(text).split()))

# - map each (Comment, {words}) tuple into N (Comment, word) pairs


def split(left, elm_set):
    return [(left, elm) for elm in elm_set]

# - collect the pairs into (word -> {Comments}) pairs


def nuples_to_map(nuple_set, key_idx):
    nuple_map = {nuple[key_idx]: set() for nuple in nuple_set}
    for key in nuple_map.keys():
        nuple_map[key] = set(filterfalse(
            lambda elm: elm[key_idx] != key, nuple_set))
    return nuple_map

# - select the highest scoring comment for each, resulting in (word -> Comment) mapping


def map_to_max(m, maxed_key):
    return {k: max(m[k], key=maxed_key) for k in m.keys()}


def map_word_to_comment(comment_bag_pairs):
    comment_word_pairs = list()
    for pair in comment_bag_pairs:
        comment_word_pairs.extend(split(pair[0], pair[1]))
    word_to_comments_map = nuples_to_map(comment_word_pairs, 1)
    word_to_comment = map_to_max(
        word_to_comments_map, lambda comment_word: comment_word[0].score)
    return word_to_comment


def hot_sub_comment_bags(sub, lim, post_score, post_hours, comm_score, comm_hours):
    hot_posts = sub.hot(limit=lim)
    hot_posts = filter_posts(hot_posts, post_score, post_hours)
    bag = list()
    for p in hot_posts:
        if(p.num_comments != 0):
            p.comments.replace_more()
            hot_comments = list(filter_comments(
                p.comments.list(), comm_score, comm_hours))
            print("Comments found: " + str(len(hot_comments)))
            for c in hot_comments:
                bag.append(associate_words(c, c.body))
    return bag

# Set((Comment, {words})) -> Map((word -> Comment))
# Highest scoring comment wins in a collision
# Algo:
# - map each (Comment, {words}) pair to N (Comment, word) pairs, as a set
# - collect the pairs into (word, {Comments}) pairs
# - select highscore comment for each word, resulting in (word -> Best_Comment) mapping


def hot_all_word_map(reddit, lim, post_score, post_hours, comm_score, comm_hours):
    # assume you have a Subreddit instance bound to variable `subreddit`
    hot_posts = reddit.subreddit("all").new(limit=lim)
    hot_posts = filter_posts(hot_posts, post_score, post_hours)

    hot_subs = {p.subreddit.display_name: p.subreddit for p in hot_posts}
    bags = list()
    for sub_name in hot_subs.keys():
        sub = reddit.subreddit(sub_name)
        print("Working on: " + sub_name)
        bags.extend(hot_sub_comment_bags(sub, lim,
                                         post_score, post_hours, comm_score, comm_hours))
    return map_word_to_comment(bags)


def word_set_from_dir(directory, folder, encoding):
    words = ''
    for filename in next(walk(directory))[2]:
        with io.open(folder + filename, "r", encoding=encoding, errors='ignore') as f:
            for line in f:
                words += clean(line) + ' '
    return set(clean(words).split())


def word_set_from_dir_no_clean(directory, folder, encoding):
    words = ''
    for filename in next(walk(directory))[2]:
        with io.open(folder + filename, "r", encoding=encoding, errors='ignore') as f:
            for line in f:
                words += line + ' '
    return set(words.strip().split())


def partition(items, predicate=bool):
    a, b = tee((predicate(item), item) for item in items)
    return ((item for pred, item in a if not pred),
            (item for pred, item in b if pred))


def stem_set(word_set):
    stemmer = PorterStemmer()
    return set([stemmer.stem(word) for word in word_set])


reddit_ro = praw.Reddit(client_id=secrets.reddit_client_id, client_secret=secrets.reddit_client_secret,
                        user_agent='com.local.litwordbot:Python 3.8:v1.0 (by /u/lit_word_bot)')
reddit_word_to_comment = hot_all_word_map(reddit_ro, None, 3, 1, 1, 1)
reddit_set = set(reddit_word_to_comment.keys())
# some positive tests. These words should always appear in the output list.
#reddit_set = reddit_set.union(set(["litten", "minaret", "effaces"]))
print("Possible words, prior to any filtering: " + str(reddit_set))

stemmer = PorterStemmer()
reddit_set_stem_map = {stemmer.stem(word): word for word in reddit_set}

print("Reddit Not Stemmed Unique Count: " + str(len(reddit_set)))
print("Reddit Stemmed Unique Count: " + str(len(reddit_set_stem_map.keys())))

offensive_set = word_set_from_dir_no_clean(
    "./offensive", "offensive/", "windows-1252")

corpus_stem_dict = {}
corpus_word_dict = {}

txt_files = glob.glob("./" + "corpusfreq/" + "*.txt")
with io.open(txt_files[0], "r", encoding="utf-8") as f:
    for line in f:
        w, c = line.split(":")
        corpus_word_dict[w] = int(c)
        w = stemmer.stem(clean(w))
        if(w in corpus_stem_dict.keys()):
            count = corpus_stem_dict[w]
            corpus_stem_dict[w] = count + int(c)
        else:
            corpus_stem_dict[w] = int(c)

corpus_word_set = corpus_word_dict.keys()

# Rough frequency filter to get rid of words over X frequency, including
# their various forms
# 300,000 is permissive for now, to get an idea of rarities
rare_stems = set(filterfalse(
    lambda s: corpus_stem_dict[s] >= 70000, corpus_stem_dict.keys()))

print("Corpus stem set filtered for rare stems size: " +
      str(len(rare_stems)))

# What do we gain for using the corpus?
# We avoid "words" like "bloop" (blooper)
candidate_stems = rare_stems.intersection(
    reddit_set_stem_map.keys()) - offensive_set

for candidate_stem in candidate_stems:
    print("Calling API for candidate: " + reddit_set_stem_map[candidate_stem])

# This is going to be cleaned up & simplified but for now it is what it is
# This could be made !!!!WAY!!!! more abstract to pull in many sources.
# Existing desire: if(isWorthy(word)): post(word, Comment)
# That line above is literally all that matters here.

final_results = []
for w in candidate_stems:
    # Expand the stem back to its original word
    real_word = reddit_set_stem_map[w]
    print("Working on: " + real_word)
    response = requests.get("https://www.dictionaryapi.com/api/v3/references/collegiate/json/" +
                            real_word + "?key=" + secrets.webster_dict_key)
    webster_def = response.json()
    if (len(webster_def) == 0 or type(webster_def[0]) is str):
        print("Thesaurus fallback...")
        response = requests.get("https://www.dictionaryapi.com/api/v3/references/thesaurus/json/" +
                                real_word + "?key=" + secrets.webster_thes_key)
        webster_def = response.json()
        if (len(webster_def) == 0 or type(webster_def[0]) is str):
            print("Thesaurus fallback missed...\n\n\n")
            continue

    first_def = webster_def[0]
    first_def_meta = first_def['meta']
    # Filter out offensive words not included in my list
    if(first_def_meta["offensive"]):
        continue  # obviously don't define offensive words
    elif (first_def_meta["id"].lower() != first_def_meta["id"]):
        continue  # probably a name or an acronym

    # get rid of phrasal variants
    real_variants = list(filterfalse(lambda variant: len(
        variant.split()) > 1, first_def_meta['stems']))

    # add current word to variants
    real_variants.append(real_word)

    # reduce to unique variants
    real_variants = set([variant.lower() for variant in real_variants])

    print("Checking variant frequency:" + str(real_variants))

    real_freq = 0
    for variant in real_variants:
        if variant in corpus_word_dict:
            variant_frequency = corpus_word_dict[variant]
            print("found variant in frequencies: " +
                  variant + " : " + str(variant_frequency))
            real_freq += corpus_word_dict[variant]

    if real_freq != 0 and "shortdef" in first_def and len(first_def["shortdef"]) != 0:
        def_field = first_def["shortdef"]
        is_archaic = "sls" in def_field and "archaic" in def_field["sls"]
        rarity_score = real_freq
        if(is_archaic):
            rarity_score = rarity_score/5
        final_results.append((real_word, rarity_score, def_field[0]))
        print(first_def_meta['id'].split(":")[
              0] + " || stem-reduced rarity score: " + str(rarity_score))
        print("\n\n\n")

# This is what all that work was for: the rarest word, associated with the best comment
final_results = sorted(final_results, key=lambda x: x[1])
count = 0
for final_tup in final_results:
    print(str(count) + ". " + str(final_tup) + " || Associated comment ID: " +
          str(reddit_word_to_comment[final_tup[0]]))
    count += 1

choice = int(input("Pick a word to define (0-" + str(count - 1) + ": "))
chosen_word = final_results[choice][0]
chosen_word_def = final_results[choice][2]
chosen_comment = reddit_word_to_comment[chosen_word][0]
poster = chosen_comment.author.name

comment = "Hey /u/" + poster + "! **" + chosen_word + "** is a great word!\n\n" + "It means:\n\n**" + \
    chosen_word_def + \
    "**\n\n(according to Merriam-Webster).\n\nI'm new. Was this interesting?"
print(comment)

reddit_rw = praw.Reddit(client_id=secrets.reddit_client_id, client_secret=secrets.reddit_client_secret,
                        user_agent='com.local.litwordbot:Python 3.8:v0.1 (by /u/lit_word_bot)',
                        username=secrets.reddit_username,
                        password=secrets.reddit_password)

to_be_replied = reddit_rw.comment(chosen_comment.id)
to_be_replied.reply(comment)
