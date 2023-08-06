
import rebot
from rebot import Bot
from rebot import regular
upd = []
bot = Bot(token="")

def on(message):
    #print(message)
    if message.data:
        print(message)
        if message.data == "1":
            bot.answer(message.call_id,"you click 1.",show_alert=True)
        if message.data == "2":
            bot.answer(message.call_id,"you click 2.",show_alert=True)
        if message.data == "3":
            bot.answer(message.call_id,"you click 3.",show_alert=True)
    if message.text == "/start":
        msg_id = message.message_id
        key = regular.InlineMarkup(row_width=1)
        btn1 = regular.InlineBtn(text="- One .",callback_data="1")
        btn2 = regular.InlineBtn(text="- Two .",callback_data="2")
        btn3 = regular.InlineBtn(text="- Three .",callback_data="3")
        key.add(btn1)
        key.add(btn2,btn3)
        bot.msg(chat_id=message.chat_id,text="Something..",reply_markup=key)
    
while True:
    try:
        c = (bot.get_updates())
        up = c.upid
        if up in upd:
            continue
        else:
            upd.append(up)
            on(c)
    except Exception as cc:print(cc);continue