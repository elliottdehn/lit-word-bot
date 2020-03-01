from datetime import *

blacklist = [
    "anime".lower(),
    "asianamerican".lower(),
    "askhistorians".lower(),
    "askscience".lower(),
    "askreddit".lower(),
    "AskTeenGirls".lower(),
    "aww".lower(),
    "chicagosuburbs".lower(),
    "cosplay".lower(),
    "cumberbitches".lower(),
    "d3gf".lower(),
    "deer".lower(),
    "depression".lower(),
    "depthhub".lower(),
    "drinkingdollars".lower(),
    "FemaleDatingStrategy".lower(),
    "forwardsfromgrandma".lower(),
    "geckos".lower(),
    "giraffes".lower(),
    "grindsmygears".lower(),
    "indianfetish".lower(),
    "me_irl".lower(),
    "misc".lower(),
    "movies".lower(),
    "mixedbreeds".lower(),
    "news".lower(),
    "newtotf2".lower(),
    "omaha".lower(),
    "petstacking".lower(),
    "pics".lower(),
    "pigs".lower(),
    "politicaldiscussion".lower(),
    "politics".lower(),
    "pokemontrades".lower(),
    "programmingcirclejerk".lower(),
    "raerthdev".lower(),
    "rants".lower(),
    "runningcirclejerk".lower(),
    "salvia".lower(),
    "science".lower(),
    "seiko".lower(),
    "shoplifting".lower(),
    "shortcels".lower(),
    "sketches".lower(),
    "sociopath".lower(),
    "suicidewatch".lower(),
    "talesfromtechsupport".lower(),
    "TeenAmIUgly".lower(),
    "torrent".lower(),
    "torrents".lower(),
    "trackers".lower(),
    "tr4shbros".lower(),
    "unitedkingdom".lower(),
    "crucibleplaybook".lower(),
    "cassetteculture".lower(),
    "italy_SS".lower(),
    "DimmiOuija".lower(),
    "benfrick".lower(),
    "bsa".lower(),
    "futurology".lower(),
    "graphic_design".lower(),
    "historicalwhatif".lower(),
    "lolgrindr".lower(),
    "malifaux".lower(),
    "MechanicalKeyboards".lower(),
    "nfl".lower(),
    "toonami".lower(),
    "trumpet".lower(),
    "ps2ceres".lower(),
    "duelingcorner".lower(),
    "medical_advice".lower()
]


def inPastHours(ts, hs):
    difference = timedelta(hours=6)
    delta = timedelta(hours=hs)
    then = datetime.fromtimestamp(ts) + difference
    now = datetime.utcnow()
    res = now-delta <= then
    return res


def subreddit_criteria(sub):
    res = str(sub).lower() not in blacklist and not sub.over18
    return res


def comment_criteria(c, score=0, hours=24):
    recent = inPastHours(c.created_utc, hours)
    normal = not c.stickied
    points = c.score >= score
    person = c.distinguished != "moderator"
    res = recent and normal and points and person
    return res


def submission_criteria(s, comments=0, score=0, hours=24):
    res = comment_criteria(s, score=score, hours=hours) \
        and subreddit_criteria(s.subreddit) \
        and not s.locked \
        and s.num_comments >= comments
    return res
