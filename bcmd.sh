#!/bin/bash
#background cmd

export LOG_FILE=${LOG_FILE:-/dev/null}


echo "bcmd start" >> $LOG_FILE
set -f


is_me(){

  if [[ "$username" = 'X liqsliu: ' ]]; then
    return
  else
    return 1
  fi


}


changeai(){
    [[ -e $SH_PATH/.mode_for_${1}_${2} ]] && local m=1
    # (cd $SH_PATH && rm .mode_* )
    (cd $SH_PATH && {
      for f in `ls -a|grep '^\.mode_'`;do
        # echo $f
        rm $f
      done
    }
    )
    if [[ -n "$m" ]]; then
      echo "${1} is out"
    else
      touch $SH_PATH/.mode_for_${1}_${2}
      echo "${1} is here"
    fi
    echo $1 > $SH_PATH/.mode_cur
}


SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}) || exit; pwd )}

cmds() {
  # cmd="$*"
  if [[ "${text:0:2}" == ". " ]]; then
    return 0
  fi
  cmd="$1"
  # if [[ "$cmd" == "pong" ]]; then
  #   cmd=".pong"
  # else
  #   cmd=$1
  # fi
  # if [[ "${cmd:0:1}" != "." ]] && [[ "${cmd:0:1}" != "/" ]]; then
  if [[ "${cmd:0:1}" != "." ]]; then
    if bash "$SH_PATH/faq.sh" "$text" ; then
      return 0
    elif [[ -e $SH_PATH/.mode_for_ai_$gateway ]]; then
      echo -n "$username"
      bash "$SH_PATH/ai.sh" "$text" || echo "E: $?"
    elif [[ -e $SH_PATH/.mode_for_bd_$gateway ]]; then
      echo -n "$username"
      bash "$SH_PATH/bd.sh" "$text" || echo "E: $?"
    # elif [[ -e $SH_PATH/.mode_for_bot_$gateway ]]; then
    #   echo -n "$username"
    #   bash "$SH_PATH/bot.sh" "$text" || echo "E: $?"
    # elif [[ -e $SH_PATH/.mode_for_gpt_$gateway ]]; then
    #   echo -n "$username"
    #   bash "$SH_PATH/gpt.sh" "$text" || echo "E: $?"
    elif echo "$text" | tail -n1 | grep -q -G "^> " && echo "$text" | head -n1 | grep -q -G "^> "; then
      return 0
    elif [[ -e $SH_PATH/.mode_for_tr_$gateway ]]; then
      echo -n "$username"
      bash "$SH_PATH/tr.sh" "$text" || echo "E: $?"
    fi
    return 0
  fi
  echo -n "$username"
  case ${cmd:1} in
  help|h)
    if [[ -z "$2" ]]; then
      [[ -e "$SH_PATH/group_help.txt" ]] && cat "$SH_PATH/group_help.txt" || echo "E: no group_help.txt"
      [[ -e "$SH_PATH/group_help_bot.txt" ]] && echo && cat "$SH_PATH/group_help_bot.txt"
      [[ -e "$SH_PATH/group_help_rule.txt" ]] && echo && cat "$SH_PATH/group_help_rule.txt"
    # elif [[ "$2" == "cmd" ]]; then
    #   cat "$SH_PATH/group_cmd.txt"
    else
      [[ -e "$SH_PATH/group_help_${2}.txt" ]] && cat "$SH_PATH/group_help_$2.txt" || echo "E: no group_help_${2}.txt"
    fi
    ;;
  cmd)
    cat "$SH_PATH/group_cmd.txt"
    ;;
  echo)
    echo -e "${text#.echo }"
    ;;
  ok)
    rm "$SH_PATH/STOP"
    if [[ -e "$SH_PATH/STOP" ]]; then
      echo stoped
    else
      echo running
    fi
    ;;
  stop|sb)
    if [[ -e "$SH_PATH/STOP" ]]; then
      rm "$SH_PATH/STOP"
      echo running
    else
      touch "$SH_PATH/STOP"
      echo stoped
    fi
    ;;
  debug)
      echo ".debugcmd?"
    ;;
  debugcmd)
    # if [[ "$2" = "cmd" ]]; then
    [[ -e "$SH_PATH/DEBUG" ]] && {
      rm "$SH_PATH/DEBUG"
      echo "debug off"
    } || {
      touch "$SH_PATH/DEBUG"
      echo "debug on"
    }
    # fi
    ;;
  ping)
    if [[ -z "$2" ]]; then
      echo "pong"
      # if is_me; then
      #   echo "pong"
      # fi

    else
      local host=$(echo "$2" | grep -o -P "[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+" | head -n1)
      [[ -z "$host" ]] && host=$(echo "$2" | grep -o -P "[0-9a-zA-Z.-]+\.[a-zA-Z]+" | head -n1)
      echo -n "${host}: "
      local ms=$(ping -W 5 -c 1 $host | cut -d "=" -s -f4)
      [[ -z "$ms" ]] && echo "超时" || echo "$ms"
    fi
    ;;
  qy)
    # shift
    bash "$SH_PATH/qy.sh" "$@" || echo "E: $?"
    ;;
  ai|AI)
    shift
    bash "$SH_PATH/ai.sh" "$@" || echo "E: $?"
    ;;
  bd|BD)
    shift
    bash "$SH_PATH/bd.sh" "$@" || echo "E: $?"
    ;;
  bdi)
    shift
    bash "$SH_PATH/bdi.sh" "$@" || echo "E: $?"
    ;;
  bot|BOT)
    shift
    bash "$SH_PATH/bot.sh" "$@" || echo "E: $?"
    bash "$SH_PATH/bot.sh" "reset" &>/dev/null
    ;;
  gpt|GPT)
    return 0
  #   shift
  #   bash "$SH_PATH/gpt.sh" "$@" || echo "E: $?"
  #   bash "$SH_PATH/gpt.sh" "reset" &>/dev/null
    ;;
  gptr|gt|gtz|se|img|voice)
    return 0
    ;;
  gptmode)
    return 0
    # changeai gpt $gateway
    ;;
  botmode)
    exit 1
    changeai bot $gateway
    ;;
  aimode)
    changeai ai $gateway
    ;;
  bdmode)
    changeai bd $gateway
    ;;
  dig)
    shift
    [[ -z "$2" ]] && echo "$(dig +short "$@" || echo "E: $?")" || echo "$(dig "$@" || echo "E: $?")"
    ;;
  google | g)
    shift
    bash "$SH_PATH/google.sh" "$@" || echo "E: $?"
    ;;
  is)
    bash "$SH_PATH/is.sh" "$@" || echo "E: $?"
    ;;
  an | ia)
    shift
    bash "$SH_PATH/an.sh" "$@" || echo "E: $?"
    ;;
  icp)
    shift
    bash "$SH_PATH/icp.sh" "$@" || echo "E: $?"
    ;;
  tw)
    shift
    bash "$SH_PATH/twitter_to_text.sh" "$@" || echo "E: $?"
    ;;
  ip | nali*)
    if [[ -z "$2" ]]; then
      echo "ip \$domain/\$ip"
      echo
      echo "https://github.com/out0fmemory/nali"
    else
      if [[ "$1" == ".ip" ]]; then
        if [[ $(echo "$2" | grep -c -P "[0-9a-zA-Z.-]+\.[a-zA-Z]+" | head -n1) -eq 1 ]]; then
          local host=$(echo "$2" | grep -o -P "[0-9a-zA-Z.-]+\.[a-zA-Z]+" | head -n1)
          echo "$host"
          echo -n "from us: "
          nali-dig +short "$host" || echo "E: $?"
          echo -n "fake cn: "
          nali-dig @8.8.8.8 +subnet=114.114.114.114/24 +short "$host" || echo "E: $?"
#          echo -n "114(from cn): ";  nali-dig @172.22.0.6 -p 54 +timeout=2 +short "$host" || echo "E: $?"
#          echo -n "ali(from cn): ";  nali-dig @172.22.0.7 -p 55 +timeout=2 +short "$host" || echo "E: $?"
          echo -n "114(from us): "
          nali-dig @114.114.114.114 +timeout=2 +short "$host" || echo "E: $?"
          echo -n "ali(from us): "
          nali-dig @223.5.5.5 +timeout=2 +short "$host" || echo "E: $?"
          echo -n "ipv6 from us: "
          nali-dig +short aaaa "$host" || echo "E: $?"
        elif [[ $(echo "$2" | grep -c -P "[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+") -eq 1 ]]; then
          local host=$(echo "$2" | grep -o -P "[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+" | head -n1)
          echo "$host"
          echo -n "纯真: "
          nali "$host" | grep -o -P "\[.*\]" | grep -o -P "[^[\]]+" || echo "E: $?"
          # echo "$res"
        else
          echo "W: 格式不正确: $2"
        fi
      else
        nali=${1:1}
        shift
        "$nali" "$@" || echo "E: $?"
      fi
    fi
    ;;
  ip6)
    if [[ -z "$2" ]]; then
      echo "ip6 \$domain/\$ip"
    else
      if [[ $(echo "$2" | grep -c -P "[0-9a-zA-Z.-]+\.[a-zA-Z]+" | head -n1) -eq 1 ]]; then
        local host=$(echo "$2" | grep -o -P "[0-9a-zA-Z.-]+\.[a-zA-Z]+" | head -n1)
        echo "$host"
        echo -n "from us: "
        nali-dig +short aaaa "$host" || echo "E: $?"
        echo -n "fake cn: "
        nali-dig @8.8.8.8 +subnet=114.114.114.114/24 +short aaaa "$host" || echo "E: $?"
        echo -n "114(from us): "
        nali-dig @114.114.114.114 +timeout=2 +short aaaa "$host" || echo "E: $?"
        echo -n "ali(from us): "
        nali-dig @223.5.5.5 +timeout=2 +short aaaa "$host" || echo "E: $?"
      else
        echo "W: 格式不正确: $2"
      fi
    fi
    ;;
  ipfs)
    if [[ -z "$2" ]]; then
      echo ".ipfs \$URL [all|tmp|*only dtube]"
    else
      # echo "for: $2"
#      echo -n "$username"
      #bash "$SH_PATH/file_to_ipfs.sh" "$(bash "$SH_PATH/link_to_file.sh" "$2")" "${3}" || echo "E: $?"
      file_path=$(bash "$SH_PATH/link_to_file.sh" "$2")
      [[ -f "$file_path" ]] && bash "$SH_PATH/file_to_ipfs.sh" "$file_path" "${3}" || {
        echo "E: $file_path"
      }
    fi
    ;;
  sf)
    echo -n "https://managedway.dl.sourceforge.net/project/"
    echo "${2%/download}" | cut -d'/' -f5,7-
    ;;
  tr)
    # shift
    # bash "$SH_PATH/muxiaoguo.sh" Tn_google "$@"
    # trans -brief "${@}"
    # bash "$SH_PATH/tr.sh" "$*" || echo "E: $?"
    local tmp
    tmp=${text#\.tr}
    tmp=${tmp# }
    bash "$SH_PATH/tr.sh" "$tmp" || echo "E: $?"
    ;;
  trmode)
    [[ -e $SH_PATH/.mode_for_tr_$gateway ]] && rm $SH_PATH/.mode_for_tr_$gateway || touch $SH_PATH/.mode_for_tr_$gateway
    [[ -e $SH_PATH/.mode_for_tr_$gateway ]] && echo "trmode on" || echo "trmode off"
    ;;
  trans)
    shift
    # bash "$SH_PATH/muxiaoguo.sh" Tn_google "$@"
    # trans -brief "${@}"
    # echo bash "$SH_PATH/trans.sh" "$@" &>>~/tera/mt_msg.log
    bash "$SH_PATH/trans.sh" "$@" || echo "E: $?"
    ;;
  # pong | xd)
  #   shift
  #   echo
  #   echo pong
  #   echo pong
  #   ;;
  type)
    if [[ -z "$2" ]]; then
      echo ".type \$URL"
    else
      bash "$SH_PATH/link_to_file.sh" "$2" type "$3" || echo "E: $?"
    fi
    ;;
  note)
    shift
    # bash "$SH_PATH/note.sh" "$username" "$@" || echo "E: $?"
    # echo bash "$SH_PATH/note.sh" "$username" "${text:6}" &>>~/tera/mt_msg.log
    # bash "$SH_PATH/note.sh" "$username" "${text:6}" &>>~/tera/mt_msg.log
    bash "$SH_PATH/note.sh" "$username" "${text:6}$qt_text" || echo "E: $?"
    ;;
  faq)
    bash "$SH_PATH/faq.sh" "$text" "$username" || echo "E: $?"
    ;;
  hhsh | wtf)
    shift
    bash "$SH_PATH/nbnhhsh.sh" "$@" || echo "E: $?"
    ;;
  uptime)
    if [[ -z "$2" ]]; then
      uptime
      echo
      free -h
      echo
      df -h
    fi
    ;;
  testcmd)
    if [[ -z "$2" ]]; then
      nali-dig -h
    fi
    ;;
  *)
    # echo "E: unknown cmd > $*"
    echo '?'
    ;;
  esac
}



if [[ "$1" == "just_get_reply" ]]; then
  text=$2
  text=$(cmds $text)
  echo -n "$text"
  exit 0

fi

# echo "arg: $*"
echo "bcmd.sh arg: $*" >> $LOG_FILE


send(){
  # curl -s -XPOST -H 'Content-Type: application/json' -d "$(bash "$SH_PATH/gene_res.sh" "$1" $gateway)" http://127.0.0.1:4240/api/message
  bash "$SH_PATH/sm.sh" bot "$text" 4240 $gateway
}


_push_err(){
  local res=$1
  if [[ "$(echo "$res" | jq ".message")" != "null" ]]; then
    date &>> $LOG_FILE
    echo "res :|$res|" >> $LOG_FILE
    msg=$(echo "$res" | jq ".message")
    res=$(send "E: mt api: $msg res: $res") 
    if [[ "$(send "E: mt api: $msg res: $res" | jq ".message")" != "null" ]]; then
      if [[ "$(send "E: mt api: $msg res_b64: $(echo "$res"|base64)" | jq ".message")" != "null" ]]; then
        if [[ "$(send "E: can't send res to mt api: $msg" | jq ".message")" != "null" ]]; then
          if [[ "$(send "E: can't send res to mt api, msg_b64: $(echo "$msg"|base64)" | jq ".message")" != "null" ]]; then
            echo "E: can't send text and err msg to mt api: |$msg|$res|" >> $LOG_FILE
            if [[ "$(send "E: can't send res and err msg to mt api" | jq ".message")" != "null" ]]; then
              :
            fi
          fi
        fi
      fi
    fi
  fi
}


push_err(){
  local res=$1

  if ! echo "$res" | jq ".message" &>/dev/null; then
    res=$(send "$res ") || {
      _push_err "failed to send: $res"
      exit 1
    }
    _push_err "$res"
  elif [[ "$(echo "$res" | jq ".message")" != "null" ]]; then
    _push_err "$res"
  else
    if [[ -z "$(echo "$res" | jq -r ".text")" ]]; then
      send "E: empty message"
    fi
  fi

}


[[ -z "$3" ]] && exit 1
gateway=$1
username=$2
text=$3
res=$4
# username=$(echo "$restmp" | jq -r ".username")
qt_text=$5



echo "b0 :|$text|" >> $LOG_FILE
  # if [[ "${text:0:6}" == ".note " ]]; then
#text=$(cmds $text)
#text=$(cmds $text 2>&1)
out=$(cmds $text 2>"$SH_PATH/error") || {
  e=$?
# [[ -f "$SH_PATH/error" ]] && {
[[ -f "$SH_PATH/error" ]] && [[ -n "$(cat $SH_PATH/error)" ]] && {
  set -x
  cmds $text 2>"$SH_PATH/error" 1>"$SH_PATH/out"
  set +x
  text=$(cat "$SH_PATH/out") && rm "$SH_PATH/out"
  r=$(cat "$SH_PATH/error") && rm "$SH_PATH/error"
}
  push_err "E: failed to run cmd: $text|$e|$r"
  exit 1
}

if [[ -f "$SH_PATH/error" ]] && [[ -n "$(cat $SH_PATH/error)" ]]; then
  [[ -e "$SH_PATH/DEBUG" ]] && {
    set -x
    cmds $text 2>"$SH_PATH/error" 1>"$SH_PATH/out"
    set +x
    tout=$(cat "$SH_PATH/out") && rm "$SH_PATH/out"
  }
  text_e=$(cat "$SH_PATH/error") && rm "$SH_PATH/error"
fi
text=$tout

[[ -n "$text_e" ]] && text="$text
--
E: $text_e" || {
  [[ -z "$text" ]] && exit 0
  [[ "$text" = "$username" ]] && exit 0
}

# text=$(echo "$text"|sed 's/\r//g')
# text=$(echo "$text" | sed -r "s/\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[m|K]//g")

# send_to_mt "$text"
# send_to_mt "E: $text_e"



echo "b1 :|$text|" >> $LOG_FILE

  [[ -z "$text" ]] && exit
  # text=$(bash "$SH_PATH/gene_res.sh" "$text" $gateway)

# echo "b2 :|$text|" >> ~/tera/mt_msg.log
#  res=$(curl -s -XPOST -H 'Content-Type: application/json' -d "$text" http://127.0.0.1:4243/api/message)
# bash "$SH_PATH/sm.sh" bot "$text" 4240 $gateway || echo "E: $?"
send "$text" || echo "E: $?"
exit 0

#下面的代码暂时废弃

res=$(send "$text" 2>"$SH_PATH/error") || {
  e=$?
# [[ -f "$SH_PATH/error" ]] && {
[[ -f "$SH_PATH/error" ]] && [[ -n "$(cat $SH_PATH/error)" ]] && {
  set -x
  send "$text" 2>"$SH_PATH/error" 1>"$SH_PATH/out"
  set +x
  r=$(cat "$SH_PATH/error") && rm "$SH_PATH/error"
  res=$(cat "$SH_PATH/out") && rm "$SH_PATH/out"
}
  push_err "E: failed to send text: $text|$e|$r"
  if [[ -n "$res" ]]; then
    push_err "$res"
  fi
  exit
}
# echo "res: $res"
# echo "json: $text"
# echo "res :|$res|" >> ~/tera/mt_msg.log
push_err "$res"

