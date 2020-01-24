from nltk.stem import *
from functools import reduce

def __read_data__(file_name, delim):
    data = dict()
    with open(file_name, "r", encoding="utf-8") as f:
        for line in f:
            l, r = line.split(delim)
            data[l] = int(r)
    return data

def words_from_file(file_name):
    f = open(file_name)
    words = f.read()
    words = words.replace("\n", " ")
    return set(words.lower().strip().split())

def __reduce_map__(m1, init, acc_f, key_f=lambda k: k):
    ret = dict()
    for key, value in m1.items():
        new_key = key_f(key)
        if new_key in ret:
            ret[new_key] = acc_f(ret[new_key], value)
        else:
            ret[new_key] = acc_f(init, value)
    return ret

def stem(word):
    stemmer = PorterStemmer()
    return stemmer.stem(word)

def depre_s(s, prefix):
    return s[len(prefix) :] if s.startswith(prefix) else s

def depre_w(w, vocab, prefix):
    return depre_s(w, prefix) if depre_s(w, prefix) in vocab else w

def depre_cloud(w, vocab, prefixes):
    return {depre_w(w, vocab, pre) for pre in prefixes}

def drop_prefix(vocab, prefix):
    return set(map(lambda w: depre_w(w, vocab, prefix), vocab))

def drop_prefixes(vocab, prefixes):
    return reduce(
        lambda acc, elm: acc.intersection(elm),
        [drop_prefix(vocab, pre) for pre in prefixes],
        set(vocab))

# Use post-dictionary API call
def all_word_freqs():
    return __read_data__("./frequency/world_scrabble_freq.txt", ":")

def corpus_word_freqs():
    return __read_data__("./frequency/corpus_scrabble_freq.txt", ":")

def offensive_words():
    return words_from_file("./offensive/offensive.txt")

def scrabble_dictionary():
    return words_from_file("./dictionary/scrabble.txt")

def prefixes():
    return words_from_file("./dictionary/prefixes.txt")

# Used pre-dictionary API call
def stem_freqs(word_freqs):
    return __reduce_map__(word_freqs, 0, lambda acc, v: acc + v, stem)
