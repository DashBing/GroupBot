#!/bin/bash



NAME="$2"
SPLIT="_SPLIT_FOR_MT_"
TEXT="$1"


block_msg(){
  echo -n "blockthismessage"
  exit 0
}
# orig_msg(){
#   echo -n "originalmessage"
#   exit 0
# }


if [[ -z "$2" ]]; then
  case $8 in
    discord.*|irc.*)
      if [[ "${3}" == "api.gpt" ]] ; then
        # echo -n "C gpt: "
        NAME="gpt"
      elif [[ "${3}" == "api.cmdres" ]] ; then
        # echo -n "C bot: "
        NAME="C bot"
      else
        # echo -n "C fixme_need_name: "
        NAME="C fixme_need_name"
      fi
      ;;
    # telegram.*)
    *)
      :
      ;;
  esac
  # echo -n "$SPLIT"
  # echo -n "$TEXT"
  # exit 0
elif [[ "$2" == "blockthismessage" ]]; then
  block_msg
fi

md_name(){
  if [[ -n "$NAME" ]]; then
    # [[ $(echo "$NAME" | wc -l) -ge 3 ]] && QT=$(echo "$NAME" | sed '/^[^>]/d'; echo )
    [[ $(echo "$NAME" | wc -l) -ge 3 ]] && QT=$(echo "$NAME" | sed '$d')
    NAME=$(echo "$NAME" | tail -n1)
    # NAME=$(echo "$NAME" | cut -d ":" -f 1)
    # NAME=${NAME%: }
    NAME="**${NAME% }** "
    if [[ -n "$QT" ]]; then
      NAME="$QT
${NAME}"
    fi
  fi


}



# [[ "${NAME:0:1}" == ">" ]] && orig_msg
# [[ "${NAME:0:2}" == "> " ]] && orig_msg
# [[ "${NAME:1:1}" == " " ]] && [[ "${NAME: -2}" == ": " ]] && orig_msg
# [[ "${NAME:3:1}" == " " ]] && [[ "${NAME: -4}" == ":** " ]] && orig_msg
# [[ $( echo "${NAME}" | wc -l ) -ge 3 ]] && orig_msg


log_msg(){
  echo
  echo "#### mt $(date) ####"
  echo "msgText, msgUsername, inAccount, inProtocol, inChannel, inGateway, inEvent, outAccount, outProtocol, outChannel, outGateway, outEvent"
  local i
  for i in "$@"
  do
    echo -n "^$i"
  done
  echo
  echo "##"
}
# alias log_msg='_log_msg "$@" >> ~/mt.log'
  # log_msg
  # log_msg "$@" >> ~/mt.log


#if [[ $3 = xmpp.myxmpp ]]; then
# if [[ "$1" =~ *pong* ]]; then
# if [[ $3 = xmpp.conversations ]]; then
# if [[ "$6" = test ]]; then
#   log_msg
# fi


#if [[ $3 = xmpp.myxmpp ]]; then
# if [[ $3 = xmpp.conversations ]]; then
#   log_msg "$@" >> ~/tera/mt_msg.log
# fi



SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}) || exit; pwd )}

# if [[ $3 = api.cmd ]]; then
#   :
# elif [[ $6 = gateway6 ]]; then
#   :
# # elif [[ $2 = "wtfipfs" ]] && [[ $8 = xmpp.myxmpp ]]; then
# #   block_msg
# elif [[ $2 = "liqsliu" ]] && [[ $8 = api.cmd ]] && [[ $3 = xmpp.myxmpp ]]; then
#   :
# else
#   if [[ -e "$SH_PATH/STOP" ]]; then
#     block_msg
#   fi
# fi

# if [[ "$5" =~ acg|ipfsrss ]]; then
#   :
#   NAME+="[rss]"
# fi
if [[ $5 = wtfipfs_rss ]] || [[ $5 = acg ]]; then
  if [[ ${11} = "gateway1" ]]; then
    if [[ "$NAME" = wtfipfs ]]; then
      block_msg
    else
      NAME+='[rss]'
    fi
  else
    # if [[ "$2" = wtfipfs ]] || [[ "$2" = bot ]]; then
    if [[ "$NAME" = wtfipfs ]]; then
      # if [[ $5 = wtfipfs_rss ]]; then
      #   NAME=news
      # elif [[ $5 = acg ]]; then
      #   NAME=acg
      # fi
      # NAME=$(echo "$TEXT"|head -n1 | cut -d ' ' -f2)
      TEXT=$( echo "$TEXT" | sed -e '1s/^\[\s*/**/' -e '1s/\s*\]$/**/')
      echo -n $SPLIT
      echo -n "$TEXT"
      exit 0
    fi
  fi
fi

LABLE="C"



# msgText, msgUsername, inAccount, inProtocol, inChannel
# inGateway, inEvent, outAccount, outProtocol, outChannel
# outGateway, outEvent

case $3 in
# xmpp.myxmpp|xmpp.myxmpp2)
xmpp.*)
  # for ipfsrss
  # if [[ "$5" = "wtfipfs_rss" ]]; then
  #   if [[ "$2" =~ liqsliu* ]]; then
  #   block_msg
  #   fi
  # fi
  # if [[ "$2" == debitcards ]]; then
  #   block_msg
  # elif [[ "$2" =~ *debit* ]]; then
  #   block_msg
  if [[ "$NAME" =~ *debit*card* ]]; then
    block_msg
  fi
  LABLE="X"
  if echo "$TEXT" | head -n1 | grep -q -P "^>" && [[ $(echo "$TEXT" | sed '/^[^>]/,$!d' | grep -c -P "^>") -eq 0 && $(echo "$TEXT" | sed -n '/^>/!p' | sed -n '/^$/!p' | wc -l) -ge 1 ]]; then
    # QT=$( echo "$TEXT" | sed -n '/^> /p')
    QT=$( echo "$TEXT" | sed '/^[^>]/,$d')
    H=$(echo "$QT"|head -n1)

    if [[ "$H" =~ ^\>\ .+:$ ]] && echo "$QT"|sed -n '2p'|grep -q -P '^> [0-9]{4}-[0-9]{2}-[0-9]{2}  [0-9]{2}:[0-9]{2}'; then
      QT=$( echo "$QT" | sed '2d')
    elif [[ "$H" =~ ^\>\ bot\ wrote:$ ]]; then
      QT=$( echo "$QT" | sed '1d')
#    elif [[ "$(echo "$QT"|head -n1|grep -c -P '^> [a-zA-Z0-9_]+ wrote:$')" -eq "1" ]]; then
    elif [[ "$H" =~ ^\>\ .+\ wrote:$ ]]; then
      # nick=$(echo "$H"|cut -d' ' -f2)
      nick=$(echo "$H"|cut -d':' -f1|cut -d' ' -f2-)
      nick=${nick% wrote}
      QT=$( echo "$QT" | sed -e '1d' -e '1s/^> /> X '"${nick}"': /')
    elif [[ "$H" =~ ^\>\ .+:$ ]] && [[ "$(echo "$QT" |wc -l)" -ge 2 ]]; then
      # monocles
      if [[ "$H" =~ ^\>\ bot:$ ]]; then
        QT=$( echo "$QT" | sed '1d')
      else
        # nick=$(echo "$H"|cut -d' ' -f2)
        nick=$(echo "$H"|cut -d':' -f1|cut -d' ' -f2-)
        QT=$( echo "$QT" | sed -e '1d' -e '1s/^> /> X '"${nick}"': /')
      fi
    fi

    if echo "$H" | grep -q -P "^> \*\*[a-zA-Z0-9] .+?:\*\* "; then
      # default
      QT=$( echo "$QT" | sed -r '1s/^> \*\*([a-zA-Z0-9] .+?:)\*\* /> \1 /')
    fi
    TEXT=$( echo "$TEXT" | sed '/^[^>]/,$!d')
  elif echo "$TEXT" | head -n1 | grep -q -P '^» \['; then
    QT=$( echo "$TEXT" | sed -e '/^[^»]/,$d' -e 's/» /> /1')
    TEXT=$( echo "$TEXT" | sed '/^[^»]/,$!d')
  fi

  # if [[ "$2" == "wtfipfs" ]] || [[ "$2" == " " ]]; then
  if [[ "$NAME" == "wtfipfs" ]]; then
    NAME=$( echo "$TEXT" | grep -o -P '^\*\*\w+ \S+?:\*\* ')
    NAME=${NAME:2}
    LABLE=${NAME%% *}
    NAME=${NAME%:\*\* }
    NAME=${NAME#* }
    # TEXT=$( echo "$TEXT" | sed -r 's/^\*\*\w+ \S+?:\*\* //')
    TEXT=$( echo "$TEXT" | sed -r 's/^\*\*[a-zA-Z0-9] .+?:\*\* //')
  elif [[ "$NAME" == "bot" ]]; then
    NAME+="[xmpp]"
    TEXT=$( echo "$TEXT" | sed -r 's/^\*\*[a-zA-Z0-9] .+?:\*\* //')
  fi

# if [[ ${11} = "gateway1" ]] && { [[ $5 = wtfipfs_rss ]] || [[ $5 = acg ]]; }; then
# if [[ ${11} = "gateway1" ]] && [[ $5 = wtfipfs_rss ]]; then

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
  # if [[ "$NAME" == "coybot beta" ]]; then
  #   block_msg
  # fi
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
    elif [[ "${matrix_name}" == "telegram:t2bot.io" ]]; then
      block_msg
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
  if [[ "$NAME" == "Telegram" ]]; then
    block_msg
  fi
  LABLE="G"
  # if [[ "$NAME" == "Group" ]]; then
  if [[ "$NAME" == "wtfipfs_fucktelegram" ]]; then
    NAME="admin"
  elif [[ "$NAME" == "wtfipfs" ]]; then
    NAME="admin"
  # elif [[ "$NAME" == "‏⁠‎ l​i​q​s‏l​i​u​‎" ]]; then
  #   NAME="liqsliu"
  fi

# https://github.com/42wim/matterbridge/pull/1272
#    echo "block the msg" &>> ~/tera/test_tengo.log
    # echo -n "bot"

  # if [[ "${TEXT:0:15}" == "Forwarded from " ]]; then
  #   # echo -n "bot"
  #   echo -n "blockthismessage"
  #   exit 0
  # fi
#   if [[ "${TEXT:0:15}" == "Forwarded from " ]]; then
#     TEXT=$( echo "${TEXT}" | sed -r '1s/[^:]+: //' )
#     block_msg
#   fi

  # if [[ $(echo "$TEXT" | grep -c -G "^> reply_from_telegram$" ) -eq 1 ]]; then
  if echo "$TEXT" | grep -q -G "^_reply_$"; then
    # QT=$( python3 "$SH_PATH/get_msg.py" reply_msg "$(echo "$TEXT" | sed '/^> reply_from_telegram$/,$d')" "$NAME" "$5" ) || QT=""
    # QT=""
    # [[ -z "$QT" ]] && QT=$( echo "$TEXT" | sed '0,/^_reply_$/d' )
    QT=$( echo "$TEXT" | sed '0,/^_reply_$/d' |sed -e '1s/^G Matrix Telegram Bridge: //1' -e '1s/^G bot: //1' -e '1s/^G Group: /G admin: /1' -e '1s/:#0000: /: /1' -e 's/^/> /' )
    TEXT=$(echo "$TEXT" | sed '/^_reply_$/,$d')

  fi



  # if [[ $(echo "$TEXT" | grep -c -G "^> reply_from_telegram$" ) -eq 1 ]]; then
  # if echo "$TEXT" | grep -q -G "^_reply_$"; then
    #skip nick
    # TEXT=$(echo "$TEXT" | sed '/^> reply_from_telegram$/,$d';)
    # TEXT=$(echo "$TEXT" | sed '/^_reply_$/,$d';)
  # fi

  # if echo "$TEXT" |tail -n1| grep -q -G ": https://wtfipfs.eu.org/"; then
  # if echo "$TEXT" |tail -n1| grep -q ": https://wtfipfs.eu.org/\S*$"; then
  #   TEXT=$(echo "$TEXT"|sed -r '$s|: (https://wtfipfs.eu.org/\S*)$|\n--\n\1|')
  # if echo "$TEXT" |tail -n1| grep -q ": $"; then
  #   # TEXT=$(echo "$TEXT"|sed -r '$s|: $|\n--\n|')
  #   TEXT=$(echo "$TEXT"|sed '$s|: $|\n--\n|')
  # fi
   if [[ $8 = xmpp.myxmpp ]]; then
    log_msg "$@" >> ~/mt.log
   fi
  ;;
slack.*)
  LABLE="s"
  ;;
zulip.*)
  LABLE="Z"
  # if [[ $(echo "$TEXT" | grep -c -P "^\[.*\]\(/user_uploads/.*\)$" ) -eq 1 ]]; then
  #   TEXT="${TEXT%](/user_uploads/*}](https://wtfipfs.zulipchat.com/user_uploads/${TEXT##*](/user_uploads/}"
  # fi
  ;;
discord.*)
  LABLE="D"
      # block_msg
  # if [[ "$5" == "wtfipfs" ]]; then
    # if [[ "${NAME##*#}" == "0000" ]]; then
  if echo "${NAME}" | grep -q -P ".+#[0-9]{1,4}$"; then
    NAME=${NAME%#*}
  elif [[ "$3" = "discord.mydiscord2" ]]; then
    :
  elif [[ "$NAME" == "Telegram Bridge" ]]; then
      block_msg
#    if [[ "${TEXT:0:15}" == "Forwarded from " ]]; then
  elif [[ "${TEXT:0:31}" == "Forwarded message from channel " ]]; then
    block_msg
  else
    block_msg
  fi

  if echo "$TEXT" | grep -q -G "^_reply_$"; then
    QT=$( echo "$TEXT" | sed '0,/^_reply_$/d' )
    QT=$(echo "$QT" | sed '1s/^D bot: //' | sed 's/^/> /' )

  fi

  ;;
irc.irc2p)
  LABLE="2"
  ;;
irc.*)
  LABLE="I"
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
api.simplex)
  LABLE="S"
  if [[ "$NAME" == "simplexbot" ]]; then
    LABLE="C"
  fi
  ;;
api.tg)
  LABLE="G"
  ;;
api.*)
  LABLE="A"
  ;;
mattermost.*)
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


if [[ -z "$NAME" ]]; then
  :
else
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
    # if [[ "$NAME" == "C twitter: " ]]; then
    #   TEXT=$(echo "$TEXT" | sed '2,$s/^/> /' )
    # elif [[ "$NAME" == "C bot: " && "$( echo ${1} | cut -d":" -f2 )" == " twitter to text" ]]; then
    #   TEXT=$(echo "$TEXT" | sed '2,$s/^/> /')
    # fi
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
      TEXT=${TEXT#*: }
    else
      md_name
    fi
    ;;
  api.simplex)
    :
    ;;
  irc.*)
  # elif [[ "$9" == "irc" ]] ; then
    if [[ "$(echo "$NAME" | wc -l)" -ge 3 ]]; then
      QT=$(echo "$NAME" | head -n 1 | sed 's/> //' )
      TEXT="$TEXT RE: $QT"
      NAME=$(echo "$NAME" | tail -n1)
    fi
#    echo -n "$(echo "$NAME" | tail -n1)"
    # text_en=$(echo "$TEXT" | awk '{printf "%s\\n", $0}' | sed "s/\\\\n$//g")
    # length=$(echo -n "$text_en"|wc -c)
    # if [[ $length -le 400 ]]; then
    #   TEXT=$text_en
    # else
    #   TEXT=$(bash "$SH_PATH/split.sh" "$TEXT" "$NAME")
    # fi
    TEXT=$(bash "$SH_PATH/split.sh" "$TEXT" "$NAME" 450)
    ;;
  matrix.*)
  # elif [[ "$9" == "matrix" ]] ; then
    if [[ "${5}" == "-1001193563578" ]] ; then
      if [[ "${10}" == "#wtfipfs:mozilla.org" ]] ; then
        block_msg
      fi
    fi
#     tmp=$NAME
#     NAME=$(echo "$NAME" | tail -n1)
#     # NAME=$(echo "$NAME" | cut -d ":" -f 1)
#     NAME=${NAME%: }
#     NAME="**${NAME}:** "
#     qt=$(echo "$tmp" | sed '$d')
#     [[ -n "$qt" ]] && NAME="$qt
#
# $NAME"
    md_name
    if [[ -z "$TEXT" ]]; then
#      [[ $(echo "$NAME" | wc -l) -ge 3 ]] && [[ $(echo "$NAME" | grep -c -G '^$') -ge 1 ]] && echo "$NAME" | tail -n1 && echo "$NAME" | sed '/^$/,$d' && NAME=""
      if [[ $(echo "$NAME" | wc -l) -ge 3 ]]; then
        NAME=$(echo "$NAME" | tail -n1; echo "$NAME" | sed '/^$/,$d')
      fi
    else
      # if [[ "$NAME" == "C twitter: " ]]; then
      #   TEXT=$(echo "$TEXT" | sed '2,$s/^/> /' | sed '2s/^/\n/')
      # elif [[ "$NAME" == "C bot: " && "${1:0:16}" == "twitter to text:" ]]; then
      #   TEXT=$(echo "$TEXT" | sed '2,$s/^/> /' | sed '2s/^/\n/')
      # elif [[ "$NAME" == "C bot: " && "$( echo ${1} | cut -d":" -f2 )" == " twitter to text" ]]; then
      #   TEXT=$(echo "$TEXT" | sed '2,$s/^/> /' | sed '2s/^/\n/')
      # else
      #   :
      #   # if [[ -n "$(echo "$NAME" | sed '$d')" ]]; then
      #   # if [[ "$(echo "$NAME" | wc -l)" -ge 3 ]]; then
      #   #   QT=$(echo "$NAME" | sed '$d')
      #   # fi
      # fi
      TEXT="$NAME$TEXT"
      unset NAME
    fi
    ;;
  slack.*)
    if [[ "$(echo "$NAME" | wc -l)" -ge 3 ]]; then
      TEXT="$(echo "$NAME" | sed '$d')
$TEXT"
#       TEXT="$TEXT
# $(echo "$NAME" | sed '$d')"
      NAME=$(echo "$NAME" | tail -n1)
    fi
    ;;
  discord.*)
  # elif [[ "$9" == "discord" ]] ; then
    if [[ "${10}" == "ID:753567017822453861" ]] ; then
    # if [[ "${10}" == "ID:1049107401992843306" ]] ; then
      # if [[ "${3}" != "api.in" ]] ; then
      if [[ "${5}" == "#wtfipfs:mozilla.org" ]] ; then
        block_msg
      elif [[ "${5}" == "-1001503043923" ]] ; then
      # elif [[ "${5}" == "-1001193563578" ]] ; then
        block_msg
      fi
    # if [[ "${10}" == "wtfipfs" ]] ; then
    # if [[ "${10}" == "ID:753567017822453861" ]] ; then
    #   if [[ "${5}" == "#wtfipfs:matrix.org" ]] ; then
    #     block_msg
    #   elif [[ "${5}" == "-1001503043923" ]] ; then
    #     # new wtfipfs tg group
    #     block_msg
    #   fi
    # elif [[ "${10}" == "wtfipfs2" ]] ; then
    fi
#     if [[ "$NAME" == "C twitter: " ]]; then
#       :
# #      NAME="bot"
#     else
#     fi
    # if [[ "$NAME" == "C twitter: " ]]; then
    #   TEXT=$(echo "$TEXT" | sed '2,$s/^/> /' )
    # elif [[ "$NAME" == "C bot: " && "${1:0:16}" == "twitter to text:" ]]; then
    #   TEXT=$(echo "$TEXT" | sed '2,$s/^/> /')
    # elif [[ "$NAME" == "C bot: " && "$( echo ${1} | cut -d":" -f2 )" == " twitter to text" ]]; then
    #   TEXT=$(echo "$TEXT" | sed '2,$s/^/> /')
    # fi

    if [[ "$(echo "$NAME" | wc -l)" -ge 3 ]]; then
      TEXT="$(echo "$NAME" | sed '$d')
$TEXT"
#       TEXT="$TEXT
# $(echo "$NAME" | sed '$d')"
      NAME=$(echo "$NAME" | tail -n1)
    fi
    # NAME="${NAME:0:-2}"
    if [[ -z "$NAME" ]] || [[ "$NAME" == " " ]]; then
      NAME="error"
    fi
    ;;
  telegram.*)
  # elif [[ "$9" == "telegram" ]] ; then
    # if [[ "${10}" == "-1001193563578" ]] ; then
    #   block_msg
    # fi

    # if [[ "NAME" == "C twitter: " ]]; then
    #   exit 0 # another bot
    # fi
    # if [[ "NAME" == "C twitter: " ]]; then
    #   TEXT='.>)\`'
    # elif [[ "$3" == "api.tg" && "$11" != "gateway0" ]]; then
    #   TEXT='.>)\`'
#     if [[ $(echo "$NAME" | wc -l) -ge 3 ]]; then
# #      NAME=$(bash "$SH_PATH/text2markdown.sh" "$NAME" | tail -n1 | sed 's/ / */' | sed 's/: $/*: /' )
#       last=$(echo "$NAME" | tail -n1)
#
#       NAME=${last%: *}
#       P=${NAME:0:1}
#       NAME=${NAME:2}
#       NAME=$(bash "$SH_PATH/text2markdown.sh" "$NAME")
#       NAME="$P *${NAME}*: "
#
#       qt_text=$(echo "NAME" | sed '/^> /!d' | sed 's/^> //')
#       line1=$(echo "$qt_text" | head -n1)
#
#       if [[ "${line1:0:2}" == "G " || "${line1%%: *}" == "C twitter" ]]; then
#
#         msg_text=$(echo "${line1#*: }"; echo "$qt_text" |sed '1d')
#         msg_text=$(echo "$msg_text" | sed -r '$s|: https://wtfipfs\.eu\.org/[a-zA-Z0-9_./?=%-]+$||')
#
# #        msg_sender=$(echo "NAME" | head -n1 | cut -d' ' -f3- | cut -d':' -f1 )
#         msg_sender="${line1%%: *}"
#         msg_sender="${line1%%:\*\* *}"
#         msg_sender="${msg_sender#* }"
#
#
#       else
#         msg_sender="bot"
#         if [[ $( echo "$line1" | grep -c -P '^[A-Z] .*: .*' ) -eq 1 ]]; then
#           msg_text=$qt_text
#         else
#           msg_text="$P ?: $qt_text"
#         fi
#       fi
#       # use user api to send msg to tg and block this TEXT to tg
#       bash "$SH_PATH/tg.sh" settoken wtfipfs setcid "${10}" "--reply" "$msg_text" "$msg_sender" "--md" "$NAME$(bash "$SH_PATH/text2markdown.sh" "$1")"
#       TEXT='.>)\`'
#     else
#       TEXT=$(bash "$SH_PATH/text2markdown.sh" "$TEXT")
#     fi

    TEXT=$(bash "$SH_PATH/text2markdown.sh" "$TEXT")
    QT=""
    [[ $(echo "$NAME" | wc -l) -ge 3 ]] && QT=$(bash "$SH_PATH/text2markdown.sh" "$(echo "$NAME" | sed '/^$/,$d')" && echo)
    NAME=$(bash "$SH_PATH/text2markdown.sh" "$(echo "$NAME" | tail -n1)")
    # echo -n "*$(echo "$NAME" | cut -d' ' -f 2- | sed '$s|: $||')*: "
    M=$(echo "$NAME" | cut -d' ' -f1)
    NAME=$(echo "$NAME" | cut -d' ' -f 2-)
    NAME=${NAME%: }
#     NAME="$QT
# $M *$NAME*: "
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
  api.tox)
    :
    # go to edit cmd.sh
    ;;
  # api.gpt)
  api.*)
    :
    # go to edit cmd.sh
#     if [[ "$(echo "$NAME" | wc -l)" -ge 3 ]]; then
# #       TEXT="$(echo "$NAME" | sed '$d')
# # $TEXT"
#       TEXT="$TEXT
#
# $(echo "$NAME" | sed -e '/^> [^>]/!d' -e 's/^> //')"
# # $(echo "$NAME" | sed -e '/^$/,$d' -e 's/^> //')"
# # $(echo "$NAME" | sed -e '/^[^>]/,$d' -e 's/^> //')"
#       NAME=$(echo "$NAME" | tail -n1)
#     fi
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
