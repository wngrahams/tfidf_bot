import praw
import time

__author__ = 'grahamstubbs'


def authenticate():
    print("Authenticating...")
    reddit = praw.Reddit('trumpify_bot', user_agent="trumpify_bot v0.1")
    print("Authenticated as {}".format(reddit.user.me()))  # forces authentication
    return reddit


def main():
    reddit = authenticate()
    while True:
        run_bot(reddit)


def run_bot(reddit):
    print("obtaining 25 comments")
    for comment in reddit.subreddit('test').comments(limit=25):
        if "send their best" in comment.body:
            print("String with \"send their best\" found in comment " + comment.id)
            comment.reply("SAD! [Here's a pup to cheer you up!](http://imgur.com/r/aww/b7ILK3p)")
            print("Replied to comment " + comment.id)

    print("Sleeping for 10 seconds...")
    # Sleep for 10 seconds:
    time.sleep(10)


# run the program:
if "__main__" == __name__:
    main()
