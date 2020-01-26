
from source import obtain
import secrets
import praw
from webster import WebsterClient
from words import *
from queue import Queue

def predictionary_variants(w):
    depre_wc = depre_cloud(w, all_vocab, pres)
    repre_wc = {pre + w for pre in pres if pre + w in all_vocab}
    desuf_wc = desuf_cloud(w, all_vocab, sufs)
    resuf_wc = {w + suf for suf in sufs if w + suf in all_vocab}
    presuf_wc = {
        pre + resuf
        for pre in pres
        for resuf in resuf_wc if pre + resuf in all_vocab}
    word_cloud = depre_wc.union(repre_wc).union(desuf_wc).union(resuf_wc).union(presuf_wc)
    word_cloud.add(w)
    return word_cloud

word_frequencies = all_word_freqs()
stem_frequencies = stem_freqs(word_frequencies)

all_vocab = scrabble_dictionary().intersection(set(word_frequencies.keys()))
all_stem = \
    ({stem(w) for w in all_vocab} - {stem(w) for w in offensive_words()})\
    .intersection(stem_frequencies.keys())

# https://en.wikipedia.org/wiki/English_prefix
pres = prefixes()
sufs = suffixes()

infinite_feed = filter(
    lambda w_c: len(w_c[0]) > 3 \
        and w_c[0] in all_vocab \
        and stem(w_c[0]) in all_stem \
        and stem_frequencies[stem(w_c[0])] < 200000,
    obtain(buffer=50))

c = WebsterClient()
for w, comment in infinite_feed:
    print(w)
    variant_cloud = predictionary_variants(w)
    print(variant_cloud)
    rarity = sum([word_frequencies[variant] for variant in variant_cloud])

    if (rarity > 80000):
        continue

    print(w + " might be rare! " + str(rarity))

    definition = c.define(w)

    if (not definition.exists()):
        continue

    if(definition.offensive()):
        continue  # obviously don't define offensive words

    real_variants = definition.variants().union(variant_cloud)
    print("Checking variant frequency:" + str(real_variants))

    real_freq = sum([6000 for variant in real_variants if variant not in word_frequencies])
    real_freq += sum([word_frequencies[variant] for variant in real_variants if variant in word_frequencies])
    print(w + " real frequency: " + str(real_freq))

    if (real_freq < 60000 \
        and not definition.is_name() \
        and not definition.is_simple_mashup(all_vocab)):
            print(w + " qualified to be defined!")
    
