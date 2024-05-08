
#!/usr/bin/python
# -*- coding: UTF-8 -*-

import logging
logger = logging.getLogger(__name__)

from functools import wraps
import asyncio

def exceptions_handler(func):

    if asyncio.iscoroutinefunction(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                return _exceptions_handler(e)

    else:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
               return  _exceptions_handler(e)
    return wrapper



def _exceptions_handler(e, *args, **kwargs):
  try:
    res = f'{e=} line: {e.__traceback__.tb_next.tb_lineno}'
    raise e
  except KeyboardInterrupt:
    logger.info("W: 用户手动终止")
    raise
  except SystemExit as e:
    logger.warning(f"W: systemexit: {e=}")
    raise
  except RuntimeError as e:
    logger.warning(f"W: {e=} line: {e.__traceback__.tb_lineno}")
    raise
  except AttributeError as e:
    logger.warning(f"W: {repr(e)} line: {e.__traceback__.tb_lineno}", exc_info=True, stack_info=True)
    return f"{e=}"
  except Exception as e:
    print(res)
    print(f"W: {repr(e)} line: {e.__traceback__.tb_next.tb_next.tb_lineno}")
    logger.error(f"W: {repr(e)} line: {e.__traceback__.tb_lineno}", exc_info=True, stack_info=True)
    return f"{e=}"





@exceptions_handler
def t():
  raise ValueError


t()
