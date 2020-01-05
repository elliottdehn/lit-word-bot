import requests
import secrets as secrets
import re
import json


class WebsterClient:

    d_key = secrets.webster_dict_key
    t_key = secrets.webster_thes_key

    dictionary_base = "https://www.dictionaryapi.com/api/v3/references/collegiate/json"
    thesaurus_base = "https://www.dictionaryapi.com/api/v3/references/thesaurus/json"

    def __init__(self):
        self.d_cache = dict()
        self.t_cache = dict()

    def define(self, word, fetch=True):
        if(word not in self.d_cache and fetch):
            self.d_cache[word] = requests.get(
                self.dictionary_base + "/" + word + "?key=" + self.d_key).json()
        elif(word not in self.d_cache and not fetch):
            return None

        return DictionaryResult(word, self.d_cache[word])

    def thesaurus(self, word, fetch=True):
        if(word not in self.t_cache and fetch):
            self.t_cache[word] = requests.get(
                self.thesaurus_base + "/" + word + "?key=" + self.t_key).json()
        elif(word not in self.t_cache and not fetch):
            return None

        return ThesaurusResult(self.t_cache[word])


class DictionaryResult:

    def __init__(self, word, json):
        self.json = json
        self.word = word

    def exists(self):
        return len(self.json) != 0 and type(self.json[0]) is not str

    #For frequency tallying purposes
    def variants(self, phrases=False):
        vs = set()
        if (self.exists()):
            #well-formed stems provided by the dictionary
            vs = vs.union(self.metavariants())
            #for things like "cannot/can't help oneself"
            vs = vs.union(self.subvariants(vs))
            #clever way to grab additional stems/variants
            #ex: orangish -> orange | snakily -> snake
            vs = vs.union(self.link_words())
            vs = set(filt.toLower() for filt in filter(lambda w: "-" in w, vs))
            if (phrases):
                return vs
            else:
                return set(filter(lambda v: len(v.split()) == 1, vs))
        else:
            return None

    def link_words(self):
        link_words = re.findall(r"(?<={a_link\|)([^}]+)(?=})", json.dumps(self.json))
        return set(link_words)

# "Private"

    def find_alternatives(self, v):
        if "/" in v:
            words = v.split()
            alt_splits = set(filter(lambda word: "/" in word, words))
            alt_splits = [splt.replace("'", "") for splt in alt_splits]
            ss = set()
            for splt in alt_splits:
                alts = splt.split("/")
                ss = ss.union(set(filter(lambda a: a != self.word, alts)))
            return set(ss)
        return None

    def metavariants(self):
        if (self.exists()):
            entries = set()
            for entry in self.json:
                meta_entries = entry["meta"]["stems"]
                entries = entries.union(set(meta_entries))
            return entries
        else:
            return None

    def subvariants(self, variants):
        s = set()
        for variant in variants:
            alts = self.find_alternatives(variant)
            if alts is not None:
                s = s.union(alts)
        return s


class ThesaurusResult:

    def __init__(self, json):
        self.json = json

    def variants(self): pass
