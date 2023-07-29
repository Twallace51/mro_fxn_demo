#! /bin/python

"""This script can be run as-is as a visual demo of the c3-linearization algorithm used in mro(),  
It is not an emulation of mro(),  since it orders a list of lists of strings,  rather than lists of objects.

Based on:
   Implements Python Method Resolution Order(MRO)
   https://gist.github.com/bellbind/1614683
   by https://gist.github.com/bellbind

See below for test examples.

twallace51@gmail.com
"""

from rich import print
from pprint import pprint
import os
os.system('clear')
from time import sleep
step_sec = 1   # pause between merge() regressions
bp = breakpoint

def mro(example):
    return tuple(merge(example))

def merge(lists):
    """
    lists is a list of lists,
    where each of the lists is considerered to have a head element and zero or more additional elements in the *tail.
    merge regresively updates the lists by removing a specific head element from the lists,
    until either the lists are all empty,
    or aborts when a head element is also found in the tail of a list.
    This prevents merge from selecting a unique order for all the elements in the lists.

    """

    # lists will be regresively updated below,  save the original here
    original = lists
    MRO = []

    while lists:   # for each list in lists
         # exit when updated lists == []


        print("\nmerging ... \n")

        target = None

        # loop searches for next target
        for current_list in lists:

            # head is first element of current list in loop
            head = current_list[0]

            # True if head not found in tail of any of lists
            if all(head not in _list[1:] for _list in lists):
                # head ACCEPTED as target
                target = head
                break

        if not target:
            # head was found in a tail ==> error
            print(F"\n[red]MRO error:  list contain circular relations involving [green]{head}.[red] \nIn these lists:[normal]")

            # show sublists with problem head (was found in *tail)
            for i in ( [ [_head,*tail]  for [_head,*tail] in original     if head in tail ] ):
                print(i)

            # delete remaining lists to exit while loop and abort further merge() regressions
            lists = []

        # add target to MRO
        MRO.append(target)

        #  `remover` is a generator function
        #     will remove target element from head of all lists
        #     and delete list if empty
        remover = ([e for e in _list if e != target] for _list in lists)

        # update lists in current lists and put them in new lists
        lists = [_list for _list in remover if _list]

        # intermediate results
        for _list in lists: print(_list)
        print("\nCurrent MRO: ", MRO,"\n")
        sleep(step_sec)
        if target:
            os.system('clear')

    return MRO


def convert(_example):
    # initial   [ 'A()', 'B()', 'C()', 'D()', 'E()', 'K1(A,B,C)', 'K2(D,B,E)', 'K3(D,A)', 'Z(K1,K2,K3)']
    # goal:     [ ['A', 'O'], ['B', 'O'], ['C', 'O'], ['D', 'O'], ['E', 'O']', ['K1','A','B',C']', ['K2','D','B','E'], ['K3','D',''A'], ['Z','K1','K2','K3'] ]
    # where each sublist has at least one member (HEAD) and zero or more additional members
    result = []
    for _str in _example:
        _str = "['"+_str
        _str = _str.replace("()", ",O']")     # add implied Object class O to simple classes
        _str = _str.replace(",", "','")
        _str = _str.replace("(", "','")
        _str = _str.replace(")", "']")
        result.append(eval(_str))
    return result

# Demo examples

# Following are lists similar to what would be provided by
#      [list(mro(b)) for b in cls.__bases__]
# are converted to format suitable for merge()

# following has good MRO as test demo - dont edit
good = [
"A()",
"B()",
"C()",
"D()",
"E()",
"K1(A,B,C)",
"K2(D,B,E)",
"K3(D,A)",
"good(K1,K2,K3)",
]
good = convert(good)

# always bad - don't waste your time
bad = [
"A()",
"B()",
"C()",
"D()",
"E()",
"K1(A,B,C)",
"K2(D,B,E,A)",
"K3(D,A)",
"bad(K1,K2,K3)",
]
bad = convert(bad)

# play with this one - there's hope
ugly = [
"A()",
"B()",
"C()",
"D()",
"E()",
"K1(A,B,C)",
"K2(D,B,E,A)",
"K3(D,A)",
"ugly(K1,K2,K3)",
]
ugly = convert(ugly)

# Possible solutions to inconsistent error

#  change order of an A,B B,A pair
#     K1(A,B,C) -> K1(B,A,C)
#  move A to first among base classes
#     in K1 K2 K3
#  move A's to base of another common class
#     A's in K2 and K3 to D

def report(example):
    print("Merging done on:\n", example,  F"\nFinal MRO is:  {mro(example)}\n")

report(good)

#report(bad)

report(ugly)
