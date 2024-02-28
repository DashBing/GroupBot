#!/usr/bin/python
# -*- coding: UTF-8 -*-
from . import *  # noqa: F403


logger = logging.getLogger(__name__)


async def run():
  #  from . import init
  await init()

  from . import bot
  #  from .bot import mt_read
  #  asyncio.create_task(mt_read(MSG_QUEUE), name="mt_read")
  asyncio.create_task(bot.mt_read(), name="mt_read")


  logger.warning("init ok, loop...")
  #  from pyrogram import idle
  #  if "idle" in locals():
  #    await idle()
  await UB.run_until_disconnected()


def main():
  try:
    # with UB:
    loop.run_until_complete(run())
  except KeyboardInterrupt as e:
    logger.info("I: 手动终止")
    #  raise e
  except SystemExit as e:
    raise e
  except Exception as e:
    logger.error("error: stop...", exc_info=True, stack_info=True)
    raise e
  finally:
    loop.run_until_complete(loop.shutdown_asyncgens())
    loop.close()


if __name__ == '__main__':
  print('{} 作为主程序运行'.format(__file__))
  logger.debug("test debug")
  logger.info("test info")
  logger.warning("test warn")
  logger.error("test err")
  main()
else:
  print('{} 运行 :('.format(__file__))
