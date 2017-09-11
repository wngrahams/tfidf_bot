import operator
import os

__author__ = 'grahamstubbs'


def read_quotes(filename):
    if not os.path.isfile(filename):
        quotes_list = []
    else:
        with open(filename, "r") as file:
            quotes_list = file.read().split()

    quotes_dict = {}
    for i in range(0, len(quotes_list)):
        if quotes_list[i].casefold() not in quotes_dict:
            quotes_dict[quotes_list[i].casefold()] = 1
        else:
            quotes_dict[quotes_list[i].casefold()] += 1

    print(quotes_dict)

    sorted_quotes = sorted(quotes_dict.items(), key=operator.itemgetter(1))
    sorted_quotes.reverse()
    print(sorted_quotes)

#   quotes_dict.clear()
#
#   for i in range(0, len(sorted_quotes)):
#       if sorted_quotes[i][0] not in quotes_dict:
#           quotes_dict[sorted_quotes[i][0]] = sorted_quotes[i][1]
#       else:
#           quotes_dict[sorted_quotes[i][0]] += sorted_quotes[i][1]
#
#   print(quotes_dict)

    return sorted_quotes
