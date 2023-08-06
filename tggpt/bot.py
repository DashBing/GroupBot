
#!/usr/bin/python
# -*- coding: UTF-8 -*-


from . import *  # noqa: F403


import logging

from telethon import events




logger = logging.getLogger(__name__)


@UB.on(events.NewMessage)
async def my_event_handler(event):
  #  if 'hello' in event.raw_text:
  #    await event.reply('hi!')
  if 'new_chat' in event.raw_text:
    print(event.stringify())



