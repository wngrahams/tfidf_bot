__author__ = 'grahamstubbs'

import praw
import src.config as config #use when running in pycharm
#import config              #use when running in terminal

def bot_login():
    praw.Reddit(username = config.username,
                password = config.password,
                client_id = config.client_id,
                client_secret = config.client_secret,
                user_agent = "trumpify_bot v0.1")