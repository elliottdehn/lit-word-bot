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
    "duelingcorner"
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
    spacify= r"([^a-zA-z]|[\\]|[\^])"
    despaced = r"[\s]+"
    no_dummies = r"\b.{1,2}\b"

    replaced = re.sub(urls, ' ', body)
    replaced = multirepl_list("-|[|]".split('|'), " ", replaced)
    replaced = multirepl_list("n't|n’t".split('|'), " ", replaced)
    replaced = multirepl_list("'|’".split('|'), " ", replaced)
    replaced = replaced.replace("_", " ")
    replaced = re.sub(spacify, ' ', replaced)
    replaced = re.sub(no_dummies, ' ', replaced)
    replaced = re.sub(despaced, ' ', replaced)
    return replaced.strip().lower()

def hot_relevant_reddit_bag(reddit, sub, lim, comm_score, post_score, hours):
    subreddit = reddit.subreddit(sub)

    # assume you have a Subreddit instance bound to variable `subreddit`
    hot_posts = subreddit.hot(limit=lim)
    hot_posts = filterfalse(lambda p: not scoreOver(p, post_score), hot_posts)
    hot_posts = filterfalse(lambda p: not inPastHours(p.created_utc, hours), hot_posts)

    bag = ""
    for p in hot_posts:
        if(p.subreddit.name.lower() not in blacklist and not p.locked):
            p.comments.replace_more(limit=0)
            comment_queue = p.comments[:]  # Seed with top-level
            while comment_queue:
                comment = comment_queue.pop(0)
                if(scoreOver(comment, comm_score)):
                    bag += ' ' + clean(comment.body)
                comment_queue.extend(comment.replies)
    return set(bag.split())

def word_set_from_dir(directory, folder, encoding):
    words = ''
    for filename in next(walk(directory))[2]:
        with io.open(folder + filename, "r", encoding=encoding) as f:
            for line in f:
                words += ' ' + clean(line)
    return set(clean(words).split())

def word_set_from_dir_no_clean(directory, folder, encoding):
    words = ''
    for filename in next(walk(directory))[2]:
        with io.open(folder + filename, "r", encoding=encoding) as f:
            for line in f:
                words += ' ' + line
    return set(words.split())

def real_word_set_from_word_set(word_set, real_words):
    fake_words = word_set - real_words
    return word_set - fake_words

def prefix_remainder(word, prefix):
    zipChain = zip(chain(word), chain(prefix))
    return len(word) - len()

def partition(items, predicate=bool):
    a, b = tee((predicate(item), item) for item in items)
    return ((item for pred, item in a if not pred),
            (item for pred, item in b if pred))

dictionary_set = set()
with open('dictionary/words_dictionary.json', 'r') as json_file:
    dictionary_set = set(json.load(json_file))

#response = requests.get("https://www.dictionaryapi.com/api/v3/references/collegiate/json/" + "disempower" + "?key=" + secrets.webster_dict_key)
#webster_def = response.json()
#print(json.dumps(webster_def, indent=2))

lovecraft_set = real_word_set_from_word_set(word_set_from_dir("./lovecraft", "lovecraft/", "windows-1252"), dictionary_set)
poe_set = real_word_set_from_word_set(word_set_from_dir("./poe", "poe/", "utf-8"), dictionary_set)
shake_set = real_word_set_from_word_set(word_set_from_dir("./shakespeare","shakespeare/","windows-1252"), dictionary_set)

offensive_set = word_set_from_dir_no_clean("./offensive", "offensive/", "windows-1252")
corpus_word_set = lovecraft_set.union(poe_set).union(shake_set)

stemmer = PorterStemmer()
corpus_word_set_stems = set([stemmer.stem(w) for w in corpus_word_set]) - offensive_set
valid_stem_set = set([stemmer.stem(w) for w in dictionary_set])

print("Corpus Not Stemmed Unique Count: " + str(len(corpus_word_set)))
print("Corpus Stemmed Unique Count: " + str(len(corpus_word_set_stems)))

freq_stem_dict = {}
freq_word_dict = {}
for filename in next(walk("./frequency"))[2]:
        with io.open("frequency/" + filename, "r", encoding="utf-8") as f:
            for line in f:
                w, c = line.split("\t")
                freq_word_dict[w] = int(c)
                w = stemmer.stem(clean(w))
                if(len(w) != 0 and w in valid_stem_set):
                    if(w in freq_stem_dict.keys()):
                        count = freq_stem_dict[w]
                        freq_stem_dict[w] = count + int(c)
                    else:
                        freq_stem_dict[w] = int(c)

print("Freq Stem Map Count: " + str(len(freq_stem_dict)))

freq_set_20 = set(filterfalse(lambda s: freq_stem_dict[s] >= 300000, freq_stem_dict.keys()))

reddit_ro = praw.Reddit(client_id=secrets.reddit_client_id, client_secret=secrets.reddit_client_secret, user_agent='com.local.litwordbot:Python 3.8:v0.1 (by /u/lit_word_bot)')
reddit_set = hot_relevant_reddit_bag(reddit_ro, "all", 100, 15, 15, 4)
reddit_set_stem_map = {}
for word in reddit_set:
    reddit_set_stem_map[stemmer.stem(word)] = word #dirty hack, fix this

print("Reddit Not Stemmed Unique Count: " + str(len(reddit_set)))
print("Reddit Stemmed Unique Count: " + str(len(reddit_set_stem_map.keys())))

lit_words_20 = corpus_word_set_stems.intersection(reddit_set_stem_map.keys()).intersection(freq_set_20)

print(lit_words_20)

final_results = []
for w in lit_words_20:
    real_word = reddit_set_stem_map[w]
    response = requests.get("https://www.dictionaryapi.com/api/v3/references/collegiate/json/" + real_word + "?key=" + secrets.webster_dict_key)
    webster_def = response.json()
    if(len(webster_def) != 0):
        if(type(webster_def[0]) is str): #not-a-word that happened to be in our word dict
            continue
        real_freq = 0
        first_def = webster_def[0]
        first_def_meta = first_def['meta']
        if(first_def_meta["offensive"]): #Filter out offensive words not included in my list
            continue
        word_webster_stems = first_def_meta['stems']
        real_variants = list(filterfalse(lambda variant: len(variant.split()) > 1, word_webster_stems))
        real_variants.append(real_word)
        real_variants = set([variant.lower() for variant in real_variants]) #reduce to uniques

        #take each unique porter stem and map it to the most common variant of this word which maps to it
        real_variants_stem_map = {}
        for variant in real_variants:
            variant_stem = stemmer.stem(variant)
            if(variant_stem not in real_variants_stem_map):
                if(variant in freq_word_dict):
                    real_variants_stem_map[variant_stem] = (variant)
            else:
                #if the this stem is already in the map, we want that stem to map to
                #the most common version of this word with the same stem
                most_common_variant_to_stem = real_variants_stem_map[variant_stem]
                if(variant in freq_word_dict.keys() and most_common_variant_to_stem in freq_word_dict.keys()):
                    current_variant_freq = freq_word_dict[variant]
                    most_common_variant_to_stem_freq = freq_word_dict[most_common_variant_to_stem]
                    if(current_variant_freq > most_common_variant_to_stem_freq):
                        real_variants_stem_map[variant_stem] = variant

        print(real_variants_stem_map)

        for variant_stem in real_variants_stem_map.keys():
            most_common_variant_to_stem = real_variants_stem_map[variant_stem]
            if(most_common_variant_to_stem in freq_word_dict.keys()):
                variant_freq = freq_word_dict[most_common_variant_to_stem]
                print(most_common_variant_to_stem + " " + str(variant_freq))
                real_freq += variant_freq
        def_field = first_def["def"]
        is_archaic = "sls" in def_field and "archaic" in def_field["sls"]
        rarity_score = real_freq*len(webster_def)
        if(is_archaic):
            rarity_score = rarity_score/5
        final_results.append((real_word, rarity_score))
        print(real_word + " || stem-reduced rarity score: " + str(rarity_score))
        print("\n\n\n")

final_results = sorted(final_results, key = lambda x: x[1])
for final_tup in final_results:
    print(final_tup)