
import rebot
from rebot import Bot
import regular
upd = []
bot = Bot(token="5467797160:AAEtPWOO9trEV8Xpcyk-70MvoOZo5DDkO8U")
while True:
    try:
        message = bot.get_updates(limit=int(3))
        up = (message.upid)
        hand = message.text
        id = message.userid
        msg_i = message.message_id
        chat_id = message.chat_id
        if up in upd:
            pass 
        else:
            upd.append(up)
            print(message)
            if message.data:
                if message.data == "hi":
                    a = bot.msg(chat_id=chat_id,text="you cliick on a button.")
                    print(a)
            if message.text == "/start":
                a = regular.InlineMarkup(row_width=1)
                btn1 = regular.InlineBtn(text="hello",callback_data="hi")
                a.add(btn1)
                bot.msg(chat_id=chat_id,text="t.jpg",reply_markup=a)
            
                
    except:continue 