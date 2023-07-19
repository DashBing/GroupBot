
from lxml import etree
import prof
#  import subprocess
#
#
#  def _cmd_ascii(text):
#      proc = subprocess.Popen(['figlet', '--', text], stdout=subprocess.PIPE)
#      ascii_out = proc.communicate()[0].decode('utf-8')
#      recipient = prof.get_current_recipient()
#      room = prof.get_current_muc()
#      if recipient:
#          prof.send_line(u'\u000A' + ascii_out)
#      elif room:
#          prof.send_line(u'\u000A' + ascii_out)
#      elif prof.current_win_is_console():
#          prof.cons_show(u'\u000A' + ascii_out)



#  def prof_init(version, status, account_name, fulljid):
#      synopsis = [ "/ascii <message>" ]
#      description = "ASCIIfy a message."
#      args = [
#          [ "<message>", "The message to be ASCIIfied" ]
#      ]
#      examples = [
#          "/ascii \"Hello there\""
#      ]
#
#      prof.register_command("/ascii", 1, 1, synopsis, description, args, examples, _cmd_ascii)

from time import time

msgs={}

enable = False

# 1s
slow_mmode=1


# max length of a msg
max_length=64







def _reply(barejid, message):
  prof.send_line('/win '+barejid)
  prof.send_line(message)

def prof_pre_chat_message_display(barejid, resource, message):
  prof.cons_show("I: before user msg: "+message)
  if message:
    if message == '.ab' or message[0:4] == '.ab ':
      prof.send_line('/win '+barejid)
      _auto_ban(message[1:].split(' '))
  return None

#  def prof_post_chat_message_display(barejid, resource, message):
#    prof.cons_show("I: after user msg: "+message)

def prof_pre_priv_message_display(barejid, nick, message):
  prof.cons_show("I: before priv msg: "+message)
  if message:
    if message == '.ab' or message[0:4] == '.ab ':
      prof.send_line('/win '+barejid)
      _auto_ban(message[1:].split(' '))
  return None

#  def prof_post_priv_message_display(barejid, nick, message):
#    prof.cons_show("I: after priv msg: "+message)


def prof_pre_room_message_display(barejid, nick, message):
  prof.cons_show("I: before group msg: "+message)
  #  if message == ".ab ping":
  #    prof.cons_show("I: ping")
  #    prof.send_line('pong from xmppbot')
  if message:
    if message == '.ab' or message[0:4] == '.ab ':
      prof.send_line('/win '+barejid)
      _auto_ban(message[1:].split(' '))
  return None

#  def prof_post_room_message_display(barejid, nick, message):
#    prof.cons_show("I: after group msg: "+message)


def prof_on_presence_stanza_receive(stanza):
  prof.cons_show("I: receive stanza: "+stanza)
  return True



# /plugins install ~/projects-git/profanity-plugins/say.py
#  ~/.local/share/profanity/plugins/
# /plugins install ~/bot/profanity/auto_ban.py
# /plugins update ~/bot/profanity/auto_ban.py

def _auto_ban(arg1=None, arg2=None):
  global enable
  #  room = prof.get_current_muc()
  #  prof.send_line("/who online")
  if arg1 == "off":
    enable = False
    #  off = True
    #  prof.send_line('stop to auto ban')
    prof.cons_show("I: auto ban mode: off")
    
  #  elif arg1 == "on":
  #    prof.settings_boolean_set("ab", "off", False)
  #    prof.cons_show("I: auto ban mode")
  elif arg1 == "ping":
    prof.send_line('pong from xmppbot')
  else:
    if arg1 == "now":
      now= prof.settings_boolean_get("ab", "now", True)
      if now == True:
        now = False
      prof.settings_boolean_set("ab", "now", now)
    elif arg1 == "new":
      new= prof.settings_boolean_get("ab", "new", True)
      if new == True:
        new = False
      prof.settings_boolean_set("ab", "new", new)
    elif arg1 == "slow":
      slow= prof.settings_boolean_get("ab", "slow", True)
      if slow == True:
        slow = False
      prof.settings_boolean_set("ab", "slow", slow)
    elif arg1 == "max":
      max= prof.settings_int_get("ab", "max", 0)
      if arg2 == None:
        if max == 0:
          max = 64
        else:
          max = 0
      else:
        max = arg2
      prof.settings_int_set("ab", "max", max)
    else:
      pass
    enable = True
    prof.cons_show("I: auto ban mode: on")
  prof.cons_show("I: auto ban mode off: "+off)
  prof.settings_boolean_set("ab", "off", off)
  prof.cons_show("I: now: "+now)
  prof.settings_boolean_set("ab", "now", now)
  prof.settings_boolean_set("ab", "new", new)
  prof.settings_boolean_set("ab", "slow", slow)
  prof.cons_show("I: max: "+max)
  prof.settings_int_set("ab", "max", max)




def prof_init(version, status, account_name, fulljid):
    synopsis = [
        "/ab d <domain>",
        "/ab <jid>",
        "/ab unban <jid>",
        "/ab max <number>",
        "/ab new",
        "/ab slow",
        "/ab now"
    ]
    description = "auto ban spam accounts"
    args = [
        [ "now", "ban all speaking accounts from now" ],
        [ "time <number>", "hours" ],
        [ "slow", "slow mode" ],
        [ "new", "ban all new group mambers from now" ],
        [ "<domain>", "block all new members with the <domain>" ],
        [ "<jid>", "block the account and the domain in it" ],
        [ "max <number>", "the length of msg" ],
        [ "unban <jid>", "unban <jid>" ]
    ]
    examples = [
        "/ab now",
        "/ab time 4h",
        "/ab slow",
        "/ab new",
        "/ab max 64",
        "/ab a@xmpp.net",
        "/ab unban a@xmpp.net",
    ]

    prof.register_command("/ab", 0, 2, synopsis, description, args, examples, _auto_ban)
    prof.completer_add("/ab", [ "now", "new","slow"])

