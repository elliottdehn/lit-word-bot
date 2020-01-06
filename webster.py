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
                    if stem in text:
                        matches[entry["meta"]["id"]] = entry
                        break
        pass

    #filter down for the matches who have the "longest match"
    def best_matches(self, matches, text):
        #it's more efficient to create a list structure, then sort it
        #but N is so small for this, it's better to just do it piece by piece

        #first, find the longest match length
        maxMatch = ""
        for head, stems in matches:
            for stem in stems:
                if len(stem) > len(maxMatch) and stem in text:
                    maxMatch = stem
        
        # Now get all of the entries with stems in the text which meet that length
        ret = dict()
        for meta_id, entry in matches:
            for stem in entry["meta"]["stems"]:
                if (len(stem) == len(maxMatch) and stem in text):
                    ret[head] = entry
                    break

        return ret


class ThesaurusResult:

    def __init__(self, json):
        self.json = json

    def variants(self): pass
