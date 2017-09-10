import os
import praw
import time

__author__ = 'grahamstubbs'

STR_SEARCH = "send their best"

FINGERS_SPLAYED = u'\U0001F590'
INDEX_POINTING_UP = u'\u261D'
OK_HAND = u'\U0001F44C'
OPEN_HANDS = u'\U0001F450'
RAISED_FIST = u'\u270A'
RAISED_HAND = u'\u270B'
WAVING_HAND = u'\U0001F44B'


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
                and (comment.author != reddit.user.me()):  # dont reply to self or comments already replied to
            print("String with \"send their best\" found in comment {}".format(comment.id))
            # comment.reply("SAD! [Here's a pup to cheer you up!](http://imgur.com/r/aww/b7ILK3p) Pups send THEIR best.")
            print("Replied to comment " + comment.id)

            replies_dict[comment.id] = comment.id

            with open ("../res/comments_replied_to.txt", "a") as file:
                file.write(comment.id + "\n")

    print("Sleeping for 10 seconds...")
    # Sleep for 10 seconds:
    time.sleep(10)


# run the program:
if "__main__" == __name__:
    main()
