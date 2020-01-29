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

def depre_s(s, prefix):
    return s[len(prefix) :] if s.startswith(prefix) else s

def desuf_s(s, suffix):
    return s[:len(s)-len(suffix)] if s.endswith(suffix) else s

def depre_w(w, vocab, prefix):
    return depre_s(w, prefix) if depre_s(w, prefix) in vocab else w

def desuf_w(w, vocab, suffix):
    return desuf_s(w, suffix) if desuf_s(w, suffix) in vocab else w

def depre_cloud(w, vocab, prefixes):
    return {depre_w(w, vocab, pre) for pre in prefixes}

def desuf_cloud(w, vocab, suffixes):
    return {desuf_w(w, vocab, suf) for suf in suffixes}

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

def suffixes():
    return words_from_file("./dictionary/suffixes.txt")