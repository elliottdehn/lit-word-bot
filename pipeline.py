
from source import obtain
import secrets
import praw
from words import *
from queue import Queue


def __merge_map__(m1, m2, collision_f):
    m3 = dict()
    for k, v in m1.items():
        m3[k] = v
    for k, v in m2.items():
        if (k in m3):
            m3[k] = collision_f(m1[k], v)
        else:
            m3[k] = v
    return m3

all_word_f = all_word_freqs()
all_stem_f = stem_freqs(all_word_f)

corp_word_f = corpus_word_freqs()
corp_stem_f = stem_freqs(corp_word_f)

merge_word_f = __merge_map__(all_word_f, corp_word_f, lambda v1, v2: v1 + v2)
merge_stem_f = __merge_map__(all_stem_f, corp_stem_f, lambda v1, v2: v1 + v2)

vocab = set(merge_word_f.keys()).intersection(set(corp_word_f.keys()))
vocab_stem = {stem(w) for w in vocab} - {stem(w) for w in offensive_words()}

# https://en.wikipedia.org/wiki/English_prefix
drop = [
    'anti', 'after', 'de', 'dis', 'em', 'en',
    'ex', 'hind', 'un', 'pre', 're']
depre_vocab = drop_prefixes(vocab, drop)

feed = filter(
    lambda w_c:\
        len(w_c[0]) > 3\
        and w_c[0] in vocab\
        and stem(w_c[0]) in vocab_stem\
        and merge_stem_f[stem(w_c[0])] < 80000,
    obtain(buffer=50))

for w, comment in feed:
    print(w)
    depre_wc = depre_cloud(w, vocab, drop).add(w)
    print(depre_wc)
