# coding=utf-8
from wxpy import *

bot = Bot()
tuling = Tuling(api_key='a72dc2a74fc14f83b494a6f88cf5b641')


@bot.register(msg_types=TEXT)
def auto_reply_all(msg):
    tuling.do_reply(msg)


bot.join()
