
#!/usr/bin/python
# -*- coding: UTF-8 -*-


from . import *  # noqa: F403


import logging

from telethon import events




logger = logging.getLogger(__name__)




@UB.on(events.NewMessage(outgoing=True))
async def my_event_handler(event):
  #  if 'hello' in event.raw_text:
  #    await event.reply('hi!')
  #  if 'new_chat' in event.raw_text:
  #    print(event.stringify())
  if event.chat_id != gpt_id:
    return
  msg = event.message
  text = msg.raw_text
  if text:
    print("< %s" % text)



@UB.on(events.NewMessage(incoming=True))
async def my_event_handler(event):
  #  if 'hello' in event.raw_text:
  #    await event.reply('hi!')
  #  if 'new_chat' in event.raw_text:
  #    print(event.stringify())
  if event.chat_id != gpt_id:
    return
  msg = event.message
  text = msg.raw_text
  if text:
    print("> %s" % text)


@UB.on(events.MessageEdited(incoming=True))
async def my_event_handler(event):
  #  if 'hello' in event.raw_text:
  #    await event.reply('hi!')
  #  if 'new_chat' in event.raw_text:
  #    print(event.stringify())
  if event.chat_id != gpt_id:
    return
  msg = event.message
  text = msg.raw_text
  if text:
    print("> %s" % text)




