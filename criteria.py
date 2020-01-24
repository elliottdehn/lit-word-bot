from datetime import *

blacklist = [
    "anime",
    "asianamerican",
    "askhistorians",
    "askscience",
    "askreddit",
    "aww",
    "chicagosuburbs",
    "cosplay",
    "cumberbitches",
    "d3gf",
    "deer",
    "depression",
    "depthhub",
    "drinkingdollars",
    "FemaleDatingStrategy",
    "forwardsfromgrandma",
    "geckos",
    "giraffes",
    "grindsmygears",
    "indianfetish",
    "me_irl",
    "misc",
    "movies",
    "mixedbreeds",
    "news",
    "newtotf2",
    "omaha",
    "petstacking",
    "pics",
    "pigs",
    "politicaldiscussion",
    "politics",
    "pokemontrades",
    "programmingcirclejerk",
    "raerthdev",
    "rants",
    "runningcirclejerk",
    "salvia",
    "science",
    "seiko",
    "shoplifting",
    "sketches",
    "sociopath",
    "suicidewatch",
    "talesfromtechsupport",
    "TeenAmIUgly"
    "torrent",
    "torrents",
    "trackers",
    "tr4shbros",
    "unitedkingdom",
    "crucibleplaybook",
    "cassetteculture",
    "italy_SS",
    "DimmiOuija",
    "benfrick",
    "bsa",
    "futurology",
    "graphic_design",
    "historicalwhatif",
    "lolgrindr",
    "malifaux",
    "MechanicalKeyboards",
    "nfl",
    "toonami",
    "trumpet",
    "ps2ceres",
    "duelingcorner",
    "medical_advice"
]


def inPastHours(ts, hs):
    difference = timedelta(hours=6)
    delta = timedelta(hours=hs)
    then = datetime.fromtimestamp(ts) + difference
    now = datetime.utcnow()
    res = now-delta <= then
    return res


def subreddit_criteria(sub):
    res = sub.display_name not in blacklist and not sub.over18
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
