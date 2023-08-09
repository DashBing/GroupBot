
#!/usr/bin/python
# -*- coding: UTF-8 -*-


from . import *  # noqa: F403

import logging

import json
import base64


import re
import base64
import zstandard
import ast
import socket
import sys
import io

import urllib
import urllib.request
import urllib.error
from urllib import request
from urllib import parse

import io
import mimetypes
import uuid

import binascii
import traceback

import zlib
import gzip
import brotli
import time

import threading
from subprocess import Popen, PIPE

from telethon import events

import aiofiles
from aiofile import async_open


MT_API = "127.0.0.1:4246"
HTTP_RES_MAX_BYTES = 15000000
FILE_DOWNLOAD_MAX_BYTES = 64000000
TMP_PATH=HOME+"/tera/tmp"

gpt_chat=None

UA = 'Chrome Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) Apple    WebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36'

logger = logging.getLogger(__name__)


gptmode=[]
CLEAN = "/new_chat"
#  stuck= 0
stuck= {}

#  queue = asyncio.Queue(512)

queue = {}
queue_lock = asyncio.Lock()

no_reset = asyncio.Event()
no_reset.set()

LOADING="思考你发送的内容..."
LOADING2="Thinking about what you sent..."
LOADINGS="\n\n"+LOADING
LOADINGS2="\n\n"+LOADING2


#  UB.parse_mode = None
#  UB.parse_mode = 'html'
UB.parse_mode = 'md'

from functools import wraps

def exceptions_handler(func):

    if asyncio.iscoroutinefunction(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                _exceptions_handler(e)

    else:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                _exceptions_handler(e)
    return wrapper



def _exceptions_handler(e, *args, **kwargs):
    if type(e) == KeyboardInterrupt:
        raise e
    elif type(e) == SystemExit:
        raise e
    elif type(e) == RuntimeError:
        raise e
    elif type(e) == AttributeError:
        logger.warning(f"E: {repr(e)}", exc_info=True, stack_info=True)
    else:
        # logger.error(f"error: {exc=}", exc_info=True, stack_info=True)
        logger.warning(f"E: {repr(e)}", exc_info=True, stack_info=True)


def http_exceptions_handler(func):

    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except KeyboardInterrupt:
            raise
        except urllib.error.HTTPError as error:
            logging.error('Data not retrieved because %s\nURL: %s %s', error, args, kwargs)
            info = "E: {}".format(sys.exc_info())
            logger.error(info)
        except urllib.error.URLError as error:
            if isinstance(error.reason, socket.timeout):
#                logging.error('socket timed out - URL %s', url)
                logging.error('socket timed out')
                info = "E: {}".format(sys.exc_info())
    #            await NB.send_message(MY_ID, info)
                logger.error(info)
            else:
                logging.error('some other error happened')
                info = "E: {}".format(sys.exc_info())
                logger.error(info)
        #  except urllib.error.URLError:
        #      logger.warning("can not send")
        #      info = "E: {}".format(sys.exc_info())
        #      logger.error(info)
        except socket.timeout:
            info = "E: {}".format(sys.exc_info())
            logger.error(info)
        except UnicodeDecodeError as e:
            info = "E: {}".format(sys.exc_info())
            logger.error(info)
        except Exception as e:
            info = "E: {}".format(sys.exc_info())
            info = f"http exception: {e=}"
            logger.error(info, exc_info=True)
            @exceptions_handler
            async def _():
                raise e
            return await _()

    return wrapper

# https://www.utf8-chartable.de/unicode-utf8-table.pl
chr_list = ["\u200b"]

chr_list.append("\u180e")
chr_list.append("\ufeff")

# chr_list.append("\u200b") # added
chr_list.append("\u200c")
# chr_list.append("\u200d") # need test
# chr_list.append("\u200e") # fuck telegram
#chr_list.append("\u200f") # not good

chr_list.append("\u2060")
chr_list.append("\u2061")
chr_list.append("\u2062")
chr_list.append("\u2063")
chr_list.append("\u2064")
#    chr_list.append("\u2065")
chr_list.append("\u2066")
#chr_list.append("\u2067") # not good
chr_list.append("\u2068")
chr_list.append("\u2069")

#chr_list.append("\u206a") # not good

chr_list.append("\u206b")

chr_list.append("\u206c")
chr_list.append("\u206d")
chr_list.append("\u206e")
chr_list.append("\u206f")

num_jz = len(chr_list)



def ennum(k):
    # convert num to zero width spaces

    if type(k) != int:
        return None
    s = chr_list[k%num_jz]
    k = k//num_jz
    if k > 0:
        s = ennum(k)+s
    return s

def denum(s):
    # convert zero width spaces to num
    if not s:
        return None
    s = s.replace('"', '')
    try:
        kk = chr_list.index(s[-1])
        if len(s) > 1:
            k = denum(s[:-1])*num_jz+kk
        else:
            k = kk
    except IndexError:
        return None
    except ValueError:
        return None
    return k


def denum_auto(ss):
    s = ""
    n = False
    for i in ss:
        if i in chr_list:
            if n:
                s = i
                n = False
            else:
                s += i
        else:
            if s:
                n = True
    if n == "":
        return None
    return denum(s)

def enstr(s):
    # return ennum(int(s.encode().hex(),16))
    return ennum(byte2num(s.encode()))


def destr(s):
    if not s:
        return None
    try:
        s = s.replace('"', '')
    except AttributeError:
        pass

    try:
        # return bytes().fromhex(hex(denum(s))[2:]).decode()
        # return bytes.fromhex(hex(denum(s))[2:]).decode()
        #  return num2byte(denum(s)).decode()
        return num2byte(denum_auto(s)).decode()
    except TypeError:
        # (<class 'TypeError'>, TypeError("'NoneType' object cannot be interpreted as an integer"), <traceback object at 0xb5793bc8>)
        return None
    except AttributeError:
        # 'NoneType' object has no attribute 'decode'
        return None
    except UnicodeDecodeError as e:
        raise
        info = f"error: {e=}"



def num2byte(num):
    return bytes.fromhex(hex(num)[2:])

def byte2num(b):
    return int(b.hex(), 16)


# def int_to_bytes(x: int) -> bytes:
def num2byte(x):
    if type(x) == int:
        return x.to_bytes((x.bit_length() + 7) // 8, 'big')
    else:
        logger.warning("type error")
    
# def int_from_bytes(xbytes: bytes) -> int:
def byte2num(b):
    if isinstance(b, bytes):
        return int.from_bytes(b, 'big')
    else:
        logger.warning("type error")

def load_str(msg, no_ast=False):
    """str to dict"""
    msg = msg.strip()
    if no_ast:
        import json
        return json.loads(msg)
    try:
        return ast.literal_eval(msg)
    except ValueError:
        logger.warning(msg)
        import json
        return json.loads(msg)


# https://stackoverflow.com/a/9807138
def decode_base64(data, altchars=b'+/'):
    """Decode base64, padding being optional.

  :param data: Base64 data as an ASCII byte string
  :returns: The decoded byte string.

  """
    #  if type(data) == str:
    if isinstance(data, str):
        data = data.encode()
    #  if type(data) != bytes:
    if not isinstance(data, bytes):
        logger.error(f"wtf: {data=}")
        logger.error(f"wtf: {type(data)}")
        return
    data = bytes(data)
    data = re.sub(rb'[^a-zA-Z0-9%s]+' % altchars, b'', data)  # normalize
    missing_padding = len(data) % 4
    if missing_padding:
        data += b'=' * (4 - missing_padding)
    try:
        return base64.b64decode(data, altchars)
    except binascii.Error as e:
        logger.error(e)


def encode_base64(data, altchars=b'+/'):
    if isinstance(data, str):
        data = data.encode()
    return base64.b64encode(data, altchars=altchars).decode().rstrip("=")


def compress(data, m="zst"):
    if isinstance(data, str):
        data = data.encode()
    if m == "zst":
        return zstandard.compress(data, level=22)
    if m == "br":
        return brotli.compress(data)
    if m == "gzip":
        return gzip.compress(data)
    if m == "deflate":
        return zlib.compress(data)


#  return zlib.compress(data,level=9)


def decompress(data):
    if isinstance(data, str):
        data = data.encode()
    return zstandard.decompress(data)


from aiohttp import FormData
from aiohttp.client_exceptions import ClientPayloadError
from io import BufferedReader, TextIOWrapper, BytesIO

pb_list = {
        "anon": ["https://api.anonfiles.com/upload", "file"],
        "0x0": ["https://0x0.st/", "file"],
        "fars": ["https://fars.ee/?u=1", "c"]
        }
#async def pastebin(data="test", filename=None, url="https://fars.ee/?u=1", fieldname="c", extra={}, **kwargs):
@http_exceptions_handler
async def pastebin(data="test", filename=None, url=pb_list["fars"][0], fieldname="c", extra={}, ce=None, use=None, **kwargs):
    if not data:
        return
    if use:
        if use not in pb_list:
            use = "fars"
        url = pb_list[use][0]
        fieldname = pb_list[use][1]
    if not ce:
        if url == pb_list["fars"][0]:
            ce = "br"

    headers = {}
    #  if type(data) == str:
    if isinstance(data, str):
#    data = {"content": data}
#        data = zlib.compress(data)
#        headers = {'Content-Encoding': 'deflate'}
#        data = gzip.compress(data.encode())
#        headers = {'Content-Encoding': 'gzip'}
        if ce:
            data = compress(data.encode(), ce)
            headers = {'Content-Encoding': ce}
        data = {fieldname: data}
        data.update(extra)
    elif isinstance(data, bytes) or type(data) == BufferedReader or type(data) == TextIOWrapper or type(data) == BytesIO:
        if filename:
            data = file_for_post(data, filename=filename, fieldname=fieldname, **extra)
        else:
            data = {fieldname: data}
            data.update(extra)
    elif isinstance(data, dict):
        pass
#    elif type(data) == aiohttp.formdata.FormData:
    elif type(data) == FormData:
        pass
    else:
        return

    res = await http(url=url, method="POST", data=data, headers=headers,  **kwargs)
#        res = res + "." + filename.split(".")[-1]
    return res.strip()

def raise_error(error: str):
    error = "-" * 24 + f"\nerror:\n" + "-" * 24 + f"\n{error}" + "-" * 24
    #            logger.exception(info)
    logger.critical("\n" + error)
    raise SystemExit(error)

#  def get_sh_path(path='SH_PATH'):
def read_file_1line(path='/SH_PATH'):
  # f = open(os.getcwd() + "/SH_PATH")
  # p = Path(__package__).absolute()
  # p = p.parent
  # f = p / "SH_PATH"
  #  p = "/".join(__file__.split("/")[:-2])
  #  p = "/".join(__file__.split("/")[:-3])
  #  #  f = p + "/SH_PATH"
  #  f = p + "/" + path
  if path[0:1] != '/':
    path=PARENT_DIR.as_posix()+ "/" + path

  with open(path) as f:
      line = f.readline()
      line = line.rstrip('\n')
  if line:
      return line
  else:
    raise_error("E: can't find file: SH_PATH")
    return None


async def read_file(path='SH_PATH', *args, **kwargs):
  if path[0:1] != '/':
    path=PARENT_DIR.as_posix()+ "/" + path
  async with aiofiles.open(path, *args, **kwargs) as file:
      return await file.read()

#async def ipfs_add(data, filename=None, url="https://ipfs.infura.io:5001/api/v0/add?cid-version=1", *args, **kwargs):
async def ipfs_add(data, filename=None, url="https://ipfs.pixura.io/api/v0/add", *args, **kwargs):
#    res = data2url(data, url=url, filename=filename, fieldname="file", *args, **kwargs)
    if isinstance(data, str):
        data = data.encode()
    data = {"file": data}
    res = await http(url=url, method="POST", data=data, **kwargs)
    if not res:
        logger.error("fail to ipfs")
        return
    url = res.strip()
#    url = json.loads(url)
    try:
        url = load_str(url)
    except SyntaxError as e:
        info = f"{e=}\n\n{url}"
        print(info)
        return
#    url = url["Hash"]
    #  url = "https://{}.ipfs.infura-ipfs.io/".format(url["Hash"])
    url = "https://https://ipfs.pixura.io/ipfs/{}".format(url["Hash"])
    if filename:
    #    url += "?filename={}".format(parse.urlencode(filename))
        url += "?filename={}".format(parse.quote(filename))
#    await session.close()
    return url

def file_for_post(data, filename=None, fieldname="c", mimetype=None, **kwargs):
#    file = aiohttp.FormData()
    file = FormData(kwargs)
    if filename and not mimetype:
        mimetype = mimetypes.guess_type(filename)[0]
        if not mimetype:
            mimetype = 'application/octet-stream'
#    for i in kwargs:
#        file.add_fields((i, kwargs[i]))
    file.add_field(fieldname, data, filename=filename, content_type=mimetype)
    return file


async def pb_0x0(data, filename=None, *args, **kwargs):
    url = "https://0x0.st/"
    if isinstance(data, str):
        data = data.encode()
        if not filename:
            filename = "0.txt"
    return await pastebin(data, url=url, filename=filename, fieldname="file", *args, **kwargs)


async def itzmx(data, filename=None, *args, **kwargs):
    # https://send.itzmx.com/?info
    # 7z, exe, gif, jpg, png, rar, torrent, zip
    allowed = ("7z", "exe", "gif", "jpg", "png","rar","torrent","zip")
    url = "https://send.itzmx.com/api.php?d=upload-tool"
    if isinstance(data, str):
        data = data.encode()
        #  if not filename:
        #      filename = "0.txt"
        #  data = compress(data, "zst")
        #  if not filename:
        #      filename = "bin_zst.zip"
        if not filename:
            filename = "txt_not_zip.zip"
    extra = {}
    if not filename and filename.split(".")[-1] not in allowed:
        #  extra = { "randomname": "on" }
        filename += "_not_zip.zip"
    fieldname = "file"
    res = await pastebin(data, url=url, filename=filename, fieldname=fieldname, extra=extra, *args, **kwargs)
    return res

async def transfer1(data, filename=None, *args, **kwargs):
    url = "https://transfer.sh"
    if isinstance(data, str):
        data = data.encode()
        if not filename:
            filename = "0.txt"
    if filename:
        url = "https://transfer.sh/"+filename
    headers = {}
    headers['Max-Days'] = str(64)
    headers['Max-Downloads'] = str(64)
    res = await http(url=url, method="PUT", data=data, headers=headers,  **kwargs)
    return res

async def transfer(data, filename=None, *args, **kwargs):
    url = "https://transfer.sh"
    if isinstance(data, str):
        data = data.encode()
        if not filename:
            filename = "0.txt"
    if not filename:
        filename = "file"
    return await pastebin(data, url=url, fieldname=filename, *args, **kwargs)

async def file_io(data, filename=None, *args, **kwargs):
    url = "https://file.io"
    if isinstance(data, str):
        data = data.encode()
        if not filename:
            filename = "0.txt"
    res = await pastebin(data, url=url, filename=filename, fieldname="file", *args, **kwargs)
#    return load_str(res)["link"]
    try:
        d = load_str(res, no_ast=True)
    except SyntaxError as e:
        info = f"{e=}\n\n{url}"
        print(info)
        return
    return d["link"]


async def catbox(data, filename=None, tmp=False, *args, **kwargs):
    # https://catbox.moe/tools.php
    # https://litterbox.catbox.moe/tools.php
    if tmp:
        url = "https://litterbox.catbox.moe/resources/internals/api.php"
    else:
        url = "https://catbox.moe/user/api.php"
    reqtype = "fileupload"
    fieldname = "fileToUpload"
    if isinstance(data, str):
        if not tmp and url_only_re.match(data):
            # litterbox disallow upload via url
            reqtype = "urlupload"
            fieldname = "url"
        else:
            data = data.encode()
            if not filename:
                filename = "0.txt"
    extra = {
#            "userhash": "",
            "reqtype": reqtype
            }
    if tmp:
        extra["time"] = "72h"
    res = await pastebin(data, url=url, filename=filename, fieldname=fieldname, extra=extra, *args, **kwargs)
    if res:
        if "https://files.catbox.moe/" in res:
            res = res.replace("https://files.catbox.moe/", "https://de.catbox.moe/")
        return res

def tmp_save(data, ex=""):
    #  from ..config import SH_PATH
    name = "{}/{}{}".format(SH_PATH, time.time(), ex)
    if not isinstance(data, bytes):
        logger.error("need bytes")
        return
    data = bytes(data)
    with open(name, "wb") as file:
        file.write(data)
    return name


def format_byte(num):
    if not isinstance(num, (int, float)):
        num = int(num)
    if num < 0:
        s = "-"
        num = -1*num
    else:
        s = ""
    if num < 1000:
        u = "B"
        num = f"{num:.3g}"
    #  elif num < 1024*1024:
    elif num < 1024*1000:
        u = "KB"
        num = f"{num/1024:.3g}"
    elif num < 1024**2*1000:
        u = "MB"
        num = f"{num/1024/1024:.3g}"
    else:
        u = "GB"
        num = f"{num/1024/1024/1024:.3g}"
    return s+num+u


#  @exceptions_handler
#  async def send2mt(client, message):
#      "get msg for matterbridge api"
#      chat_id = get_chat_id(message)
#      if chat_id in MT_GATEWAY_LIST_for_tg:
#          sender_id = get_sender_id(message)
#  #        logger.warning(f"send 2 mt: {message.raw_text}")
#          logger.debug("start to mt")
#  #        if message.fwd_from:
#          if is_forward(message):
#              if sender_id == cid_tw:
#                  logger.info("I: ignore a msg from tw")
#                  raise StopPropagation
#  #        if message.sender_id == 1494863126:
#              # wtfipfsbot
#  #            pass
#          if sender_id == 420415423:
#              # t2bot
#              if message.text.startswith("bot: "):
#                  await message.delete()
#                  raise StopPropagation
#          if MT_GATEWAY_LIST_for_tg[chat_id] == "gateway5":  # need not to send in order
#              if is_edit(message):
#                  raise StopPropagation
#              msg = await parse_msg_for_mt(client, message)
#              if msg:
#                  await mt_send(msg[0], msg[1], msg[2], msg[3])
#          else:
#              global locks
#              if chat_id in locks:
#                  pass
#              else:
#                  locks.update({chat_id: asyncio.Lock()})
#              lock = locks[chat_id]
#              async with lock:
#                  msg = await parse_msg_for_mt(client, message)  # return [text, username, gateway, qt]
#                  if msg:
#                      if sender_id == BOT_ID:
#                          pass
#                      elif sender_id == TG_BOT_ID_FOR_MT:
#                          pass
#                      elif await parse_bridge_name(msg[1].rstrip(": ")):
#                          msg[1] = await parse_bridge_name(msg[1].rstrip(": "))
#                      else:
#                          #  if is_my_group(client, message):
#                          # if is_me(client, message):
#                              #  print(message)
#                              #  print(msg)
#                          await mt_send(msg[0], msg[1], msg[2], msg[3])
#                      #  if message.media is not None:
#                      #      return
#                      if not is_my_group(client, message):
#                          return
#                      if msg[2] == "gateway11":
#                          msg[2] = "gateway1"
#                      #for cmd answer
#                      if msg[1].endswith(": "):
#                          msg[1] = msg[1].strip(": ")
#                      if msg[1] != "C bot":
#                          if await CMD.check_cmd(client, message):
#                              logger.debug("cmd ok")
#                              pass
#                          else:
#                              text = msg[0]
#                              #  cmd = text.split(': ', 1)[1]
#                              cmd = text
#                              faq = await faq_get(cmd)
#                              if faq:
#                                  await cmd_answer_for_my_group(faq, message)
#
#                              elif cmd.startswith('.'):
#                                  logger.info("use bash")
#                                  asyncio.create_task(send_cmd_to_bash(msg))
#                                  raise StopPropagation
#  #        if message.out:
#  #            raise StopPropagation



import aiohttp
from aiohttp.client_exceptions import ClientPayloadError, ClientConnectorError

session = None

async def init_aiohttp_session():
    global session
    if session is None:
        session = aiohttp.ClientSession()
        logger.warning("a new session")
    else:
        logger.debug("session existed")
    return session





@exceptions_handler
async def mt_read():
  url = "http://" + MT_API + "/api/stream"
  session = await init_aiohttp_session()
  logger.info("start read msg from mt api...")
  while True:
    try:
      async with session.get(url, timeout=0) as resp:
        print("N: mt api init ok")
        #  resp.content.read()
        async for line in resp.content:
          logger.info("I: got a msg from mt api: %s", len(line))
          print(f"I: original msg: %s" % line)
          await mt2tg(line)
        # buffer = b""
        # async for data, end_of_http_chunk in resp.content.iter_chunks():
          # buffer += data
          # if end_of_http_chunk:
            # # print(buffer)
            # await send_mt_msg_to_queue(buffer, queue)
            # buffer = b""

    except ClientPayloadError:
      logger.warning("mt closed")
      print("mt closed, data lost")
    except ClientConnectorError:
      logger.warning("mt api is not ok, retry...")
    except Exception as e:
      logger.error(e)
      print(str(e))
    await asyncio.sleep(5)



@exceptions_handler
async def mt2tg(msg):
    try:
        try:
            msg = msg.decode()
#       Data sent: 'GET /api/stream HTTP/1.1\r\nHost: 127.0.0.1\r\n\r\n'
#      Data received: 'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nDate: Wed, 19 Jan 2022 02:03:29 GMT\r\nTransfer-Encoding: chunked\r\n\r\nd5\r\n{"text":"","channel":"","username":"","userid":"","avatar":"","account":"","event":"api_connected","protocol":"","gateway":"","parent_id":"","timestamp":"2022-01-19T10:03:29.666861315+08:00","id":"","Extra":null}\n\r\n'
            if not msg or msg.startswith("HTTP/1.1"):
              logger.info("I: ignore init msg")
              return

#        msg.replace(',"Extra":null}','}',1)
#        msgd=ast.literal_eval(msg.splitlines()[1])
#            msgd = json.loads(msg.splitlines()[1])
#            print(msg)
            msgd = json.loads(msg)
        except json.decoder.JSONDecodeError:
            logger.error("fail to decode msg from mt")
            print("################")
            print(msg)
            print("################")
            #  info = "E: {}\n==\n{}\n==\n{}".format(sys.exc_info()[1], traceback.format_exc(), sys.exc_info())
            #  logger.error(info)
            logger.error("E: failed to decode msg from mt...", exc_info=True, stack_info=True)
            return

        text = msgd["text"]
        name = msgd["username"]
        print(f"I: got msg: {name}: {text}")
        if not text:
          return

        #  if name == "C twitter: ":
        #      return
        if name.startswith("C "):
            return
        if name.startswith("**C "):
            return

        #  # need fix
        #  if "gateway11" in MT_GATEWAY_LIST:
        #      if msgd["gateway"] == "gateway1":
        #          msgd["gateway"] = "gateway11"

        #  if msgd["gateway"] == "test":
        #    pass
        #  else:
        #    return



        global queue
        need_clean = False

        if text[0:1] == ".":
          if text == ".gptmode":
            if msgd["gateway"] in gptmode:
              gptmode.remove(msgd["gateway"])
              await mt_send("gpt mode off", gateway=msgd["gateway"])
              return
            else:
              gptmode.append(msgd["gateway"])
              await mt_send("gpt mode on", gateway=msgd["gateway"])
              return
          elif text == ".gpt reset":
            if no_reset.is_set():
              no_reset.clear()
              async with queue_lock:
                if len(queue.keys()) > 1:
                  queue ={min(queue.keys()): queue[min((queue.keys()))] }
              text= CLEAN
              if len(queue.keys()) > 0:
                await mt_send("waiting...", gateway=msgd["gateway"])
            else:
              await mt_send("waiting reset...", gateway=msgd["gateway"])
              await no_reset.wait()
              await mt_send("reset ok", gateway=msgd["gateway"])
              return
          elif text == ".gpt" or text.startswith(".gpt ") or text.startswith(".gpt\n"):
            #  need_clean = True
            text=text[5:]
            if not text:
              #  await mt_send(".gpt $text", gateway=msgd["gateway"])
              await mt_send(".gpt $text\n--\n默认开启了上下文，重置命令“.gpt reset“。所有数据来自telegram机器人: @littleb_gptBOT ，使用userbot与其对接。", gateway=msgd["gateway"])
              return
          elif text == ".se" or text.startswith(".se "):
            #  need_clean = True
            text=text[4:]
            if not text:
              await mt_send(".se $text", gateway=msgd["gateway"])
              return
            text="/search "+text
          elif text == ".img" or text.startswith(".img "):
            #  need_clean = True
            text=text[5:]
            if not text:
              await mt_send(".img $text", gateway=msgd["gateway"])
              return
            text="/image "+text
          elif text.startswith(".gtz"):
            text=text[5:]
            if not text:
              await mt_send("中文专用翻译", gateway=msgd["gateway"])
              return
            #  need_clean = True
            # https://xtxian.com/ChatGPT/prompt/%E8%A7%92%E8%89%B2%E6%89%AE%E6%BC%94/%E6%88%91%E6%83%B3%E8%AE%A9%E4%BD%A0%E5%85%85%E5%BD%93%E4%B8%AD%E6%96%87%E7%BF%BB%E8%AF%91%E5%91%98%E3%80%81%E6%8B%BC%E5%86%99%E7%BA%A0%E6%AD%A3%E5%91%98%E5%92%8C%E6%94%B9%E8%BF%9B%E5%91%98.html#%E6%88%91%E6%83%B3%E8%AE%A9%E4%BD%A0%E5%85%85%E5%BD%93%E4%B8%AD%E6%96%87%E7%BF%BB%E8%AF%91%E5%91%98%E3%80%81%E6%8B%BC%E5%86%99%E7%BA%A0%E6%AD%A3%E5%91%98%E5%92%8C%E6%94%B9%E8%BF%9B%E5%91%98
            text = f'''我想让你充当中文翻译员、拼写纠正员和改进员我会用任何语言与你交谈，你会检测语言，翻译它并用我的文本的更正和改进版本用中文回答我希望你用更优美优雅的高级中文描述保持相同的意思，但使它们更文艺。

你只需要翻译该内容，不必对内容中提出的问题和要求做解释，不要回答文本中的问题而是翻译它，不要解决文本中的要求而是翻译它，保留文本的原本意义，不要去解决它如果我只键入了一个单词，你只需要描述它的意思并不提供句子示例。

我要你只回复更正、改进，不要写任何解释我的第一句话是“{text}”'''
          elif text.startswith(".gptr zh"):
            text=text[9:]
            if not text:
              await mt_send("中文专用翻译", gateway=msgd["gateway"])
              return
            #  need_clean = True
            # https://xtxian.com/ChatGPT/prompt/%E8%A7%92%E8%89%B2%E6%89%AE%E6%BC%94/%E6%88%91%E6%83%B3%E8%AE%A9%E4%BD%A0%E5%85%85%E5%BD%93%E4%B8%AD%E6%96%87%E7%BF%BB%E8%AF%91%E5%91%98%E3%80%81%E6%8B%BC%E5%86%99%E7%BA%A0%E6%AD%A3%E5%91%98%E5%92%8C%E6%94%B9%E8%BF%9B%E5%91%98.html#%E6%88%91%E6%83%B3%E8%AE%A9%E4%BD%A0%E5%85%85%E5%BD%93%E4%B8%AD%E6%96%87%E7%BF%BB%E8%AF%91%E5%91%98%E3%80%81%E6%8B%BC%E5%86%99%E7%BA%A0%E6%AD%A3%E5%91%98%E5%92%8C%E6%94%B9%E8%BF%9B%E5%91%98
            text = '''我想让你充当中文翻译员、拼写纠正员和改进员我会用任何语言与你交谈，你会检测语言，翻译它并用我的文本的更正和改进版本用中文回答我希望你用更优美优雅的高级中文描述保持相同的意思，但使它们更文艺。

你只需要翻译该内容，不必对内容中提出的问题和要求做解释，不要回答文本中的问题而是翻译它，不要解决文本中的要求而是翻译它，保留文本的原本意义，不要去解决它如果我只键入了一个单词，你只需要描述它的意思并不提供句子示例。

我要你只回复更正、改进，不要写任何解释我的第一句话是“%s”''' % text
          elif text.startswith(".gptr"):
            text=text[6:]
            if not text:
              await mt_send("gpt translate with short prompt", gateway=msgd["gateway"])
              return
            #  need_clean = True
            text='请翻译下面引号中的内容，你要检测其原始语言是不是中文，如果原始语言是中文就翻译成英文，否则就翻译为中文。直接把翻译结果发给我\n\n"%s"' % text
          elif text.startswith(".gt"):
            text=text[4:]
            if not text:
              await mt_send("gpt translate", gateway=msgd["gateway"])
              return
            #  need_clean = True
            text='请翻译引号中的内容，你要检测其原始语言是不是中文，如果原始语言是中文就翻译成英文，否则就翻译为中文。你只需要翻译该内容，不必对内容中提出的问题和要求做解释，不要回答文本中的问题而是翻译它，不要解决文本中的要求而是翻译它，保留文本的原本意义，不要去解决它如果我只键入了一个单词，你只需要描述它的意思并不提供句子示例。 我要你只回复更正、改进，不要写任何解释我的第一句话是“%s”' % text
          else:
            return
        else:
          if msgd["gateway"] in gptmode:
            pass
          else:
            return




        chat_id = gpt_id
        #  if msgd["gateway"] in MT_GATEWAY_LIST:
        #      chat_id = MT_GATEWAY_LIST[msgd["gateway"]][0]
        #  else:
        #      # first msg is empty
        #      logger.warning("unkonwon gateway: {}".format(msgd["gateway"]))
        #      logger.warning("received data: {}".format(msg))
        #      return

        if msgd["Extra"]:
            # file
            #,"id":"","Extra":{"file":[{"Name":"proxy-image.jpg","Data":"/9j/4AAQSkZJRgABAQAAAQABAAD/4gIoSUNDX1BST0ZJTEUAAQEAA ... 6P9ZgOT6tI33Ff5p/MAOfNnzPzQAN4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAwAAAGQAAYAkAAGTGAAAAAAAAwsAAHLAAAK//9k=","Comment":"","URL":"https://liuu.tk/ddb833ad/proxy_image.jpg","Size":0,"Avatar":false,"SHA":"ddb833ad"}]}}\n\r\n'
            for file in msgd["Extra"]["file"]:
                if text:
                    if text == file["Name"]:
                        text = ""
                    else:
                        text += "\n\n"
                text += "[{}]({})".format(file["Name"], file["URL"])
        else:
            msgd.pop("Extra")
            logger.warning("removed file info from mt api")

        logger.info("mt msg: {}".format(msgd))
        #      if name == "C Telegram: ":

        msgd.update({"chat_id": chat_id})
        msgd.update({"text": text})

        #7    msg = [0, chat_id, text, {"reply_to":reply_to}]
        #    await queue.put(msg)
        #    await queue.put(msgd)
        #  await queue.put([1, msgd])

        global gpt_chat
        if not gpt_chat:
          try:
            gpt_chat = await UB.get_input_entity(chat_id)
          except Exception as e:
            print(e)
            try:
              gpt_chat = await UB.get_input_entity('littleb_gptBOT')
            except ValueError:
              print("wtf, wrong id?")
              try:
                gpt_chat = await UB.get_entity(chat_id)
                print(gpt_chat.stringify())
              except:
                gpt_chat = await UB.get_entity('littleb_gptBOT')
                print(gpt_chat.stringify())
        #  print(f">{chat.user_id}: {text}")
        print(f"I: send {text} to gpt")
        if text != CLEAN:
          if not no_reset.is_set():
            await no_reset.wait()
          elif need_clean is True:
            msg = await UB.send_message(gpt_chat, CLEAN)

        #    while len(queue.keys()) > 0:
        #      print("W: waiting to reset...")
        #      await asyncio.sleep(1)
        msg = await UB.send_message(gpt_chat, text)
        #  await queue.put({msg.id: [msgd, msg]})
        #  await queue.put([msg, msgd])
        if text != CLEAN:
          async with queue_lock:
            queue[msg.id]=[msgd, None]
            global stuck
            #  if stuck == 0:
            if msgd["gateway"] not in stuck:
              #  stuck = min(queue.keys())
              stuck[msgd["gateway"]] = min(queue.keys())
        else:
          no_reset.set()
          await mt_send("reset ok", gateway=msgd["gateway"])
        return

        text = name + text
        #    await NB.send_message(chat_id, text, reply_to=reply_to)
        #    return [0, chat_id, text, {"reply_to":reply_to}]
        msg = [0, chat_id, text, {"reply_to": reply_to}]
#    await queue.put(msg)

    except:
        #  info = "E: " + str(sys.exc_info()[1]) + "\n==\n" + traceback.format_exc() + "\n==\n" + str(sys.exc_info())
        #  logger.error(info)
        logger.error("error: msg from mt to tg: ", exc_info=True, stack_info=True)
        #  await NB.send_message(MY_ID, info)
        await asyncio.sleep(5)



@exceptions_handler
async def http(url, method="GET", return_headers=False, **kwargs):
    await init_aiohttp_session()

    if "headers" in kwargs:
        headers = kwargs["headers"]
    else:
        headers = {}
        kwargs["headers"] = headers
    if "Accept-Encoding" not in headers:
        headers.update({
            "Accept-Encoding": "br;q=1.0, gzip;q=0.8, deflate;q=0.5"
            })
    if "User-agent" not in headers:
        headers.update({'User-agent': UA})

    try:
        res = await session.request(url=url, method=method, **kwargs)
    except asyncio.TimeoutError as e:
        raise
    async with res:
        # print("All:", res)
#        res.raise_for_status()
        if res.status == 304:
            logger.warning(f"http status: {res.status} {res.reason}\nurl: {res.url}")
            logger.warning("ignore: {}".format(await res.text()))
            if return_headers:
                return None, res.headers
            else:
                return
        if res.status != 200:
#            logger.error(res)
#            put(str(res))
            html = f"error http status: {res.status} {res.reason}\nurl: {res.url}\nheaders: {res.headers}"
            if return_headers:
                return html, res.headers
            else:
                return html
        # print(type(res))
        # print("Status:", res.status)
        # print("Content-type:", res.headers['content-type'])
        # print("Content-Encoding:", res.headers['Content-Encoding'])
        # print('Content-Length:', res.headers['Content-Length'])
        # print('Content-Length:', res.headers['Content-Length'])
            # print(res)
            # print("q: ", res.request_info)
            # print("a: ",  res.headers)

        try:
            data = None
            html = None
            if 'Content-Length' in res.headers and int(res.headers['Content-Length']) > HTTP_RES_MAX_BYTES:
                logger.warning(f"skip: too big: {url}")
            elif 'Transfer-Encoding' in res.headers and res.headers['Transfer-Encoding'] == "chunked":

                #  async for data in res.content.iter_chunked(HTTP_RES_MAX_BYTES):
                #      break
                data = b""
                async for tmp, _ in res.content.iter_chunks():
                    data += tmp
                    if len(data) > HTTP_RES_MAX_BYTES:
                        break
            else:
            # if res.headers['content-type'] == "text/plain; charset=utf-8":
                #  data = await res.read()
                data = await res.content.read(HTTP_RES_MAX_BYTES)

            if data is not None:
                #  try:
                #      if "Content-Encoding" in res.headers:
                #          if res.headers['Content-Encoding'] == "gzip":
                #              print("use gzip")
                #              data = gzip.decompress(data)
                #          elif res.headers['Content-Encoding'] == "deflate":
                #              print("use zlib")
                #              data = zlib.decompress(data)
                #          elif res.headers['Content-Encoding'] == "br":
                #              print("use br")
                #              data = brotli.decompress(data)
                #          elif res.headers['Content-Encoding']:
                #              logger.error("url: {}\nunknown encoding: {}".format(url, res.headers['Content-Encoding']))
                #              put("url: {}\nunknown encoding: {}".format(url, res.headers['Content-Encoding']))
                #              #  return data
                #  except Exception as e:
                #      logger.warning(e)
                #      put(e)

                # if "text/plain" in res.headers['content-type']:
                if "text" in res.headers['content-type']:
                    # return await res.text()
                    html = data.decode(errors='ignore')
                else:
                    # html = data.decode(errors='ignore')
                    html = data.decode()
        except ClientPayloadError as e:
            try:
                if "data" in locals():
                    html = data.decode(errors='ignore')
                else:
                    html = None
            except UnicodeDecodeError as e:
                html = None
        except UnicodeDecodeError as e:
            print("res.headers: ",  res.headers)
            print(f"res data: {data[:64]} 64/{len(data)}")
            logger.warning(f"decode failed: {url}\nerror: {e}")
            #  put(f"decode failed: {url}")
            html = data
        if return_headers:
            return html, res.headers
        else:
            return html

@exceptions_handler
async def mt_send(text="null", username="gpt", gateway="test", qt=None):

    # send msg to matterbridge
    url = "http://" + MT_API + "/api/message"

    #nc -l -p 5555 # https://mika-s.github.io/http/debugging/2019/04/08/debugging-http-requests.html
    #  url="http://127.0.0.1:5555/api/message"

#    if not username.startswith("C "):
#        username = "T " + username


    if qt:
        username = "{}\n\n{}".format("> " + "\n> ".join(qt.splitlines()), username)


#  gateway="gateway0"
    data = {
        "text": "{}".format(text),
        "username": "{}".format(username),
        "gateway": "{}".format(gateway)
    }
    res = await http(url, method="POST", json=data)
    logger.info("sent msg to mt, res: {}".format(res))
    return res






#  @exceptions_handler
#  @UB.on(events.NewMessage(outgoing=True))
#  async def my_event_handler(event):
#    #  if 'hello' in event.raw_text:
#    #    await event.reply('hi!')
#    #  if 'new_chat' in event.raw_text:
#    #    print(event.stringify())
#    msg = event.message
#    text = msg.raw_text
#    if event.chat_id != gpt_id:
#      if debug:
#        print("<%s %s" % (event.chat_id, text))
#      return
#    if event.chat_id != gpt_id:
#      if debug:
#        print(">%s %s" % (event.chat_id, text))
#      return
#    if text:
#      print("me: %s" % text)


async def download_media(msg, in_memory=False):
  pass



@UB.on(events.NewMessage(incoming=True))
@UB.on(events.MessageEdited(incoming=True))
@exceptions_handler
async def read_res(event):
  if event.chat_id != gpt_id:
    #  print("N: skip: %s != %s" % (event.chat_id, gpt_id))
    return
  #  if not no_reset.is_set():
  #    print("W: skiped the msg because of reset is waiting")
  #    return
  msg = event.message
  if msg.is_reply:
    if msg.reply_to_msg_id in queue:
      qid=msg.reply_to_msg_id
      global stuck
      gateway = queue[qid][0]["gateway"]
      is_loading= True
    else:
      print("W: skip: got a msg with a unkonwon id: all: %s\n queue: %s" % (msg.stringify(), queue))
      return
  else:
    print("W: skip: got a msg without reply: is_reply: %s\nall: %s" % (msg.is_reply, msg.stringify()))
    return

  #  text = msg.raw_text
  text = msg.text
  if msg.file:
    file = msg.file
    if file.size > FILE_DOWNLOAD_MAX_BYTES:
      await mt_send(f"文件过大，取消下载。\nfile name: {file.name}\nsize: {format_byte(file.size)}\n type: {file.mime_type}", gateway=gateway)
      return

    logger.info(file)
    if hasattr(file, "name") and file.name:
      file_name = file.name
    else:
      logger.info("file: no name")
      file_name = "%s.%s" % (int(time.time()), "jpg")
    url = f"tmp link:https://{DOMAIN}/{file_name}"
    try:
      async with async_open(f"{TMP_PATH}/{file_name}", 'wb') as f:
        #  async for chunk in UB.iter_download(file):
        async for chunk in UB.iter_download(msg):
          await f.write(chunk)
          await mt_send(f"下载中：{format_byte(f.tell())}/{format_byte(file.size)}", gateway=gateway)
    except Exception as e:
      logger.warning(f"E: {repr(e)}", exc_info=True, stack_info=True)
      try:
        await UB.download_media(msg, f"{TMP_PATH}/{file_name}")
      except Exception as e:
        logger.warning(f"E: {repr(e)}", exc_info=True, stack_info=True)
        try:
          url = await UB.download_media(msg, bytes)
        except Exception as e:
          logger.warning(f"E: {repr(e)}", exc_info=True, stack_info=True)
          await mt_send(f"E: failed to downlaod, error: {repr(e)}\nfile_name: {file_name}\nsize: {format_byte(file.size)}\n type: {file.mime_type}", gateway=gateway)
          return

    try:
      if isinstance(url, bytes):
        url = "pb: %s" % await pastebin(url, filename=file_name)
      else:
        async with async_open(f"{TMP_PATH}/{file_name}", 'wb') as f:
          url = f"pb: %s\n{url}" % await pastebin(f, filename=file_name)
    except Exception as e:
      logger.warning(f"E: {repr(e)}", exc_info=True, stack_info=True)
      print(f"E: {repr(e)}")
      if isinstance(url, bytes):
        url = f"E: pb: {repr(e)}"
      else:
        url = f"{url}\n--\nE: pb: {repr(e)}"

    try:
      if isinstance(url, bytes):
        url = "ipfs: %s" % await ipfs_add(url, filename=file_name)
      else:
        async with async_open(f"{TMP_PATH}/{file_name}", 'wb') as f:
          url = f"ipfs: %s\n{url}" % await ipfs_add(f, filename=file_name)
    except Exception as e:
      logger.warning(f"E: {repr(e)}", exc_info=True, stack_info=True)
      print(f"E: {repr(e)}")
      if isinstance(url, bytes):
        url = f"E: ipfs: {repr(e)}"
      else:
        url = f"{url}\n--\nE: ipfs: {repr(e)}"


    await mt_send(f"{text}\n--\n{url}\n--\nfile_name: {file_name}\nsize: {format_byte(file.size)}\n type: {file.mime_type}", gateway=gateway)
    is_loading= False

  elif text == "处理图片请求并获得响应可能需要最多5分钟，请耐心等待。" or text == "It may take up to 5 minutes to process image request and give a response, please wait patiently.":
    await mt_send(queue[qid][0]['username']+text, gateway=gateway)
    return
  elif text:
    pass
    #  print("I: > %s %s: %s" % (msg.chat_id, msg.sender_id, text[:9]))
    res = ""
    #  if qid > min(queue.keys()):
    #  while qid > min(queue.keys()):
    #    print("waiting...")
    #    await asyncio.sleep(2)

    async with queue_lock:
      #  if qid == min(queue.keys()) and stuck < qid:
      if stuck[gateway] < qid and qid == min(queue.keys()):
        stuck[gateway] = qid
        if queue[qid][1] is not None:
          res= queue[qid][0]['username']+"".join(queue[qid][1:])

    if qid == stuck[gateway]:
      if text == LOADING or text == LOADING2:
        await mt_send(f"{queue[qid][0]['username']}[思考中...]", gateway=gateway)
        return
    elif qid < stuck[gateway]:
      print("W: skip: gpt bot is editing history, but will be skipped")
      return
    print("< Q: %s" % queue[qid][0]['text'])
    if text.endswith(LOADING):
      print("> gpt(未结束): %s" % text)
      is_loading=True
      text = text.rstrip(LOADINGS)
    elif text.endswith(LOADING2):
      print("> gpt(未结束): %s" % text)
      is_loading=True
      text = text.rstrip(LOADINGS2)
    else:
      print("> gpt: %s" % text)
      is_loading=False
    if qid > stuck[gateway]:
      queue[qid][1] = text
      print(f"W: archived msg: {qid}>{stuck[gateway]}")
      return
    else:
      if queue[qid][1] is None:
        queue[qid][1] = text
      else:
        queue[qid].append(text[len("".join(queue[qid][1:])):])

    res += queue[qid][-1]
    if not is_loading:
      #  await mt_send(queue[qid][-1]+"\n[结束]", gateway=queue[qid][0]["gateway"])
      res += "\n\n**[结束]**"
    await mt_send(res, gateway=gateway)
  else:
    #  print("I: skip msg without text")
    print(f"W: skip msg without text in chat with gpt bot, wtf: {msg.stringify()}")
    return
  #  if msg.is_reply and msg.reply_to.reply_to_msg_id in queue:
  if not is_loading:
    async with queue_lock:
      if not no_reset.is_set():
        return
      queue.pop(qid)



async def my_event_handler(event):
  #  if 'hello' in event.raw_text:
  #    await event.reply('hi!')
  #  if 'new_chat' in event.raw_text:
  #    print(event.stringify())
  await read_res(event)


#  @exceptions_handler
#  @UB.on(events.MessageEdited(incoming=True))
#  async def my_event_handler(event):
#    #  if 'hello' in event.raw_text:
#    #    await event.reply('hi!')
#    #  if 'new_chat' in event.raw_text:
#    #    print(event.stringify())
#
#    await read_res(event)

async def __init():
  global SH_PATH, DOMAIN
  SH_PATH = (await read_file()).rstrip('\n')
  DOMAIN = (await read_file("DOMAIN")).rstrip('\n')
  print(f"SH_PATH: {SH_PATH}")
  print(f"DOMAIN: {DOMAIN}")


if __name__ == '__main__':
  print('{} 作为主程序运行'.format(__file__))
#  print(data2url("test"))
  #  asyncio.run(test())
elif 0:
  with open("test.jpg", "rb") as file:
    data = file.read()
    asyncio.run(ipfs_add(data, filename="test.jpg"))
elif __package__ == "":
  print('{} 运行, empty package'.format(__file__))
  #  from .html_to_telegraph_format import convert_html_to_telegraph_format
  # from ..telegram import put
  SH_PATH = asyncio.run(read_file()).rstrip('\n')
  DOMAIN = asyncio.run(read_file("DOMAIN")).rstrip('\n')
else:
  print('{} 运行, package: {}'.format(__file__, __package__))
# /tmp/run/user/1000/bot
  asyncio.create_task(__init())



