#!/bin/bash

# log_msg(){
#   echo
#   echo
#   date
#   echo "#### mt ####"
#   echo "msgText, msgUsername, inAccount, inProtocol, inChannel, inGateway, inEvent, outAccount, outProtocol, outChannel, outGateway, outEvent"
#   local i=0
#   for i in "$@"
#   do
#     echo -n "|$i|"
#   done
#   echo
#   echo "#### end ####"
# }

#if [[ $3 = xmpp.myxmpp ]]; then
# if [[ "$1" =~ *pong* ]]; then
# if [[ $3 = xmpp.conversations ]]; then
# if [[ "$6" = test ]]; then
#   log_msg "$@" >> ~/tera/mt_msg.log
# fi





NAME="$2"
SPLIT="_SPLIT_FOR_MT_"
TEXT="$1"
if [[ -z "$2" ]]; then
  echo -n $SPLIT
  echo -n "$TEXT"
  exit 0
elif [[ "$2" == "blockthismessage" ]]; then
    # echo -n "bot"
    echo -n "$2"
    exit 0
fi




[[ $( echo "${NAME}" | wc -l ) -ge 3 ]] && echo -n "$2" && exit 0
[[ "${NAME:0:1}" == ">" ]] && echo -n "$2" && exit 0
[[ "${NAME:0:2}" == "> " ]] && echo -n "$2" && exit 0
[[ "${NAME:1:1}" == " " ]] && [[ "${NAME: -2}" == ": " ]] && echo -n "$2" && exit 0
[[ "${NAME:3:1}" == " " ]] && [[ "${NAME: -4}" == ":** " ]] && echo -n "$2" && exit 0



SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}) || exit; pwd )}




block_msg(){
  echo -n "blockthismessage"
  exit 0
}

#if [[ $3 = xmpp.myxmpp ]]; then
# if [[ $3 = xmpp.conversations ]]; then
#   log_msg "$@" >> ~/tera/mt_msg.log
# fi




if [[ $3 = api.cmd ]]; then
  :
elif [[ $6 = gateway6 ]]; then
  :
# elif [[ $2 = "wtfipfs" ]] && [[ $8 = xmpp.myxmpp ]]; then
#   block_msg
elif [[ $2 = "liqsliu" ]] && [[ $8 = api.cmd ]] && [[ $3 = xmpp.myxmpp ]]; then
  :
else
  if [[ -e "$SH_PATH/STOP" ]]; then
    block_msg
  fi
fi

LABLE="C"



# msgText, msgUsername, inAccount, inProtocol, inChannel
# inGateway, inEvent, outAccount, outProtocol, outChannel
# outGateway, outEvent





case $3 in
# xmpp.myxmpp|xmpp.myxmpp2)
xmpp.*)
  LABLE="X"
  if echo "$TEXT" | head -n1 | grep -q -P "^>" && [[ $(echo "$TEXT" | sed '/^[^>]/,$!d' | grep -c -P "^>") -eq 0 && $(echo "$TEXT" | sed -n '/^>/!p' | sed -n '/^$/!p' | wc -l) -ge 1 ]]; then
    QT=$( echo "$TEXT" | sed -n '/^> /p')
    H=$(echo "$QT"|head -n1)
    if [[ "$H" =~ ^\>\ .+:$ ]] && echo "$QT"|sed -n '2p'|grep -q -P '^> [0-9]{4}-[0-9]{2}-[0-9]{2}  [0-9]{2}:[0-9]{2}'; then
      QT=$( echo "$QT" | sed '2d')
    fi
    if [[ "$H" =~ ^\>\ bot\ wrote:$ ]]; then
      QT=$( echo "$QT" | sed '1d')
#    elif [[ "$(echo "$QT"|head -n1|grep -c -P '^> [a-zA-Z0-9_]+ wrote:$')" -eq "1" ]]; then
    elif [[ "$H" =~ ^\>\ .+\ wrote:$ ]]; then
      nick=$(echo "$QT"|head -n1|cut -d ' ' -f2)
      QT=$( echo "$QT" | sed '1d')
      QT=$( echo "$QT" | sed "1s/^> /> X ${nick}: /")
    elif [[ "$H" =~ ^\>\ .+:$ && "$(echo "$QT" |wc -l)" -ge 2 ]]; then
      # monocles
      if [[ "$H" =~ ^\>\ bot:$ ]]; then
        QT=$( echo "$QT" | sed '1d')
      else
        nick=$(echo "$QT"|head -n1|cut -d ' ' -f2)
        QT=$( echo "$QT" | sed '1d')
        QT=$( echo "$QT" | sed "1s/^> /> X ${nick} /")
      fi
    fi
    TEXT=$( echo "$TEXT" | sed '/^[^>]/,$!d')
  fi
  # if [[ "$2" == "wtfipfs" ]] || [[ "$2" == " " ]]; then
  if [[ "$2" == "wtfipfs" ]]; then
    NAME=$( echo "$TEXT" | grep -P -o '^\*\*\w+ \S+?:\*\* ')
    NAME=${NAME:2}
    LABLE=${NAME%%\ *}
    NAME=${NAME%:\*\*\ }
    NAME=${NAME#* }
    TEXT=$( echo "$TEXT" | sed -r 's/^\*\*\w+ \S+?:\*\* //')
  elif [[ "$2" == "bot" ]]; then
    NAME+="[xmpp]"
    TEXT=$( echo "$TEXT" | sed -r 's/^\*\*\w+ \S+?:\*\* //')
  fi
  # if [[ "$5" =~ acg|ipfsrss ]]; then
  #   :
  #   NAME+="[rss]"
  # fi

  # if [[ -z "$NAME" ]] || [[ "$NAME" == " " ]]; then
  if [[ -z "$NAME" ]]; then
    NAME="fixme_empty_name"
  elif [[ "$NAME" == " " ]]; then
    NAME="fixme_error_name"
  fi
  ;;
# elif [[ "$3" == "matrix.mymatrix" ]]; then
# matrix.mymatrix)
matrix.*)
  if [[ "$2" == "coybot beta" ]]; then
    block_msg
  fi
  LABLE="M"
#  log_msg "$@" &>> ~/tera/mt.log

_chang_name_from_bifrost(){
  # local matrix_name=$1
  if [[ "$(echo "${matrix_name%%=40*}" | wc -m )" -le 2 ]]; then
    matrix_name=${matrix_name%%=2f*}
    matrix_name=$(echo "${matrix_name}" | sed "s/=40/@/")
  else
    matrix_name=${matrix_name%%=40*}
  fi
  # echo -n "$matrix_name"
}
chang_name_from_bifrost(){
  # local matrix_name=$1
  if [[ "${matrix_name: -12}" == ":libera.chat" ]]; then
    LABLE=I
    if [[ "${matrix_name:0:6}" == "_xmpp_" ]]; then
      block_msg
      LABLE="X"
      matrix_name=${matrix_name:6}
      _chang_name_from_bifrost
      return 0
    elif [[ "${matrix_name:0:9}" == "_discord_" ]]; then
      block_msg
      LABLE="D"
    elif [[ "${matrix_name:0:9}" == "telegram_" ]]; then
      block_msg
      LABLE="T"
    elif [[ "${matrix_name%%=40*}" == "_neb_rssbot_" ]]; then
      block_msg
      LABLE="M"
      # NAME="rssbot"
      matrix_name=rssbot
      return 0
    elif [[ "${matrix_name: -15}" == "[m]:libera.chat" ]]; then
      # from matrix to irc, then back to matrix
      block_msg
      LABLE="T"
    fi
    return 1
  elif [[ "${matrix_name: -13}" == ":aria-net.org" ]]; then
    if [[ "${matrix_name:0:9}" == "_bifrost_" ]]; then
      LABLE="X"
      matrix_name=${matrix_name:9}
      _chang_name_from_bifrost
    fi
  elif [[ "${matrix_name: -11}" == ":matrix.org" ]]; then
    if [[ "${matrix_name:0:6}" == "_xmpp_" ]]; then
      block_msg
      LABLE="X"
      matrix_name=${matrix_name:6}
      _chang_name_from_bifrost
      return 0
    elif [[ "${matrix_name%%=40*}" == "_neb_rssbot_" ]]; then
      block_msg
      LABLE="M"
      # NAME="rssbot"
      matrix_name=rssbot
      return 0
    fi
    return 1
  elif [[ "${matrix_name##*:}" == "t2bot.io" ]]; then
    if [[ "${matrix_name:0:9}" == "_discord_" ]]; then
      block_msg
      LABLE="D"
    elif [[ "${matrix_name:0:9}" == "telegram_" ]]; then
      block_msg
      LABLE="T"
    fi
  else
    return 1
  fi
}


chang_name_from_matrix(){
  # local matrix_name=$1
  # if is_bifrost "$matrix_name"; then
    # matrix_name=$(chang_name_from_bifrost "$matrix_name")
  if chang_name_from_bifrost; then
    :
  else
    # if [[ "$(echo "$matrix_name" | cut -d':' -f2 )" == "matrix.org" ]]; then
    if [[ "${matrix_name##*:}" == "matrix.org" ]]; then
      matrix_name=$(echo "$matrix_name" | cut -d':' -f1)
    else
      # if [[ "$(echo "$matrix_name" | cut -d':' -f1 | wc -m )" -gt 3 ]]; then
      if [[ "$(echo "${matrix_name%%:*}" | wc -m )" -gt 3 ]]; then
        matrix_name=$(echo "$matrix_name" | cut -d':' -f1)
      fi
    fi
  fi
  # echo -n "$matrix_name"
}

chang_name_for_qt_from_matrix(){
  local qt_tmp=$1
  username=$(echo "$qt_tmp" | head -n1 | grep -o -P "> <@[a-zA-Z0-9_]+:[0-9a-zA-Z.-]+\.[a-zA-Z]+> ")
  if [[ -n "$username" ]]; then
#      qt_tmp=$(echo "$qt_tmp" | sed "1s|^$username||" )
    qt_tmp=$(echo "$qt_tmp" | sed "1s|$username|matrix_username|" )
    username=$(echo "$username" | cut -d"@" -f2 | cut -d ">" -f1 )
    # username=$(chang_name_from_matrix "$username")
    username=$(matrix_name="$username"; chang_name_from_matrix; echo "$matrix_name")
#      qt_tmp=$( echo -n "> M ${username}: "; echo "$qt_tmp")
    username="> M ${username}: "
    qt_tmp=$(echo "$qt_tmp" | sed "1s|matrix_username|$username|" )
  fi
  echo -n "$qt_tmp"

}

  # NAME=$(chang_name_from_matrix "$NAME")
  matrix_name=$NAME
  chang_name_from_matrix
  NAME=$matrix_name

  #for reply from matrix
  if [[ $(echo "$TEXT" | grep -c -G "^$" ) -ge 1 && $(echo "$TEXT" | head -n 1 | grep -c -G "^>" ) -eq 1 && $(echo "$TEXT" | sed '0,/^$/d' | grep -c -P "^>") -eq 0 && $(echo "$TEXT" | sed '/^$/,$d' | grep -c -P "^>") -eq $(echo "$TEXT" | sed '/^$/,$d' | wc -l ) ]]; then
    # TEXT=$( echo "$TEXT" | sed "1s/^> <@wtfipfs:matrix.org> /> /" )



#    QT=$( echo "$TEXT" | sed "1s/^> <@wtfipfs:matrix.org> /> /" | sed '/^$/,$d' )
    QT=$( echo "$TEXT" | sed "1s/^> <@wtfipfs:matrix.org> /> /" )
    QT=$( echo "$QT" | sed -E '/^([^$>]|>[^ ])/,$d' )
#    username=$(echo "$QT" | head -n1 | grep -o -P "^> <@[a-zA-Z0-9_]+:[0-9a-zA-Z.-]+\.[a-zA-Z]+> ")

    QT=$(chang_name_for_qt_from_matrix "$QT")

  elif [[ $(echo "$TEXT" | sed '/^> [^>]/,$!d' | grep -c -G "^$" ) -ge 1 && $(echo "$TEXT" | head -n 1 | grep -c -G "^> " ) -eq 1 && $(echo "$TEXT" | sed '/^$/,$d' | grep -c -P "^> ") -ge 1 && $(echo "$TEXT" | sed '/^> [^>]/,$!d' | sed '/^$/,$d' | grep -c -P "^>") -eq $(echo "$TEXT" | sed '/^> [^>]/,$!d' | sed '/^$/,$d' | wc -l ) ]]; then

    QT=$( echo "$TEXT" | sed -E '/^([^$>]|>[^ ])/,$d' )
    QT=$(chang_name_for_qt_from_matrix "$QT")
  fi

  if [[ $(echo "$TEXT" | grep -c -G "^$" ) -ge 1 && $(echo "$TEXT" | head -n 1 | grep -c -G "^>" ) -eq 1 && $(echo "$TEXT" | sed '0,/^$/d' | grep -c -P "^>") -eq 0 && $(echo "$TEXT" | sed '/^$/,$d' | grep -c -P "^>") -eq $(echo "$TEXT" | sed '/^$/,$d' | wc -l ) ]]; then
    TEXT=$( echo "$TEXT" | sed -E '/^([^$>]|>[^ ])/,$!d' )
  elif [[ $(echo "$TEXT" | sed '/^> [^>]/,$!d' | grep -c -G "^$" ) -ge 1 && $(echo "$TEXT" | head -n 1 | grep -c -G "^> " ) -eq 1 && $(echo "$TEXT" | sed '/^$/,$d' | grep -c -P "^> ") -ge 1 && $(echo "$TEXT" | sed '/^> [^>]/,$!d' | sed '/^$/,$d' | grep -c -P "^>") -eq $(echo "$TEXT" | sed '/^> [^>]/,$!d' | sed '/^$/,$d' | wc -l ) ]]; then
    TEXT=$( echo "$TEXT" | sed -E '/^([^$>]|>[^ ])/,$!d' )
  fi
  ;;
# elif [[ "$3" == "telegram.mytelegram" ]]; then
# telegram.mytelegram)
telegram.*)
  if [[ "$2" == "Telegram" ]]; then
    block_msg
  fi
  LABLE="G"
  if [[ "$2" == "Telegram" ]]; then
# https://github.com/42wim/matterbridge/pull/1272
#    echo "block the msg" &>> ~/tera/test_tengo.log
    echo -n "blockthismessage"
    # echo -n "bot"
    exit 0
  fi

  # if [[ "${TEXT:0:15}" == "Forwarded from " ]]; then
  #   # echo -n "bot"
  #   echo -n "blockthismessage"
  #   exit 0
  # fi



  if [[ $(echo "$TEXT" | grep -c -G "^> reply_from_telegram$" ) -eq 1 ]]; then
    # QT=$( python3 "$SH_PATH/get_msg.py" reply_msg "$(echo "$TEXT" | sed '/^> reply_from_telegram$/,$d')" "$2" "$5" ) || QT=""
    QT=""
    [[ -z "$QT" ]] && QT=$( echo "$TEXT" | sed '0,/^> reply_from_telegram$/d' )
    QT=$(echo "$QT" | sed '1s/^T bot: //' | sed 's/^/> /' )

  fi

  # if [[ "$NAME" == "Group" ]]; then
  #   NAME="liqsliu"
  # elif [[ "$NAME" == "‏⁠‎ l​i​q​s‏l​i​u​‎" ]]; then
  #   NAME="liqsliu"
  # fi

#   if [[ "${TEXT:0:15}" == "Forwarded from " ]]; then
# #    TEXT=$( echo "${TEXT}" | sed -r '1s/[^:]+: //' )
#     block_msg
#   fi

  if [[ $(echo "$TEXT" | grep -c -G "^> reply_from_telegram$" ) -eq 1 ]]; then
    #skip nick
    TEXT=$(echo "$TEXT" | sed '/^> reply_from_telegram$/,$d';)
  fi
  ;;
zulip.myzulip)
  LABLE="Z"
  # if [[ $(echo "$TEXT" | grep -c -P "^\[.*\]\(/user_uploads/.*\)$" ) -eq 1 ]]; then
  #   TEXT="${TEXT%](/user_uploads/*}](https://wtfipfs.zulipchat.com/user_uploads/${TEXT##*](/user_uploads/}"
  # fi
  ;;
discord.mydiscord)
  LABLE="D"
      # block_msg
  # if [[ "$5" == "wtfipfs" ]]; then
    # if [[ "${NAME##*#}" == "0000" ]]; then
  if echo "${NAME}" | grep -q -P ".+#[0-9]{4}$"; then
    NAME=${NAME%#*}
  else
    :
    # block_msg
  fi
  if [[ "$2" == "Telegram Bridge" ]]; then
      echo -n "blockthismessage"
      exit 0
#    if [[ "${TEXT:0:15}" == "Forwarded from " ]]; then
    if [[ "${TEXT:0:31}" == "Forwarded message from channel " ]]; then
      echo -n "blockthismessage"
      exit 0
    fi
  fi

  ;;
irc.myirc)
  LABLE="I"
  ;;
irc.irc2p)
  LABLE="2"
  ;;
api.tox)
  LABLE="T"
  ;;
api.in)
  LABLE="0"
  ;;
api.cmd)
  LABLE="0"
  ;;
api.cmdres)
  LABLE="0"
  ;;
api.gpt)
  LABLE="C"
  ;;
api.tg)
  LABLE="G"
  ;;
mattermost.mymattermost)
  LABLE="m"
  ;;
*)
  LABLE="R"
  ;;
esac

if [[ "$(echo "$QT" | head -n1 | grep -c -G "^> >" )" -eq 1 ]]; then
  QT=$( echo "$QT" | sed '/^> [^>]/,$!d' )
fi

# if [[ "$(echo "$QT" | tail -n1 | grep -c -G "^$" )" -eq 1 ]]; then
if echo "$QT" | tail -n1 | grep -q -G "^$"; then
  QT=$( echo "$QT" | sed '$d')
fi


if [[ $11 = "gateway1" ]] && { [[ $6 = ipfsrss ]] && [[ $6 = acg ]]; }; then
  NAME+='[rss]'
fi

if [[ "$LABLE" == "0" ]]; then
# echo -n "${NAME}: "
NAME="${NAME}: "
else
# [[ -z "$QT" ]] && echo -n "$LABLE ${NAME}: " || echo -n "$QT
#
# $LABLE ${NAME}: "
[[ -z "$QT" ]] && NAME="$LABLE ${NAME}: " || NAME="$QT

$LABLE ${NAME}: "
fi


# if [[ "$6" = test ]]; then
# echo "mid NAME:|$NAME|" >> ~/tera/mt_msg.log
# echo "mid TEXT:|$TEXT|" >> ~/tera/mt_msg.log
# fi

# echo -n "$NAME"
# echo -n $SPLIT
# echo -n "$TEXT"
# exit 0

unset QT


if [[ -n "$4" ]] ; then
  # case $9 in
  case $8 in
  # xmpp)
  xmpp.*)
  # if [[ "$9" == "xmpp" ]] ; then
    if [[ "$NAME" == "C twitter: " ]]; then
      TEXT=$(echo "$TEXT" | sed '2,$s/^/> /' )
    elif [[ "$NAME" == "C bot: " && "$( echo ${1} | cut -d":" -f2 )" == " twitter to text" ]]; then
      TEXT=$(echo "$TEXT" | sed '2,$s/^/> /')
    fi
    if [[ "$NAME" == "M rssbot: " ]] || [[ "$NAME" == "M feeds: " ]]; then
      # forbid msg from ipfsrss sent by rssbot
      # if [[ "${11}" == "gateway1" ]]; then
      #   block_msg
      # fi
      # NAME=$(echo "$TEXT"  | cut -z -d ":" -f 1)
      # TEXT=$(echo "$TEXT" | cut -z -d ":" -f 2-)
      # NAME=$(echo "$TEXT" | head -n1 | cut -d ":" -f 1)
      NAME=${TEXT%%:*}
      # TEXT=$(echo "$TEXT" | sed '1s/[^:]*://')
      TEXT=${TEXT#*:}
      TEXT=${TEXT# }
    else
      [[ $(echo "$NAME" | wc -l) -ge 3 ]] && QT=$(echo "$NAME" | sed '/^[^>]/d'; echo )
      NAME=$(echo "$NAME" | tail -n1)
      # NAME=$(echo "$NAME" | cut -d ":" -f 1)
      # NAME=${NAME%: }
      NAME="**${NAME%: }:** "
      if [[ -n "$QT" ]]; then
        NAME="$QT
${NAME}"
      fi
    fi
    ;;
  irc.*)
  # elif [[ "$9" == "irc" ]] ; then
    NAME=$(echo "$NAME" | tail -n1)
#    echo -n "$(echo "$NAME" | tail -n1)"
    TEXT=$(echo "$TEXT" | awk '{printf "%s\\n", $0}' | sed "s/\\\\n$//g")
    if [[ "$(echo "$NAME" | wc -l)" -ge 3 ]]; then
      QT=$(echo "$NAME" | head -n 1 | sed 's/> //' )
      TEXT="$TEXT RE: $QT"
    fi
    ;;
  matrix.*)
  # elif [[ "$9" == "matrix" ]] ; then
    if [[ "${5}" == "-1001193563578" ]] ; then
      if [[ "${10}" == "#ipfs:mozilla.org" ]] ; then
        block_msg
      fi
    fi
    tmp=$NAME
    NAME=$(echo "$NAME" | tail -n1)
    # NAME=$(echo "$NAME" | cut -d ":" -f 1)
    NAME=${NAME%: }
    NAME="**${NAME}:** "
    qt=$(echo "$tmp" | sed '$d')
    [[ -n "$qt" ]] && NAME="$qt

$NAME"
    if [[ -z "$TEXT" ]]; then
#      [[ $(echo "$NAME" | wc -l) -ge 3 ]] && [[ $(echo "$NAME" | grep -c -G '^$') -ge 1 ]] && echo "$NAME" | tail -n1 && echo "$NAME" | sed '/^$/,$d' && NAME=""
      [[ $(echo "$NAME" | wc -l) -ge 3 ]] && NAME=$(echo "$NAME" | tail -n1; echo "$NAME" | sed '/^$/,$d')
    else
      if [[ "$NAME" == "C twitter: " ]]; then
        TEXT=$(echo "$TEXT" | sed '2,$s/^/> /' | sed '2s/^/\n/')
      elif [[ "$NAME" == "C bot: " && "${1:0:16}" == "twitter to text:" ]]; then
        TEXT=$(echo "$TEXT" | sed '2,$s/^/> /' | sed '2s/^/\n/')
      elif [[ "$NAME" == "C bot: " && "$( echo ${1} | cut -d":" -f2 )" == " twitter to text" ]]; then
        TEXT=$(echo "$TEXT" | sed '2,$s/^/> /' | sed '2s/^/\n/')
      else
        :
        # if [[ -n "$(echo "$NAME" | sed '$d')" ]]; then
        # if [[ "$(echo "$NAME" | wc -l)" -ge 3 ]]; then
        #   QT=$(echo "$NAME" | sed '$d')
        # fi
      fi
      TEXT="$NAME$TEXT"
      unset NAME
    fi
    ;;
  discord.*)
  # elif [[ "$9" == "discord" ]] ; then
    if [[ "${10}" == "wtfipfs" ]] ; then
      if [[ "${5}" == "#wtfipfs:matrix.org" ]] ; then
        block_msg
      elif [[ "${5}" == "-1001503043923" ]] ; then
        # new wtfipfs tg group
        block_msg
      fi
    elif [[ "${10}" == "wtfipfs2" ]] ; then
      # if [[ "${3}" != "api.in" ]] ; then
      if [[ "${5}" == "#ipfs:mozilla.org" ]] ; then
        block_msg
      elif [[ "${5}" == "-1001193563578" ]] ; then
        block_msg
      fi
    fi
#     if [[ "$NAME" == "C twitter: " ]]; then
#       :
# #      NAME="bot"
#     else
#     fi
    if [[ "$NAME" == "C twitter: " ]]; then
      TEXT=$(echo "$TEXT" | sed '2,$s/^/> /' )
    elif [[ "$NAME" == "C bot: " && "${1:0:16}" == "twitter to text:" ]]; then
      TEXT=$(echo "$TEXT" | sed '2,$s/^/> /')
    elif [[ "$NAME" == "C bot: " && "$( echo ${1} | cut -d":" -f2 )" == " twitter to text" ]]; then
      TEXT=$(echo "$TEXT" | sed '2,$s/^/> /')
    fi

    if [[ "$(echo "$NAME" | wc -l)" -ge 3 ]]; then
      TEXT="$(echo "$NAME" | sed '$d')
$TEXT"
    fi
    NAME=$(echo "$NAME" | tail -n1)
    NAME="${NAME:0:-2}"
    if [[ -z "$NAME" ]] || [[ "$NAME" == " " ]]; then
      NAME="fixme"
    fi
    ;;
  api.tox)
    :
    ;;
  # api.gpt)
  api.*)
    if [[ "$(echo "$NAME" | wc -l)" -ge 3 ]]; then
      TEXT="$(echo "$NAME" | sed '$d')
$TEXT"
    fi
    NAME=$(echo "$NAME" | tail -n1)
    ;;
  telegram.*)
  # elif [[ "$9" == "telegram" ]] ; then
    if [[ "${10}" == "-1001193563578" ]] ; then
      block_msg
    fi

    if [[ "NAME" == "C twitter: " ]]; then
      exit 0 # another bot
    fi
    if [[ "NAME" == "C twitter: " ]]; then
      TEXT='.>)\`'
    elif [[ "$3" == "api.tg" && "$11" != "gateway0" ]]; then
      TEXT='.>)\`'
    elif [[ $(echo "$NAME" | wc -l) -ge 3 ]]; then
#      NAME=$(bash "$SH_PATH/text2markdown.sh" "$NAME" | tail -n1 | sed 's/ / */' | sed 's/: $/*: /' )
      last=$(echo "$NAME" | tail -n1)

      NAME=${last%: *}
      P=${NAME:0:1}
      NAME=${NAME:2}
      NAME=$(bash "$SH_PATH/text2markdown.sh" "$NAME")
      NAME="$P *${NAME}*: "

      qt_text=$(echo "NAME" | sed '/^> /!d' | sed 's/^> //')
      line1=$(echo "$qt_text" | head -n1)

      if [[ "${line1:0:2}" == "T " || "${line1%%: *}" == "C twitter" ]]; then

        msg_text=$(echo "${line1#*: }"; echo "$qt_text" |sed '1d')
        msg_text=$(echo "$msg_text" | sed -r '$s|: https://liuu\.tk/[a-zA-Z0-9_./?=%-]+$||')

#        msg_sender=$(echo "NAME" | head -n1 | cut -d' ' -f3- | cut -d':' -f1 )
        msg_sender="${line1%%: *}"
        msg_sender="${msg_sender#* }"


      else
        msg_sender="bot"
        if [[ $( echo "$line1" | grep -c -P '^[A-Z] .*: .*' ) -eq 1 ]]; then
          msg_text=$qt_text
        else
          msg_text="$P ?: $qt_text"
        fi
      fi
      # use user api to send msg to tg and block this TEXT to tg
      # bash "$SH_PATH/tg.sh" settoken wtfipfs setcid "${10}" "--reply" "$msg_text" "$msg_sender" "--md" "$NAME$(bash "$SH_PATH/text2markdown.sh" "$1")"
      # TEXT='.>)\`'
    else
      TEXT=$(bash "$SH_PATH/text2markdown.sh" "$TEXT")
    fi

    [[ $(echo "$NAME" | wc -l) -ge 3 ]] && QT=$(bash "$SH_PATH/text2markdown.sh" "$(echo "$NAME" | sed '/^$/,$d')" && echo)
    NAME=$(bash "$SH_PATH/text2markdown.sh" "$(echo "$NAME" | tail -n1)")
    # echo -n "*$(echo "$NAME" | cut -d' ' -f 2- | sed '$s|: $||')*: "
    M=$(echo "$NAME" | cut -d' ' -f1)
    NAME=$(echo "$NAME" | cut -d' ' -f 2-)
    NAME=${NAME%: }
    NAME="$QT
$M *$NAME*: "


    ;;
  zulip.*)
  # elif [[ "$9" == "zulip" ]] ; then
    if [[ "$NAME" == "C twitter: " ]]; then
      TEXT=$(echo "$TEXT" | sed '2,$s/^/> /' )
    elif [[ "$NAME" == "C bot: " && "${1:0:16}" == "twitter to text:" ]]; then
      TEXT=$(echo "$TEXT" | sed '2,$s/^/> /')
    elif [[ "$NAME" == "C bot: " && "$( echo ${1} | cut -d":" -f2 )" == " twitter to text" ]]; then
      TEXT=$(echo "$TEXT" | sed '2,$s/^/> /')
    fi
    ;;
  esac
  # fi
fi


# if [[ "$9" != discord ]]; then
# if [[ "$3" == "api.gpt" ]]; then
#   # if [[ $(echo "$TEXT" | wc -l) -gt 1 ]]; then
#   # if [[ "${TEXT%*\[结束\]}" == "${TEXT}" ]] && [[ "${TEXT%*\[思考中...\]}" == "${TEXT}" ]]; then
#   # if [[ "${TEXT%*\[思考中...\]}" == "${TEXT}" ]]; then
#   if echo "$TEXT" | head -n1 | grep -q -P "^[A-Z] \S+: "; then
#     :
#   else
#       NAME=""
#   fi
# fi
# fi

echo -n "$NAME"
echo -n $SPLIT
echo -n "$TEXT"

# if [[ "$6" = test ]]; then
# echo "finally NAME:|$NAME|" >> ~/tera/mt_msg.log
# echo "finally TEXT:|$TEXT|" >> ~/tera/mt_msg.log
# fi
