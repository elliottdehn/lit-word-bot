# https://www.reddit.com/r/raerth/comments/cw70q/reddit_comment_formatting/

from functools import reduce


def b(b):
    return "**" + str(b) + "**"


def it(i):
    return "_" + str(i) + "_"

# no closing tag!


def ss(u):
    return "^" + str(u)


def code(c):
    return "`" + str(c) + "`"


def code_line(c, indent):
    ret = "    "
    for i in range(indent):
        ret += "    "
    return ret + c


def quote(q):
    return ">" + q


def link(desc, url):
    return "[" + desc + "]" + "(" + url + ")"


def newline():
    return "    "  # four spaces

# Paragraphs in Lists and Nested lists using a combination
# of ordered and unordered lists are no longer supported.


def p(p):
    return p + "\n\n"


def list_item(pre, li):
    return pre + li + "\n"


def nested_list_item(pre, li):
    return " " + list_item(pre, li) + "\n"


def p_list(ls, nest=False):
    ret = ""
    for item in ls:
        if(not nest):
            ret += list_item("+", item)
        else:
            ret += nested_list_item("", item)
    return ret


def n_list(ls):
    idx = 1
    ret = ""
    for item in ls:
        pre = str(idx) + "."
        ret += list_item(pre, item)
        idx += 1
    return ret


def rule():
    return "\n***\n"


def header(n, txt):
    ret = ""
    for i in range(n):
        ret += "#"
    return ret.slice[0:6] + " " + txt


def cr():
    return "\n--\n"


def user(u):
    return "/u/" + u

# Task-specific formatting


def designate(d):
    return b(d)


def designate_w(w):
    return designate(code(w.upper()))


def pos(p):
    return it(p)


def mean(d):
    return it(d)


def sj(*s):
    return " ".join(s)


def greet(u, word):
    return sj("Hey", user(u + ","), designate_w(word), "is a great word!")


def bc():
    return " " + b(":") + " "


def sense(defs):
    root = [designate(defs[0])]
    others = ["..or " + mean(d) for d in defs[1:]]
    root.extend(others)
    return p_list(root, nest=True)


def definition(word, pos, defs):
    return \
        p(sj(it("(" + pos + ")"), designate_w(word))) + \
        n_list([sense(sn) for sn in defs])

def disclaimer():
    return \
        ss("(Downvote this if I was a bad bot! I will immediately delete it.)") \
        + newline() \
        + ss(link("github", "https://github.com/elliottdehn/lit-word-bot"))


def make_response(word, comment, entries):
    resp = greet(comment.author.name, word) + rule()
    for meta_id, entry in entries.items():
        resp = resp + definition(entry["hwi"]["hw"], entry["fl"], [entry["shortdef"]])
        resp = resp + rule()
        resp = resp + disclaimer()
    return resp
