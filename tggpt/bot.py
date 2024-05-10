
#!/usr/bin/python
# -*- coding: UTF-8 -*-


#  from . import *  # noqa: F403
from enum import auto
from . import debug, WORK_DIR, PARENT_DIR, LOG_FILE, get_my_key, HOME, LOGGER
#  from tg.telegram import DOWNLOAD_PATH
from telethon.tl.types import KeyboardButton, KeyboardButtonUrl, PeerUser, PeerChannel, PeerChat, User, Channel, Chat

#  import aioxmpp
from aioxmpp import stream, ibr, protocol, node, dispatcher, connector, JID, im, errors, MessageType, PresenceType, misc
from inspect import isawaitable, currentframe


#  HOME = os.environ.get("HOME")

import logging
logger = logging.getLogger(__name__)

class NoParsingFilter(logging.Filter):
  def filter(self, record):
    #  if record.name == 'tornado.access' and record.levelno == 20:
    if record.levelno == 20:
      if record.name == 'httpx':
        #  pprint(record)
        msg = record.getMessage()
        if msg.startswith('HTTP Request: GET https://qwen-qwen1-5-72b-chat.hf.space/--replicas/3kh1x/heartbeat/') and msg.endswith(' "HTTP/1.1 404 Not Found"'):
          return False
        elif '404 Not Found' in msg and 'GET https://qwen-qwen1-5-72b-chat.hf.space/--replicas/3kh1x/heartbeat/' in msg:
           #  logger.info(f"根据关键词找到了文本: {msg=}")
           return False
        elif '404 Not Found' in msg:
           logger.info(f"根据关键词找到了文本: {msg=}")
           return False
        #  else:
        #    logger.info(f"文本不对: {msg=}")
    return True


import asyncio




import logging
from functools import wraps

import os

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
import subprocess
from subprocess import Popen, PIPE

from telethon import events

import aiofiles
#  from aiofile import async_open

from  urltitle.urltitle import URLTitleError
from urltitle import URLTitleReader


from collections import deque


import asyncio




from os.path import isdir
import aiofiles, aioxmpp, aiohttp

import asyncio, logging, json, ast, getpass, random, string, re
import sys, os
#  from time import time, sleep
#  from time import time
#  from asyncio import sleep
from collections import deque




gpt_bot = int(get_my_key("TELEGRAM_GPT_ID"))
gpt_bot_name = 'littleb_gptBOT'

#  rss_id = int(get_my_key("TELEGRAM_RSS_ID"))
rss_bot = 284403259
music_bot = 1404457467
music_bot_name = 'Music163bot'
id2gateway = {
    rss_bot: "rss",
    gpt_bot: "gateway1",
    }






def pprint(e):
  print('---')
  print("||%s: %s" % (type(e), e))
  print('---')
  for i in dir(e):
    print("  %s: %s: %s" % (i, type(getattr(e, i)), getattr(e, i)))
  print('===')


def info0(s):
  print("%s\r" % s.replace("\n", " "), end='')

def info1(s):
  print("%s" % s.replace("\n", " "), end='')

def info2(s):
  print("%s" % s.replace("\n", " "))

def send_log(text):
  #  asyncio.create_task(mt_send_for_long_text(text))
  asyncio.create_task(send1(text))

def err(text):
  if type(text) is not str:
    text = "{text=}"
  #  lineno = currentframe().f_back.f_lineno
  lineno = sys._getframe(1).f_lineno
  text = f"E: {lineno}: {text}"
  send_log(text)
  logger.error(text, exc_info=True, stack_info=True)
  #  raise ValueError


def warn(text, more=True):
  if type(text) is not str:
    text = "{text=}"
  #  lineno = currentframe().f_back.f_lineno
  lineno = sys._getframe(1).f_lineno
  text = f"W: {lineno}: {text}"
  send_log(text)
  if more:
    logger.warning(text, exc_info=True, stack_info=True)
  else:
    logger.warning(text)

def info(text):
  if type(text) is not str:
    text = "{text=}"
  lineno = sys._getframe(1).f_lineno
  text = f"{lineno}: {text}"
  logger.info(text)

def dbg(text):
  logger.debug(text)

def log(text):
  if type(text) is not str:
    text = "{text=}"
  #  lineno = currentframe().f_back.f_lineno
  lineno = sys._getframe(1).f_lineno
  text = f"{lineno}: {text}"
  send_log(text)
  logger.warning(text)

def get_cmd(text):
  cmd = text.split(' ')
  tmp = []
  for i in cmd:
    if tmp:
      ii = tmp[-1].split("\\\\")[-1]
      if ii and ii[-1] == "\\":
        tmp[-1] = tmp[-1][:-1] + " " + i
      else:
        #  if i:
        tmp.append(i)
    else:
      if i:
        tmp.append(i)
  if tmp:
    cmd = tmp
    logger.info(f"return cmd {len(cmd)}: {cmd=}")
    return cmd

def check_str(nick, nicks):
  for i in nicks:
    if i in nick:
      return True
  return False

def generand(N=4, M=None, *, no_uppercase=False):
  #  return ''.join(random.choice(string.ascii_lowercase+ string.digits) for x in range(N))
  if no_uppercase:
    l = string.ascii_lowercase + string.digits
  else:
    l = string.ascii_letters + string.digits
  if M is not None:
    N = random.randint(N, M)
  return ''.join(random.choice(l) for x in range(N))



def split_long_text(text, msg_max_length=500):
  texts = []
  if len(text.encode()) > msg_max_length:
    ls = text.splitlines()
    tmp = None
    last = None
    for l in ls:
      if tmp:
        if len((tmp+l).encode()) > msg_max_length:
          #  break
          texts.append(tmp)
          tmp = l
        else:
          tmp += '\n'+l
      else:
        if last:
          if len((last+l).encode()) > msg_max_length:
            texts.append(last)
            last = None
          else:
            texts.append(last+'\n'+l)
            last = None
            continue
        if len(l.encode()) > msg_max_length:
          tmp = l[:1300]
          while True:
            if len(tmp.encode()) > msg_max_length:
              tmp = tmp[:-1]
            else:
              texts.append(tmp)
              l = l[len(tmp):]
              if len(l.encode()) > msg_max_length:
                tmp = l[:1300]
              else:
                last = l
                break
        else:
          tmp = l

    if tmp:
      texts.append(tmp)
  else:
    texts = [text]
  return texts


#  api_id = int(get_my_key("TELEGRAM_API_ID"))



MY_ID = int(get_my_key("TELEGRAM_MY_ID"))


HTTP_RES_MAX_BYTES = 15000000
FILE_DOWNLOAD_MAX_BYTES = 64000000
TMP_PATH=HOME+"/tera/tmp"
DOWNLOAD_PATH = "/var/www/dav/tmp"

SH_PATH='/run/user/1000/bot'

#  gpt_chat=None

UA = 'Chrome Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) Apple    WebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36'
#  urlre=re.compile(r'((^|https?://|\s+)((([\dA-Za-z0-9.]+-?)+\.)+[A-Za-z]+|(\d+\.){3}\d+|(\[[\da-f]*:){7}[\da-f]*\])(:\d+)?(/[^/\s]+)*/?)')
#  urlre=re.compile(r'((https?://)?((([\dA-Za-z0-9.]+-?)+\.)+(?!https?)[A-Za-z]+|(\d+\.){3}\d+|(\[[\da-f]*:){7}[\da-f]*\])(:\d+)?(/[^/\s]+)*/?)')
#  urlre=re.compile(r'(^|\n|\s+)((https?://)?((([\dA-Za-z0-9.]+-?)+\.)+(?!https?)[A-Za-z]+|(\d+\.){3}\d+|(\[[\da-f]*:){7}[\da-f]*\])(:\d+)?(/[^/\s]+)*/?)')
#  urlre=re.compile(r'(^|\n|\s+)((https?://)?((([\dA-Za-z0-9.]+-?)+\.)+(?!https?)[A-Za-z]+|(\d+\.){3}\d+|(\[[\da-f]*:){7}[\da-f]*\])(:\d+)?(/[^/\s"]+)*/?)')
#  urlre=re.compile(r'(^|\n|\s+)((https?://)?((([\dA-Za-z0-9.]+-?)+\.)+(?!https?)[A-Za-z]+|(\d+\.){3}\d+|(\[[\da-f]*:){7}[\da-f]*\])(:\d+)?(/[0-9a-zA-Z$\-_\.\+\!\*\'\(\)\,]+)*/?)')
urlre=re.compile(r'(^|\n|\s+)(https?://((([\dA-Za-z0-9.]+-?)+\.)+(?!https?)[A-Za-z]+|(\d+\.){3}\d+|(\[[\da-f]*:){7}[\da-f]*\])(:\d+)?(/[0-9a-zA-Z$\-_\.\+\!\*\'\(\)\,\?\=%]+)*/?)')
url_md_left=re.compile(r'\[[^\]]+\]\([^\)]+')

qre = re.compile(r'^(>( .+)?)$', re.M)


#  gptmode=[]
CLEAN = "/new_chat"

#  queue = asyncio.Queue(512)

#  queue = {}
#  stuck= {}
queues = {}
nids = {}
mt_send_lock = asyncio.Lock()
downlaod_lock = asyncio.Lock()
bash_lock = asyncio.Lock()

rss_lock = asyncio.Lock()


gid_src = {}
mtmsgsg={}





allright = asyncio.Event()
#  allright.set()

allright_task = 0

LOADING="思考你发送的内容..."
LOADING2="Thinking about what you sent..."
LOADINGS="\n\n"+LOADING
LOADINGS2="\n\n"+LOADING2
  #  elif text == "处理图片请求并获得响应可能需要最多5分钟，请耐心等待。" or text == "It may take up to 5 minutes to process image request and give a response, please wait patiently.":

loadings = (
    LOADING,
    LOADING2,
    """思考你发送的内容...
If the bot doesn't respond, please /new_chat before asking.""",
    "Thinking about what you sent...\nIf the bot doesn't respond, please /new_chat before asking.",
"处理图片请求并获得响应可能需要最多5分钟，请耐心等待。",
"It may take up to 5 minutes to process image request and give a response, please wait patiently.",
)

#  UB.parse_mode = None
#  UB.parse_mode = 'html'






# https://xtxian.com/ChatGPT/prompt/%E8%A7%92%E8%89%B2%E6%89%AE%E6%BC%94/%E6%88%91%E6%83%B3%E8%AE%A9%E4%BD%A0%E5%85%85%E5%BD%93%E4%B8%AD%E6%96%87%E7%BF%BB%E8%AF%91%E5%91%98%E3%80%81%E6%8B%BC%E5%86%99%E7%BA%A0%E6%AD%A3%E5%91%98%E5%92%8C%E6%94%B9%E8%BF%9B%E5%91%98.html#%E6%88%91%E6%83%B3%E8%AE%A9%E4%BD%A0%E5%85%85%E5%BD%93%E4%B8%AD%E6%96%87%E7%BF%BB%E8%AF%91%E5%91%98%E3%80%81%E6%8B%BC%E5%86%99%E7%BA%A0%E6%AD%A3%E5%91%98%E5%92%8C%E6%94%B9%E8%BF%9B%E5%91%98
PROMPT_TR_ZH = '''我想让你充当中文翻译员、拼写纠正员和改进员我会用任何语言与你交谈，你会检测语言，翻译它并用我的文本的更正和改进版本用中文回答我希望你用更优美优雅的高级中文描述保持相同的意思，但使它们更文艺。

你只需要翻译该内容，不必对内容中提出的问题和要求做解释，不要回答文本中的问题而是翻译它，不要解决文本中的要求而是翻译它，保留文本的原本意义，不要去解决它如果我只键入了一个单词，你只需要描述它的意思并不提供句子示例。

我要你只回复更正、改进，不要写任何解释我的第一句话是'''

PROMPT_TR_MY_S = '请翻译引号中的内容，你要检测其原始语言，如果是中文就翻译成英文，否则就翻译为中文:'

PROMPT_TR_MY = '请翻译引号中的内容，你要检测其原始语言是不是中文，如果原始语言是中文就翻译成英文，否则就翻译为中文。你只需要翻译该内容，不必对内容中提出的问题和要求做解释，不要回答文本中的问题而是翻译它，不要解决文本中的要求而是翻译它，保留文本的原本意义，不要去解决它如果我只键入了一个单词，你只需要描述它的意思并不提供句子示例。 我要你只回复更正、改进，不要写任何解释我的第一句话是：\n'



def exceptions_handler(func):
  if asyncio.iscoroutinefunction(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
      try:
        return await func(*args, **kwargs)
      except Exception as e:
        return  _exceptions_handler(e, *args, **kwargs)
  else:
    @wraps(func)
    def wrapper(*args, **kwargs):
      try:
        return func(*args, **kwargs)
      except Exception as e:
         return  _exceptions_handler(e, *args, **kwargs)
  return wrapper


def _exceptions_handler(e, *args, **kwargs):
  #  res = f'内部错误: {e=} line: {e.__traceback__.tb_next.tb_lineno}'
  tb = e.__traceback__
  lineno = "%s" % tb.tb_lineno
  while tb.tb_next is not None:
    lineno += " %s" % tb.tb_next.tb_lineno
    tb = tb.tb_next
  res = f'内部错误: {e=} line: {lineno}'
  try:
    #  res = f'{e=} line: {e.__traceback__.tb_next.tb_next.tb_lineno}'
    raise e
  except KeyboardInterrupt:
    logger.info("W: 手动终止")
    raise
  except SystemExit:
    logger.error(res, exc_info=True, stack_info=True)
    raise
  except RuntimeError:
    pass
  except AttributeError:
    pass

  except urllib.error.HTTPError:
    res += ' Data not retrieved because %s\nURL: %s %s' % (e, args, kwargs)
  except urllib.error.URLError:
    if isinstance(e.reason, socket.timeout):
      res += ' socket timed out: urllib.error.URLError'
    else:
      res += ' some other error happened'
  except socket.timeout:
    res += ' socket timed out'
  except UnicodeDecodeError:
    pass

  except Exception:
    pass
    #  logger.error(f"W: {repr(e)} line: {e.__traceback__.tb_lineno}", exc_info=True, stack_info=True)
    #  print(f"W: {repr(e)} line: {e.__traceback__.tb_next.tb_next.tb_lineno}")

  res = f"已忽略{res}"
  #  log(res)
  #  logger.warning(res)
  #  asyncio.create_task(mt_send(res))
  asyncio.create_task(send(res, ME))
  #  logger.warning(res)
  logger.warning(res, exc_info=True, stack_info=True)
  return res


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
@exceptions_handler
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
def read_file_1line(path='SH_PATH'):
  # f = open(os.getcwd() + "/SH_PATH")
  # p = Path(__package__).absolute()
  # p = p.parent
  # f = p / "SH_PATH"
  #  p = "/".join(__file__.split("/")[:-2])
  #  p = "/".join(__file__.split("/")[:-3])
  #  #  f = p + "/SH_PATH"
  #  f = p + "/" + path
  if path[0:1] != '/':
    path = PARENT_DIR / path
    path = path.as_posix()

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
    path = PARENT_DIR / path
    path = path.as_posix()
  if not os.path.exists(path):
    warn(f"文件不存在: {path}")
    return
  async with aiofiles.open(path, *args, **kwargs) as file:
      return await file.read()

async def write_file(text, path='config.json', *args, **kwargs):
  if path[0:1] != '/':
    path = PARENT_DIR / path
    path = path.as_posix()
  async with aiofiles.open(path, *args, **kwargs) as file:
      return await file.write(text)

async def my_split(path, is_str=False):
  if is_str:
    text = path
  else:
    if os.path.exists(path):
      text = await read_file(path)
      logger.info(f"{path}: {text[:64]}...")
    else:
      warn(f"文件不存在: {path}")
      return []

  if text:
    pass
  else:
    warn(f"error text: {text=} {path=} {is_str=}")
    return []
  if text[-1] == '\n':
    text = text[:-1]
  if not text:
    warn(f"empty file: {path}")
    return []

  l = text.splitlines()
  tmp = []
  for i in l:
    if i:
      if i.strip(' ').strip('\t'):
        tmp.append(i.lstrip(' ').lstrip('\t'))
  l = tmp

  tmp = []
  for i in l:
    if i.startswith("#"):
      tmp.append(i)
    elif i.startswith("/* "):
      tmp.append(i)
    elif i.startswith("// "):
      tmp.append(i)
  for i in tmp:
    l.remove(i)
  return l


#async def ipfs_add(data, filename=None, url="https://ipfs.infura.io:5001/api/v0/add?cid-version=1", *args, **kwargs):
async def ipfs_add(data, filename=None, url="https://ipfs.pixura.io/api/v0/add", *args, **kwargs):
#  res = data2url(data, url=url, filename=filename, fieldname="file", *args, **kwargs)
  if isinstance(data, str):
    data = data.encode()
  data = {"file": data}
  res = await http(url=url, method="POST", data=data, **kwargs)
  if not res:
    logger.error("E: fail to ipfs")
    return

  url = res.strip()
  logger.info(res)
#  url = json.loads(url)
  try:
    url = load_str(url)
  except SyntaxError as e:
    info = f"{e=}\n\n{url}"
    print(info)
    return
#  url = url["Hash"]
  #  url = "https://{}.ipfs.infura-ipfs.io/".format(url["Hash"])
  url = "https://ipfs.pixura.io/ipfs/{}".format(url["Hash"])
  if filename:
  #  url += "?filename={}".format(parse.urlencode(filename))
    url += "?filename={}".format(parse.quote(filename))
#  await session.close()
  return url

def file_for_post(data, filename=None, fieldname="c", mimetype=None, **kwargs):
#  file = aiohttp.FormData()
  file = FormData(kwargs)
  if filename and not mimetype:
    mimetype = mimetypes.guess_type(filename)[0]
    if not mimetype:
      mimetype = 'application/octet-stream'
#  for i in kwargs:
#    file.add_fields((i, kwargs[i]))
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
    #    filename = "0.txt"
    #  data = compress(data, "zst")
    #  if not filename:
    #    filename = "bin_zst.zip"
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
#  return load_str(res)["link"]
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
#      "userhash": "",
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
    try:
      return json.loads(msg)
    except Exception as e:
      err(f"json: error str: {msg} line: {e.__traceback__.tb_lineno}")
      #  raise e




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





async def update_stdouterr(data):
  while data[2].poll() == None:
    try:
      data[0], data[1] = data[2].communicate(timeout=0.6)
    except subprocess.TimeoutExpired as e:
      if e.stdout:
        data[0] = e.stdout.decode("utf-8")
      if e.stderr:
        data[1] = e.stderr.decode("utf-8")
    await asyncio.sleep(0.3)


async def update_stdout(data):
  while True:
    print(1)
    await asyncio.sleep(0.4)
    tmp = await data[2].stdout.readline()
    if tmp:
      data[0] = data[0] + tmp.decode("utf-8")
    else:
      break
  logger.info(11)


async def update_stderr(data):
  while True:
    print(2)
    await asyncio.sleep(0.2)
    tmp = await data[2].stderr.readline()
    if tmp:
      data[1] = data[1] + tmp.decode("utf-8")
    else:
      break
  logger.info(22)


async def my_popen(cmd,
           shell=True,
           max_time=512,
           client=None,
           msg=None,
           combine=True,
           return_msg=False,
           executable='/bin/bash',
           **args):
  
  async with bash_lock:
    logger.info(cmd)
    #    args=shlex.split(message.text.split(' ',1)[1])

    #    p=subprocess.Popen(message.text.split(' '))
    #    p=subprocess.Popen(message.text.split(' ')[1:],universal_newlines=True,bufsize=1,text=True,stdout=PIPE, stderr=PIPE, shell=True)
    #    p=subprocess.Popen(shlex.split(message.text.split(' ',1)[1]),text=True,stdout=PIPE, stderr=PIPE, shell=True)

    #    p=subprocess.Popen(args,text=True,stdout=PIPE, stderr=PIPE, shell=True)
    #    p=Popen(args,text=True,universal_newlines=True,bufsize=1,stdout=PIPE, stderr=PIPE)
    #    p=Popen(args,text=True,stdout=PIPE, stderr=PIPE)
    #    p=await asyncio.create_subprocess_shell(message.text.split(' ',1)[1],stdout=PIPE, stderr=PIPE)#limit=None
    #    p=Popen(args,stdout=PIPE, stderr=PIPE,bufsize=8000000)
    #    p=Popen(args,stdout=PIPE, stderr=PIPE,text=True,encoding="utf-8",errors="ignore")
    #  p=Popen(cmd,shell=shell,stdout=PIPE, stderr=PIPE,text=True,encoding="utf-8",errors="ignore")
    p = Popen(cmd,
          shell=shell,
          stdout=PIPE,
          stderr=PIPE,
          text=True,
          encoding="utf-8",
          errors="ignore",
          executable=executable)

    start_time = time.time()
    res = ""
    errs = ""
    data = ["", "", p]
    asyncio.create_task(update_stdouterr(data))
    await asyncio.sleep(1)
    logger.info(str(p.args))
    while True:
      #  if p.poll() == None and p.returncode == None:
      if p.poll() == None:
        pass
      else:
        break
      #  await asyncio.sleep(0.5)
      res = data[0]
      errs = data[1]

      #  tmp = "...\n" + res + "\n==\nE: \n" + errs
      tmp = "...\n%s\n==\nE: ?\n%s" % (res, errs)
      tmp = tmp.strip()
      #  if msg:
      #    if tmp != msg.text:
      if True:
          try:
            #  msg = await cmd_answer(tmp, client, msg, **args)
            logger.info(f"临时输出: {tmp}")
          except Exception as e:
            logger.error(f"can not send tmp: {e=}")
            #  msg = await client.send_message(MY_ID, tmp)
            logger.info(f"临时输出: {tmp} {e=}")
      await asyncio.sleep(2)
      if time.time() - start_time > max_time:
        p.kill()
        res = "my_popen: timeout, killed, cmd: {}\nres: {}".format(cmd, res)
        warn(res)
        #  await cmd_answer(res, client, msg)
        #  logger.info(f"最终输出: {res}")
        break

    try:
      res, errs = p.communicate(timeout=5)
    except subprocess.TimeoutExpired as e:
      logger.error("timeout")
      res = e.stdout
      errs = e.stderr

    logger.info("popen exit")
    if res:
      if isinstance(res, bytes):
        res = res.decode()
    if errs:
      if isinstance(errs, bytes):
        errs = errs.decode()
    if not res:
      return False
      res = "null"

    #  if msg:
    #    #  msg = await cmd_answer(res, client, msg, **args)
    #    logger.info(f"发送: {res}")
    #    if return_msg:
    #      return msg
    if combine:
      if p.returncode:
        res = "%s\n==\nE: %s" % (res, p.returncode)
        if errs:
          res += "\n%s" % errs
      return res
    else:
      return p.returncode, res, errs


async def run_my_bash(cmd, shell=True, max_time=64):
  p = Popen(cmd,
        shell=shell,
        stdout=PIPE,
        stderr=PIPE,
        text=True,
        encoding="utf-8",
        errors="ignore")

  start_time = time.time()
  res = ""
  errs = ""
  await asyncio.sleep(0.5)
  if p.poll() == None and p.returncode == None:
    while p.poll() == None and p.returncode == None:
      if time.time() - start_time > max_time:
        p.kill()
        break
      await asyncio.sleep(1)

  try:
    res, errs = p.communicate(timeout=3)
  except subprocess.TimeoutExpired as e:
    res = e.stdout
    errs = e.stderr
  if not res:
    res = "null"
  #  res = str(res)
  if p.returncode:
    #  res = res + "\n==\nE: " + str(p.returncode)
    res = "%s\n==\nE: %s" % (res, p.returncode)
    if errs:
      res = res + "\n" + errs
    #await msg.delete()
  return res


async def my_exec(cmd, client=None, msg=None, **args):
  #  exec(cmd) #return always is None
  #  p=Popen("my_exec.py "+message.text.split(' ',1)[1],shell=True,stdout=PIPE, stderr=PIPE,text=True,encoding="utf-8",errors="ignore")
  #  await my_popen(["python3", "my_exec.py", cmd], shell=False, msg=msg)
  #  await my_popen([ SH_PATH + "/my_exec.py", cmd], shell=False, msg=msg, executable="/usr/bin/python3")
  res = await my_popen(cmd,
             shell=True,
             client=client, 
             msg=msg,
             executable="/usr/bin/python3",
             **args)
  return res


async def my_eval(cmd, client=None, msg=None, **args):
  res = eval(cmd)
  logger.info(str(res) + "\n" + str(type(res)))
  res = await cmd_answer(str(res), client=client, msg=msg, **args)
  return res


async def send_cmd_to_bash(msg):
  """run cmd of text msg from mt by bash(old)"""
  if isinstance(msg, str):
    shell_cmd = ["bash", SH_PATH + "/bcmd.sh"]
    shell_cmd.append("just_get_reply")
    shell_cmd.append(msg)
  else:
    # [gateway, username, text]
    if type(msg) == list:
      #  if not " " in msg[1]:
      if len(msg[1]) < 2 or msg[1][1] != ' ':
        msg[1] = "X " + msg[1]
      msg_mt = {
        "text": msg[2],
        "username": "{}".format(msg[1]),
        "gateway": msg[0]
      }
      msg = msg_mt
    text = msg["text"]
    name = msg["username"]
    if not text:
      return
    if name.startswith("C "):
      return
    logger.info("run cmd: {}".format(msg))
    #  shell_cmd="{} {} {} {}"
    #  shell_cmd = ["bash -l", SH_PATH + "/bcmd.sh"]
    shell_cmd = ["bash", SH_PATH + "/bcmd.sh"]
    shell_cmd.append(msg["gateway"])
    shell_cmd.append(msg["username"])
    shell_cmd.append(msg["text"])
    shell_cmd.append(repr(msg))

    if shell_cmd[1] == "gateway1":
      #  if my_host_re.match(shell_cmd[3]):
      if urlre.match(shell_cmd[3]):
        print("my url")
        shell_cmd[3] = ".ipfs {} only".format(shell_cmd[3])
        #  shell_cmd[1] = "gateway4"
      elif tw_re.match(shell_cmd[3]):
        print("a twitter")
        shell_cmd[3] = ".tw {}".format(shell_cmd[3])
        #  shell_cmd[1] = "gateway4"
      elif pic_re.match(shell_cmd[3]):
        print("a pic")
        shell_cmd[3] = ".ipfs {} only".format(shell_cmd[3])
        #  shell_cmd[1] = "gateway4"
      elif url_only_re.match(shell_cmd[3]):
        print("a url")
        shell_cmd[3] = ".ipfs {} autocheck".format(shell_cmd[3])
        #  shell_cmd[1] = "gateway4"
  logger.warning("bash cmd: {}".format(shell_cmd))
  #  await run_my_bash(shell_cmd, shell=False)
  #  await my_popen(shell_cmd, shell=False)
  #  await my_popen(" ".join(shell_cmd))
  res = await my_popen(shell_cmd, shell=False)
  #  logger.info(res)
  return res

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




async def load_config():
  path = PARENT_DIR / "config.json"
  config = await read_file(path.as_posix())
  config = load_str(config)

  logger.info("config\n%s" % json.dumps(config, indent='  '))
  
  if config is None:
    warn("配置文件有问题: config.json")
    return
  try:
    config["sync_groups_all"].append(config["public_groups"])
    config["sync_groups_all"].append(config["bot_groups"])

    config["public_groups"] = config["public_groups"] + config["rss_groups"] + config["bot_groups"] + config["extra_groups"]

    config["my_groups"] = config["my_groups"] + config["public_groups"]

    

    #  jid = get_my_key("JID")
    #  config['ME'] = jid

    logger.info("loaded config\n%s" % json.dumps(config, indent='  '))

    for i in config:
      if type(config[i]) is list:
        if config[i]:
          if type(config[i][0]) is str:
            config[i] = set(config[i])
          elif type(config[i][0]) is list:
            tmp = []
            for j in config[i]:
              tmp.append(set(j))
            config[i] = tmp


    globals().update(config)

    return True
  except Exception as e:
    warn(f"配置文件有问题: config.json {e=}")
    raise e

#  asyncio.run(load_config())




import aiohttp
from aiohttp.client_exceptions import ClientPayloadError, ClientConnectorError

session = None

async def init_aiohttp_session():
  global session
  if session is None:
    #  session = aiohttp.ClientSession()
    session = aiohttp.ClientSession()
    logger.warning("a new session")
  else:
    logger.debug("session existed")
  return session


# Titles for HTML content
reader = URLTitleReader(verify_ssl=True)

async def get_title(url):
  try:
    #  res = reader.title(url)
    res = await asyncio.to_thread(reader.title, url)
  except TypeError as e:
    res=f"{e=}"
    logger.info(res)
    #  prof.cons_show(res)
  #  except urltitle.urltitle.URLTitleError as e:
  except URLTitleError as e:
    res=f"{e=}"
    #  prof.cons_show(res)
    logger.info(res)
  except Exception as e:
    logger.warning(f"E: {e=}", exc_info=True, stack_info=True)
    res=f"{e=}"
    #  prof.cons_show(res)
    logger.info(res)
  return res



#  async def other_init():
#    logger.info("开始初始化其他组件")
#    res = await asyncio.to_thread(_other_init)
#    logger.info(res)
#  #  allright.set()
#    if res is True:
#      global allright_task
#      allright_task -= 1
#
#  @exceptions_handler
#  def _other_init():
#    return True


#  global G1PSID
#  BING_U = get_my_key("BING_U")
G1PSID = get_my_key('BARD_COOKIE_KEY')

from g4f.cookies import set_cookies

#  set_cookies(".bing.com", {
#    "_U": "%s" % BING_U
#  })
set_cookies(".google.com", {
  "__Secure-1PSID": G1PSID
})


from g4f import models, Provider
from g4f.client import Client as Client_g4f

#  def ai_img(prompt, model="gemini", proxy=None):
async def ai_img(prompt, model="gemini"):
  try:
    global g4fclient
    if "g4fclient" not in globals():
      g4fclient = Client_g4f()
    #  response = client.images.generate(
      #  response = await client.images.generate(
      response = await asyncio.to_thread(g4fclient.images.generate,
      model=model,
      #  prompt="a white siamese cat",
      prompt=prompt,
    )
  except Exception as e:
    image_url = f"{e=}"
  else:
    image_url = response.data[0].url
  #  print(image_url)
  return image_url

async def ai(prompt, provider=Provider.You, model=models.default, proxy=None):
  try:
    global g4fclient
    if "g4fclient" not in globals():
      g4fclient = Client_g4f()
    #  response = client.chat.completions.create(
      #  response = await client.chat.completions.create(
      #  s = await asyncio.to_thread(run_ocr, img=res)
      response = await asyncio.to_thread(g4fclient.chat.completions.create,
      model=model,
      messages=[{"role": "user", "content": prompt}],
      provider=provider,
      proxy=proxy,
    )
  except Exception as e:
    image_url = f"{e=}"
  else:
    image_url  = response.choices[0].message.content
  #  print(image_url)
  return image_url



from gradio_client import Client as Client_hg

HF_TOKEN = get_my_key('HF_TOKEN')


async def hg(prompt, provider=Provider.You, model=models.default, proxy=None):
  try:
    global hgclient
    if "hgclient" not in globals():
      hgclient = Client_hg(api_key=HF_TOKEN)
    #  response = client.chat.completions.create(
    response = await hgclient.chat.completions.create(
      model=model,
      messages=[{"role": "user", "content": prompt}],
      provider=provider,
      proxy=proxy,
    )
  except Exception as e:
    image_url = f"{e=}"
  else:
    image_url  = response.choices[0].message.content
  #  print(image_url)
  return image_url


async def qw(text):
  try:
    global qw_client
    if "qw_client" not in globals():
      qw_client = Client_hg("https://qwen-qwen1-5-72b-chat.hf.space/--replicas/3kh1x/")
    #  result = qw_client.predict(
    result = await asyncio.to_thread(qw_client.predict,
        #  sys.argv[1],	# str  in 'Input' Textbox component
        text,	# str  in 'Input' Textbox component
        #  [[sys.argv[1], sys.argv[1]]],	# Tuple[str | Dict(file: filepath, alt_text: str | None) | None, str | Dict(file: filepath, alt_text: str | None) | None]  in 'Qwen1.5-72B-Chat' Chatbot component
        [],	# Tuple[str | Dict(file: filepath, alt_text: str | None) | None, str | Dict(file: filepath, alt_text: str | None) | None]  in 'Qwen1.5-72B-Chat' Chatbot component
        "You are a helpful assistant.",	# str  in 'parameter_9' Textbox component
        api_name="/model_chat"
    )
    #  print(result)
    #  print(result[1][1][1])
    #  print(result[1][0][1])
    res = result[1][0][1]
  except Exception as e:
    res = f"{e=}"
  return res

async def qw2(text):
  try:
    global qw2_client
    if "qw2_client" not in globals():
      qw2_client = Client_hg("Qwen/Qwen1.5-110B-Chat-demo")
    #  result = qw2_client.predict(
    result = await asyncio.to_thread(qw2_client.predict,
        #  query=sys.argv[1],
        query=text,
        history=[],
        system="You are a helpful assistant.",
        api_name="/model_chat"
    )
    #  print(result)
    #  print(result[1][1][1])
    #  print(result[1][0][1])
    res = result[1][0][1]
  except Exception as e:
    res = f"{e=}"
  return res





def get_src(msg):
  if msg.type_ == MessageType.GROUPCHAT:
    return str(msg.from_.bare())
  if msg.from_.is_bare:
    return str(msg.from_)
  if str(msg.to.bare()) in my_groups:
    return str(msg.from_)
  return str(msg.from_.bare())





send_locks = {}


async def _send(*args, **kwargs):
  asyncio.create_task(__send(*args, **kwargs))
  return True

async def __send(msg, client=None, room=None, name=None):
  jid = str(msg.to)
  if jid not in send_locks:
    send_locks[jid] = asyncio.Lock()

  async with send_locks[jid]:
    if name is not None:
      room = None
      if str(msg.to.bare()) in rooms:
        room = rooms[str(msg.to.bare())]
        #  if msg.type_ == MessageType.GROUPCHAT:
        if room.me.nick != name:
          await room.set_nick(name)
          logger.info(f"set nick: {str(msg.to.bare())} {room.me.nick} -> {name}")
        else:
          logger.info(f"set nick: {str(msg.to.bare())} {room.me.nick} = {name}")
      else:
        logger.info(f"not found room: {msg.to}")


    if msg.to.is_bare or msg.type_ == MessageType.GROUPCHAT or str(msg.to.bare()) not in my_groups:
    #  if gpm is False:
      if client is not None:
        # https://docs.zombofant.net/aioxmpp/devel/api/public/node.html?highlight=client#aioxmpp.Client.send
        res = client.send(msg)
      elif room:
        # https://docs.zombofant.net/aioxmpp/devel/api/public/muc.html?highlight=room#aioxmpp.muc.Room.send_message
        res = room.send_message(msg)
      else:
        client = XB
        res = client.send(msg)
    else:
      # https://docs.zombofant.net/aioxmpp/devel/api/public/im.html#aioxmpp.im.conversation.AbstractConversation.send_message
      if client is None:
        client = XB
      p2ps = client.summon(im.p2p.Service)
      c = p2ps.get_conversation(msg.to)
      #  stanza = c.send_message(msg)
      res = c.send_message(msg)
      #  return False
    #  if isawaitable(res):
    #  logger.info(f"{type(res)}: {res} {msg}")
    if asyncio.iscoroutine(res) or type(res) is stream.StanzaToken:
      #  dbg(f"client send: {res=}")
      res2 = await res
      if res2 is None:
        dbg(f"send msg: finally: {res=}")
        return True
      #  elif hasattr(res, "stanza") and res.stanza and res.stanza.error is None:
      #    # 群内私聊
      #    logger.info(f"send gpm msg: finally: {res=}")
      #    return True
      else:
        logger.info(f"send msg: finally: {res=} {res2=}")
        return False
    else:
      warn(f"send msg: res is not coroutine: {res=} {client=} {room=} {msg=}")
    return False


async def send(text, jid=None, *args, **kwargs):
  muc = None
  if 'name' in kwargs:
    name = kwargs["name"]
    #  kwargs.pop("name")
    if name:
      kwargs["name"] = name[2:-4]
    else:
      kwargs["name"] = None
  else:
    name = "**C bot:** "
    kwargs["name"] = name[2:-4]
  if jid is None:
    if isinstance(text, aioxmpp.Message):
      if text.type_ == MessageType.GROUPCHAT:
        muc = str(text.to.bare())
      else:
        pass
    else:
      err(f"需要jid")
      return False
  else:
    muc = jid
  if isinstance(text, aioxmpp.Message):
    text0 = text.body[None]
    text.body[None] = f"{name}{text.body[None]}"
  else:
    text0 = text
    text = f"{name}{text}"
  if muc in my_groups:
    info(f"准备发送同步消息到: {get_mucs(muc)} {text=} {text0=}")
    ms = get_mucs(muc)
    for m in ms:
      if await send1(text, jid=m, *args, **kwargs):
        if isinstance(text, aioxmpp.Message):
          text = text.body[None]
          #  #  text.body[None] = text0
          #  body = text.body
          #  text = aioxmpp.Message(
          #      to=JID.fromstr(text.to),  # recipient_jid must be an aioxmpp.JID
          #      type_=text.type_,
          #  )
          #  text.body = body
        continue
      return False
    if main_group in ms:
      if len(name) > 4:
        await mt_send_for_long_text(text0, name=name[2:-4])
      else:
        await mt_send_for_long_text(text0, name=name)
    return True
  else:
    info(f"准备发送到: {muc=} {jid=}")
    return await send1(text, jid=jid, *args, **kwargs)

async def send1(text, jid=None, client=None, room=None, correct=False, name=None):

  if type(text) is str:
    #  if name:
    #    text = f"{name}{text}"
    if jid is None:
      jid = ME
    else:
      if type(jid) is JID:
        jid = get_jid(jid, True)

      #  if gpm and '/' not in jid:
      #    err(f"无法群私聊，地址错误: {jid}")
      #    return False
    texts = split_long_text(text, 4096)
    for i in texts:
      if jid in my_groups:
        msg = aioxmpp.Message(
            to=JID.fromstr(jid),  # recipient_jid must be an aioxmpp.JID
            type_=MessageType.GROUPCHAT,
        )
      else:
        #  if '/' in jid and jid.split('/', 1)[0] in my_groups:
        msg = aioxmpp.Message(
            to=JID.fromstr(jid),  # recipient_jid must be an aioxmpp.JID
            type_=MessageType.CHAT,
        )
      #  j = get_msg_jid(msg)
      #  if correct:
      #    if j in last_outmsg:
      #      #  msg.xep0308_replace = misc.Replace(last_outmsg[get_jid(msg.to, True)])
      #      r = misc.Replace()
      #      r.id_ = last_outmsg[j]
      #      msg.xep0308_replace = r
      #  else:
      #    if j in last_outmsg:
      #      last_outmsg.pop(j)
      #  if len(texts) > 1:
      #    await add_id_to_msg(msg, False)
      #  else:
      await add_id_to_msg(msg, correct)
      msg.body[None] = i
      if await _send(msg, client, room, name) is not True:
        return False
      if correct:
        break

    return True
  elif isinstance(text, aioxmpp.Message):
    #  logger.info(f"send1: {jid=} {text=}")
    msg = text
    #  if name:
    #    msg.body[None] = f"{name}{msg.body[None]}"
    if msg.type_ == MessageType.GROUPCHAT:
    #    if msg.to.resource is not None:
      if jid is not None:
        msg.to = JID.fromstr(jid)
      if not msg.to.is_bare:
          #  msg.to.resource = None
        #  if '/' in get_jid(msg.to, True):
          #  msg.to = JID.fromstr(get_jid(msg.to))
          #  msg.to = msg.to.replace(resource=None)
        orig = msg.to
        msg.to = msg.to.bare()
        logger.info(f"已修正地址错误: {orig} -> {msg=}")
    #  elif gpm and msg.to.resource is None:
    #    err(f"无法群私聊，地址错误: {msg.to}")
    #    return False

    await add_id_to_msg(msg, correct)

    return await _send(msg, client, room, name)
  else:
    err(f"text类型不对: {type(text)}")
    return False
    #  elif isinstance(text, aioxmpp.stanza.Message):
    #    #  logger.info(f"send2: {jid=} {text=}")
    #    msg = text

#  async def __send(msg, jid=None, client=None, gpm=False):
#    #  if type(text) is str:
#      #  logger.info(f"send: {jid=} {text=}")
#      # None is for "default language"
#    #  logger.info(f"send: {type(msg)} {msg=}")
#    if client is None:
#      client = XB
#    #  return await client.send(msg)
#    return await _send(msg, client, gpm=gpm)

async def sendg(text, jid=None, room=None, client=None, name="**C bot:** "):
  if name:
    text = f"{name}{text}"
  logger.info(f"send group msg: {jid} {text}")
  if jid is None:
    jid = test_group
  recipient_jid = JID.fromstr(jid)
  msg = aioxmpp.Message(
      to=recipient_jid,  # recipient_jid must be an aioxmpp.JID
      type_=aioxmpp.MessageType.GROUPCHAT,
  )
  # None is for "default language"
  msg.body[None] = text

  if room is not None:
    return await _send(msg, room=room)

  if client is None:
    client = XB
  #  return await client.send(msg)
  if client is not None:
    return await _send(msg, client)
    #  res = room.send_message(msg)
    #  # https://docs.zombofant.net/aioxmpp/devel/api/public/muc.html?highlight=room#aioxmpp.muc.Room.send_message
    #  if asyncio.iscoroutine(res):
    #    res = await res
    #    if res is None:
    #      dbg(f"room send: finally: {res=}")
    #      return True
    #    else:
    #      logger.info(f"room send: finally: {res=}")
    #      return False
    #  else:
    #    logger.info(f"room send res is not coroutine: {res=}")
    #    return False
  else:
    warn(f"need client or room")
    return False




@exceptions_handler
async def mt_read():
  # api.xmpp
  MT_API = "127.0.0.1:4247"
  url = "http://" + MT_API + "/api/stream"
  session = await init_aiohttp_session()
  logger.info("start read msg from mt api...")
  while True:
    line = ""
    try:
      #  async with session.get(url, timeout=0, read_bufsize=2**20) as resp:
        #  print("N: mt api init ok")
        #  resp.content.read()
        #  async for line in resp.content:
        #    #  logger.info("I: got a msg from mt api: %s", len(line))
        #    #  print(f"I: original msg: %s" % line)
        #    await mt2tg(line)

      async with session.get(url, timeout=0, read_bufsize=2**18*4, chunked=True) as resp:
        logger.info("N: mt api init ok")
        #  await mt_send("N: tggpt: mt read: init ok")
        line = b""
        async for data, end_of_http_chunk in resp.content.iter_chunks():
          line += data
          #  logger.info(f"read bytes: {len(data)}")
          if end_of_http_chunk:
            #  logger.info(f"read end: {len(line)}")
            # # print(buffer)
            # await send_mt_msg_to_queue(buffer, queue)
            #  await mt2tg(line)
            asyncio.create_task(mt2tg(line))
            line = b""

    except ClientPayloadError:
      logger.warning("mt closed, data lost")
    except ClientConnectorError:
      logger.warning("mt api is not ok, retry...")
    except ValueError as e:
      #  print("W: maybe a msg is lost")
      err(f"{e=}: {line}")
    except Exception as e:
      err(f"{e=}: {line}")
    await asyncio.sleep(3)


#  @exceptions_handler
#  async def titlebot(msgd):
#
#    await asyncio.sleep(5)
#    text = msgd['text']


@exceptions_handler
async def mt2tg(msg):
  '''
  #       Data sent: 'GET /api/stream HTTP/1.1\r\nHost: 127.0.0.1\r\n\r\n'
  #      Data received: 'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nDate: Wed, 19 Jan 2022 02:03:29 GMT\r\nTransfer-Encoding: chunked\r\n\r\nd5\r\n{"text":"","channel":"","username":"","userid":"","avatar":"","account":"","event":"api_connected","protocol":"","gateway":"","parent_id":"","timestamp":"2022-01-19T10:03:29.666861315+08:00","id":"","Extra":null}\n\r\n'
  2024-05-07 17:26:25,343 [INFO] tggpt.bot [bot.info:157]: msg of mt_read: {'text': 'ping', 'channel': 'bebat', 'username': 'X liqsliu_: ', 'userid': 'bebat@muc.pimux.de/liqsliu_', 'avatar': 'https://wtfipfs.eu.org/0789fa8d/bebat_muc_pimux_de_liqsliu_.png', 'account': 'xmpp.pimux', 'event': '', 'protocol': 'xmpp', 'gateway': 'test', 'parent_id': '', 'timestamp': '2024-05-07T17:26:25.22885781+08:00', 'id': '', 'Extra': None}
  2024-05-07 17:26:25,778 [INFO] tggpt.bot [bot.mt_send:1806]: res of mt_send: {"text":"pong. now tasks: 0/0","channel":"api","username":"C bot","userid":"","avatar":"","account":"api.cmdres","event":"","protocol":"api","gateway":"test","parent_id":"","timestamp":"2024-05-07T17:26:25.367596549+08:00","id":"","Extra":null}
  '''
  try:
    try:
        msg = msg.decode()
        if not msg or msg.startswith("HTTP/1.1"):
          logger.info("I: ignore init msg")
          return

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

    account = msgd["account"]
    if account == "api.cmdres":
      logger.info("I: ignore msg from cmdres")
      return
    name = msgd["username"]
    text = msgd["text"]
    gateway = msgd["gateway"]
    if gateway == 'me':
      if text:
        global last_mt_res_jid
        if text.startswith("X "):
          tmp = text.splitlines()[0]
          if ': ' in tmp:
            tmp = tmp.split(': ', 1)[0]
            if ' ' in tmp:
              tmp = tmp.split(' ', 1)[1]
              if tmp in me:
                last_mt_res_jid = tmp
                text = text.split(': ', 1)[1]
        warn(f"reply to {last_mt_res_jid}")
        if last_mt_res_jid:
          await send(text, last_mt_res_jid)
      return

    #  print(f"I: got msg: {name}: {text}")
    if not text:
      logger.info("I: ignore msg: no text")
      return
    if not name:
      logger.info("I: ignore msg: no name")
      return

    #  if name == "C twitter: ":
    #      return
    if name.startswith("C "):
      logger.info("I: ignore msg: C ")
      return
    if name.startswith("X "):
      logger.info("I: ignore msg: X ")
      return
    if name.startswith("**C "):
      logger.info("I: ignore msg: **C ")
      return

    #  if len(username.splitlines()) > 1:
    #    pass
    #  # need fix
    #  if "gateway11" in MT_GATEWAY_LIST:
    #      if gateway == "gateway1":
    #          gateway = "gateway11"

    #  if gateway == "test":
    #    pass
    #  else:
    #    return
    logger.info("msg of mt_read: %s" % msgd)


    global queue
    need_clean = False
    chat_id = gpt_bot

    if gateway not in mtmsgsg:
      mtmsgsg[gateway] = {}
    #  if gateway not in queues:
    #    queues[gateway] = asyncio.PriorityQueue(maxsize=512)
      #  asyncio.create_task(tg2mt_loop(gateway))

    #  if text == "ping":
    #    all = 0
    #    for i in mtmsgsg:
    #      all += len(mtmsgsg[i])
    #    #  await mt_send(f"pong. now tasks: {here}/{all} {mtmsgsg}", gateway=gateway)
    #    here = len(mtmsgsg[gateway])
    #    await mt_send(f"pong. now tasks: {here}/{all}", gateway=gateway)
    #    return

    #  if text.startswith(".py "):
    #    text = "." + text[4:]
    #  if text[0:1] == ".":
    #  if 1 > 2:
    #    if text[1:2] == " ":
    #      return
    #    #  cmds = deque(text[1:].split(' '))
    #    #  cmds = text[1:].split(' ')
    #    cmds = get_cmd(text[1:])
    #    if cmds:
    #      pass
    #    else:
    #      return
    #    #  print(f"> I: {cmds}")
    #    logger.info("got cmds: {}".format(cmds))
    #    cmd = cmds[0]
    #    length = len(cmds)
    #    here = len(mtmsgsg[gateway])
    #    if text == ".gtpmode":
    #      if gateway in gptmode:
    #        gptmode.remove(gateway)
    #        await mt_send("gtp mode off", gateway=gateway)
    #        return
    #      else:
    #        gptmode.append(gateway)
    #        await mt_send("gtp mode on", gateway=gateway)
    #        return
    #    elif text == ".gtg reset":
    #      if allright.is_set():
    #        await mt_send(f"now tasks: {here}, waiting...", gateway=gateway)
    #        #  for g in mtmsgsg:
    #        #  for g in queues:
    #        #    await mt_send(f"clean {g}...", gateway="test")
    #        #    await queues[g].put((0,0,0))
    #        text= CLEAN
    #      else:
    #        await mt_send("waiting...", gateway=gateway)
    #        await allright.wait()
    #        here = len(mtmsgsg[gateway])
    #        await mt_send(f"reset ok, now tasks: {here}", gateway=gateway)
    #        return
    #    #  elif text == ".gpt" or text.startswith(".gpt ") or text.startswith(".gpt\n"):
    #    #  elif text == ".se" or text.startswith(".se "):
    #    elif cmd == "gse":
    #      #  need_clean = True
    #      text = ' '.join(cmds[1:])
    #      if not text:
    #        await mt_send(".gse $text", gateway=gateway)
    #        return
    #      text="/search "+text
    #    #  elif text == ".img" or text.startswith(".img "):
    #    #  elif text.startswith(".gtz"):
    #    elif cmd == "gptr":
    #      #  text=text[6:]
    #      text = ' '.join(cmds[1:])
    #      if not text:
    #        await mt_send("gpt translate with short prompt", gateway=gateway)
    #        return
    #      #  need_clean = True
    #      text = f'{PROMPT_TR_MY_S}“{text}”'
    #
    #    else:
    #      return
    #  elif gateway in gptmode:
    #    pass
    #    return
    #  if gateway in MT_GATEWAY_LIST:
    #      chat_id = MT_GATEWAY_LIST[gateway][0]
    #  else:
    #      # first msg is empty
    #      logger.warning("unkonwon gateway: {}".format(gateway))
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

    logger.info("got msg from mt: {}".format(msgd))
    #      if name == "C Telegram: ":
    if gateway == "gateway1":
      res = await run_cmd(text, gateway, name)
      if res:
        await mt_send(res, gateway)
      await send(f"{name}{text}", main_group, name=name.strip())
      if res:
        await send(f"{name}{res}", main_group)
      #  for m in get_mucs(main_group):
      #    if await send1(f"{name}{text}", m, name) is False:
      #      return
      #    if res:
      #      if await send1(f"{name}{res}", m, "C bot") is False:
      #        return

    return
    if 1 < 2:
      return
    msgd.update({"chat_id": chat_id})
    msgd.update({"text": text})

    #  global chat
    #  if not chat:
    chat = await get_entity(chat_id)
    #  print(f">{chat.user_id}: {text}")
    print(f"I: send {text} to gpt")
    if text != CLEAN:
      if need_clean is True:
        await UB.send_message(chat, CLEAN)

    #    while len(queue.keys()) > 0:
    #      print("W: waiting to reset...")
    #      await asyncio.sleep(1)
    msg = await UB.send_message(chat, text)
    #  await queue.put({msg.id: [msgd, msg]})
    #  await queue.put([msg, msgd])
    if text != CLEAN:
      #  async with queue_lock:
      #  queues[gateway] = {msg.id: [msgd, None]}
      #  if gateway not in nids:
        #  nids[gateway] = msg.id
      gid_src[msg.id] = gateway
      #  mtmsgs[msg.id] = [msgd,None]
      #  if gateway not in mtmsgs:
      #  mtmsgsg[gateway][msg.id] = [msgd, None]
      mtmsgsg[gateway][msg.id] = [msgd]
    else:
      await clear_history()
      here = len(mtmsgsg[gateway])
      all = 0
      for i in mtmsgsg:
        all += len(mtmsgsg[i])
      await mt_send(f"reset ok, now tasks: {here}/{all}", gateway=gateway)
    return

    #  text = name + text
    #  #    await NB.send_message(chat_id, text, reply_to=reply_to)
    #  #    return [0, chat_id, text, {"reply_to":reply_to}]
    #  msg = [0, chat_id, text, {"reply_to": reply_to}]
    #  await queue.put(msg)

  except:
    #  info = "E: " + str(sys.exc_info()[1]) + "\n==\n" + traceback.format_exc() + "\n==\n" + str(sys.exc_info())
    #  logger.error(info)
    logger.error("error: msg from mt to tg: ", exc_info=True, stack_info=True)
    #  await NB.send_message(MY_ID, info)
    await asyncio.sleep(5)



async def send_to_tg_bot(text, chat_id, src=None):
  chat = await get_entity(chat_id)
  msg = await UB.send_message(chat, text)
  gid_src[msg.id] = src
  if src not in mtmsgsg:
    mtmsgsg[src] = {}
  #  mtmsgsg[src][msg.id] = [msg]
  mtmsgsg[src][msg.id] = [None]
  return msg.id




async def clear_history(src=None):
  if not allright.is_set():
    warn("wait for allright...")
    await allright.wait()
    return
  allright.clear()
  #  await asyncio.sleep(1)
  #  for g in queues:
  if src:
    tmp = []
    for i in gid_src:
      if gid_src[i] == src:
        tmp.append(i)
    for i in tmp:
      gid_src.pop(i)

    if src in mtmsgsg:
      ms = mtmsgsg[src]
      ms.clear()
  else:
    for g in mtmsgsg:
      mtmsgs = mtmsgsg[g]
      mtmsgs.clear()
    #  await mt_send(f"cleaned: {mtmsgsg=}", gateway="test")
    gid_src.clear()
    #  await mt_send(f"cleaned: {gid_src=}", gateway="test"):w
  allright.set()
  logger.info("reset ok")






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
        #  raise
        res = f"{e=}"
    async with res:
        # print("All:", res)
#        res.raise_for_status()
        if res.status == 304:
            logger.warning(f"W: http status: {res.status} {res.reason} {res.url=}")
            logger.warning("ignore: {}".format(await res.text()))
            if return_headers:
                return None, res.headers
            else:
                return
        if res.status != 200:
#            logger.error(res)
#            put(str(res))
            #  html = f"E: error http status: {res.status} {res.reason} url: {res.url} headers: {res.headers}"
            html = f"E: error http status: {res.status} {res.reason} url: {res.url}"
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

async def mt_send(*args, **kwargs):
  asyncio.create_task(_mt_send(*args, **kwargs))
  return True

#  async def mt_send(text="null", name="bot", gateway="test", qt=None):
async def _mt_send(text="null", gateway="gateway1", name="C bot", qt=None):

  # api.xmpp
  MT_API_RES = "127.0.0.1:4247"
  #  if gateway == 'me':
  #    # api.xmpp
  #    MT_API_RES = "127.0.0.1:4247"
  #  else:
  #    # api.cmdres
  #    MT_API_RES = "127.0.0.1:4249"
  # send msg to matterbridge
  url = "http://" + MT_API_RES + "/api/message"

  #nc -l -p 5555 # https://mika-s.github.io/http/debugging/2019/04/08/debugging-http-requests.html
  #  url="http://127.0.0.1:5555/api/message"

#  if not username.startswith("C "):
#    username = "T " + username

  if qt:
    username = "{}\n\n{}".format("> " + "\n> ".join(qt.splitlines()), name)
#  gateway="gateway0"
  data = {
    "text": "{}".format(text),
    "username": "{}".format(name),
    "gateway": "{}".format(gateway)
  }
  res = await http(url, method="POST", json=data)
  logger.info("res of mt_send: {}".format(res))
  return True
  return res

#  async def mt_send_for_long_text(text, gateway='test'):
#    fn='gpt_res'
#    async with queue_lock:
#      async with aiofiles.open(f"{SH_PATH}/{fn}", mode='w') as file:
#        await file.write(text)
#      #  os.system(f"{SH_PATH}/sm4gpt.sh {fn} {gateway}")
#      return await asyncio.to_thread(os.system, f"{SH_PATH}/sm4gpt.sh {fn} {gateway}")

async def mt_send_for_long_text(text, gateway="gateway1", name="C bot", *args, **kwargs):
  async with mt_send_lock:
    need_delete = False
    if os.path.exists(f"{SH_PATH}"):
      fn = f"{SH_PATH}/SM_LOCK_{gateway}"
      for _ in range(5):
        if os.path.exists(fn):
          logger.info(f"busy: {gateway} {fn}")
          await asyncio.sleep(2)
        else:
          break

      await write_file(text, fn, "w")
      need_delete = True

    for i in split_long_text(text):
      #  if await send(i, *args, **kwargs) is not True:
      if await mt_send(i, gateway=gateway, name=name, *args, **kwargs) is not True:
        break
      #  await mt_send(res, gateway=gateway, name="")
      name = ""

    if need_delete:
      os.remove(fn)

  return True





#  @exceptions_handler
#  @UB.on(events.NewMessage(outgoing=True))
#  async def my_event_handler(event):
#    #  if 'hello' in event.raw_text:
#    #    await event.reply('hi!')
#    #  if 'new_chat' in event.raw_text:
#    #    print(event.stringify())
#    msg = event.message
#    text = msg.raw_text
#    if event.chat_id != gpt_bot:
#      if debug:
#        print("<%s %s" % (event.chat_id, text))
#      return
#    if event.chat_id != gpt_bot:
#      if debug:
#        print(">%s %s" % (event.chat_id, text))
#      return
#    if text:
#      print("me: %s" % text)



last_time = {}

async def download_media(msg, src='gateway1', path=f"{DOWNLOAD_PATH}/", in_memory=False):
#  await client.download_media(message, progress_callback=callback)
  async with downlaod_lock:

    if msg.file and msg.file.name:
      res = f"{msg.file.name}"
    else:
      res = ''
    if msg.buttons:
      logger.info(msg.buttons)
      for i in get_buttons(msg.buttons):
        if isinstance(i.button, KeyboardButtonUrl):
          logger.info(f"add url from: {i}")
          res += f" {i.url}"
        else:
          logger.info(f"ignore button: {i}")
    #  await mt_send(f"{res} 下载中...", gateway=gateway)
    await send(f"{res} 下载中...", src, correct=True)
    last_time[src] = time.time()

    # Printing download progress
    def download_media_callback(current, total):
      print('Downloaded', current, 'out of', total,
        'bytes: {:.2%}'.format(current / total))
      if time.time() - last_time[src] > 5:
        #  await mt_send("{:.2%} %s/%s".format(current / total, current, total), gateway=gateway)
        #  asyncio.create_task(mt_send("{:.2%} {}/{} bytes".format(current / total, current, total), gateway=gateway))
        asyncio.create_task(send("{:.2%} {}/{} bytes".format(current / total, current, total), src, correct=True))
        last_time[src] = time.time()

    path = await msg.download_media(path, progress_callback=download_media_callback)
    if path:
      return path
    else:
      warn(f"下载失败: {path}")
      #  await mt_send(f"下载失败: {path}", gateway=gateway)
      await send(f"下载失败: {path}", src)




def get_buttons(bs):
  tmp = []
  for i in bs:
    if type(i) is list:
      tmp += i
    else:
      tmp.append(i)
  return tmp

async def get_entity(peer):
  #  if isinstance(peer, PeerUser):
  #    #  logger.info(f"PeerUser: {peer}")
  #    peer = await UB.get_input_entity(peer)
  #  elif isinstance(peer, PeerChat):
  #    #  logger.info(f"PeerChat: {peer}")
  #    peer = await UB.get_input_entity(peer)
  #  elif isinstance(peer, PeerChannel):
  #    #  logger.info(f"PeerChannel: {peer}")
  #    peer = await UB.get_input_entity(peer)
  #  elif isinstance(peer, str):
  #    peer = await UB.get_input_entity(peer)
  #  else:
  peer = await UB.get_input_entity(peer)
  if peer:
    entity = await UB.get_entity(peer)
    return entity
  raise ValueError(f"无法获取chat信息: {peer}")



async def print_msg(event):
  msg = event.message
  res = ''
  if event.is_private:
    res += "@"
    #  peer = await get_entity(event.chat_id)
    peer = await event.get_chat()
    if peer is not None:
      res += " [%s %s]" % (peer.first_name, peer.last_name)
  else:
    if event.is_group:
      res += "+"
    else:
      #  if event.is_channel:
      res += "#"

    #  peer = await get_entity(event.chat_id)
    peer = await event.get_chat()
    if peer is not None:
      res += " %s" % peer.title
    if event.from_id:
      #  peer = await get_entity(event.from_id)
      peer = await event.get_sender()
      if peer is not None:
        if isinstance(peer, User):
          res += " [%s %s]" % (peer.first_name, peer.last_name)
        else:
        #  if isinstance(peer, Channel):
          res += " [# %s]" % peer.title
  if msg.text:
    res += ": %s" % msg.text.splitlines()[0][:64]
  else:
    res += ": "
  if msg.file:
    res += " %s" % msg.file
    if msg.file.name:
      res += " %s" % msg.file.name
  print(res)



music_bot_state = {}


@exceptions_handler
async def parse_msg(event):
  msg = event.message
  
  #  if event.chat_id not in id2gateway:
  #    #  print("W: skip: got a unknown: chat_id: %s\nmsg: %s" % (event.chat_id, msg.stringify()))
  #    return
  #  if event.chat_id in id2gateway:
  if event.chat_id == gpt_bot:
    pass

  elif event.chat_id == music_bot:
    #  print("I: music bot: chat_id: %s\nmsg: %s" % (event.chat_id, msg.stringify()))
    if msg.is_reply:
      pass
    else:
      return
    #  try:
    qid=msg.reply_to_msg_id
    if qid not in gid_src:
      logger.error(f"E: not found src for {qid=}, {gid_src=} {msg.text=}")
      return
    text = msg.text
    if not text:
      print(f"W: skip msg without text in chat with gpt bot, wtf: {msg.stringify()}")
      return
    
    if text == '等待下载中...':
      #   message='等待下载中...',
      logger.info(text)
      return
    if text == '正在获取歌曲信息...':
      #         message='正在获取歌曲信息...',
      logger.info(text)
      return
    if text == '搜索中...':
      #         message='搜索中...',
      logger.info(text)
      return
    if text.endswith('正在发送中...'):
      # message='大熊猫\n专辑: 火火兔儿歌\nflac 14.87MB\n命中缓存, 正在发送中...',
      logger.info(text)
      return
    if '中...' in text:
      #         message='搜索中...',
      warn(f"已忽略疑似临时消息: {text}", False)
      return

    src = gid_src[qid]
    mtmsgs = mtmsgsg[src]
    if music_bot_state[src] == 1:
      logger.info(msg.buttons)
      #  logger.info(f"找到了几个音乐:{len(msg.buttons)} {msg.text}")

      music_bot_state[src] += 1

      #  logger.info(f"{mtmsgs[qid]}搜索结果(回复序号)\n{text}")
      res = f"{mtmsgs[qid][0]}搜索结果(回复序号)\n{text}"
      #  await mt_send_for_long_text(res, src)
      await send(res, src)

      gid_src[msg.id] = src
      mtmsgs[qid].append(msg.buttons)
      mtmsgs[msg.id] = mtmsgs[qid]
      gid_src.pop(qid)
      mtmsgs.pop(qid)

    elif music_bot_state[src] == 2:
      warn(f"不应该出现: music bot: {gid_src=} {music_bot_state[src]}\nmsg:\n{msg.stringify()}")
      gid_src.pop(qid)
      mtmsgs.pop(qid)
      return
    elif msg.file and music_bot_state[src] == 3:
      path = await download_media(msg, src)
      if path is not None:
        #  path = "https://%s/%s" % (DOMAIN, path.lstrip(DOWNLOAD_PATH))
      #  req = request.Request(url=url, data=parse.urlencode(data).encode('utf-8'))
        path = "https://%s/%s" % (DOMAIN, (parse.urlencode({1: path.lstrip(DOWNLOAD_PATH)})).replace('+', '%20')[2:])
      res = f"{mtmsgs[qid][0]}{path}\n{text}"
      if msg.buttons:
        for i in get_buttons(msg.buttons):
          #  if isinstance(i, KeyboardButtonUrl):
          if isinstance(i.button, KeyboardButtonUrl):
            res += f"\n原始链接: {i.url}"
      #  await mt_send_for_long_text(res, gateway)
      await send(res, src)
      if music_bot_state[src] == 3:
        music_bot_state[src] -= 1
    else:
      warn(f"未知状态，已忽略: music bot: {gid_src=} {music_bot_state[src]}\nmsg:\n{msg.stringify()}")
      return


    #  except Exception as e:
    #    err(f"fixme: music bot: {gid_src=} {e=} line: {e.__traceback__.tb_lineno}")

    return

  elif event.chat_id == rss_bot:
    async with rss_lock:
      #  await mt_send(msg.text, "C rss2tg_bot", id2gateway[rss_bot])
      #  await mt_send_for_long_text(msg.text, id2gateway[rss_bot])
      await send(msg.text, rss_channel, name="")
      await asyncio.sleep(5)
    return
    #  print("N: skip: %s != %s" % (event.chat_id, gpt_bot))
  else:
    #  print("W: skip unknown chat_id: %s %s" % (event.chat_id, msg.text[:64]))
    await print_msg(event)
    return


  if msg.is_reply:
    qid=msg.reply_to_msg_id
    print(f"tg msg id: {msg.id=} {event.id=} {qid=}")
    if qid not in gid_src:
      logger.error(f"E: not found src for {qid=}, {gid_src=} {msg.text=}")
      return
    #  await queues[gid_src[qid]].put( (id(msg), qid, msg) )
    #  await queues[gid_src[qid]].put( (msg.date, qid, msg) )
    #  await queues[gid_src[qid]].put( (msg.id, "test") )
    #  await queues[gid_src[qid]].put( (id(msg), qid, msg) )
    if msg.file:
      return
    text = msg.text
    if not text:
      print(f"W: skip msg without text in chat with gpt bot, wtf: {msg.stringify()}")
      return
    print(f"tg msg: {text}: {msg.id=} {event.id=} {qid=} {gid_src=} {mtmsgsg=}")
    l = text.splitlines()
    if l[-1] in loadings:
      return
    elif len(l) > 1 and f"{l[-2]}\n{l[-1]}" in loadings:
      return
    else:
      src = gid_src[qid]
      mtmsgs = mtmsgsg[src]
      res = f"{mtmsgs[qid][0]}{text}"
      #  await mt_send_for_long_text(res, src)
      await send(res, src)
      gid_src.pop(qid)
      mtmsgs.pop(qid)

    #  except Exception as e:
    #    err(f"fixme: {qid=} {gid_src=} {queues=} {e=} line: {e.__traceback__.tb_lineno}")
      #  raise e
    return
    await queues[gid_src[qid]].put( (msg.id, msg, qid) )
    return


    #  gateway = None
    #  if qid in set(nids.values()):
    #    for gateway in nids:
    #      if qid == nids[gateway]:
    #        break
    #  else:
    #    for gateway in queues:
    #      if qid in set(queues[gateway]):
    #        break
    #      gateway = None
    #  if gateway is None:
    #    print("W: skip: got a msg with a unkonwon id: all: %s\n queue: %s" % (msg.stringify(), queues))
    #    return
    #  nid = nids[gateway]
    #  queue = queues[gateway]
    #  is_loading= True
  else:
    print("W: skip: got a msg without reply: is_reply: %s\nmsg: %s" % (msg.is_reply, msg.stringify()))
    return


@exceptions_handler
async def parse_out_msg(event):
  if event.chat_id == MY_ID:
    msg = event.message
    text = msg.text
    if not text:
      return
    if text == 'id':
      await UB.send_message('me', "id @name https://t.me/name")
      return
    if text.startswith("id "):
      url = text.split(' ')[1]
      if url.startswith("https://t.me/"):
        username = url.split('/')[3]
      elif url.startswith("@"):
        username = url[1:]
      else:
        await UB.send_message('me', "error url")
        return

      e = await UB.get_entity(username)
      if e:
        await UB.send_message('me', f"{e.stringify()}")
        await UB.send_message('me', "peer id: %s" % await UB.get_peer_id(e))
      else:
        await UB.send_message('me', "not fount entity")
        e = await UB.get_input_entity(username)
        if e:
          await UB.send_message('me', f"{e.stringify()}")
          await UB.send_message('me', "peer id: %s" % await UB.get_peer_id(e))
        else:
          await UB.send_message('me', "not fount input entity")



#  @UB.on(events.NewMessage(incoming=True))
#  @UB.on(events.MessageEdited(incoming=True))
#  @exceptions_handler
#  async def read_res(event):
#
#    if not allright.is_set():
#      return
#    #  if event.chat_id in id2gateway:
#    if event.chat_id == gpt_bot:
#      pass
#    elif event.chat_id == rss_bot:
#      msg = event.message
#      await mt_send(msg.text, id2gateway[rss_bot], "rss2tg_bot")
#      return
#      #  print("N: skip: %s != %s" % (event.chat_id, gpt_bot))
#    else:
#      return
#    #  if not allright.is_set():
#    #    print("W: skiped the msg because of reset is waiting")
#    #    return
#    #  elif event.chat_id not in gid_src:
#    #    logger.error(f"E: not found gateway for {event.chat_id}, {gid_src=}")
#    #    return
#    msg = event.message
#
#    if msg.is_reply:
#      qid=msg.reply_to_msg_id
#      print(f"msg id: {msg.id=} {event.id=} {qid=} {gid_src=} {mtmsgsg=}")
#      if qid not in gid_src:
#        logger.error(f"E: not found gateway for {qid=}, {gid_src=} {msg.text=}")
#        return
#      try:
#        #  await queues[gid_src[qid]].put( (id(msg), qid, msg) )
#        #  await queues[gid_src[qid]].put( (msg.date, qid, msg) )
#        await queues[gid_src[qid]].put( (id(msg), qid, msg) )
#        #  await queues[gid_src[qid]].put( (msg.id, "test") )
#      except Exception as e:
#        logger.info(f"E: fixme: {qid=} {gid_src=} {queues=} {e=}")
#        #  raise e
#      return
#      await queues[gid_src[qid]].put( (msg.id, msg, qid) )
#      return



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

def get_jid(i, full=False):
  if full:
    if i.resource:
      return f"{i.localpart}@{i.domain}/{i.resource}"
    else:
      return f"{i.localpart}@{i.domain}"
  else:
    return f"{i.localpart}@{i.domain}"

async def stop(client=None):
  if client is None:
    if 'XB' in globals():
      client = XB
    else:
      return
  jid = get_jid(client.local_jid)
  if client.running:
    logger.info(f"开始断开账户: {jid}")
    client.stop()
    while True:
      if client.running:
        logger.info(f"等待断开账户: {jid}")
        await asyncio.sleep(0.5)
      else:
        logger.info(f"已断开: {jid}")
        break
  else:
    logger.info(f"已离线: {jid}")



async def get_disco(jid, client=None):
  if client is None:
    client = XB
  #  for i in my_groups:
  #    jid = i
  #    break
  jid = test_group.rsplit('@', 1)[1]
  dc = client.summon(aioxmpp.DiscoClient)
  res = await dc.query_info(JID.fromstr(jid))
  pprint(res)
  print(jid, res.to_dict())



async def regisger_handler(client):
#  class FooService(aioxmpp.service.Service):
#    feature = aioxmpp.disco.register_feature(
#      "some:namespace"
#    )
#
#    #  @aioxmpp.service.depsignal(aioxmpp.DiscoServer, "on_info_changed")
#    #  def handle_on_info_changed(self):
#    #    pass
#
#    #@aioxmpp.dispatcher.message_handler(aioxmpp.MessageType.CHAT, None)
#    @aioxmpp.service.depsignal(aioxmpp.MUCClient, "on_message")


#  @aioxmpp.dispatcher.message_handler(aioxmpp.MessageType.GROUPCHAT, None)
#  async def gmsg_in(msg):
#    logger.info("\n>> group msg: %s\n" % msg)

  #  # obtain an instance of the service (we’ll discuss services later)
  message_dispatcher = client.summon(
     #  aioxmpp.dispatcher.SimpleMessageDispatcher
     dispatcher.SimpleMessageDispatcher
  )
  # register a message callback here
  #  message_dispatcher.register_callback(
  #      aioxmpp.MessageType.CHAT,
  #      None,
  #      msg_in,
  #  )
  message_dispatcher.register_callback(
      #  aioxmpp.MessageType.GROUPCHAT,
      None,
      None,
      msg_in,
  )
  #  message_dispatcher.register_callback(
  #      aioxmpp.MessageType.NORMAL,
  #      None,
  #      msg_in,
  #  )

  #  MUC = i.summon(aioxmpp.MUCClient)
  #  MUC.on_message.connect(gmsg)
  #  i.stream.register_message_callback(aioxmpp.MessageType.GROUPCHAT, None, gmsg_in)
  #  i.stream.register_message_callback(aioxmpp.MessageType.CHAT, None, msg_in)

  presence_dispatcher = client.summon(
     #  aioxmpp.dispatcher.SimpleMessageDispatcher
     dispatcher.SimplePresenceDispatcher
  )
  presence_dispatcher.register_callback(
      None,
      None,
      msg_in,
  )

#  client.stream.register_iq_request_handler(
#      aioxmpp.IQType.GET,
#      aioxmpp.disco.xso.InfoQuery,
#      request_handler,
#  )

  #  async def request_handler(request):
  #      print("request_handler: %s" % request)
  #
  #  client.stream.register_iq_request_handler(
  #      aioxmpp.IQType.GET,
  #      aioxmpp.disco.xso.InfoQuery,
  #      request_handler,
  #  )

  from aioxmpp.version.xso import Query

  async def handler(iq):
      print("software version request from {!r}".format(iq.from_))
      result = Query()
      result.name = "bot"
      result.version = ":)"
      result.os = "by liqsliu"
      return result

  client.stream.register_iq_request_handler(
      aioxmpp.IQType.GET,
      Query,
      handler,
  )

  #  pprint(client.stream)
  #  pprint(client.stream.service_outbound_message_filter)
  #  return
  #  client.stream.service_outbound_messages_filter = stream.AppFilter()
  #  client.stream.service_outbound_message_filter.register(msg_out, 1)
  client.stream.app_outbound_message_filter.register(msg_out, 1)


last_outmsg = {}


def get_msg_jid(msg):
  if msg.type_ == MessageType.GROUPCHAT:
    jid = get_jid(msg.to)
  elif msg.type_ == MessageType.CHAT:
    jid = get_jid(msg.to)
    if jid in my_groups:
      jid = get_jid(msg.to, True)
  else:
    return
  return jid

def clear_msg_jid(msg):
  j = get_msg_jid(msg)
  if j in last_outmsg:
    last_outmsg.pop(j)
    logger.info(f"已清除msg记录: {j}")
  else:
    logger.info(f"没找到msg记录: {j}")


async def add_id_to_msg(msg, correct):
  j = get_msg_jid(msg)
  if correct:
    if j in last_outmsg:
      #  msg.xep0308_replace = misc.Replace(last_outmsg[get_jid(msg.to, True)])
      for _ in range(5):
        if last_outmsg[j][1]:
          last_outmsg[j][0] = msg
          r = misc.Replace()
          r.id_ = last_outmsg[j][1]
          msg.xep0308_replace = r
          break
        else:
          logger.info("msg id 不可用: {last_outmsg[j][1]}")
          await asyncio.sleep(1)
      if last_outmsg[j][1] is None:
        last_outmsg[j] = [msg, None]
    else:
      last_outmsg[j] = [msg, None]
      logger.info("已添加msg")
  else:
      #  last_outmsg.pop(j)
    if j in last_outmsg:
      #  msg.xep0308_replace = misc.Replace(last_outmsg[get_jid(msg.to, True)])
      for _ in range(5):
        if last_outmsg[j][1]:
          last_outmsg[j][0] = msg
          r = misc.Replace()
          r.id_ = last_outmsg[j][1]
          msg.xep0308_replace = r
        else:
          logger.info("msg id 不可用: {last_outmsg[j][1]}")
          await asyncio.sleep(1)
      if last_outmsg[j][1] is None:
        last_outmsg[j] = [msg, None]
      last_outmsg[j].append(0)

def get_mucs(muc):
  for s in sync_groups_all:
    if muc in s:
      return s
  return set([muc])




@exceptions_handler
def msg_out(msg):
  if not allright.is_set():
    logger.info("skip msg: allright is not ok: {msg.from_}: {msg.body}")
    return
  #  pprint(msg)
  j = get_msg_jid(msg)
  if j in last_outmsg:
    if last_outmsg[j][0] == msg:
      if len(last_outmsg[j]) > 2 and last_outmsg[j][2] < 1:
        logger.info(f"停止记录msg id: {msg.id_}")
        last_outmsg.pop(j)
      else:

        logger.info(f"更新msgid: {last_outmsg[j][1]} -> {msg.id_}")
        last_outmsg[j][1] = msg.id_
    else:
      logger.info(f"msg不匹配: {last_outmsg[j][0]=} != {msg=}")
      last_outmsg.pop(j)
  else:
    logger.debug(f"忽略: {msg=}")
  return msg


#  def gmsg(msg, member, source, **kwargs):
def msg_in(msg):
  if not allright.is_set():
    logger.info("skip msg: allright is not ok")
    return
  #  if hasattr(msg, "xep0203_delay"):
  #    pprint(msg.xep0203_delay)
  #    logger.info("skip msg: delayed: {msg.xep0203_delay}")
  #  if hasattr(msg, "xep308_replace"):
  #    pprint(msg.xep308_replace)
  asyncio.create_task(parse_xmpp_msg(msg))
  #  return
  #  logger.info("\n>>> msg: %s\n" % msg)





@exceptions_handler
async def parse_xmpp_msg(msg):
  if not hasattr(msg, "body"):
    #  print("%s %s" % (type(msg), msg.type_))
    if msg.type_ == PresenceType.SUBSCRIBE:
      #  pprint(msg)
      log(f"状态订阅请求：{msg.from_}")
      if get_jid(msg.from_) in me:
        rc = XB.summon(aioxmpp.RosterClient)
        #  pprint(rc)
        res = rc.approve(msg.from_)
        #  print(f"结果：{res}")
        res = rc.subscribe(msg.from_)
        #  print(f"结果：{res}")
        await send("ok", msg.from_)
      else:
        await send("not allowed", msg.from_)
    elif msg.type_ == PresenceType.AVAILABLE:
      pprint(msg)
      print(f"上线: {msg.from_} {msg.status}")
    elif msg.type_ == PresenceType.UNAVAILABLE:
      print(f"离线: {msg.from_} {msg.status}")
    else:
      pprint(msg)
    return

  if msg.xep0203_delay:
    print("跳过旧消息%s %s %s %s %s %s" % (msg.type_, msg.id_,  str(msg.from_), msg.to, msg.body, msg.xep0203_delay))
    return
  if msg.type_ == MessageType.NORMAL:
    logger.info("normal msg")
  if msg.type_ == MessageType.GROUPCHAT:
    pass
  elif msg.type_ == MessageType.CHAT:
    pass
  elif msg.type_ == MessageType.ERROR:
    warn(f"收到错误消息：{msg} {msg.error}")
  else:
    pprint(msg)
    logger.info(f"skip msg type: {msg.type_} {msg}")
    return

  #  clear_msg_jid(msg)

  text = None
  for i in msg.body:
    text = msg.body[i]
    break
  if text is None:
    #  print("跳过空消息: %s %s %s %s" % (msg.type_, msg.from_, msg.to, msg.body))
    return

  muc = str(msg.from_.bare())

  #  if text == "ping":
  #    #  await send("pong", ME)
  #    if msg.type_ == MessageType.GROUPCHAT:
  #
  #      nick = msg.from_.resource
  #      ms = get_mucs(muc)
  #      for m in ms - {muc}:
  #        if await send1(f"**X {nick}:** {text}", m) is False:
  #          return
  #      if main_group in ms:
  #        if await mt_send(text, name=f"X {nick}") is False:
  #          return
  #
  #      #  pprint(msg.from_)
  #      #  await sendg("pong1")
  #      #  await sendg("pong2", get_jid(msg.from_))
  #      await send("pong", msg.from_, gpm=True)
  #      reply = msg.make_reply()
  #      reply.body[None] = "pong"
  #      await send(reply)
  #      #  await mt_send("pong")
  #    elif msg.type_ == MessageType.CHAT:
  #
  #      reply = msg.make_reply()
  #      reply.body[None] = "pong"
  #      await send(reply)
  #    return


  is_admin = False
  if muc in my_groups:
    #  if str(msg.from_) == str(rooms[muc].me.conversation_jid.bare()):
    if msg.from_.resource == rooms[muc].me.nick:
      #  print("跳过自己发送的消息%s %s %s %s %s" % (msg.type_, msg.id_,  str(msg.from_), msg.to, msg.body))
      return
    if msg.type_ == MessageType.CHAT:
      if muc not in rooms:
        err("not found room: {muc}")
        return
      room = rooms[muc]
      for i in room.members:
        if i.direct_jid is None:
          err("没有权限查看jid: {muc}")
          return
        if i.nick == msg.from_.resource and (i.direct_jid.bare()) in me:
          is_admin = True
          break
      if is_admin is False:
        if text == "ping":
          reply = msg.make_reply()
          reply.body[None] = "pong"
          await send(reply)
        logger.info("已忽略群内私聊: %s" % msg)
        return
  elif muc == myjid:
    #  print("跳过自己发送的消息%s %s %s %s %s" % (msg.type_, msg.id_,  str(msg.from_), msg.to, msg.body))
    return
  elif muc in me:
    is_admin = True
    pass
  else:
    print("未知来源的消息%s %s %s %s %s" % (msg.type_, msg.id_,  str(msg.from_), msg.to, msg.body))
    if text == "ping":
      reply = msg.make_reply()
      reply.body[None] = "pong"
      await send(reply)
    return
    #  pprint(msg)

  print("%s %s %s %s %s" % (msg.type_, msg.id_,  str(msg.from_), msg.to, msg.body))
  if msg.type_ == MessageType.GROUPCHAT:
    nick = msg.from_.resource
    ms = get_mucs(muc)
    for m in ms - {muc}:
      if await send1(f"**X {nick}:** {text}", m, name=f"X {nick}") is False:
        return
    if main_group in ms:
      if await mt_send_for_long_text(text, name=f"X {nick}") is False:
        return
    if muc == acg_channel:
      await send(text, rssbot, name="")
      return
  else:
    if muc == rssbot:
      await send(text, acg_channel, name="")
      return
    if get_jid(msg.to) in my_groups:
      nick = msg.from_.resource
    else:
      nick = msg.from_.localpart
  res = await run_cmd(text, get_src(msg), f"X {nick}: ", is_admin)
  if res is True:
    return
  if res:
    reply = msg.make_reply()
    reply.body[None] = res
    await send(reply)
    return

  if get_jid(msg.from_) not in me:
    return
  #  awai:t mt_send(text, 'me', get_jid(msg.from_))
  if text == "disco":
    await get_disco(get_jid(msg.from_))
  elif text == "test":
    logger.setLevel(logging.DEBUG)
    reply = msg.make_reply()
    reply.body[None] = "ok"
    await send(reply)
  elif text == "ok":
    log(f"got a msg: ok")
  elif text == "correct":
    reply = msg.make_reply()
    reply.body[None] = generand(3)
    await send(reply, correct=True)
  #  elif text == "correct":
  #    pprint(msg.xep308_replace)

  #  pprint(msg)
  return
  print(">>>> %s << %s" % (msg.body, msg))
  src = msg.from_
  text = msg.body



cmd_funs = {}
cmd_for_admin = set()

async def add_cmd():

  async def _(cmds, src):
    return "pong"
  cmd_funs["ping"] = _

  async def _(cmds, src):
    if len(cmds) == 1:
      return f"添加好友\n.{cmds[0]} $jid"
    rc = XB.summon(aioxmpp.RosterClient)
    #  pprint(rc)
    res = rc.subscribe(JID.fromstr(cmds[1]))
    #  print(f"结果：{res}")
    await send(f"结果：{res}", src)
    await asyncio.sleep(1)
    res = rc.approve(JID.fromstr(cmds[1]))
    #  print(f"结果：{res}")
    await send(f"结果：{res}", src)
  cmd_funs["connect"] = _
  cmd_for_admin.add('connect')

  async def _(cmds, src):
    if len(cmds) == 1:
      rc = XB.summon(aioxmpp.RosterClient)
      return "items: %s" % rc.items
    elif cmds[1] == "json":
      rc = XB.summon(aioxmpp.RosterClient)
      return "json:\n%s" % rc.export_as_json()
    #  else:
    #    #  pc = XB.summon(aioxmpp.PresenceClient)
    #    #  res = XB.get_most_available_stanza(cmds[1])
    #    return res
  cmd_funs["list"] = _
  cmd_for_admin.add('list')

  async def _(cmds, src):
    if len(cmds) == 1:
      return f"阿里千问\n.{cmds[0]} $text"
    text = ' '.join(cmds[1:])
    return await qw(text)
  cmd_funs["qw"] = _



  async def _(cmds, src):
    if len(cmds) == 1:
      return f"阿里千问\n{cmds[0]} $text"
    text = ' '.join(cmds[1:])
    return await qw2(text)
  cmd_funs["qw2"] = _


  async def _(cmds, src):
    if len(cmds) == 1:
      return f"音乐下载\n.{cmds[0]} $text\n.{cmds[0]} clear\n--\ntelegram bot: https://t.me/{music_bot_name}"
    if cmds[1] == "clear":
      await clear_history()
      return "ok"
    text = ' '.join(cmds[1:])
    music_bot_state[src] = 1
    text="/search "+text
    mid = await send_to_tg_bot(text, music_bot, src)
    return 1, mid
  cmd_funs["music"] = _

  async def _(cmds, src):
    if len(cmds) == 1:
      return f"gpt bot\n.{cmds[0]} $text\n--\n所有数据来自telegram机器人: https://t.me/littleb_gptBOT"
    text = ' '.join(cmds[1:])
    mid = await send_to_tg_bot(text, gpt_bot, src)
    return 1, mid
  cmd_funs["gtg"] = _


  async def _(cmds, src):
    if len(cmds) == 1:
      return f"gpt(telegram bot) translate\n.{cmds[0]} $text\n--\n所有数据来自telegram机器人: https://t.me/littleb_gptBOT"
    text = ' '.join(cmds[1:])
    text = f'{PROMPT_TR_MY}“{text}”'
    mid = await send_to_tg_bot(text, gpt_bot, src)
    return 1, mid
  cmd_funs["gtr"] = _

  async def _(cmds, src):
    if len(cmds) == 1:
      return f"gpt(telegram bot) translate 中文专用翻译\n.{cmds[0]} $text\n--\n所有数据来自telegram机器人: https://t.me/littleb_gptBOT"
    text = ' '.join(cmds[1:])
    text = f'{PROMPT_TR_ZH}“{text}”'
    mid = await send_to_tg_bot(text, gpt_bot, src)
    return 1, mid
  cmd_funs["gtz"] = _

  async def _(cmds, src):
    if len(cmds) == 1:
      return f"gemini 图像生成(仅支持英文)\n.{cmds[0]} $text"
    text = ' '.join(cmds[1:])
    return await ai_img(text)
  cmd_funs["img"] = _

  async def _(cmds, src):
    if len(cmds) == 1:
      return f"HuggingChat\n.{cmds[0]} $text\n\n--\nhttps://github.com/xtekky/gpt4free\n问答: hg/di/lb/kl/you/bd/ai"
    text = ' '.join(cmds[1:])
    return await hg(text, provider=Provider.HuggingChat)
  cmd_funs["hg"] = _

  async def _(cmds, src):
    if len(cmds) == 1:
      return f"DeepInfra\n.{cmds[0]} $text"
    text = ' '.join(cmds[1:])
    return  await ai(text, provider=Provider.DeepInfra)
  cmd_funs["di"] = _

  async def _(cmds, src):
    if len(cmds) == 1:
      return f"Liaobots\n.{cmds[0]} $text"
    text = ' '.join(cmds[1:])
    return await ai(text, provider=Provider.Liaobots)
  cmd_funs["lb"] = _

  async def _(cmds, src):
    if len(cmds) == 1:
      return f"Liaobots\n.{cmds[0]} $text"
    text = ' '.join(cmds[1:])
    return await ai(text, provider=Provider.Koala, proxy="http://127.0.0.1:6080")
  cmd_funs["kl"] = _

  async def _(cmds, src):
    if len(cmds) == 1:
      return f"You\n.{cmds[0]} $text\n\n--\nhttps://github.com/xtekky/gpt4free\n问答: hg/di/lb/kl/you/bd/ai"
    text = ' '.join(cmds[1:])
    return await ai(text, provider=Provider.You, proxy="http://127.0.0.1:6080")
  cmd_funs["you"] = _

  async def _(cmds, src):
    i = 0
    for g in mtmsgsg:
      i += 1
      for j in mtmsgsg[g]:
        i += 1
    for g in gid_src:
      i += 1
    ii = i

    if cmds[1] == "all":
      await clear_history()
    else:
      await clear_history(src)
    i = 0
    for g in mtmsgsg:
      i += 1
      for j in mtmsgsg[g]:
        i += 1
    for g in gid_src:
      i += 1
    #  return "ok {ii} -> {i}"
    return f"清除状态\n.{cmds[0]} all\n--\n{ii} -> {i}"
  cmd_funs["clear"] = _


async def run_cmd(text, src, name="test", is_admin=False):
  if text[0:1] == ".":
    if text[1:2] == " ":
      return
    cmds = get_cmd(text[1:])
    if cmds:
      pass
    else:
      return
    #  print(f"> I: {cmds}")
    logger.info("got cmds: {}".format(cmds))
    cmd = cmds[0]
    res = False
    if cmd in cmd_for_admin:
      if is_admin is False:
        return
      res = True
    elif cmd in cmd_funs:
      res = True
    if res is True:
      res = await cmd_funs[cmd](cmds, src)
      if type(res) is tuple:
        if res[0] == 1:
          mtmsgsg[src][res[1]][0] = name
        return True
      if res:
        return res
      else:
        return True
      #  reply = msg.make_reply()
      #  reply.body[None] = "%s" % res
      #  await send(reply)
      #  return True
    else:
      res = await send_cmd_to_bash([src, name, text])
      if res:
        return res
  elif text.isnumeric() and music_bot_state[src] == 2:
    mtmsgs = mtmsgsg[src]
    tmp = []
    for i in gid_src:
      if gid_src[i] == src:
        tmp.append(i)
    qid = max(tmp)
    logger.info(f"尝试下载：{text} {qid}")
    bs = mtmsgs[qid][1]
    logger.info(f"尝试下载：{text} {qid} msg: {bs}")
    i = None
    for i in get_buttons(bs):
      #  if type(i) is list:
      #    for j in i:
      #      if j.text == text:
      #        logger.info(f"已找到：{text}")
      #        await j.click()
      #        i = True
      #        break
      #    if i is True:
      #      break
      #  else:
        if i.text == text:
          logger.info(f"已找到：{text}")
          await i.click()
          i = True
          break

    if i is True:
      music_bot_state[src] += 1
    else:
      logger.info(f"没找到：{text}")
    return
  else:
    # tilebot
    res = await send_cmd_to_bash([src, name, text])
    if res:
      return res
    tmp=""
    for i in text.splitlines():
      if not i.startswith("> ") and  i != ">":
        tmp += i+"\n"
    urls=urlre.findall(qre.sub("", tmp))
    res=None
    #  M=' 🔗 '
    #  M='- '
    #  M=' ⤷ '
    for url in urls:
      #  url=url[0]
      url=url[1]
      if url.startswith("https://t.me/"):
        return
      if url.startswith("https://conversations.im/j/"):
        return
      if url.startswith("https://icq.im"):
        return
      if not res:
        if len(urls) == 1:
          res="%s" % await get_title(url)
          break
        res="[ %s urls ]" % len(urls)
      res+="\n\n> %s\n%s" % (url, await get_title(url))
    if res:
      return name + res
      #  await mt_send(res, gateway=gateway, name="titlebot")

  return False






@exceptions_handler
async def login(client=None):
  if client is None:
    client = XB
  jid = get_jid(client.local_jid)
  logger.info(f"登录中: {jid}")
  try:
    #  steam = await i.connected().__aenter__()
    steam = await asyncio.wait_for(client.connected().__aenter__(), timeout=30)
    logger.info(f"登录成功：{jid}")

    vs = client.summon(aioxmpp.vcard.VCardService)
    vc = await vs.get_vcard(None)
    if vc.get_photo_mime_type() is None:
    #  if True:
      #  fn = WORK_DIR / "photo.png"
      fn = WORK_DIR / "w.png"
      fn = fn.as_posix()
      #  fn = 'tx.jpg'
      data = await read_file(fn, 'rb')
      #  vc.set_photo_data('image/jpeg', data)
      vc.set_photo_data('image/png', data)
      await vs.set_vcard(vc)
      await asyncio.sleep(1)
      vc = await vs.get_vcard(None)
      if vc.get_photo_mime_type() is not None:
        logger.info(f"头像设置成功: {jid} {fn}")
        #  logger.warning(f"修改头像需要重新登录才能生效：{jid}")
        #  await stop(client)
        #  if await login(client, True):
        #    #  n = fn.split("@", 1)[1].split('_', 1)[1].rsplit('.', 1)[0]
        #    #  mynicks.add((jid, n))
        #    logger.info(f"头像设置成功: {jid} {fn}")
        #    return True
        #  else:
        #    return False
      else:
        logger.warning(f"头像设置失败：{jid}")
    else:
      logger.info(f"无需设置头像：{jid}")


    await regisger_handler(client)

  except TimeoutError as e:
    warn(f"登录失败(超时)：{jid}, {e=}")
    await stop(client)
    return False
  except Exception as e:
    warn(f"登录失败：{jid}, {e=}")
    await stop(client)
    return False

  return True




ocr_ok = None

def ocr_init():
  global ocr_ok
  ocr_ok = []
  logger.info("开始初始化ocr")
  #  if 'liqsliu' not in HOME:
  if os.path.exists("%s/ddddocr" % HOME):
    sys.path.append("%s/ddddocr" % HOME)
    import ddddocr
    ocr = ddddocr.DdddOcr()
    def f(img):
      logger.info("正在运行识别程序：ddddocr")
      return ocr.classification(img)
    ocr_ok.append(f)
  if os.path.exists("%s/ddddocr" % HOME):
    sys.path.append("%s/muggle/muggle-ocr-1.0.3" % HOME)
    import muggle_ocr
    sdk = muggle_ocr.SDK(model_type=muggle_ocr.ModelType.Captcha)
    def f(img):
      logger.info("正在运行识别程序：muggle_ocr")
      return sdk.predict(image_bytes=img)
    ocr_ok.append(f)
  if ocr_ok is None:
    logger.info("没找到orc程序，将会无法识别验证码")
    return False

def run_ocr(img):
  if ocr_ok is None:
    if ocr_init() is False:
      return
  elif ocr_ok == []:
    for _ in range(5):
      logger.info("等待orc初始化")
      time.sleep(5)
      if ocr_ok:
        break
    if ocr_ok == []:
      logger.info("等待orc初始化超时")
      return
  f = None
  try:
    while True:
      f = random.choice(ocr_ok)
    #  for f in ocr_ok:
      s = f(img)
      if s:
        logger.info(f" 识别结果: {s}")
        return s
      else:
        logger.info(f" 识别失败: {s}")
  except Exception as e:
    warn(f"识别程序出现错误 {f=} {e=}")



def jbypass(msg):
  #  logger.warn(f"无法进群: {msg}")
  asyncio.create_task(_bypass(msg))

async def _bypass(msg):
  """
  body: <class 'aioxmpp.structs.LanguageMap'>: {<aioxmpp.structs.LanguageTag.fromstr('en')>: 'Your subscription request and/or messages to kvpxdg0u68wq4tae@conference.conversations.im have been blocked. To unblock your subscription request, visit https://xmpp.conversations.im/captcha/8977672564368233645'}

  https://xmpp.conversations.im/captcha/12941499225798303289/image
  --
	curl 'https://suchat.org:5443/captcha/7412684044252318043/image' \
		-H 'Accept: image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8' \
		-H 'Accept-Language: zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6' \
		-H 'Connection: keep-alive' \
		-H 'Referer: https://suchat.org:5443/captcha/7412684044252318043' \
		-H 'Sec-Fetch-Dest: image' \
		-H 'Sec-Fetch-Mode: no-cors' \
		-H 'Sec-Fetch-Site: same-origin' \
		-H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36' \
		-H 'sec-ch-ua: "Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"' \
		-H 'sec-ch-ua-mobile: ?0' \
		-H 'sec-ch-ua-platform: "Windows"'
  ==

	curl 'https://suchat.org:5443/captcha/13773455620261259216' \
		-H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7' \
		-H 'Accept-Language: zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6' \
		-H 'Cache-Control: max-age=0' \
		-H 'Connection: keep-alive' \
		-H 'Content-Type: application/x-www-form-urlencoded' \
		-H 'Origin: https://suchat.org:5443' \
		-H 'Referer: https://suchat.org:5443/captcha/13773455620261259216' \
		-H 'Sec-Fetch-Dest: document' \
		-H 'Sec-Fetch-Mode: navigate' \
		-H 'Sec-Fetch-Site: same-origin' \
		-H 'Sec-Fetch-User: ?1' \
		-H 'Upgrade-Insecure-Requests: 1' \
		-H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36' \
		-H 'sec-ch-ua: "Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"' \
		-H 'sec-ch-ua-mobile: ?0' \
		-H 'sec-ch-ua-platform: "Windows"' \
		--data-raw 'id=13773455620261259216&key=427617&enter=OK'

	--
	<?xml
	version='1.0'?>
	<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
	<html xmlns='http://www.w3.org/1999/xhtml' xml:lang='en' lang='en'>
			<head>
					<meta http-equiv='Content-Type' content='text/html; charset=utf-8'/>
			</head>
			<body>
					<p>验证码有效。</p>
			</body>
	</html>

  --
  e=XMPPAuthError("{urn:ietf:params:xml:ns:xmpp-stanzas}not-authorized ('The CAPTCHA verification has failed')")

  """
  #  pprint(request)
  #  pprint(request.xep0004_data)
  #  pprint(request.xso_serialise_to_sax())
  #  pprint(request.body)
  #  pprint(request.body.get(aioxmpp.structs.LanguageTag.fromstr('en')))
  #  pprint(request.body.get(aioxmpp.structs.LanguageTag.fromstr('zh')))

  #  pprint(msg.body.any())
  #  return
  if msg.body.get(aioxmpp.structs.LanguageTag.fromstr('zh')):
    text = msg.body.get(aioxmpp.structs.LanguageTag.fromstr('zh'))
  elif msg.body.get(aioxmpp.structs.LanguageTag.fromstr('en')):
    text = msg.body.get(aioxmpp.structs.LanguageTag.fromstr('en'))
  else:
    text = msg.body.any()

  jid = get_jid(msg.from_)
  myid = get_jid(msg.to)

  if text:
    tmp = []
    for u in urlre.findall(text):
      tmp.append(u[1])
    if tmp == []:
      warn("需要验证才能入群，但无法输入验证码，没找到URL: {myid} {jid} {text}")
      return
    else:
      logger.info(f"需要验证才能入群: {myid} {jid} {text} {tmp}")
  else:
    logger.info(f"fixme: 这个群需要验证才能进吗？那就程序有bug: {myid} {jid} {text}")
    return

  u = None
  for u in tmp:
    #  if jid.split('@', 1)[1] in u:
    if msg.from_.domain in u:
      break
    u = None
  if u is None:
    logger.info(f"没找到合适的，随便选第一个作为验证码地址: {jid} {tmp}")
    u = tmp[0]
  logger.info(f"验证码地址: {u}")
  #  logger.info(f"验证码地址: {u=}")
  headers = {
      #  'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
      'Accept': 'image/jpeg,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
      'Accept-Language': 'zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6',
      'Connection': 'keep-alive',
    }

  #  res = await http(f"{u}")
  res = await http(f"{u}", headers=headers, proxy="http://127.0.0.1:6080")
  print(res)
  headers['Referer'] = u
  iu = f"{u}/image"
  res = await http(f"{iu}", headers=headers, proxy="http://127.0.0.1:6080")
  #  res = await http("https://fars.ee/eUVh.jpg")
  logger.info(f"image size: {len(res)} {iu}")
  #  print("===")
  #  s = ocr.classification(res)
  s = await asyncio.to_thread(run_ocr, img=res)
  if s:
    await asyncio.sleep(3)
		#  -H 'Origin: https://suchat.org:5443' \
		#  --data-raw 'id=13773455620261259216&key=427617&enter=OK'
    data = {
        "id": "%s" % u.rsplit('/', 1)[1],
        "key": f"{s}",
        "enter": "OK",
        }
    headers.pop('Referer')
    headers['Origin'] = "%s//%s" % (u.split('//', 1)[0], u.split('//', 1)[1].split('/', 1)[0])
    headers['Accept'] = 'application/json,application/xhtml+xml,application/xml,text/html;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
    logger.info(f"headers: {headers}")
    logger.info(f"data: {data}")
    res = await http(f"{u}", "POST", headers=headers, data=data, proxy="http://127.0.0.1:6080")
    logger.info(res)
    #  while True:
    #    logger.info(f"等待进群结果: {myid} {jid}")
    #    await asyncio.sleep(3)
    #    if jid in muc_now:
    #      if myid in muc_now[jid]:
    #        break
  else:
    #  pprint(s)
    logger.info(f"识别验证码失败: {myid} {jid} {s}")




#  test_group = 'ipfs@salas.suchat.org'
rooms = {}
auto_input = False

@exceptions_handler
async def join(jid=None, nick=None, client=None):
  if jid is None:
    jid = test_group
  if nick is None:
    #  if "wtf" in myjid:
    #    nick = 'bot'
    #  else:
    #    nick = 'liqsliu_bot'
    nick = 'bot'
  if client == None:
    client = XB

  global mucsv
  if "mucsv" not in globals():
    mucsv = client.summon(aioxmpp.MUCClient)
  J = JID.fromstr(jid)

  #  client.stream.register_iq_request_handler(
  #  try:
  #    client.stream.unregister_message_callback(
  #        aioxmpp.MessageType.NORMAL,
  #        None,
  #    )
  #  except KeyError as e:
  #    pass

  if auto_input:
    client.stream.register_message_callback(
    #  stream.message_handler(client.stream,
        aioxmpp.MessageType.NORMAL,
        J,
    #      #  None,
        jbypass,
    )

  myid = get_jid(client.local_jid)
  #  client.stream.on_message_received.connect(bypass)
  try:
    sum_try = 0
    while True:
      try:
        room, fut = mucsv.join(J, nick=nick, autorejoin=True)
        #  if fut is not None and room.muc_joined is False:
        if room.muc_joined is False:
          logger.info(f"等待进群: {get_jid(client.local_jid)} {jid}")

          await fut
          logger.info(f"进群成功: {myid} {jid}")
        else:
          pass
        rooms[jid] = room
        return room
      
      except TimeoutError as e:
        #  logger.warning(f"进群超时(废弃): {jid} {muc} {e=}")
        warn(f"进群超时(废弃){sum_try}: {myid} {jid} {nick} {e=}")
      except errors.XMPPCancelError as e:
        # XMPPCancelError("{urn:ietf:params:xml:ns:xmpp-stanzas}remote-server-not-found ('Server-to-server connection failed: No route to host')")
        if e.args[0] == "{urn:ietf:params:xml:ns:xmpp-stanzas}remote-server-not-found ('Server-to-server connection failed: No route to host')" or e.args[0].startswith("{urn:ietf:params:xml:ns:xmpp-stanzas}remote-server-not-found"):
          logger.info(f"进群失败, 网络问题{e.args}: {myid} {jid} {e=}")
          return False
        elif e.args[0] == "{urn:ietf:params:xml:ns:xmpp-stanzas}conflict ('That nickname is already in use by another occupant')" or e.args[0] == '{urn:ietf:params:xml:ns:xmpp-stanzas}conflict' or '{urn:ietf:params:xml:ns:xmpp-stanzas}conflict' in e.args[0]:
          if '_' in nick:
            nick = f"{nick}%s" % generand(1)
          else:
            nick = f"{nick}_%s" % generand(1)
          logger.warning(f"群名字冲突{sum_try}: {myid} {jid} {nick} {e=}")
        else:
          logger.info(f"进群失败{e.args}: {myid} {jid} {e=}")
          return False
      except errors.XMPPAuthError as e:
        #  pprint(e.args)
        #  if e.args == ("{urn:ietf:params:xml:ns:xmpp-stanzas}not-authorized ('The CAPTCHA verification has failed')", ):
        if e.args:
          if e.args[0] == "{urn:ietf:params:xml:ns:xmpp-stanzas}not-authorized ('The CAPTCHA verification has failed')" or e.args[0].startswith("{urn:ietf:params:xml:ns:xmpp-stanzas}not-authorized"):
            if auto_input is False:
              return False
            logger.info(f"进群失败, 验证码不正确，准备重试: {myid} {jid} {e=}")
          else:
            if e.args[0] == '{urn:ietf:params:xml:ns:xmpp-stanzas}forbidden':
              logger.info(f"进群失败，被ban了(forbiden): {myid} {jid} {e=}")
            elif e.args[0] == "{urn:ietf:params:xml:ns:xmpp-stanzas}forbidden ('You have been banned from this room')" or e.args[0].startswith("{urn:ietf:params:xml:ns:xmpp-stanzas}forbidden"):
              logger.info(f"进群失败，被ban了: {myid} {jid} {e=}")
            else:
              logger.info(f"进群失败{e.args}: {myid} {jid} {e=}")
            return False
        else:
          logger.info(f"进群失败(无权限): {myid} {jid} {e=}")
          return False
      except Exception as e:
        logger.info(f"进群失败: {myid} {jid} {e=}")
        return False
      sum_try += 1
      if sum_try > 3:
        logger.info(f"进群失败(重试次数达到最大值): {myid} {jid}")
        return False
      await asyncio.sleep(0.1)

  finally:
    if auto_input:
      client.stream.unregister_message_callback(
          aioxmpp.MessageType.NORMAL,
          J,
      )
  return False


@exceptions_handler
async def xmppbot():
  logger.info("开始登录xmpp")
  global XB, myjid
  myjid = get_my_key("JID")
  logger.info(f"bot jid: {myjid}")
  password = get_my_key("JID_PASS")
  #  jid = aioxmpp.JID.fromstr(jid)
  XB = aioxmpp.PresenceManagedClient(
      JID.fromstr(myjid),
      aioxmpp.make_security_layer(password)
  )
  logger.info(f"已导入新账户: {myjid} password: {password[:4]}...")
  if await load_config():
    if await login():
      logger.info(f"join all groups...\n%s" % my_groups)
      #  await join()
      global mucsv
      #  mucsv = client.summon(aioxmpp.MUCClient)
      ms = my_groups
      while True:
        #  await join(test_group)
        #  break
        tmp = []
        for i in ms:
          if await join(i):
            continue
          tmp.append(i)
        if tmp:
          logger.info(f"无法进入的群组: {tmp}")
          await mt_send_for_long_text(f"无法进入的群组: {tmp}")
          ms = tmp
          await asyncio.sleep(5)
        else:
          break

  global allright_task
  allright_task -= 1



#  @exceptions_handler
async def amain():
  try:
    if len(sys.argv) > 1:
      #  if sys.argv[1] == '1':
      if sys.argv[1].isnumeric():
        pass
      elif sys.argv[1] == 'cmd':
        res = await my_popen(' '.join(sys.argv[2:]))
        print(res)
      elif sys.argv[1] == 'cmd2':
        res = await send_cmd_to_bash(["gateway1", "X test", ' '.join(sys.argv[2:])])
        print(res)
      return

    global loop
    loop = asyncio.get_event_loop()
    global allright_task
    allright_task += 1
    asyncio.create_task(xmppbot(), name="xmppbot")
    #  allright_task += 1
    #  asyncio.create_task(other_init())

    # with UB:
    #  loop.run_until_complete(run())

    #  LOGGER.addFilter(NoParsingFilter())

    # https://stackoverflow.com/questions/17275334/what-is-a-correct-way-to-filter-different-loggers-using-python-logging
    for handler in logging.root.handlers:
      #  handler.addFilter(logging.Filter('foo'))
      #  handler.addFilter(NoParsingFilter())
      f = NoParsingFilter()
      handler.addFilter(f)
      logger.info(f"added filter to: {handler}")


    global MY_NAME, MY_ID, UB


    api_id = int(get_my_key("TELEGRAM_API_ID"))
    api_hash = get_my_key("TELEGRAM_API_HASH")

    from telethon import TelegramClient
    #  client = TelegramClient('anon', api_id, api_hash)
    #  UB = TelegramClient('%s/.ssh/%s.session' % (HOME, "telegram_userbot"), api_id, api_hash, proxy=("socks5", '172.23.176.1', 6084), loop=loop)

    global UB
    #  global loop
    #  loop = asyncio.get_event_loop()
    #  UB = TelegramClient('%s/.ssh/%s.session' % (HOME, "telegram_userbot"), api_id, api_hash, loop=loop)
    UB = TelegramClient('%s/.ssh/%s.session' % (HOME, "telegram_userbot"), api_id, api_hash)

    del api_id
    del api_hash
    #  del bot_token


    @UB.on(events.NewMessage(incoming=True))
    @UB.on(events.MessageEdited(incoming=True))
    async def _(event):
      if not allright.is_set():
        logger.info("skip msg: allright is not ok")
        return
      asyncio.create_task(parse_msg(event))

    @UB.on(events.NewMessage(outgoing=True))
    async def _(event):
      if not allright.is_set():
        logger.info("skip msg: allright is not ok")
        return
      asyncio.create_task(parse_out_msg(event))

    #  await UB.start()
    async with UB:
      me = await UB.get_me()
      #  print(me.stringify())
      MY_ID = me.id
      MY_NAME = me.username
      print(f"{MY_NAME}: {MY_ID}")

      UB.parse_mode = 'md'

      global SH_PATH, DOMAIN
      SH_PATH = (await read_file()).rstrip('\n')
      DOMAIN = (await read_file("DOMAIN")).rstrip('\n')
      print(f"SH_PATH: {SH_PATH}")
      print(f"DOMAIN: {DOMAIN}")



      await add_cmd()
      while True:
        if allright_task > 0:
          logger.info(f"等待初始化完成，剩余任务数：{allright_task}")
          await asyncio.sleep(3)
          continue
        allright.set()
        break
      logger.info(f"初始化完成")

      #  await mt_send("gpt start")
      asyncio.create_task(mt_read(), name="mt_read")

      await UB.run_until_disconnected()

    logger.info("主程序正常结束")
  #  except KeyboardInterrupt as e:
  #    logger.info("I: 手动终止")
  #    #  raise e
  #  except SystemExit as e:
  #    raise e
  #  except Exception as e:
  #    logger.error("error: stop...", exc_info=True, stack_info=True)
  #    raise e
  finally:
    logger.info("正在收尾...")
    await stop()
    #  loop.run_until_complete(stop())
    #  loop.run_until_complete(loop.shutdown_asyncgens())
    #  loop.close()
    logger.info("正在退出...")




def main():
  try:

    #  with UB:
    #    UB.loop.run_until_complete(amain())
    asyncio.run(amain())
  except KeyboardInterrupt as e:
    logger.info("停止原因：用户手动终止")
    sys.exit(1)
  except SystemExit as e:
    logger.warning(f"捕获到systemexit: {e=}", exc_info=True, stack_info=True)
    sys.exit(2)
  except Exception as e:
    logger.error(f"出现未知异常: 正在停止运行...{e=}", exc_info=True, stack_info=True)
    sys.exit(5)
    raise e


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
  #  asyncio.create_task(_init())

