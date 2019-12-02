#!/bin/python3
import sys, os, re, requests
import argparse
from telegram.bot import Bot

TMAIL_BOT_TOKEN=''

aparser = argparse.ArgumentParser()
aparser.add_argument('-bot', metavar='bot-token', help='bot token (optional)')
aparser.add_argument('-s', metavar='subject', help='subject (optional)')
aparser.add_argument('-chat', metavar='chat-id', help='chat id (optional)')
aparser.add_argument('-a', metavar='attachment', help='attachment (optional)')
aparser.add_argument('--documentype', help='specify attachment type like document', action='store_true')
aparser.add_argument('--chatsonly', help='return avail chats', action='store_true')
args = aparser.parse_args()

#token recovery process
if TMAIL_BOT_TOKEN == '':
    if not args.bot:
        try:
            TMAIL_BOT_TOKEN = os.environ['TMAIL_BOT_TOKEN']
        except KeyError:
            if not os.path.isfile(os.environ['HOME']+'/.tmail'):
                raise Exception("Environment variable 'TMAIL_BOT_TOKEN' is not set")
            else:
                with open(os.environ['HOME']+'/.tmail', 'r') as tokenfile:
                    TMAIL_BOT_TOKEN = tokenfile.read()[:-1]
    else:
        if os.path.isfile(args.bot):
            with open(args.bot, 'r') as tokenfile:
                token = tokenfile.read()[:-1]
        else:
            token = args.bot
        TMAIL_BOT_TOKEN=token

bot = Bot(TMAIL_BOT_TOKEN)

if args.chat:
    dst_chats = [args.chat,]
else:
    bot_updates = requests.get('https://api.telegram.org/bot%s/getUpdates'%TMAIL_BOT_TOKEN)
    #print(bot_updates.json())
    dst_chats = [result['message']['chat']['id'] for result in bot_updates.json()['result']]
    dst_chats = list(dict.fromkeys(dst_chats))

if args.chatsonly:
    list(map(print, dst_chats))
    sys.exit(0)

message = sys.stdin.read()[:-1]

#check message len
if len(message) > 4096:
    raise Exception("Len of the message is too big")

#check if subject passed
if args.s:
    message = '<b>%s</b>\n\n%s'%(args.s, message)

#process attachment
if args.a:
    attachment = open(args.a, 'rb')
    attachment_name = re.search(r'[0-9a-zA-Z._-]*$', args.a).group(0)
    if not args.documentype:
        attachment_type = re.search(r'[a-z]*$', args.a).group(0)
        print(attachment_type)
    else:
        attachment_type = None
    images = ('jpg', 'png',)
    videos = ('mp4', 'gif')
    audio = ('mp3',)

#send messages
for chat in dst_chats:
    bot.sendMessage(chat_id=chat, text=message, parse_mode='HTML')
    if args.a:
        attachment.seek(0)
        if attachment_type in images:
            bot.send_photo(chat_id=chat, photo=attachment, caption=attachment_name)
            
        elif attachment_type in videos:
            bot.send_video(chat_id=chat, video=attachment, caption=attachment_name)
        
        else:
            bot.sendDocument(chat_id=chat, document=attachment, filename=attachment_name)