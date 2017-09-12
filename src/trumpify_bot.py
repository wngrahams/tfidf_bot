import operator
import os
import praw
import requests
import time
import src.ngram_analysis as ng
import src.trumpify as trumpify  # when running in pycharm
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
# import trumpify  # when running in terminal

__author__ = 'grahamstubbs'

# TODO: clean input from txt file
# TODO: clean output (don't reply to comments with a ton of formatting)
# TODO: n-gram analysis

STOP_WORDS = set(stopwords.words('english'))

STR_SEARCH_0 = "sends its people"
STR_SEARCH_1 = "believe me, I have many"
STR_SEARCH_2 = "believe me"
STR_SEARCH_3 = "good"
STR_SEARCH_4 = "very good"
STR_SEARCH_5 = "I have a"
STR_SEARCH_6 = "I've always had a"
SEARCH_LIST = [STR_SEARCH_0, STR_SEARCH_1, STR_SEARCH_2, STR_SEARCH_3, STR_SEARCH_4, STR_SEARCH_5, STR_SEARCH_6]

# COMMENT_REPLY = ("SAD! [Here's a pup to cheer you up!](http://imgur.com/r/aww/b7ILK3p)"
# "Pups send THEIR best. " + FINGERS_SPLAYED + " " + OK_HAND + " " + OPEN_HANDS + " " + WAVING_HAND)
COMMENT_JOKE = "You requested a joke! Here it is:\n\n"
JOKE = requests.get("http://api.icndb.com/jokes/random").json()['value']['joke']


def authenticate():
    print("Authenticating...")
    reddit = praw.Reddit('trumpify_bot', user_agent="trumpify_bot v0.1")
    print("Authenticated as {}".format(reddit.user.me()))  # forces authentication
    return reddit


def find_match(comment):
    return False  # remove this later

    counter = 0
    for i in range(0, 3):
        if SEARCH_LIST[i] in comment:
            counter += 1

    if (counter >= 2) \
            or (SEARCH_LIST[5] in comment and SEARCH_LIST[6] in comment):
        print("Case 0")
        return True

    word_list = comment.split()
    if len(word_list) < 50:
        return False

    word_dict = {}
    for i in range(0, len(word_list)):
        if word_list[i].casefold() not in word_dict:
            word_dict[word_list[i].casefold()] = 1
        else:
            word_dict[word_list[i].casefold()] += 1

    sorted_words = sorted(word_dict.items(), key=operator.itemgetter(1))
    sorted_words.reverse()

    i = 0
    while (sorted_words[i][1]/(len(word_list) + 0.0)) >= 1.0/11.0 and i < len(word_list):
        if sorted_words[i][0] not in STOP_WORDS:
            print("Case 1")
            return True
        i += 1

    return False


def get_saved_comments():
    if not os.path.isfile("../res/comments_replied_to.txt"):
        comments_replied_to = []
    else:
        with open("../res/comments_replied_to.txt", "r") as file:
            comments_replied_to = file.read()
            comments_replied_to = comments_replied_to.split("\n")
            comments_replied_to = filter(None, comments_replied_to)

    return list(comments_replied_to)


def main():
    ng.read_quotes("../res/trump_quotes.txt")

    # use a dict for O(1) lookup
    comments_replied_to = {}
    saved_comments = get_saved_comments()
    for i in range(0, len(saved_comments)):
        comments_replied_to[saved_comments[i]] = saved_comments[i]

    reddit = authenticate()
    while True:
        run_bot(reddit, comments_replied_to)


def run_bot(reddit, replies_dict):
    print("streaming comments...")
    for comment in reddit.subreddit('all').stream.comments():
        if (find_match(comment.body.casefold())) \
                and (comment.id not in replies_dict) \
                and (comment.author != reddit.user.me()):  # don't reply to self or comments already replied to
            print("String found in comment {}".format(comment.id))
            print("Comment: {}".format(comment.body))
            print("Comment author: {}".format(comment.author))

            reply = trumpify.trumpify(comment.body)
            print("Reply: {}".format(reply))

            comment.reply("> " + reply)
            print("Replied to comment " + comment.id)

            replies_dict[comment.id] = comment.id

            with open("../res/comments_replied_to.txt", "a") as file:
                file.write(comment.id + "\n")

    print("Sleeping for 10 seconds...")
    # Sleep for 10 seconds:
    time.sleep(10)


# run the program:
if "__main__" == __name__:
    main()
