# -*- coding: utf-8 -*-
# -- By TRAKOS -- #
import json, logging, os, time, requests, json , time
from rebot import regular
from datetime import datetime
from collections import namedtuple
print(f"Logger Started - Rebot - api.telegram.org")
logger = logging.getLogger(__name__)
import json
from requests import get,post
import requests
import itertools
from threading import Thread
BASE_URL = "https://api.telegram.org/bot" 
class dotdict(dict):
    __getattr__= dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

class Bot:
    
    def __init__(self, token):
        self.token = token
        self.url = BASE_URL
        self.marker = None
        
    def to_json(self):
        return json.dumps(self.to_dict())
    def get_updates(self, limit=None, timeout=10):
        
        update = {}
        non = []
        if not self.token:
            print("add token, if dont have search in your ass xD")
            time.sleep(2)
            exit()
        else:
            try:
                response = requests.get(f"https://api.telegram.org/bot{self.token}/getUpdates", timeout=90)
                update = response.json()
            except requests.exceptions.ReadTimeout:
                logger.info('get_updates ReadTimeout')
            except requests.exceptions.ConnectionError:
                logger.error('get_updates ConnectionError')
                time.sleep(1)

            except requests.exceptions.RequestException as e:
                logger.error('get_updates Request Error: {}'.format(e))
            except Exception as e:
                logger.error(('get_updates General Error: {}'.format(e)))
            if 'result' in update.keys():
                if len(update['result']) != 0:
                    p = 0
                else:
                    update = None
            else:
                update = None
            if update:
                a = 0
            a = update['result'][-1]
            
            import re
            
            if "reply_to_message" in str(a):
                aae = {"upid":a['update_id'],"userid":a['message']['from']['id'],"message_id":a['message']['message_id'],"text":a['message']['text'],"fname":a['message']['from']['first_name'],"chat_id":a['message']['chat']['id'],"chat_type":a['message']['chat']['type'],"reply_message_id":a['message']['reply_to_message']['message_id'],"reply_to_userid":a['message']['reply_to_message']['from']['id'],"reply_to_isbot":a['message']['reply_to_message']['from']['is_bot'],"reply_to_fname":a['message']['reply_to_message']['from']['first_name'],"reply_to_text":a['message']['reply_to_message']['text']}
                dict = dotdict(aae)
                return dict
            if "callback_query" in str(a) or "reply_markup" in str(a):
                ae = {"upid":a['update_id'],"call_id":a['callback_query']['id'],"data":a['callback_query']['data'],"chat_id":a['callback_query']['message']['chat']['id'],"userid":a['callback_query']['from']['id'],"text":a['callback_query']['message']['text'],"message_id":a['callback_query']['message']['message_id']}
                dict = dotdict(ae)
                return dict
            if "set_name" in str(a):
                set = (re.findall("'set_name': '(.*?)'",str(a))[0])
                emo = (re.findall("'emoji': '(.*?)'",str(a))[0])
                aa = {"upid":a['update_id'],"message_id":a['message']['message_id'],"userid":a['message']['from']['id'],"fname":a['message']['from']['first_name'],"chat_id":a['message']['chat']['id'],"chat_type":a['message']['chat']['type'],"sticker":emo,"text":set}
                dict = dotdict(aa)
                return dict
            if "dice" in str(a):
                aa = {"upid":a['update_id'],"message_id":a['message']['message_id'],"userid":a['message']['from']['id'],"fname":a['message']['from']['first_name'],"chat_id":a['message']['chat']['id'],"chat_type":a['message']['chat']['type'],"text":a['message']['dice']['emoji']}
                dict = dotdict(aa)
                return dict
            if "text" in str(a):
                
                aa = {"upid":a['update_id'],"message_id":a['message']['message_id'],"userid":a['message']['from']['id'],"fname":a['message']['from']['first_name'],"chat_id":a['message']['chat']['id'],"chat_type":a['message']['chat']['type'],"text":a['message']['text']}
                dict = dotdict(aa)
                return dict
    
    def file(self,chat_id=None,file=None,reply_to_message_id=None, reply_markup=None,
        parse_mode=None):
        files = {'document': open(file, 'rb')}
        r = requests.post("https://api.telegram.org/bot{}/".format(self.token) + "sendDocument?chat_id={}".format(chat_id), files=files)
        if "result" in r.text:
            info = r.json()['result']
            message_id = info['message_id']
            from_info = info['from']
            id = from_info['id']
            first_name = from_info['first_name']
            username = from_info['username']
            chat_info = info['chat']
            cid = chat_info['id']
            title = chat_info['title']
            chat_type = chat_info['type']
            docinfo = info['document']
            filename = docinfo['file_name']
            file_id = docinfo['file_id']
            a =  {"status":True,"document":{"file":filename,"file_id":file_id,"chat":{"chat_type":chat_type,"id":cid,"title":title,"user":{"id":id,"username":username,"first_name":first_name,"message_id":message_id}}}}
            dict = dotdict(a)
            return dict
        else:
            des = r.json()['description']
            a = {"badRequest":"True","message":des}
            dict = dotdict(a)
            return dict
    def msg(self,chat_id=None, text=None,
        disable_web_page_preview=None, reply_to_message_id=None, reply_markup=None,
        parse_mode=None, disable_notification=None, timeout=None,
        entities=None, allow_sending_without_reply=None, protect_content=None):
        if reply_markup == None:
            params = {
                "disable_web_page_preview":disable_web_page_preview,
                "reply_to_message_id":reply_to_message_id,
                "reply_markup":(reply_markup),
                "parse_mode":parse_mode,
                "disable_notification":disable_notification,
                "timeout":timeout,
                "entities":entities,
                "allow_sending_without_reply":allow_sending_without_reply,
                "protect_content":protect_content
            }
        
            r = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}".format(self.token,chat_id,text),params=params)
            if "result" in r.text:
                info = r.json()['result']
                textt = info['text']
                date = info['date']
                message_id = info['message_id']
                message_from= info['from']
                id = message_from['id']
                is_bot = message_from['is_bot']
                first_name = message_from['first_name']
                username = message_from['username']
                a = {"status":"True","message_id":message_id,"id":id,"first_name":first_name,"isRobot":is_bot,"username":username,"text":textt}
                dict = dotdict(a)
                return dict
            else:
                des = r.json()['description']
                a = {"badRequest":True,"message":des}
                dict = dotdict(a)
                return dict
        else:
                params = {
                "disable_web_page_preview":disable_web_page_preview,
                "reply_to_message_id":reply_to_message_id,
                "reply_markup":Bot.to_json(reply_markup),
                "parse_mode":parse_mode,
                "disable_notification":disable_notification,
                "timeout":timeout,
                "entities":entities,
                "allow_sending_without_reply":allow_sending_without_reply,
                "protect_content":protect_content
            }
        
                r = requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}".format(self.token,chat_id,text),params=params)
                if "result" in r.text:
                    info = r.json()['result']
                    textt = info['text']
                    date = info['date']
                    message_id = info['message_id']
                    message_from= info['from']
                    id = message_from['id']
                    is_bot = message_from['is_bot']
                    first_name = message_from['first_name']
                    username = message_from['username']
                    a = {"status":"True","message_id":message_id,"id":id,"first_name":first_name,"isRobot":is_bot,"username":username,"text":textt}
                    dict = dotdict(a)
                    return dict
                else:
                    des = r.json()['description']
                    a = {"badRequest":True,"message":des}
                    dict = dotdict(a)
                    return dict
    def user_channel(self,chat_id=None,id=None):
        r = requests.get("https://api.telegram.org/bot{}/getchatmember?chat_id={}&user_id={}".format(self.token,chat_id,id))
        if "result" in r.text:
            info = r.json()['result']['user']
            user = info['username']
            status = r.json()['result']['status']
            premium = info['is_premium']
            a =  {"status":status,"username":user,"id":id,"is_premium":premium}
            dict = dotdict(a)
            return dict
        else:
            des = r.json()['description']
            a =  {"badRequest":"True","message":des,}
            dict = dotdict(a)
            return dict
    def bot(self):
        r = requests.get("https://api.telegram.org/bot{}/getme".format(self.token))
        if "result" in r.text:
            info = r.json()['result']
            id = info['id']
            is_bot = info['is_bot']
            fname = info['first_name']
            username = info['username']
            can_join = info['can_read_all_group_messages']
            a =  {"id":id,"is_bot":is_bot,"first_name":fname,"username":username,"can_join":can_join}
            dict = dotdict(a)
            return dict
        else:
            des = r.json()['description']
            return {"badRequest":"True","message":des}
    def count(self,chat_id):
        r = requests.get("https://api.telegram.org/bot{}/getChatMembersCount?chat_id={}".format(self.token,chat_id))
        if "result" in r.text:
            count = r.json()['result']
            a = {"count":count,"chat":chat_id,}
            dict = dotdict(a)
            return dict
        else:

            des = r.json()['description']
            a=  {"badRequest":"True","message":des}
            dict = dotdict(a)
            return dict
    def admins(self,chat_id):
        r = requests.get("https://api.telegram.org/bot{}/getChatAdministrators?chat_id={}".format(self.token,chat_id))
        if "result" in r.text:
            info = r.json()['result']
            c = 0
            for i in info:
                c+=1
            a =  {"count":c,"admins":info,}
            dict = dotdict(a)
            return dict
        else:
            des = r.json()['description']
            a =  {"badRequest":"True","message":des}
            dict = dotdict(a)
            return dict
    def commands(self):
        r = requests.get("https://api.telegram.org/bot{}/getMyCommands".format(self.token))
        if "result" in r.text:
            info = r.json()['result']
            c = 0
            for i in info:
                c+=1
            a = {"count":c,"commands":info}
            dict = dotdict(a)
            return dict
        else:
            des = r.json()['description']
            a = {"badRequest":"True","message":des}
            dict = dotdict(a)
            return dict
    def exportLink(self,chat_id):
        r = requests.get("https://api.telegram.org/bot{}/exportChatInviteLink?chat_id={}".format(self.token,chat_id))
        if "result" in r.text:
            info = r.json()['result']
            a = {"Link":info,"username":chat_id}
            dict = dotdict(a)
            return dict
        else:
            des = r.json()['description']
            a = {"badRequest":"True","message":des}
            dict = dotdict(a)
            return dict
    def leaveChat(self,chat_id):
        r = requests.get("https://api.telegram.org/bot{}/leaveChat?chat_id={}".format(self.token,chat_id))
        if "result" in r.text:
            info = r.json()['result']
            a = {"Status":info,"username":chat_id}
            dict = dotdict(a)
            return dict
        else:
            des = r.json()['description']
            a = {"badRequest":"True","message":"des"}
            dict = dotdict(a)
            return dict
    def fowrard(self,chat_id,from_chat_id,disable_notification=None,protect_content=None,message_id=None):
        params = {
            "disable_notification":disable_notification,
            "protect_content":protect_content
        }
        r = requests.get("https://api.telegram.org/bot{}/forwardMessage?chat_id={}&from_chat_id={}&message_id={}".format(self.token,chat_id,from_chat_id,message_id),params=params)
        if "result" in r.text:
            info = r.json()['result']
            dict = dotdict(info)
            return dict
        else:
            des = r.json()['description']
            aa = {"badRequest":True,"message":des}
            dict = dotdict(aa)
            return dict
    def action(self,chat_id,action):
        """
        Type of action to broadcast. Choose one, depending on what the user is about to receive: typing for text messages, upload_photo for photos, record_video or upload_video for videos, record_voice or upload_voice for voice notes, upload_document for general files, choose_sticker for stickers, find_location for location data, record_video_note or upload_video_note for video notes.
        """
        r = requests.get("https://api.telegram.org/bot{}/sendChatAction?chat_id={}&action={}".format(self.token,chat_id,action))
        if "result" in r.text:
            info = r.json()['result']
            aa =  {"status":info}
            dict = dotdict(aa)
            return dict
        else:
            des = r.json()['description']
            aa = {"badRequest":True,"message":des}
            dict = dotdict(aa)
            return dict
    def photos(self, user_id, offset=None, limit=None):
        
        dataset = {'user_id': user_id}
        if offset:
            dataset['offset'] = offset
        if limit:
            dataset['limit'] = limit
        r = requests.get("https://api.telegram.org/bot{}/getUserProfilePhotos".format(self.token), params=dataset)
        if "result" in r.text:
            info = r.json()['result']
            dict = dotdict(info)
            return dict
        else:
            des = r.json()['description']
            aa = {"badRequest":True,"message":des}
            dict = dotdict(aa)
            return dict
    
    def photo(self,chat_id,photo,caption=None,parse_mode=None,disable_notification=None,protect_content=None,reply_to_message_id=None,allow_sending_without_reply=None,reply_markup=None):
        if reply_markup:
            if "https" not in str(photo) or "http" not in str(photo):
                
                files = {'photo': open(photo, 'rb')}
                params = {
                    "caption":caption,
                    "parse_mode":parse_mode,
                    "disable_notification":disable_notification,
                    "protect_content":protect_content,
                    "reply_to_message_id":reply_to_message_id,
                    "allow_sending_without_reply":allow_sending_without_reply,
                    "reply_markup":Bot.to_json(reply_markup),

                }
                r = requests.post("https://api.telegram.org/bot{}/sendPhoto?chat_id={}".format(self.token,chat_id),params=params, files=files)
                if "result" in r.text:
                    info = r.json()['result']
                    dict = dotdict(info)
                    return dict
                else:
                    des = r.json()['description']
                    aa = {"badRequest":True,"message":des}
                    dict = dotdict(aa)
                    return dict
            else:
                params = {
                    "photo":photo,
                    "caption":caption,
                    "parse_mode":parse_mode,
                    "disable_notification":disable_notification,
                    "protect_content":protect_content,
                    "reply_to_message_id":reply_to_message_id,
                    "allow_sending_without_reply":allow_sending_without_reply,
                    "reply_markup":Bot.to_json(reply_markup),

                }
                r = requests.post("https://api.telegram.org/bot{}/sendPhoto?chat_id={}".format(self.token,chat_id),params=params)
                if "result" in r.text:
                    info = r.json()['result']
                    dict = dotdict(info)
                    return dict
                else:
                    des = r.json()['description']
                    aa = {"badRequest":True,"message":des}
                    dict = dotdict(aa)
                    return dict
        else:
            if "https" not in str(photo) or "http" not in str(photo):
                
                files = {'photo': open(photo, 'rb')}
                params = {
                    "caption":caption,
                    "parse_mode":parse_mode,
                    "disable_notification":disable_notification,
                    "protect_content":protect_content,
                    "reply_to_message_id":reply_to_message_id,
                    "allow_sending_without_reply":allow_sending_without_reply,
                    "reply_markup":(reply_markup),

                }
                r = requests.post("https://api.telegram.org/bot{}/sendPhoto?chat_id={}".format(self.token,chat_id),params=params, files=files)
                if "result" in r.text:
                    info = r.json()['result']
                    dict = dotdict(info)
                    return dict
                else:
                    des = r.json()['description']
                    aa = {"badRequest":True,"message":des}
                    dict = dotdict(aa)
                    return dict
            else:
                params = {
                    "photo":photo,
                    "caption":caption,
                    "parse_mode":parse_mode,
                    "disable_notification":disable_notification,
                    "protect_content":protect_content,
                    "reply_to_message_id":reply_to_message_id,
                    "allow_sending_without_reply":allow_sending_without_reply,
                    "reply_markup":reply_markup,

                }
                r = requests.post("https://api.telegram.org/bot{}/sendPhoto?chat_id={}".format(self.token,chat_id),params=params)
                if "result" in r.text:
                    info = r.json()['result']
                    dict = dotdict(info)
                    return dict
                else:
                    des = r.json()['description']
                    aa = {"badRequest":True,"message":des}
                    dict = dotdict(aa)
                    return dict
    def video(self,chat_id,video,caption=None,parse_mode=None,disable_notification=None,protect_content=None,reply_to_message_id=None,allow_sending_without_reply=None,reply_markup=None):
        if reply_markup:
            if "https" not in str(video) or "http" not in str(video):
                
                files = {'video': open(video, 'rb')}
                params = {
                    "caption":caption,
                    "parse_mode":parse_mode,
                    "disable_notification":disable_notification,
                    "protect_content":protect_content,
                    "reply_to_message_id":reply_to_message_id,
                    "allow_sending_without_reply":allow_sending_without_reply,
                    "reply_markup":Bot.to_json(reply_markup),

                }
                r = requests.post("https://api.telegram.org/bot{}/sendVideo?chat_id={}".format(self.token,chat_id),params=params, files=files)
                if "result" in r.text:
                    info = r.json()['result']
                    dict = dotdict(info)
                    return dict
                else:
                    des = r.json()['description']
                    aa = {"badRequest":True,"message":des}
                    dict = dotdict(aa)
                    return dict
            else:
                params = {
                    "video":video,
                    "caption":caption,
                    "parse_mode":parse_mode,
                    "disable_notification":disable_notification,
                    "protect_content":protect_content,
                    "reply_to_message_id":reply_to_message_id,
                    "allow_sending_without_reply":allow_sending_without_reply,
                    "reply_markup":Bot.to_json(reply_markup),

                }
                r = requests.post("https://api.telegram.org/bot{}/sendVideo?chat_id={}".format(self.token,chat_id),params=params)
                if "result" in r.text:
                    info = r.json()['result']
                    dict = dotdict(info)
                    return dict
                else:
                    des = r.json()['description']
                    aa = {"badRequest":True,"message":des}
                    dict = dotdict(aa)
                    return dict
        else:
            if "https" not in str(video) or "http" not in str(video):
                
                files = {'video': open(video, 'rb')}
                params = {
                    "caption":caption,
                    "parse_mode":parse_mode,
                    "disable_notification":disable_notification,
                    "protect_content":protect_content,
                    "reply_to_message_id":reply_to_message_id,
                    "allow_sending_without_reply":allow_sending_without_reply,
                    "reply_markup":(reply_markup),

                }
                r = requests.post("https://api.telegram.org/bot{}/sendVideo?chat_id={}".format(self.token,chat_id),params=params, files=files)
                if "result" in r.text:
                    info = r.json()['result']
                    dict = dotdict(info)
                    return dict
                else:
                    des = r.json()['description']
                    aa = {"badRequest":True,"message":des}
                    dict = dotdict(aa)
                    return dict
            else:
                params = {
                    "video":video,
                    "caption":caption,
                    "parse_mode":parse_mode,
                    "disable_notification":disable_notification,
                    "protect_content":protect_content,
                    "reply_to_message_id":reply_to_message_id,
                    "allow_sending_without_reply":allow_sending_without_reply,
                    "reply_markup":reply_markup,

                }
                r = requests.post("https://api.telegram.org/bot{}/sendVideo?chat_id={}".format(self.token,chat_id),params=params)
                if "result" in r.text:
                    info = r.json()['result']
                    dict = dotdict(info)
                    return dict
                else:
                    des = r.json()['description']
                    aa = {"badRequest":True,"message":des}
                    dict = dotdict(aa)
                    return dict
    def ban(self,chat_id,user_id,until_date,revoke_messages=None):
        params = {
            "until_date":until_date,
            "revoke_messages":revoke_messages
        }
        r = requests.get("https://api.telegram.org/bot{}/banChatMember?chat_id={}&user_id={}".format(self.token,chat_id,user_id),params=params)
        if "result" in r.text:
            info = r.json()['result']
            dict = dotdict(info)
            return dict
        else:
            des = r.json()['description']
            aa = {"badRequest":True,"message":des}
            dict = dotdict(aa)
            return dict
    def unban(self,chat_id,user_id,only_if_banned=None):
        params = {
            "only_if_banned":only_if_banned
        }
        r = requests.get("https://api.telegram.org/bot{}/unbanChatMember?chat_id={}&user_id={}".format(self.token,chat_id,user_id),params=params)
        if "result" in r.text:
            info = r.json()['result']
            dict = dotdict(info)
            return dict
        else:
            des = r.json()['description']
            aa = {"badRequest":True,"message":des}
            dict = dotdict(aa)
            return dict
    def audio(self,chat_id,thumb=None,title=None,performer=None,duration=None,audio_file=None,caption=None,parse_mode=None,disable_notification=None,protect_content=None,reply_to_message_id=None,allow_sending_without_reply=None,reply_markup=None):
        if reply_markup == None:
            if "https" not in str(audio_file) or "http" not in str(audio_file):
                files = {'audio': open(audio_file, 'rb')}
                params = {
                    "caption":caption,
                    "parse_mode":parse_mode,
                    "duration":duration,
                    "performer":performer,
                    "title":title,
                    "thumb":thumb,
                    "reply_markup":reply_markup,

                }
                r = requests.post("https://api.telegram.org/bot{}/sendAudio?chat_id={}".format(self.token,chat_id),params=params, files=files)
                if "result" in r.text:
                    info = r.json()['result']
                    dict = dotdict(info)
                    return dict
                else:
                    des = r.json()['description']
                    aa = {"badRequest":True,"message":des}
                    dict = dotdict(aa)
                    return dict
            else:
                params = {
                    "audio":audio_file,
                    "caption":caption,
                    "parse_mode":parse_mode,
                    "duration":duration,
                    "performer":performer,
                    "title":title,
                    "thumb":thumb,
                    "reply_markup":reply_markup,

                }
                r = requests.post("https://api.telegram.org/bot{}/sendAudio?chat_id={}".format(self.token,chat_id),params=params)
                if "result" in r.text:
                    info = r.json()['result']
                    dict = dotdict(info)
                    return dict
                else:
                    des = r.json()['description']
                    aa = {"badRequest":True,"message":des}
                    dict = dotdict(aa)
                    return dict
        else:
            if "https" not in str(audio_file) or "http" not in str(audio_file):
                files = {'audio': open(audio_file, 'rb')}
                params = {
                    "caption":caption,
                    "parse_mode":parse_mode,
                    "duration":duration,
                    "performer":performer,
                    "title":title,
                    "thumb":thumb,
                    "reply_markup":Bot.to_json(reply_markup),

                }
                r = requests.post("https://api.telegram.org/bot{}/sendAudio?chat_id={}".format(self.token,chat_id),params=params, files=files)
                if "result" in r.text:
                    info = r.json()['result']
                    dict = dotdict(info)
                    return dict
                else:
                    des = r.json()['description']
                    aa = {"badRequest":True,"message":des}
                    dict = dotdict(aa)
                    return dict
            else:
                params = {
                    "audio":audio_file,
                    "caption":caption,
                    "parse_mode":parse_mode,
                    "duration":duration,
                    "performer":performer,
                    "title":title,
                    "thumb":thumb,
                    "reply_markup":reply_markup,

                }
                r = requests.post("https://api.telegram.org/bot{}/sendAudio?chat_id={}".format(self.token,chat_id),params=params)
                if "result" in r.text:
                    info = r.json()['result']
                    dict = dotdict(info)
                    return dict
                else:
                    des = r.json()['description']
                    aa = {"badRequest":True,"message":des}
                    dict = dotdict(aa)
                    return dict
    def contact(self,chat_id,phone_number=None,first_name=None,last_name=None,reply_markup=None,allow_sending_without_reply=None,reply_to_message_id=None,protect_content=None):
        if reply_markup == None:
            params = {
                "phone_number":phone_number,
                "first_name":first_name,
                "last_name":last_name,
                "reply_markup":reply_markup,
                "allow_sending_without_reply":allow_sending_without_reply,
                "reply_to_message_id":reply_to_message_id,
                "protect_content":protect_content,
            }
            r = requests.get("https://api.telegram.org/bot{}/sendContact?chat_id={}".format(self.token,chat_id),params=params)
            if "result" in r.text:
                info = r.json()['result']
                dict = dotdict(info)
                return dict
            else:
                des = r.json()['description']
                aa = {"badRequest":True,"message":des}
                dict = dotdict(aa)
                return dict
        else:
                params = {
                "phone_number":phone_number,
                "first_name":first_name,
                "last_name":last_name,
                "reply_markup":Bot.to_json(reply_markup),
                "allow_sending_without_reply":allow_sending_without_reply,
                "reply_to_message_id":reply_to_message_id,
                "protect_content":protect_content,
            }
                r = requests.get("https://api.telegram.org/bot{}/sendContact?chat_id={}".format(self.token,chat_id),params=params)
                if "result" in r.text:
                    info = r.json()['result']
                    dict = dotdict(info)
                    return dict
                else:
                    des = r.json()['description']
                    aa = {"badRequest":True,"message":des}
                    dict = dotdict(aa)
                    return dict
    def dice(self,chat_id,emoji=None,reply_markup=None,allow_sending_without_reply=None,reply_to_message_id=None,protect_content=None):
        params = {
            "emoji":emoji,
            "reply_markup":reply_markup,
            "allow_sending_without_reply":allow_sending_without_reply,
            "reply_to_message_id":reply_to_message_id,
            "protect_content":protect_content,
        }
        r = requests.get("https://api.telegram.org/bot{}/sendDice?chat_id={}".format(self.token,chat_id),params=params)
        if "result" in r.text:
            info = r.json()['result']
            dict = dotdict(info)
            return dict
        else:
            des = r.json()['description']
            aa = {"badRequest":True,"message":des}
            dict = dotdict(aa)
            return dict
    def animation(self,chat_id,animation,duration=None,width=None,height=None,thumb=None):
        if "http" not in str(animation) or "https" not in str(animation):

            files = {'animation': open(animation, 'rb')}
            params = {
                "duration":duration,
                "width":width,
                "height":height,
                "thumb":thumb,
            }
            r = requests.post("https://api.telegram.org/bot{}/sendAnimation?chat_id={}".format(self.token,chat_id),params=params, files=files)
            if "result" in r.text:
                info = r.json()['result']
                dict = dotdict(info)
                return dict
            else:
                des = r.json()['description']
                aa = {"badRequest":True,"message":des}
                dict = dotdict(aa)
                return dict
        else:
            params = {
                "animation":animation,
                "duration":duration,
                "width":width,
                "height":height,
                "thumb":thumb,
            }
            r = requests.post("https://api.telegram.org/bot{}/sendAnimation?chat_id={}".format(self.token,chat_id),params=params)
            if "result" in r.text:
                info = r.json()['result']
                dict = dotdict(info)
                return dict
            else:
                des = r.json()['description']
                aa = {"badRequest":True,"message":des}
                dict = dotdict(aa)
                return dict
    def mute(self,chat_id,user_id,until_date,permissions=None):
        params = {
            "until_date":until_date,
            "permissions":{"can_send_messages":False},
        }
        r = requests.get("https://api.telegram.org/bot{}/restrictChatMember?chat_id={}&user_id={}".format(self.token,chat_id,user_id),params=params)
        if "result" in r.text:
            info = r.json()['result']
            dict = dotdict(info)
            return dict
        else:
            des = r.json()['description']
            aa = {"badRequest":True,"message":des}
            dict = dotdict(aa)
            return dict
    def approve(self,chat_id,user_id):
        r = requests.get("https://api.telegram.org/bot{}/approveChatJoinRequest?chat_id={}&user_id={}".format(self.token,chat_id,user_id))
        if "result" in r.text:
            info = r.json()['result']
            dict = dotdict(info)
            return dict
        else:
            des = r.json()['description']
            aa = {"badRequest":True,"message":des}
            dict = dotdict(aa)
            return dict
    def decliend(self,chat_id,user_id):
        r = requests.get("https://api.telegram.org/bot{}/declineChatJoinRequest?chat_id={}&user_id={}".format(self.token,chat_id,user_id))
        if "result" in r.text:
            info = r.json()['result']
            dict = dotdict(info)
            return dict
        else:
            des = r.json()['description']
            aa = {"badRequest":True,"message":des}
            dict = dotdict(aa)
            return dict
    def deleteChatPhoto(self,chat_id):
        r = requests.get("https://api.telegram.org/bot{}/deleteChatPhoto?chat_id={}".format(self.token,chat_id))
        if "result" in r.text:
            info = r.json()['result']
            dict = dotdict(info)
            return dict
        else:
            des = r.json()['description']
            aa = {"badRequest":True,"message":des}
            dict = dotdict(aa)
            return dict
    def setChatTitle(self,chat_id,title=None):
        r = requests.get("https://api.telegram.org/bot{}/setChatTitle?chat_id={}&title={}".format(self.token,chat_id,title))
        if "result" in r.text:
            info = r.json()['result']
            dict = dotdict(info)
            return dict
        else:
            des = r.json()['description']
            aa = {"badRequest":True,"message":des}
            dict = dotdict(aa)
            return dict
    def setChatDescription(self,chat_id,description=None):
        r = requests.get("https://api.telegram.org/bot{}/setChatDescription?chat_id={}&title={}".format(self.token,chat_id,description))
        if "result" in r.text:
            info = r.json()['result']
            dict = dotdict(info)
            return dict
        else:
            des = r.json()['description']
            aa = {"badRequest":True,"message":des}
            dict = dotdict(aa)
            return dict
    def pinChatMessage(self,chat_id,message_id=None):
        r = requests.get("https://api.telegram.org/bot{}/pinChatMessage?chat_id={}&message_id={}".format(self.token,chat_id,message_id))
        if "result" in r.text:
            info = r.json()['result']
            dict = dotdict(info)
            return dict
        else:
            des = r.json()['description']
            aa = {"badRequest":True,"message":des}
            dict = dotdict(aa)
            return dict
    def unpinChatMessage(self,chat_id,message_id=None):
        r = requests.get("https://api.telegram.org/bot{}/unpinChatMessage?chat_id={}&message_id={}".format(self.token,chat_id,message_id))
        if "result" in r.text:
            info = r.json()['result']
            dict = dotdict(info)
            return dict
        else:
            des = r.json()['description']
            aa = {"badRequest":True,"message":des}
            dict = dotdict(aa)
            return dict
    def unpinAllChatMessages(self,chat_id):
        r = requests.get("https://api.telegram.org/bot{}/unpinAllChatMessages?chat_id={}".format(self.token,chat_id))
        if "result" in r.text:
            info = r.json()['result']
            dict = dotdict(info)
            return dict
        else:
            des = r.json()['description']
            aa = {"badRequest":True,"message":des}
            dict = dotdict(aa)
            return dict
    def convert_input_media_array(array):
        media = []
        files = {}
        
        for input_media in array:
            if isinstance(input_media, regular.InputMedia):
                media_dict = input_media.to_dict()
                if media_dict['media'].startswith('attach://'):
                    key = media_dict['media'].replace('attach://', '')
                    files[key] = input_media.media
                media.append(media_dict)
        return json.dumps(media), files
    def media_group(
        self, chat_id, media,
        disable_notification=None, reply_to_message_id=None,
        timeout=None, allow_sending_without_reply=None, protect_content=None):
        method_url = r'sendMediaGroup'
        media_json, files = Bot.convert_input_media_array(media)
        dataset = {'chat_id': chat_id, 'media': media_json}
        if disable_notification is not None:
            dataset['disable_notification'] = disable_notification
        if reply_to_message_id:
            dataset['reply_to_message_id'] = reply_to_message_id
        if timeout:
            dataset['timeout'] = timeout
        if allow_sending_without_reply is not None:
            dataset['allow_sending_without_reply'] = allow_sending_without_reply
        if protect_content is not None:
            dataset['protect_content'] = protect_content
        r = requests.post("https://api.telegram.org/bot{}/sendMediaGroup".format(self.token),params=dataset,files=files if files else None)
        if "result" in r.text:
            info = r.json()['result']
            
            return info
        else:
            des = r.json()['description']
            aa = {"badRequest":True,"message":des}
            dict = dotdict(aa)
            return dict
    def promote(
        self, chat_id, user_id, can_change_info=None, can_post_messages=None,
        can_edit_messages=None, can_delete_messages=None, can_invite_users=None,
        can_restrict_members=None, can_pin_messages=None, can_promote_members=None,
        is_anonymous=None, can_manage_chat=None, can_manage_video_chats=None):
        dataset = {'chat_id': chat_id, 'user_id': user_id}
        if can_change_info is not None:
            dataset['can_change_info'] = can_change_info
        if can_post_messages is not None:
            dataset['can_post_messages'] = can_post_messages
        if can_edit_messages is not None:
            dataset['can_edit_messages'] = can_edit_messages
        if can_delete_messages is not None:
            dataset['can_delete_messages'] = can_delete_messages
        if can_invite_users is not None:
            dataset['can_invite_users'] = can_invite_users
        if can_restrict_members is not None:
            dataset['can_restrict_members'] = can_restrict_members
        if can_pin_messages is not None:
            dataset['can_pin_messages'] = can_pin_messages
        if can_promote_members is not None:
            dataset['can_promote_members'] = can_promote_members
        if is_anonymous is not None:
            dataset['is_anonymous'] = is_anonymous
        if can_manage_chat is not None:
            dataset['can_manage_chat'] = can_manage_chat
        if can_manage_video_chats is not None:
            dataset['can_manage_video_chats'] = can_manage_video_chats
        r =  requests.post("https://api.telegram.org/bot{}/promoteChatMember".format(self.token), params=dataset)
    def get_member(self, chat_id, user_id):
        r = requests.get("https://api.telegram.org/bot{}/getChatMember?chat_id={}&user_id={}".format(self.token,chat_id,user_id))
        if "result" in r.text:
            info = r.json()['result']
            aa = {'userid':info['user']['id'],"fname":info['user']['first_name'],"username":info['user']['username']}
            dict = dotdict(aa)
            return dict
        else:
            des = r.json()['description']
            aa = {"badRequest":True,"message":des}
            dict = dotdict(aa)
            return dict
    def delete(self,chat_id,message_id):
        r = requests.get("https://api.telegram.org/bot{}/deleteMessage?chat_id={}&message_id={}".format(self.token,chat_id,message_id))
        if "result" in r.text:
            info = r.json()['result']
            dict = dotdict(info)
            return dict
        else:
            des = r.json()['description']
            aa = {"badRequest":True,"message":des}
            dict = dotdict(aa)
            return dict
    def edit_text(self,chat_id,message_id,text=None,parse_mode=None,reply_markup=None,disable_web_page_preview=None):
        if reply_markup == None:
            params = {
                "reply_markup":reply_markup,
                "disable_web_page_preview":disable_web_page_preview,
                "parse_mode":parse_mode,
            }
            r = requests.get("https://api.telegram.org/bot{}/editMessageText?chat_id={}&text={}&message_id={}".format(self.token,chat_id,text,message_id),params=params)
            if "result" in r.text:
                info = r.json()['result']
                msg_id = info['result']['message_id']
                username = info['result']['user']['name']
                userid = info['result']['user']['id']
                ax = {"msg_id":msg_id,"userName":username,"userId":userid}
                dict = dotdict(ax)
                return dict
            else:
                des = r.json()['description']
                aa = {"badRequest":True,"message":des}
                dict = dotdict(aa)
                return dict
        else:
            params = {
                "reply_markup":Bot.to_json(reply_markup),
                "disable_web_page_preview":disable_web_page_preview,
                "parse_mode":parse_mode,
            }
            r = requests.get("https://api.telegram.org/bot{}/editMessageText?chat_id={}&text={}&message_id={}".format(self.token,chat_id,text,message_id),params=params)
            if "result" in r.text:
                info = r.json()['result']
                msg_id = info['result']['message_id']
                username = info['result']['user']['name']
                userid = info['result']['user']['id']
                ax = {"msg_id":msg_id,"userName":username,"userId":userid}
                dict = dotdict(ax)
                return dict
            else:
                des = r.json()['description']
                aa = {"badRequest":True,"message":des}
                dict = dotdict(aa)
                return dict
    def answer(self, callback_query_id, text=None, show_alert=None, url=None, cache_time=None):
        
        dataset = {'callback_query_id': callback_query_id}
        if text:
            dataset['text'] = text
        if show_alert is not None:
            dataset['show_alert'] = show_alert
        if url:
            dataset['url'] = url
        if cache_time is not None:
            dataset['cache_time'] = cache_time
        r = requests.post("https://api.telegram.org/bot{}/answerCallbackQuery".format(self.token), params=dataset)
        if "result" in r.text:
            info = r.json()['result']
            dict = dotdict(info)
            return dict
        else:
            des = r.json()['description']
            aa = {"badRequest":True,"message":des}
            dict = dotdict(aa)
            return dict
    def ban_chat(self, chat_id, sender_chat_id):
        dataset = {'chat_id': chat_id, 'sender_chat_id': sender_chat_id}
        r = requests.post("https://api.telegram.org/bot{}/banChatSenderChat".format(self.token), params=dataset)
        if "result" in r.text:
            info = r.json()['result']
            dict = dotdict(info)
            return dict
        else:
            des = r.json()['description']
            aa = {"badRequest":True,"message":des}
            dict = dotdict(aa)
            return dict
    def unban_chat(self, chat_id, sender_chat_id):
        dataset = {'chat_id': chat_id, 'sender_chat_id': sender_chat_id}
        r =  requests.post("https://api.telegram.org/bot{}/unbanChatSenderChat".format(self.token), params=dataset)
        if "result" in r.text:
            info = r.json()['result']
            dict = dotdict(info)
            return dict
        else:
            des = r.json()['description']
            aa = {"badRequest":True,"message":des}
            dict = dotdict(aa)
            return dict
    def admin_title(self, chat_id, user_id, custom_title):
        
        dataset = {
            'chat_id': chat_id, 'user_id': user_id, 'custom_title': custom_title
        }
        r  =  requests.post("https://api.telegram.org/bot{}/setChatAdministratorCustomTitle".format(self.token), params=dataset)
        if "result" in r.text:
            info = r.json()['result']
            dict = dotdict(info)
            return dict
        else:
            des = r.json()['description']
            aa = {"badRequest":True,"message":des}
            dict = dotdict(aa)
            return dict
    def poll(
        self, chat_id,
        question, options,
        is_anonymous = None, type = None, allows_multiple_answers = None, correct_option_id = None,
        explanation = None, explanation_parse_mode=None, open_period = None, close_date = None, is_closed = None,
        disable_notification=False, reply_to_message_id=None, allow_sending_without_reply=None,
        reply_markup=None, timeout=None, explanation_entities=None, protect_content=None):
        
        dataset = {
            'chat_id': str(chat_id),
            'question': question,
            'options': json.dumps(Bot._convert_poll_options(options))}

        if is_anonymous is not None:
            dataset['is_anonymous'] = is_anonymous
        if type is not None:
            dataset['type'] = type
        if allows_multiple_answers is not None:
            dataset['allows_multiple_answers'] = allows_multiple_answers
        if correct_option_id is not None:
            dataset['correct_option_id'] = correct_option_id
        if explanation is not None:
            dataset['explanation'] = explanation
        if explanation_parse_mode is not None:
            dataset['explanation_parse_mode'] = explanation_parse_mode
        if open_period is not None:
            dataset['open_period'] = open_period
        if close_date is not None:
            if isinstance(close_date, datetime):
                dataset['close_date'] = close_date.timestamp()
            else:
                dataset['close_date'] = close_date
        if is_closed is not None:
            dataset['is_closed'] = is_closed

        if disable_notification:
            dataset['disable_notification'] = disable_notification
        if reply_to_message_id is not None:
            dataset['reply_to_message_id'] = reply_to_message_id
        if allow_sending_without_reply is not None:
            dataset['allow_sending_without_reply'] = allow_sending_without_reply
        if reply_markup is not None:
            dataset['reply_markup'] = Bot._convert_markup(reply_markup)
        if timeout:
            dataset['timeout'] = timeout
        if explanation_entities:
            dataset['explanation_entities'] = json.dumps(
                regular.MessageEntity.to_list_of_dicts(explanation_entities))
        if protect_content:
            dataset['protect_content'] = protect_content
        r = requests.get("https://api.telegram.org/bot{}/sendPoll".format(self.token,chat_id), params=dataset)
        if "result" in r.text:
            info = r.json()['result']
            dict = dotdict(info)
            return dict
        else:
            des = r.json()['description']
            aa = {"badRequest":True,"message":des}
            dict = dotdict(aa)
            return dict
    def _convert_markup(markup):
        if isinstance(markup, regular.JsonSerializable):
            return markup.to_json()
        return markup
    def _convert_poll_options(poll_options):
        
        if poll_options is None:
            return None
        elif len(poll_options) == 0:
            return []
        elif isinstance(poll_options[0], str):
            # Compatibility mode with previous bug when only list of string was accepted as poll_options
            return poll_options
        elif isinstance(poll_options[0], regular.PollOption):
            return [option.text for option in poll_options]
        else:
            return poll_options
    def edit_capton(self, caption, chat_id=None, message_id=None, inline_message_id=None,
                         parse_mode=None, caption_entities=None,reply_markup=None):
        dataset = {'caption': caption}
        if chat_id:
            dataset['chat_id'] = chat_id
        if message_id:
            dataset['message_id'] = message_id
        if inline_message_id:
            dataset['inline_message_id'] = inline_message_id
        if parse_mode:
            dataset['parse_mode'] = parse_mode
        if caption_entities:
            dataset['caption_entities'] = json.dumps(regular.MessageEntity.to_list_of_dicts(caption_entities))
        if reply_markup:
            dataset['reply_markup'] = Bot._convert_markup(reply_markup)
        r = requests.post("https://api.telegram.org/bot{}/editMessageCaption".format(self.token), params=dataset)
    def convert_input_media(media):
        if isinstance(media, regular.InputMedia):
            return media.convert_input_media()
        return None, None
    def edit_media(self, media, chat_id=None, message_id=None, inline_message_id=None, reply_markup=None):
        method_url = r'editMessageMedia'
        media_json, file = Bot.convert_input_media(media)
        dataset = {'media': media_json}
        if chat_id:
            dataset['chat_id'] = chat_id
        if message_id:
            dataset['message_id'] = message_id
        if inline_message_id:
            dataset['inline_message_id'] = inline_message_id
        if reply_markup:
            dataset['reply_markup'] = Bot._convert_markup(reply_markup)
        r =  requests.post("https://api.telegram.org/bot{}/editMessageMedia".format(self.token), params=dataset, files=file)
        if "result" in r.text:
            info = r.json()['result']
            dict = dotdict(info)
            return dict
        else:
            des = r.json()['description']
            aa = {"badRequest":True,"message":des}
            dict = dotdict(aa)
            return dict