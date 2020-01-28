import requests
import secrets as secrets
import re
import json
from functools import lru_cache

class WebsterClient:

    d_key = secrets.webster_dict_key

    dictionary_base = "https://www.dictionaryapi.com/api/v3/references/collegiate/json"
    
    @lru_cache(maxsize=None)
    def define(self, word):
        r = requests.get(self.dictionary_base + "/" + word + "?key=" + self.d_key).json()
        return DictionaryResult(word, r)

class DictionaryResult:

    def __init__(self, word, json):
        self.json = json
        self.word = word

    def exists(self):
        return \
            len(self.json) != 0 \
            and type(self.json[0]) is not str

    def is_name(self):
        for entry in self.json:
            if "fl" not in entry or "name" in entry["fl"]:
                return True
        return False

    # for words like "noontime", "hellbent", "douchebag"... while keeping "carboy"
    def is_simple_mashup(self, vocab):
        for entry in self.json:
            hws = re.findall(r"[\w']+", entry["hwi"]["hw"])
            if len(hws) == 2:
                left, right = hws
                if left in vocab and right in vocab:
                    for shortdef in entry["shortdef"]:
                        if left in shortdef or right in shortdef:
                            return True
        return False

                



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
            vs = vs.union(set(self.link_words()))

            if (phrases):
                return vs
            else:
                vs = set(map(lambda w: w.lower(), filter(lambda w: "-" not in w, vs)))
                return set(filter(lambda v: len(v.split()) == 1, vs))
        else:
            return None

    def link_words(self):
        link_words = re.findall(r"(?<={a_link\|)([^}]+)(?=})", json.dumps(self.json))
        return link_words

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

    def offensive(self):
        for entry in self.json:
            if (entry["meta"]["offensive"]):
                return True
        return False

    def short_defs(self):
        ret = dict()
        for entry in self.json:
            ret[entry["meta"]["id"]] = (entry["fl"], entry["shortdef"])
        return ret

    # Select the definition entries for whom at least one stem is in the comment
    def matches(self, text):
        matches = dict()
        if (len(self.json) == 1):
            entry = self.json[0]
            matches[entry["meta"]["id"]] = entry
            return matches
        else:
            for entry in self.json:
                stems = entry["meta"]["stems"]
                for stem in stems:
                    if stem in text.lower():
                        matches[entry["meta"]["id"]] = entry
                        break
        return matches

    #filter down for the matches who have the "longest match"
    def best_matches(self, matches, text):
        #first, find the longest match length
        maxMatch = ""
        for meta_id, entry in matches.items():
            for stem in entry["meta"]["stems"]:
                if len(stem) > len(maxMatch) and stem in text.lower():
                    maxMatch = stem
        
        # Now get all of the entries with stems in the text which meet that length
        ret = dict()
        for meta_id, entry in matches.items():
            for stem in entry["meta"]["stems"]:
                if (len(stem) == len(maxMatch) and stem in text.lower()):
                    ret[meta_id] = entry
                    break

        return ret
