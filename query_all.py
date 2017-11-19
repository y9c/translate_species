#! /usr/bin/env python3
#
#     File Name           :     query_all.py
#     Created By          :     yc
#     Creation Date       :     [2017-03-20 18:31]
#     Last Modified       :     [2017-05-03 21:17]
#     Description         :     input must be a file
#


"""Example usage of terminaltables with colorclass.
Translate species name into chinese
"""

import re
import os
import sys
import getopt
import pickle
import urllib.parse
import urllib.request
from colorclass import Color
from terminaltables import SingleTable

if os.path.islink(__file__):
    __location__ = os.path.dirname(os.readlink(__file__))
else:
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


with open(os.path.join(__location__, './species.data.pickle'), 'rb') as f:
    sub = pickle.load(f)


def open_query(f):
    with open(f) as quef:
        que = [line.replace("\n", "") for line in quef]
    return que


def correct_name(quename):
    decam = " ".join(re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)', quename))
    recap = " ".join(re.split('_| ', decam)).capitalize()
    corrname = recap

    if corrname == quename:
        corrtype = "unchanged"
    else:
        corrtype = "changed"
    if corrname not in sub:
        corrtype = "empty"

    return corrname, corrtype


def wikiname(title):
    """From a title (species or genus), get a variety of
    information: the (english) common name; list of species.
    """

    try:
        q = urllib.parse.urlencode(dict(action='raw', title=title))
        url = "%s?%s" % (wikibase, q)
        body = urllib.request.urlopen(url).read().decode('utf-8')
        r1 = re.compile(r"==.*?==\n{{VN\n(.*?)\n}}", re.DOTALL)
        vn = re.findall(r1, body)[0]
        r2 = re.compile(r"\|zh=(.*?)\n")
        vc = re.findall(r2, vn)
        res = ";".join(vc)
    except:
        res = ""

    return res


def local_query(list):
    table_data = [["LatinName >>", "ChineseName"]]
    for i in list:
        corrname, corrtype = correct_name(i)
        if corrtype == "unchanged":
            table_data.append([i, sub[i]])
        elif corrtype == "changed":
            table_data.append(
                [Color('{autocyan}' + i + '{/autocyan}'), Color(sub[corrname])])
        else:
            table_data.append([Color('{autored}' + i + '{/autored}'), ""])
    return table_data


def online_query(list):
    table_data = [["LatinName >>", "ChineseName"]]
    for i in list:
        corrname, corrtype = correct_name(i)
        if corrtype == "unchanged":
            table_data.append([i, sub[i]])
        elif corrtype == "changed":
            table_data.append(
                [Color('{autocyan}' + i + '{/autocyan}'), Color(sub[corrname])])
        else:
            print(bcolors.WARNING + "Searching " + corrname + " online in wikipedia..." + bcolors.ENDC)
            onlinesub = wikiname(corrname)
            table_data.append([Color('{autored}' + i + '{/autored}'), Color('{autoyellow}' + onlinesub + '{/autoyellow}')])
    return table_data


def allonline_query(list):
    table_data = [["LatinName >>", "ChineseName"]]
    for i in list:
        corrname, corrtype = correct_name(i)
        if corrtype == "unchanged":
            table_data.append([i, sub[i]])
        elif corrtype == "changed":
            table_data.append(
                [Color('{autocyan}' + i + '{/autocyan}'), Color(sub[corrname])])
        else:
            table_data.append([Color('{autored}' + i + '{/autored}'), ""])
    return table_data


def table_print(table_data):
    print()
    """Return table string to be printed."""
    table_instance = SingleTable(table_data, 'Species Name Translate')
    table_instance.inner_heading_row_border = True
    table_instance.inner_row_border = True
    table_instance.justify_columns = {0: 'center', 1: 'center'}
    return table_instance.table


# online resoure in wikipedia
wikibase = 'http://species.wikimedia.org/'


def usage():
    usage_content = """
    Pass a file as a argument!
    Use --type \"local, online, alloneline\"
    \t\tto select search type
    \n
    There is plenty of bugs....
    May fixed someday
    """
    print(bcolors.OKBLUE+ usage_content+bcolors.ENDC)
    sys.exit()


def main():
    try:
        options, args = getopt.getopt(
            sys.argv[1:], "ht:u:", ["help", "type=", "update="])
    except getopt.GetoptError:
        print("wrong args!!")
        usage()

    for name, value in options:
        if name in ("-h", "--help"):
            usage()

    if len(args) == 0:
        print("\tno file input")
        usage()
    elif not os.path.isfile(args[0]):
        print(os.getcwd())
        print(args[0])
        print("not a file")
        usage()

    # update = True
    # for name, value in options:
    # if name in ("-u", "--update"):
    # update = value

    command = 'local'
    for name, value in options:
        if name in ("-t", "--type"):
            command = value

    if command == 'local':
        print(table_print(local_query(open_query(args[0]))))
    elif command == 'online':
        print(table_print(online_query(open_query(args[0]))))
    elif command == 'allonline':
        print(table_print(allonline_query(open_query(args[0]))))
    else:
        usage()


if __name__ == '__main__':
    main()
