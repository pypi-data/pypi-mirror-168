# for one post page
# pylint: skip-file

import os

DB_NAME = f"sqlite:///{os.path.dirname(os.path.dirname(__file__))}/spider_bot.db"



XPATHS = {
    "date": r'//*[@id="app"]/div[1]/div[2]/div[2]/main/div[1]/div/div[2]/article/div[2]/header/div[1]/div/div[2]/a',
    "text": r'//*[@id="app"]/div[1]/div[2]/div[2]/main/div[1]/div/div[2]/article/div[2]/div[1]/div[1]/div',
    "screenshot": r'//*[@id="app"]/div[1]/div[2]/div[2]/main/div[1]/div/div[2]/article/div[2]',
    "posts": r'//a[starts-with(@href,"https://weibo.com/")]',
    #//*[@id="scroller"]/div[1]/div[1]/div
    #//*[@id="scroller"]/div[1]/div[2]/div/article/div
    "name":r'//*[@id="app"]/div[1]/div[2]/div[2]/main/div[1]/div/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/div',
    "avatar": r'//*[@id="app"]/div[1]/div[2]/div[2]/main/div/div/div[2]/div[1]/div[1]/div[2]/div[1]',
    "history":r'//*[@id="__sidebar"]/div/div[1]/div[2]/div[1]/div[1]/div/div[3]/div/div[2]/div//div/button',
}

SEED = "rum://seed?v=1&e=0&n=0&b=ip34FBOuSx6ZvUuijIEcCA&c=Fo6bILZE2jUng1oPBXME74O6MuQtXHaJzZU7vhDFFTw&g=t30RM4bhS32XlIM6V_YPCw&k=A5MSiWv3TDjuFPN84YKTWTrS6-sNN1i08q5Ch8taT0ta&s=YxjdD0Fs7YhSMP7kb-w72c0uXvCgmPUiTb3UbZwMoXFfogDueH7udgCfqiuTph4uLLy0NtNll69cVQQblR8hnwA&t=FxWjgSnMnkw&a=mytest_group&y=group_timeline&u=http%3A%2F%2F127.0.0.1%3A57772%3Fjwt%3DeyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhbGxvd0dyb3VwcyI6WyJiNzdkMTEzMy04NmUxLTRiN2QtOTc5NC04MzNhNTdmNjBmMGIiXSwiZXhwIjoxODIxMDk1NDEzLCJuYW1lIjoiYWxsb3ctYjc3ZDExMzMtODZlMS00YjdkLTk3OTQtODMzYTU3ZjYwZjBiIiwicm9sZSI6Im5vZGUifQ.jXG4BhTZ4x0Z_-WXW2PKdUAKEYzcQGKUMPws-gl_AC0" # pylint: disable=line-too-long

COMMON_ACCOUNT_PWD  = "98769774-45d6-455a-b83f-7571bf7f808d"

LANG = "CN"

TIPS = {
    "EN": {
        "name": "bot",
        "origin": "origin url",
    },
    "CN": {
        "name": "微博",
        "origin": "查看原文",
    },
}

# the type of the origin url
# SPLIT: the origin url will be a new trx to reply to the content
# MERGE: the origin url will be added to the content
ORIGIN_URL_TYPE = "MERGE"

