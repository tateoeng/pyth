#!/bin/python
################################################################################
# pyth, a suite of tools for manipulating text files from inside the python interpretter
################################################################################
# glossary:
# text - txt file stored to a local dictionary
# selection - one or more texts
# shelf - a dictionary in which to store texts
# manipulation - an action performed on a text
#################################################################################
shelf, ft, fb, nl = {}, '', [], '\n'

from datetime import datetime
from itertools import chain
from os import get_terminal_size
from os import listdir
from os import remove
from os import system
from os.path import isdir
from sys import argv
import inspect
import readline
import types

################################################################################
# model:
# define the core of the function with well-defined arguments.
# def function_(arguments, inscription, selection):
    # global shelf, ft, fb
#   ... some set of instructions which returns a list (with exceptions) ...
#
# create an interface which accounts for a variety of inputs
# def f(arguments = None, inscription = None, selection = None):
    # global shelf, ft, fb
    # if selection is None: selection = [title for title in shelf.keys()]
    # elif isinstance(selection, str):
        # for title in selection.split(','):
            # if isinstance(inscription, str): inscription = inscription.strip('\n') + '\n'
            # elif isinstance(inscription, list):
                # formatted_arguments = []
                # for argument in arguments.split(';'):
       # try: formatted_arguments.append(int(argument))
                    # except: formatted_arguments.append(argument)
                # return function_(formatted_arguments, inscription, title)
################################################################################

################################################################################
# file tools
################################################################################
# shelve_() sh() 'shelves' 'selections' of 'texts': stores disk text files to local dictionary 'shelf' as list
################################################################################
def shelve_(title): # title is a string, the filename
    global shelf, ft, fb
    text = open(title, 'r')
    try: shelf[title] = [line for line in text]
    except UnicodeDecodeError as e: pass
    text.close()

def sh(selection = None):
    global shelf, ft, fb
    if selection is None:
        for title in listdir('.'):
            if not isdir(title): shelve_(title)
    elif isinstance(selection, str):
        for title in selection.split(','): shelve_(title)

sh()
################################################################################
# remove_() rm() 'removes' 'selection' from 'shelf': depopulates dictionary of specified entries
################################################################################
def remove_(title):
    global shelf
    del shelf[title]

def rm(selection = None):
    global shelf, ft, fb
    if selection is None: shelf, ft, fb = {}, '', []
    elif isinstance(selection, str):
        for title in selection.split(';'): del shelf[title]

################################################################################
# table_() tb() 'tables' 'text':  sets working title (does not by default see backups)
################################################################################
def ls():
    global shelf, ft, fb
    list = [title for title in shelf.keys()]
    list.sort()
    for item in list: print(item)

def table_(title):
    global shelf, ft, fb
    ft, fb = title, shelf[title]

def tb(title = None):
    global shelf, ft, fb
    if title is None:
        titles = [title for title in shelf.keys() if title is not None and not title.startswith('.')]
        titles.sort()
        for title in titles: print(title)
    elif isinstance(title, str) and title in shelf.keys():
        table_(title)
        print('\n tabled: ' + title + '\n')


################################################################################
# utilities
################################################################################
# print_() p() wrapping changes with print_ prints text to terminal
################################################################################
def print_(text):
    for line in text: print(line, end = '')

def p(selection = None):
    global shelf, ft, fb
    if selection is None: p(fb)
    elif isinstance(selection, str):
        if selection in shelf.keys(): p(shelf[selection])
        else: p([selection])
    elif isinstance(selection, list): print_(selection)

################################################################################
# number_() n() wrapping changes with number_ returns numbered list of strings
################################################################################
def number_(text):
    global shelf, ft, fb
    return [str(n) + '\t' + line for n, line in enumerate(text)]

def n(selection = None):
    global shelf, ft, fb
    if selection is None: return n(fb)
    elif isinstance(selection, str):
        if selection in shelf.keys(): return n(shelf[selection])
        else: return n([selection])
    elif isinstance(selection, list): return number_(selection)

def pn(selection = None): p(n(selection))

##############################################################################################################
# two simple list manipulations
##############################################################################################################
# line_() ln() print specified line
##############################################################################################################
def line_(n, text):
    global shelf, ft, fb
    return text[n]

def ln(n, text = None):
    global shelf, ft, fb
    if text is None: return ln(n, shelf[ft])
    if isinstance(n, str): ln(int(n), text)
    else: return line_(n, text)

################################################################################
# append_() app() append line or list of lines to working text
################################################################################
def append_(pendant, text):
    global shelf, ft, fb
    return text + pendant

def app(pendant = None, text = None):
    global shelf, ft, fb
    if text is None: return app(pendant, shelf[ft])
    elif isinstance(text, str): return app(pendant, [text.rstrip('\n') + '\n'])
    elif isinstance(text, list):
        if pendant is None: return app([], text)
        elif isinstance(pendant, str): return app([pendant.rstrip('\n') + '\n'], text)
        elif isinstance(pendant, list): return append_(pendant, text)

def papp(pendant = None, text = None): return p(app(pendant, text))
def napp(pendant = None, text = None): return n(app(pendant, text))
def pnapp(pendant = None, text = None): return p(n(app(pendant, text)))

################################################################################
# file tools (continued)
################################################################################
# commit_() c() store changes in shelf copy
################################################################################
def commit_(text, title):
    global shelf, ft, fb
    shelf[title] = text[:]
    tb(title)

def c(text, title = None):
    global shelf, ft, fb
    if title is None: c(text, ft)
    elif isinstance(text, str): c([text], title)
    else: commit_(text, title)

def capp(pendant = None, text = None): c(app(pendant, text))

################################################################################
# save_() sv() save specified shelved selection to disk
################################################################################
def save_(text, title):
    global shelf, ft, fb
    f = open(title, "w")
    for line in text: f.write(line)
    f.close()

def s(text = None, title = None):
    global shelf, ft, fb
    if text is None: s(fb, title)
    elif title is None: s(text, ft)
    else: save_(text, title)

def sp(): s(); pn()

def cs(text, title = None):
    global shelf, ft, fb
    if title is None: cs(text, ft)
    else:
        c(text)
        s()

################################################################################
# getinput
# getinput() gi() get multiline input
################################################################################
def getinput():
    contents = []
    while True:
        try: line = input()
        except EOFError: break
        contents.append(line + '\n')
    return contents

def gi(): return getinput()

################################################################################
# timestamp_() ts() returns formatted timestamp string
################################################################################
def timestamp_():
    dt = datetime.now()
    fdt = dt.strftime('%Y-%m-%d-%H.%M.%S')
    return str(fdt)

def ts(): return timestamp_()

################################################################################
# backup_() bk() save copy of specified title with timestamp prepended to the title
################################################################################
def backup_(text, title):
    global shelf, ft, fb
    s(text, title)
    newtitle = '.' + ts() + '-' + title
    f = open(newtitle, "w")
    for line in text: f.write(line)
    f.close()
    sh()
    tb(title)

def bk(text = None, title = None):
    global shelf, ft, fb
    if title is None: bk(text, ft)
    elif text is None: bk(shelf[ft], title)
    else: backup_(text, title)

def sbp(): s(); bk(); pn()

################################################################################
# restore_() rs() restore backup copy of file to disk
################################################################################
def restore_(title):
    working_title = ft
    shelve_(title)
    table_(title)
    commit_(fb, working_title)
    table_(working_title)
    save_(fb, ft)

def rs(title = None):
    if title is None:
        keys = [key for key in shelf.keys()]
        for key in keys:
            if ft in key and not ft is key and key.startswith('.'): print(key)
        print('enter your desired backup title (control-c to escape):')
        rs(input())
    else: restore_(title)

################################################################################
# remove_() rm() remove title from shelf
################################################################################
def remove_(title):
    print('removing...')
    r = shelf.pop(title)
    print(r)

################################################################################
# delete_() dl() deletes text files from disk
################################################################################
def delete_(title):
    affirm = input('do you want to delete ' + str(title) + '? (y/n) ')
    if affirm == 'y':
        remove_(title)
        remove(title)

def dl(titles = None):
    if titles is None: dl(ft)
    elif isinstance(titles, str):
        for t in titles.split(';'): delete_(t)

################################################################################
# list manipulations:
################################################################################
# include_() inc() return specified lines from list of strings; special formatted '0-10;15-20'
#     range_ will be passed to include_ as a list of either one or two integers
################################################################################
# dependencies:   
# include_()
# expand_()
    # inc()
    # invert_()     
        # exclude_()
            # exc()
# Define `include_,` a function, with arguments `passages,` a list of integers, and `text,` a list of strings:
# - Return a list containing the strings in `text` at each `position` in `passages.`
################################################################################
def include_(passages, text):
    return [text[position] for position in passages]

def expand_(passages = None, text_length = None):
    global shelf, ft, fb
    if text_length is None: return expand_(passages, len(fb))
    elif isinstance(text_length, str): return expand_(passages, int(text_length))
    elif isinstance(text_length, int):
        if passages is None: return []
        elif ';' in passages or '-' in passages: 
            return expand_([i.split('-') for i in passages.split(';')], text_length)
        elif isinstance(passages, str): return expand_([[passages]], text_length)
        elif isinstance(passages, list):
            if isinstance(passages[0], list):
                if isinstance(passages[0][0], str):
                    return expand_([[int(i[0])] if len(i) == 1 \
                        else [j for j in range(int(i[0]), int(i[1]) + 1)] for i in passages], text_length)
                if isinstance(passages[0][0], int): return list(chain(*passages))
            else: return passages

def inc(passages = None, text = None):
    global shelf, ft, fb
    if text is None: return inc(passages, fb)
    elif isinstance(text, str): return [string.rstrip('\n') + '\n']
    elif isinstance(text, list):
        if passages is None: return text
        elif isinstance(passages, int): return text[passages]
        elif isinstance(passages, str): return include_(expand_(passages, len(text)), text)

def pinc(inclusions = None, body = None): return p(inc(inclusions, body))
def ninc(inclusions = None, body = None): return n(inc(inclusions, body))
def pninc(inclusions = None, body = None): return p(inc(inclusions, n(body)))
def cinc(inclusions = None, body = None): c(inc(inclusions, body))

################################################################################
# utilities (2):
################################################################################
# invert_() inverts list of inclusions
################################################################################
def invert_(passages = None, text_length = None):
    global shelf, ft, fb
    if text_length is None: return invert_(passages, len(fb))
    if isinstance(passages, int):
        return invert_(str(passages), text_length)
    return [i for i in range(0, text_length) \
        if i not in expand_(passages, text_length)]
    # try:
        # return [i for i in range(text_length) if i not in expand_(passages, text_length)]
    # except:
        # print('whoops')

################################################################################
# list manipulations (2):
################################################################################
# exclude_() exc() return all lines other than those specified
################################################################################
def exclude_(exclusions, text):
    return include_(invert_(exclusions, len(text)), text)

def exc(exclusions, text = None):
    global shelf, ft, fb
    if text is None: return exc(exclusions, fb)
    elif isinstance(text, list):
        if isinstance(exclusions, int): return exc(str(exclusions), text)
        elif isinstance(exclusions, str): return exclude_(exclusions, text)
        
def pexc(exclusions, text = None): p(exc(exclusions, text))
def nexc(exclusions, text = None): exc(exclusions, n(text))
def pnexc(exclusions, text = None): p(exc(exclusions, n(text)))
def cexc(exclusions, text = None): c(exc(exclusions, text))

################################################################################
# head_() hd()
################################################################################
def head_(n, text): return [text[i] for i in range(n)]

def hd(n, text = None):
    global shelf, ft, fb
    if text is None: return hd(n, fb)
    elif isinstance(text, list): return head_(n, text)

################################################################################
# tail_() tl()
################################################################################
def tail_(n, text): return [text[i] for i in range(n, len(text))]

def tl(n, text = None):
    global shelf, ft, fb
    if text is None: return tl(n, fb)
    elif isinstance(text, list): return tail_(n, text)

################################################################################
#   insert_() ins() insert line or list of lines at specified line number 
#   of working text
################################################################################
def insert_(insertion, position, text):
    return head_(position, text) + insertion + tail_(position, text)

def ins(insertion, position, text = None):
    global shelf, ft, fb
    if text is None: return ins(insertion, position, fb)
    elif isinstance(text, list):
        if isinstance(insertion, str): return ins([insertion], position, text)
        else: return insert_(insertion, position, text)

def pins(insertion, position, text = None): p(ins(insertion, position, text))
def nins(insertion, position, text = None): return ins(insertion, position, n(text))
def pnins(insertion, position, text = None): p(ins(insertion, position, n(text)))
def cins(insertion, position, text = None): c(ins(insertion, position, text))

################################################################################
#   utilities (3)
################################################################################
#   hist_()
#   returns history of python commands given to interpreter as lines
################################################################################
def hist_(): return [str(readline.get_history_item(i + 1)) + '\n' for i in range(readline.get_current_history_length())]

def h():
    shelf['history'] = hist_()
    p(shelf['history'])

################################################################################
#   last_()
#   returns last entered python command as string
################################################################################
def last_():
    shelf['history'] = hist_()
    return shelf['history'][-2].rstrip('\n')

def last(): return last_()
def l(): last_()
def pl(): p(last_())

################################################################################
# functions_() - returns list of user-defined functions
################################################################################
def functions_():
    functions = [str(f).split(' ')[1] for f in globals().values() \
        if type(f) == types.FunctionType]
    functions.sort()
    return functions

def funcs(): return functions_()

################################################################################
# gs() - returns list of lines which, when printed, give the script for a user-defined function
################################################################################
def gs(function): return [inspect.getsource(function)]
def pgs(function): p(gs(function))

################################################################################
# search_and_replace_() snr() if only search is specified,
#     returns numbered list of lines containing search
#     otherwise, performs global search and replace
#     note that search_() can forgo text input because n() can
################################################################################
def search_(search, text = None): print_([line for line in n(text) if search in line])

def search_and_replace_(search, replace, text):
    return [line.replace(search, replace) for line in text]

def snr(search, replace = None, text = None):
    if text is None: return snr(search, replace, fb)
    elif isinstance(text, str): return snr(search, replace, [text + '\n'])
    elif isinstance(text, list):
        if replace is None: return search_(search, text)
        elif isinstance(replace, str): return search_and_replace_(search, replace, text)

def psnr(search, replace = None, text = None): p(snr(search, replace, text))
def nsnr(search, replace = None, text = None): snr(search, replace, n(text))
def pnsnr(search, replace = None, text = None): psnr(search, replace, n(text))
def csnr(search, replace = None, text = None): c(snr(search, replace, text))

################################################################################
# notes
################################################################################
# do for variables what you've done for functions.
################################################################################
def variables_(): return [i for i in dir() if i not in funcs()]
def vars(): return variables_()

################################################################################
# move_() mov() move line or list of lines from one specified point to another
# move down:
# exc('1', inc('0-3')) + inc('1') + inc('4')
# exc(n, inc(0 - (n-1))) + inc(n) + inc(n+1 - end)
################################################################################
def move_dn_(movers, position, text):
    return exclude_(movers, head_(position - 1, text)) \
        + include_(expand_(movers), text) \
        + include_([i for i in range(position, len(text))], text)    
    
################################################################################
# move up:
# inc('0') + inc('3') + exc('3', inc('1-4'))
# inc(beg - n-1) + inc(n) + exc(n, inc(n+1 - end))
################################################################################
def move_up_(movers, position, text):
    return include_([i for i in range(position)], text) \
        + include_(expand_(movers), text) \
        + include_([i for i in range(position, len(exclude_(movers, text)))], \
            exclude_(movers, text))

def mov(movers, position, text = None):
    if text is None: return mov(movers, position, fb)
    else:
        movers = expand_(movers)
        if movers[-1] < position: return move_dn_(movers, position, text)
        else: return move_up_(movers, position, text)
    
def pmov(movers, position, text): p(mov(movers, position, text))
def nmov(movers, position, text): return mov(movers, position, n(text))
def pnmov(movers, position, text): p(mov(movers, position, n(text)))
def cmov(movers, position, text): c(mov(movers, position, text))

################################################################################
# swap_() swp() swap the positions of two groups of lines in the same working 
# text.
################################################################################
def swap_(passage2, passage4, text):
    passage1 = [i for i in range(0, passage2[0])]
    passage3 = [i for i in range(passage2[-1] + 1, passage4[0])]
    passage5 = [i for i in range(passage4[-1] + 1, len(text))]
    return include_(passage1 + passage4 + passage3 + passage2 + passage5, text)

def swp(passage2, passage4, text = None): 
    if text is None: return swp(passage2, passage4, fb)
    else: return swap_(passage2, passage4, text)
    
def pswp(passage2, passage4, text = None): p(swp(passage2, passage4, text))
def nswp(passage2, passage4, text = None): return swp(passage2, passage4, n(text))
def pnswp(passage2, passage4, text = None): p(swp(passage2, passage4, n(text)))
def cswp(passage2, passage4, text = None): c(swp(passage2, passage4, text))

################################################################################
# shortcuts for utilites p, n and c paired to list manipulations
################################################################################
# print_include             pinc    pexc    papp    pins    pmov    pswp    psnr
# number_include            ninc    nexc
# print_number_include      pninc   pnexc
# commit_include            cinc    cexc
# commit_save_include       csinc   csexc
#
# history_                  hst     returns history of python commands as list of strings
# last_                     lst     returns last executed command as string
# functions_                fnc     returns list of locally defined functions as list of strings
# function_source_          fns     returns function source as list of strings
#
# set_page_length_          spl     sets default page length, in number of lines
# page_  pg      prints current page
# page_down_                pgd     advance page and print
# page_up_                  pgu     rewind page and print
################################################################################

# fix pn() and pn-headed functions
# pygmentize

if len(argv) > 1: tb(argv[1])
else: tb(argv[0])

def clear(): system('clear')

current_page_number = 1

def page(n = None, text = None):
    global current_page_number
    page_height = int(get_terminal_size().lines - 1)
    if text is None: page(n, fb)
    elif isinstance(text, list):
        if n is None: 
            n = current_page_number
            page(n)
        else:
            bgn = (n - 1) * page_height
            end = n * page_height
            clear()
            print_(include_([i for i in range(bgn, end)], number_(text)))
            current_page_number = n

def next():
    global current_page_number
    current_page_number += 1
    page(current_page_number)
    
def prev():
    global current_page_number
    current_page_number -= 1
    page(current_page_number)
    
# search_()
# list_()
    
def list_():
    global shelf
    return [title for title in shelf.keys()]
