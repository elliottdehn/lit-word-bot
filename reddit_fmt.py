# https://www.reddit.com/r/raerth/comments/cw70q/reddit_comment_formatting/

from functools import reduce


def bold(b):
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
    return str(c)


def quote(q):
    return ">" + str(q)


def link(desc, url):
    return "[" + str(desc) + "]" + "(" + str(url) + ")"


def newline(l):
    return str(l) + "    "  # four spaces

# Paragraphs in Lists and Nested lists using a combination
# of ordered and unordered lists are no longer supported.


def paragraph(p):
    return p + "\n\n"


def list_item(pre, li):
    return pre + " " + str(li) + "\n"


def nested_list_item(pre, li):
    return " " + list_item(pre, li)


def p_list(ls, nest=False):
    ret = ""
    for item in ls:
        if(not nest):
            ret += list_item("+", item)
        else:
            ret += nested_list_item("+", item)
    return ret


def n_list(ls, nest=False):
    idx = 1
    ret = ""
    for item in ls:
        pre = str(idx) + "."
        if(not nest):
            ret += list_item(pre, item)
        else:
            ret += nested_list_item(pre, item)
        idx += 1
    return ret


def rule():
    return "\n***\n"

def header(n, txt):
    ret = ""
    for i in range(n):
        ret += "#"
    return ret.slice[0:6] + " " + str(txt)

def user(un):
    return "/u/" + un

# Task-specific formatting

def designate(w):
    return bold(code(w))

def pos(p):
    return it(p)

def mean(d):
    return code(d)

def pad(n):
    empties = ""
    for i in range(n):
        empties += "⠀"  #NOT a space
    return empties

def pads(w):
    return pad(len(w))

out = \
    "Hey" + user("peterpants") + ", " + \
    designate("SQUIB") + " is a " + "cool" + " word!" + \
    rule() + \
    paragraph(designate("SQUIB") + " means:") + \
    n_list([pos("(verb)") + mean("a short humorous or satiric writing or speech")]) + \
        p_list(["something", "different"], nest=True) + \
    n_list([pos("(noun)") + mean("a small firecracker")]) + \
        p_list(["another", "thing"], nest=True) 

f = open("out.txt", "w+")
f.write(out)
f.close()
