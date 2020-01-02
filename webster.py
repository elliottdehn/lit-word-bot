import requests
import secrets as secrets

class WebsterClient:

    d_key = secrets.webster_dict_key
    t_key = secrets.webster_thes_key

    dictionary_base = "https://www.dictionaryapi.com/api/v3/references/collegiate/json"
    thesaurus_base = "https://www.dictionaryapi.com/api/v3/references/thesaurus/json"

    def __init__(self):
        self.d_cache = dict()
        self.t_cache = dict()

    def dictionary(self, word, fetch=True):
        if(word not in self.d_cache and fetch):
            self.d_cache[word] = requests.get(self.dictionary_base + "/" + word + "?key=" + self.d_key).json()
        elif(word not in self.d_cache and not fetch):
            return None
        
        return DictionaryResult(word, self.d_cache[word])
    
    def thesaurus(self, word, fetch=True):
        if(word not in self.t_cache and fetch):
            self.t_cache[word] = requests.get(self.thesaurus_base + "/" + word + "?key=" + self.t_key).json()
        elif(word not in self.t_cache and not fetch):
            return None
        
        return ThesaurusResult(self.t_cache[word])


class DictionaryResult:

    def __init__(self, word, json):
        self.json = json
        self.word = word

    def exists(self):
        return len(self.json) != 0 and type(self.json[0]) is not str 

    def variants(self):
        if (self.exists()):
            vs = set().union(self.metavariants())
            vs = vs.union(self.subvariants(vs))
            return vs
        else:
            return None

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
        if (len(s) != 0):
            return s
        else:
            return None

class ThesaurusResult:

    def __init__(self, json):
        self.json = json
    
    def variants(self): pass
        
