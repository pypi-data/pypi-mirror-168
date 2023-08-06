import requests

class bot:
    def user_channel(token=None,channel=None,id=None):
        r = requests.get("https://api.telegram.org/bot{}/getchatmember?chat_id=@{}&user_id={}".format(token,channel,id))
        if "result" in r.text:
            info = r.json()['result']['user']
            user = info['username']
            status = r.json()['result']['status']
            premium = info['is_premium']
            return {"status":status,"username":user,"id":id,"is_premium":premium}
        else:
            des = r.json()['description']
            return {"badRequest":"True","message":des,}
    def bot(token=None):
        r = requests.get("https://api.telegram.org/bot{}/getme".format(token))
        if "result" in r.text:
            info = r.json()['result']
            id = info['id']
            is_bot = info['is_bot']
            fname = info['first_name']
            username = info['username']
            can_join = info['can_read_all_group_messages']
            return {"id":id,"first":fname,"username":username,"can_join":can_join}
        else:
            des = r.json()['description']
            return {"badRequest":"True","message":des}
    def count(token=None,username=None):
        r = requests.get("https://api.telegram.org/bot{}/getChatMembersCount?chat_id=@{}".format(token,username))
        if "result" in r.text:
            count = r.json()['result']
            return {"count":count,"chat":username,}
        else:
            des = r.json()['description']
            return {"badRequest":"True","message":des}
    def admins(token=None,username=None):
        r = requests.get("https://api.telegram.org/bot{}/getChatAdministrators?chat_id=@{}".format(token,username))
        if "result" in r.text:
            info = r.json()['result']
            c = 0
            for i in info:
                c+=1
            return {"count":c,"admins":info,}
        else:
            des = r.json()['description']
            return {"badRequest":"True","message":des}
    def commands(token=None):
        r = requests.get("https://api.telegram.org/bot{}/getMyCommands".format(token))
        if "result" in r.text:
            info = r.json()['result']
            c = 0
            for i in info:
                c+=1
            return {"count":c,"commands":info}
        else:
            des = r.json()['description']
            return {"badRequest":"True","message":des}
    def exportLink(token=None,username=None):
        r = requests.get("https://api.telegram.org/bot{}/exportChatInviteLink?chat_id=@{}".format(token,username))
        if "result" in r.text:
            info = r.json()['result']
            return {"Link":info,"username":username}
        else:
            des = r.json()['description']
            return {"badRequest":"True","message":des}
    def leaveChat(token=None,username=None):
        r = requests.get("https://api.telegram.org/bot{}/leaveChat?chat_id=@{}".format(token,username))
        if "result" in r.text:
            info = r.json()['result']
            return {"Status":info,"username":username}
        else:
            des = r.json()['description']
            return {"badRequest":"True","message":"des"}
    