# -*- coding: utf-8 -*-
"""spider_bot"""
import datetime
import logging

from spider_bot.bot import SpiderBot

__version__ = "0.1.0"
__author__ = "liujuanjuan1984"

# Set default logging handler to avoid "No handler found" warnings.
logging.getLogger(__name__).addHandler(logging.NullHandler())
logging.basicConfig(
    format="%(name)s %(asctime)s %(levelname)s %(message)s",
    filename=f"spiderbot_{datetime.date.today()}.log",
    level=logging.DEBUG,
)
