import os
import praw
import requests
import time
import src.trumpify as trumpify  # when running in pycharm
# import trumpify  # when running in terminal

__author__ = 'grahamstubbs'


STR_SEARCH = "When Mexico sends its people"
# COMMENT_REPLY = ("SAD! [Here's a pup to cheer you up!](http://imgur.com/r/aww/b7ILK3p)"
                 # "Pups send THEIR best. " + FINGERS_SPLAYED + " " + OK_HAND + " " + OPEN_HANDS + " " + WAVING_HAND)
COMMENT_JOKE = "You requested a joke! Here it is:\n\n"
JOKE = requests.get("http://api.icndb.com/jokes/random").json()['value']['joke']


def authenticate():
    print("Authenticating...")
    reddit = praw.Reddit('trumpify_bot', user_agent="trumpify_bot v0.1")
    print("Authenticated as {}".format(reddit.user.me()))  # forces authentication
    return reddit


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
    # use a dict for O(1) lookup
    comments_replied_to = {}
    saved_comments = get_saved_comments()
    for i in range(0, len(saved_comments)):
        comments_replied_to[saved_comments[i]] = saved_comments[i]

    reddit = authenticate()
    while True:
        run_bot(reddit, comments_replied_to)


def run_bot(reddit, replies_dict):
    print("obtaining 25 comments")
    for comment in reddit.subreddit('test').comments(limit=25):
        if (STR_SEARCH.casefold() in comment.body.casefold()) \
                and (comment.id not in replies_dict) \
                and (comment.author != reddit.user.me()):  # don't reply to self or comments already replied to
            print("String with " + STR_SEARCH + " found in comment {}".format(comment.id))

            reply = trumpify.trumpify(comment.body)

            comment.reply(reply)
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
