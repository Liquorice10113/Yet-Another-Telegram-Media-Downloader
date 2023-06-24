import asyncio
import pyrogram
import json
from pyrogram import Client
from pyrogram.errors import FloodWait
import os
from os import path, mkdir
import sys
import time
import argparse

if path.exists("config_dev.py"):
    import config_dev as C
else:
    import config as C

parser = argparse.ArgumentParser(description='Yet Another Telegram Media Downloader.')

# Add the --help/-h argument
# parser.add_argument('-H', '--help', action='help', default=argparse.SUPPRESS,
#                     help='Show this help message and exit')

# Add the --name/-n argument
parser.add_argument('-c', '--chat', type=str, help='Specify a chat name like "https://t.me/xxx1234" or just "xxx1234". ')

args = parser.parse_args()


if C.api_hash == "your_api_hash_here":
    print("Hold on, fill your api_hash and api_id in `config.py` first! ")
    sys.exit(1)

media_types = ["video", "photo", "document"]
media_suffix = {
    "video": "mp4",
    "photo": "jpg"
}

if os.name == 'nt':
    path_divider = "\\"
else:
    path_divider = "/"

message_batch_size = 100
quitting = False

if args.chat:
    if "https://t.me/" in args.chat:
        chat_id = args.chat.replace("https://t.me/","")
    else:
        chat_id = args.chat
else:
    parser.print_help()
    sys.exit(1)


def progress_bar(current, total):
    p = current/total
    print("\r[" + int(20*p)*"▮"+int(20*(1-p))*"▯", end="] {:.2f}/{:.2f}MB".format(current/1024**2,total/1024**2) )
    sys.stdout.flush()


async def main():
    global quitting
    if not path.exists(chat_id):
        mkdir(chat_id)
    async with Client("my_account", C.api_id, C.api_hash,sleep_threshold=6000) as app:

        chat_history_count = await app.get_chat_history_count(chat_id)
        print(chat_history_count)
        if path.exists(path.join(".", chat_id, "progress.json")):
            with open(path.join(".", chat_id, "progress.json"), 'r') as f:
                data = json.loads(f.read())
                offset_id = data["offset_id"]
        else:
            offset_id = 1 + message_batch_size
        while offset_id < chat_history_count:
            cnt = 0
            try:
                async for message in app.get_chat_history(chat_id, limit=message_batch_size, offset_id=offset_id):
                    # print(message)
                    if (quitting):
                        break
                    # print("Processing message",message.id,'...')
                    if message.from_user:
                        print("{}:[{}]{}".format(
                            message.from_user.username, message.id, message.text))
                    for media_type in media_types:
                        if message.__getattribute__(media_type):
                            media = message.__getattribute__(media_type)
                            # print(media)
                            if media_type=="document":
                                filename = path.join(
                                    '.', chat_id, media_type)
                                if not filename.endswith(path_divider):
                                    filename = filename+path_divider
                            else:
                                filename = "{}{}.{}".format(str(media.date).replace(
                                "-", "").replace(" ", "").replace(":", ""), media.file_unique_id, media_suffix[media_type])
                                filename = path.join(
                                    '.', chat_id, media_type, filename)
                            if path.exists(filename):
                                print("[{}/{}]".format(offset_id-message_batch_size +
                                                    cnt, chat_history_count), "Skipped", filename)
                                continue
                            print(
                                "[{}/{}]".format(offset_id-message_batch_size+cnt, chat_history_count), filename)

                            res = await app.download_media(message, file_name=filename, progress=progress_bar)
                            if not res:
                                quitting = True
                                break
                            print()
                    cnt += 1
            except FloodWait as e:
                print(e)
                print("Oops, floodwait triggerd.")
                try:
                    await app.send_message("me", "[YATelegram] Oops, {} seconds of floodwait triggerd!".format(e.value))
                except:
                    pass
                sleep_time = 0
                while sleep_time<e.value+5:
                    print("\rStill sleeping({}/{})...".format(sleep_time,e.value) ,end="")
                    await asyncio.sleep(1)
                    sleep_time+=1
                print()
                try:
                    await app.send_message("me", "[YATelegram] Floodwait should be end now.")
                except:
                    pass
                quitting = False
            offset_id += message_batch_size
            with open(path.join(".", chat_id, "progress.json"), 'w') as f:
                f.write(json.dumps(
                    {
                        "offset_id": offset_id
                    }
                ))

asyncio.run(main())
