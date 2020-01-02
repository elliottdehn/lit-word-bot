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


def newline(l):
    return l + "    "  # four spaces

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


out = \
    greet("peterpants", "squib") + \
    rule() + \
    definition("squib", "verb", [["a short humorous or satiric writing or speech", "a short news item"], ["a small firecracker", "a broken firecracker in which the powder burns with a fizz"], ["a small electric or pyrotechnic device used to ignite a charge"]]) + \
    rule() + \
    definition("squib", "noun", [["to speak, write, or publish squibs"], ["to fire a squib"], ["to utter in an offhand manner", "to make squibs against : LAMPOON"], ["to shoot off : FIRE"], ["to kick (a football) on a kickoff so that it bounces along the ground"]])


f = open("out.txt", "w+")
f.write(out)
f.close()
