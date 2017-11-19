#! /usr/bin/env python3
###############################################################################
#     File Name           :     query_name.py
#     Created By          :     yc
#     Creation Date       :     [2017-03-20 18:31]
#     Last Modified       :     [2017-03-21 21:35]
#     Description         :
###############################################################################


"""Example usage of terminaltables with colorclass.
Just prints sample text and exits.
"""

import re
from colorclass import Color
# from terminaltables import SingleTable
from terminaltables import SingleTable
import sys
import pickle

with open('./species.data.pickle', 'rb') as f:
    sub = pickle.load(f)

# with open("./all.species.tsv") as subf:
    # sub = dict([line.replace("\n", "").split("\t") for line in subf])


def open_query(f):
    with open(f) as quef:
        que = [line.replace("\n", "") for line in quef]
    return que


def correct_name(quename):
    decam = " ".join(re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)', quename))
    recap = " ".join(re.split('_| ', decam)).capitalize()
    return recap


def query_name(list):
    table_data = [["LatinName >>", "ChineseName"]]
    for i in list:
        if i in sub:
            table_data.append([i, sub[i]])
        elif correct_name(i) in sub:
            table_data.append([Color('{autocyan}' + i + '{/autocyan}'), Color(sub[correct_name(i)])])
        else:
            table_data.append([Color('{autored}' + i + '{/autored}'), ""])
    return table_data


# table_data = [
    # [Color('{autocyan}Nominal Space{/autocyan}'), Color('Excessive Space')],
    # [Color('Nominal Load'), Color('{autored}High Load{/autored}')],
    # [Color('{autocyan}Low Free RAM{/autocyan}'), Color('High Free RAM')],
# ]


def table_print(table_data):
    """Return table string to be printed."""
    table_instance = SingleTable(table_data, 'Species Name Translate')
    table_instance.inner_heading_row_border = True
    table_instance.inner_row_border = True
    table_instance.justify_columns = {0: 'center', 1: 'center'}
    return table_instance.table


print()
print(table_print(query_name(open_query(sys.argv[1]))))
print()
