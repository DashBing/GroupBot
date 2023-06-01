import logging

logger = logging.getLogger(__name__)
mp = logger.info

from .. import *
from ..bot import *

from .telegram import MSG_QUEUE
from .telegram import get_peer, cid_wtfipfs, cid_ipfsrss, cid_tw, my_popen

from .tools import SH_PATH, tw_re, pic_re, url_only_re, my_host_re

import time
import asyncio

import os

from ..utils.telegram import my_popen


async def __tw_fav_task(tw_text, file=None):
    #from datetime import timedelta
    #from time import time
    #  delay=600 - time.time() % 600
    if time.time() % 600 < 30:
        await asyncio.sleep(30 - time.time() % 600)
    else:
        await asyncio.sleep(630 - time.time() % 600)


#  msg=await userbot.send_message(cid_tw, tw_text, parse_mode='md', link_preview=False, schedule=datetime.timedelta(seconds=delay))
#  await bot.send_message(cid_tw, tw_text, parse_mode='md', link_preview=False)

#[cid,info,False,"htm",file]
    global entry_task
    if file:
        #    if type(file) == list:
        #      msg=await client.send_file(my_chat_id, file=my_tw_files, caption=my_tw_text, parse_mode='md')
        entry_task.append([cid_tw, tw_text, False, "md", file])
    else:
        entry_task.append([cid_tw, tw_text, False, "md"])
    await start_send_entry_task(cid=cid_tw)


async def __tw_fav_loop_bu():
    #  global auto_msg_list # id [ctime interval target text]
    tw_fav_path = SH_PATH + "/tw_fav"
    while True:
        await asyncio.sleep(25)
        #    tw_path=os.environ.get("tmp")
        try:
            tw_list = os.listdir(tw_fav_path)
        except FileNotFoundError:
            continue
        for tw_file in tw_list:
            f = open(tw_fav_path + "/" + tw_file)
            #      lines = f.readlines()
            tw_text = f.read()
            f.close()
            tw_url = "https://twitter.com/"

            if debug:
                print("D: tw_text: " + tw_text)
                await bot.send_message(myid, "tw_text: " + tw_text)


#      lines = tw_text.split("\n")
#      if lines[0][0:len(tw_url)] == tw_url:
            if tw_text[0:len(tw_url)] == tw_url:
                # no file
                asyncio.create_task(tw_fav_task(tw_text),
                                    name="tw_fav " + tw_file)
            else:
                # with file
                file = tw_text.split("\n\n", 1)[0].split(" ")
                tw_text = tw_text.split("\n\n", 1)[1]
                asyncio.create_task(tw_fav_task(tw_text, file),
                                    name="tw_fav " + tw_file)
            os.remove(tw_fav_path + "/" + tw_file)


async def tw_fav_task(msg, stime):
    await asyncio.sleep(stime - time.time())
    await MSG_QUEUE.put(msg)


async def get_tw():
    path = "bash -l " + SH_PATH + "/get_fav_tw.sh"
    return await my_popen(path, shell=True, combine=False, max_time=512)


async def tw_fav_loop():
    #  global auto_msg_list # id [ctime interval target text]
    tw_fav_path = SH_PATH + "/tw_fav"
    stime = None
    while True:

        #    await asyncio.sleep(60)
        await asyncio.sleep(60 - time.time() % 60)
        res = await get_tw()
        if res[0] == 0:
            pass
        else:
            info = "error in get_tw sh: {}".format(res)
            logger.error(info)
            await NB.send_message(MY_ID, info)

#    tw_path=os.environ.get("tmp")
        try:
            tw_list = os.listdir(tw_fav_path)
        except FileNotFoundError:
            continue
        for tw_file in tw_list:
            f = open(tw_fav_path + "/" + tw_file)
            #      lines = f.readlines()
            tw_text = f.read()
            f.close()
            tw_url = "https://twitter.com/"

            logger.debug("tw_text: " + tw_text)
            #      await NB.send_message(MY_ID, "tw_text: "+tw_text)

            if tw_text[0:len(tw_url)] == tw_url:
                # no file
                file = None


#        asyncio.create_task(tw_fav_task(tw_text),name="tw_fav "+tw_file)
            else:
                # with file
                file = tw_text.split("\n\n", 1)[0].split(" ")
                if len(file) == 1:
                    file = file[0]
                tw_text = tw_text.split("\n\n", 1)[1]

            extra = {"parse_mode": "md", "link_preview": False, "file": file}
            if not stime or time.time() > stime:
                if time.time() % 600 < 30:
                    #        await asyncio.sleep(30 - time.time() % 600)
                    stime = time.time() + 30 - time.time() % 600
                else:
                    #        await asyncio.sleep(630 - time.time() % 600)
                    stime = time.time() + 630 - time.time() % 600
            else:
                stime += 3
            msg = [3, cid_tw, tw_text, extra]
            #      await MSG_QUEUE.put([0, cid_tw,tw_text,extra])
            #      asyncio.create_task(tw_fav_task(msg, stime),name="tw_"+tw_file)
            asyncio.create_task(tw_fav_task(msg, stime), name=str(cid_tw))

            os.remove(tw_fav_path + "/" + tw_file)


def main():
    asyncio.create_task(tw_fav_loop(), name="tw_fav_loop")


if __name__ == '__main__':
    main()
