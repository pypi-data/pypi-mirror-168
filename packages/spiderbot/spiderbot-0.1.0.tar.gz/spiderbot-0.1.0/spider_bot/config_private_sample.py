# -*- coding: utf-8 -*-
"""the private config file for the retweet bot; never git push it to github"""

# please update this file with fake data as example.

import os

DB_NAME = f"sqlite:///{os.path.dirname(os.path.dirname(__file__))}/spider_bot.db"  # pylint: disable=line-too-long


# the xpath for one post page
XPATHS = {
    "date": r'//*[@id="app"]/div[1]/article/div[2]/header/div[1]/div/div[2]/a',
    "text": r'//*[@id="app"]/div[1]/article/div[2]/div[1]/div[1]/div',
    "screenshot": r'//*[@id="app"]/div[1]/article/div[2]',
    "posts": r'//a[starts-with(@href,"https://example.com/")]',
    "name": r'//*[@id="app"]/div[1]/main/div[1]/div',
    "avatar": r'//*[@id="app"]/div[1]/main/div/div[2]/',
    "history": r'//*[@id="__sidebar"]//div//button',
}
