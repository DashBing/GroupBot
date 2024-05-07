import logging
from pathlib import Path
from logging.handlers import TimedRotatingFileHandler
from sys import stdout, stderr, exit



WORK_DIR = Path(__package__).absolute()
PARENT_DIR = WORK_DIR.parent

# logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.WARNING)

LOG_FILE = PARENT_DIR / 'last_run.log'
LOG_FILE = WORK_DIR / 'last_run.log'
# LOG_FORMAT = "[%(levelname)s] %(asctime)s %(name)s [%(module)s.%(funcName)s:%(lineno)d]: %(message)s"
# LOG_FORMAT = "%(asctime)s [%(levelname)s] [%(module)s.%(funcName)s:%(lineno)d]: %(message)s"
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s [%(module)s.%(funcName)s:%(lineno)d]: %(message)s"
FORMATTER: logging.Formatter = logging.Formatter(LOG_FORMAT)

LOGGER = logging.getLogger()
logger=LOGGER

debug = False
debug = True

class NoParsingFilter(logging.Filter):
  def filter(self, record):
    #  if record.name == 'tornado.access' and record.levelno == 20:
    if record.levelno == 20:
      if record.name == 'httpx':
        #  pprint(record)
        #  print("{%s}" % record.getMessage())
        msg = record.getMessage()
        #  if record.message == 'HTTP Request: GET https://qwen-qwen1-5-72b-chat.hf.space/--replicas/3kh1x/heartbeat/f6f9ef32-4cc6-470e-9bfb-957b4bc6ff5d "HTTP/1.1 404 Not Found"':
        #  if msg == 'HTTP Request: GET https://qwen-qwen1-5-72b-chat.hf.space/--replicas/3kh1x/heartbeat/f6f9ef32-4cc6-470e-9bfb-957b4bc6ff5d "HTTP/1.1 404 Not Found"':
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
    else:
      return True
      if record.levelno == 20:
        return True
        if record.message == 'HTTP Request: GET https://qwen-qwen1-5-72b-chat.hf.space/--replicas/3kh1x/heartbeat/f6f9ef32-4cc6-470e-9bfb-957b4bc6ff5d "HTTP/1.1 404 Not Found"':
          logger.info(f"找到了文本，name不对: {record}")
          return False
        if '404 Not Found' in record.message:
           logger.info(f"根据关键词找到了文本，name不对: {record}")
           return False
    return True

LOGGER.addFilter(NoParsingFilter())


if debug:
  logging.basicConfig(format=LOG_FORMAT)
  LOGGER.setLevel(logging.INFO)
  OUT = None
  ERR = None


  #  OUT = logging.StreamHandler(stdout)
  #  OUT.setFormatter(FORMATTER)
  #  OUT.setLevel(logging.INFO)
  #  #  OUT.setLevel(logging.WARNING)
  #  OUT.addFilter(NoParsingFilter())
  #
  #  LOGGER.addHandler(OUT)
else:
  logging.basicConfig(filename=str(LOG_FILE), filemode='w', format=LOG_FORMAT)

  handler = TimedRotatingFileHandler(LOG_FILE, when="d", interval=1, backupCount=3)
  handler.setFormatter(FORMATTER)
  #  handler.setLevel(logging.ERROR)
  handler.setLevel(logging.WARNING)
  LOGGER.addHandler(handler)
  del handler

  OUT = logging.StreamHandler(stdout)
  OUT.setFormatter(FORMATTER)
  OUT.setLevel(logging.INFO)
  #  OUT.setLevel(logging.WARNING)
  LOGGER.addHandler(OUT)

  ERR = logging.StreamHandler(stderr)
  ERR.setFormatter(FORMATTER)
  #  ERR.setLevel(logging.WARNING)
  ERR.setLevel(logging.ERROR)
  LOGGER.addHandler(ERR)

  # LOGGER.setLevel(logging.DEBUG)
  LOGGER.setLevel(logging.WARNING)
#  LOGGER.setLevel(logging.ERROR)




#  import pyrogram
#  from pyrogram import enums
#
#  from . import config
#  CONFIG = config.CONFIG

import os
os.environ['EVENTLET_NO_GREENDNS'] = 'yes'

HOME = os.environ.get("HOME")


#  def get_my_key(key, path=f"{HOME}/.ssh/private_keys.txt"):
def get_my_key(key, path=f"{HOME}/vps/private_keys.txt"):
  # key value
  # key value
  # key value
  path2 = "private_keys.txt"
  if os.path.isfile(path2):
    path = path2
  with open(path) as f:
    line = f.readline()
    while line:
      if len(line.split(' ', 1)) == 2 and line.split(' ', 1)[0] == key:
        f.close()
        return line.split(' ', 1)[1].rstrip('\n')
        break
      line = f.readline()
  LOGGER.error("wtf", exc_info=True)
  #  return None;
  exit(1)


#  exit(0)
# __ALL__ = ["WORK_DIR", "PARENT_DIR", "CMD", "LOGGER", "debug", "OUT", "ERR", "asyncio", "config", "UB", "loop", "MY_NAME", "NB", "BOT_ID", "BOT_NAME", "UB2_ID"]

