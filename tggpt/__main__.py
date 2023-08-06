#!/usr/bin/python
# -*- coding: UTF-8 -*-
from . import *  # noqa: F403


logger = logging.getLogger(__name__)







async def run():
  global MY_NAME, MY_ID, UB
  UB = await UB.start()
  me = await UB.get_me()
  print(me.stringify())
  MY_ID = me.id
  print(me.id)
  MY_NAME = me.username

  from .bot import mt_read
  #  asyncio.create_task(mt_read(MSG_QUEUE), name="mt_read")
  asyncio.create_task(mt_read(), name="mt_read")


  logger.warning("init ok, loop...")
  #  from pyrogram import idle
  #  if "idle" in locals():
  #    await idle()
  await UB.run_until_disconnected()


def main():
  try:
    # with UB:
    LOOP.run_until_complete(run())
  except KeyboardInterrupt as e:
    raise e
  except SystemExit as e:
    raise e
  except Exception as e:
    logger.error("error: stop...", exc_info=True, stack_info=True)
    raise e


if __name__ == '__main__':
  print('{} 作为主程序运行'.format(__file__))
  logger.debug("test debug")
  logger.info("test info")
  logger.warning("test warn")
  logger.error("test err")
  main()
else:
  print('{} 运行 :('.format(__file__))
