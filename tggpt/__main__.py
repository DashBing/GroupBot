#!/usr/bin/python
# -*- coding: UTF-8 -*-
from . import *  # noqa: F403
import sys
import asyncio
#  loop = asyncio.get_event_loop()

#  async def _init():

#loop.run_until_complete(init())
#  if loop.is_running():
#    LOGGER.error("loop running...")
#  else:
#    LOGGER.error("loop stoped...")
#
#  if loop.is_closed():
#    LOGGER.error("loop closed, this may be a error")


logger = logging.getLogger(__name__)


async def init():
  global MY_NAME, MY_ID, UB
  api_id = int(get_my_key("TELEGRAM_API_ID"))
  api_hash = get_my_key("TELEGRAM_API_HASH")

  from telethon import TelegramClient
  #  client = TelegramClient('anon', api_id, api_hash)
  UB = TelegramClient('%s/.ssh/%s.session' % (HOME, "telegram_userbot"), api_id, api_hash, loop=loop)
  #  UB = TelegramClient('%s/.ssh/%s.session' % (HOME, "telegram_userbot"), api_id, api_hash, proxy=("socks5", '172.23.176.1', 6084), loop=loop)
  #  del api_id
  #  del api_hash
  #  del bot_token


  MY_ID = int(get_my_key("TELEGRAM_MY_ID"))
  await UB.start()
  me = await UB.get_me()
  #  print(me.stringify())
  MY_ID = me.id
  MY_NAME = me.username
  print(f"{MY_NAME}: {MY_ID}")
  logger.warning("init ok, loop...")


async def _amain():
  #  from . import init
  await init()

  from . import bot
  await bot._init()
  #  from .bot import mt_read
  #  asyncio.create_task(mt_read(MSG_QUEUE), name="mt_read")

  #  from pyrogram import idle
  #  if "idle" in locals():
  #    await idle()
  await UB.run_until_disconnected()


async def amain():
  try:
    # with UB:
    #  loop.run_until_complete(run())
    global loop
    loop = asyncio.get_event_loop()
    await _amain()

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
    #  loop.run_until_complete(loop.shutdown_asyncgens())
    #  loop.close()
    logger.info("正在退出...")

def main():
  try:
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
  logger.debug("test debug")
  logger.info("test info")
  logger.warning("test warn")
  logger.error("test err")
  main()
elif __package__ == "":
  print('{} 运行, empty package'.format(__file__))
else:
  print('{} 运行, package: {}'.format(__file__, __package__))
