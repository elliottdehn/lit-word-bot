
from source import obtain
import secrets
import praw
from words import *
from queue import Queue

word_frequencies = all_word_freqs()
stem_frequencies = stem_freqs(word_frequencies)

all_vocab = scrabble_dictionary().intersection(set(word_frequencies.keys()))
all_stem = \
    ({stem(w) for w in all_vocab} - {stem(w) for w in offensive_words()})\
    .intersection(stem_frequencies.keys())

infinite_feed = filter(
    lambda w_c: len(w_c[0]) > 3 \
        and w_c[0] in all_vocab \
        and stem(w_c[0]) in all_stem \
        and stem_frequencies[stem(w_c[0])] < 80000,
    obtain(buffer=50))

# https://en.wikipedia.org/wiki/English_prefix
pre_fs = prefixes()

for w, comment in infinite_feed:
    print(w)
    depre_wc = depre_cloud(w, all_vocab, pre_fs) # TODO: duplicated work here building the map
    repre_wc = {pre + w for pre in pre_fs if pre + w in all_vocab}
    word_cloud = depre_wc.union(repre_wc)
    word_cloud.add(w)
    print(word_cloud)
