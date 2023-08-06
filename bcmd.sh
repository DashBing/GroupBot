#!/bin/bash
#background cmd

set -f


is_me(){

  if [[ "$username" = 'X liqsliu: ' ]]; then
    return
  else
    return 1
  fi


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
    if [[ -e $SH_PATH/.trmode_for_$gateway ]]; then
      echo -n "$username"
      bash "$SH_PATH/tr.sh" "$*" || echo "E: $?"
    elif [[ -e $SH_PATH/.botmode_for_$gateway ]]; then
      echo -n "$username"
      bash "$SH_PATH/bot.sh" "$@" || echo "E: $?"
    elif [[ -e $SH_PATH/.aimode_for_$gateway ]]; then
      echo -n "$username"
      bash "$SH_PATH/ai.sh" "$@" || echo "E: $?"
    elif [[ -e $SH_PATH/.gptmode_for_$gateway ]]; then
      echo -n "$username"
      bash "$SH_PATH/gpt.sh" "$@" || echo "E: $?"
    elif bash "$SH_PATH/faq.sh" "$text" ; then
      return 0
    else
      :
    fi
    return 0
  fi
  echo -n "$username"
  case ${cmd:1} in
  help | h)
    if [[ -z "$2" ]]; then
      [[ -e "$SH_PATH/group_help.txt" ]] && cat "$SH_PATH/group_help.txt" || echo "E: no group_help.txt"
    elif [[ "$2" == "cmd" ]]; then
      cat "$SH_PATH/group_cmd.txt"
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
    bash "$SH_PATH/ai.sh" "reset" &>/dev/null
    ;;
  bot|BOT)
    shift
    bash "$SH_PATH/bot.sh" "$@" || echo "E: $?"
    bash "$SH_PATH/bot.sh" "reset" &>/dev/null
    ;;
  gpt|GPT)
    shift
    bash "$SH_PATH/gpt.sh" "$@" || echo "E: $?"
    bash "$SH_PATH/gpt.sh" "reset" &>/dev/null
    ;;
  botmode)
    [[ -e $SH_PATH/.botmode_for_$gateway ]] && rm $SH_PATH/.botmode_for_$gateway || touch $SH_PATH/.botmode_for_$gateway
    [[ -e $SH_PATH/.botmode_for_$gateway ]] && echo "bot is here" || echo "bot is out"
    [[ -e $SH_PATH/.aimode_for_$gateway ]] && rm $SH_PATH/.aimode_for_$gateway
    [[ -e $SH_PATH/.gptmode_for_$gateway ]] && rm $SH_PATH/.gptmode_for_$gateway
    ;;
  aimode)
    [[ -e $SH_PATH/.aimode_for_$gateway ]] && rm $SH_PATH/.aimode_for_$gateway || touch $SH_PATH/.aimode_for_$gateway
    [[ -e $SH_PATH/.aimode_for_$gateway ]] && echo "AI is here" || echo "AI is out"
    [[ -e $SH_PATH/.botmode_for_$gateway ]] && rm $SH_PATH/.botmode_for_$gateway
    [[ -e $SH_PATH/.gptmode_for_$gateway ]] && rm $SH_PATH/.gptmode_for_$gateway
    ;;
  gptmode)
    [[ -e $SH_PATH/.gptmode_for_$gateway ]] && rm $SH_PATH/.gptmode_for_$gateway || touch $SH_PATH/.gptmode_for_$gateway
    [[ -e $SH_PATH/.gptmode_for_$gateway ]] && echo "chatgpt is here" || echo "chatgpt is out"
    [[ -e $SH_PATH/.aimode_for_$gateway ]] && rm $SH_PATH/.aimode_for_$gateway
    [[ -e $SH_PATH/.botmode_for_$gateway ]] && rm $SH_PATH/.botmode_for_$gateway
    ;;
  dig)
    shift
    [[ -z "$2" ]] && echo "$(dig +short "$@" || echo "E: $?")" || echo "$(dig "$@" || echo "E: $?")"
    ;;
  google | g)
    shift
    bash "$SH_PATH/google.sh" "$@" || echo "E: $?"
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
    shift
    # bash "$SH_PATH/muxiaoguo.sh" Tn_google "$@"
    # trans -brief "${@}"
    bash "$SH_PATH/tr.sh" "$*"
    ;;
  trmode)
    [[ -e $SH_PATH/.trmode_for_$gateway ]] && rm $SH_PATH/.trmode_for_$gateway || touch $SH_PATH/.trmode_for_$gateway
    [[ -e $SH_PATH/.trmode_for_$gateway ]] && echo "trmode on" || echo "trmode off"
    ;;
  trans)
    shift
    # bash "$SH_PATH/muxiaoguo.sh" Tn_google "$@"
    # trans -brief "${@}"
    bash "$SH_PATH/trans.sh" "$@"
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
    bash "$SH_PATH/note.sh" "$username" "${text:6}" || echo "E: $?"
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
    echo "E: unknown cmd > $*"
    ;;
  esac
}



if [[ "$1" == "just_get_reply" ]]; then
  text=$2
  text=$(cmds $text)
  echo -n "$text"
  exit 0

fi

echo "arg: $*"
# echo "bcmd > arg: $*" >> /tmp/bcmd.log



[[ -z "$3" ]] && exit 1
gateway=$1
username=$2
text=$3
res=$4




send_to_mt(){
  text=$1

[[ -n "$text" ]] && {
  text=$(bash "$SH_PATH/gene_res.sh" "$text" $gateway)
#  res=$(curl -s -XPOST -H 'Content-Type: application/json' -d "$text" http://127.0.0.1:4243/api/message)
  res=$(curl -s -XPOST -H 'Content-Type: application/json' -d "$text" http://127.0.0.1:4240/api/message)
echo "res: $res"
echo "json: $text"
  if [[ "$(echo "$res" | jq ".message")" != "null" ]]; then
    curl -s -XPOST -H 'Content-Type: application/json' -d "$(bash "$SH_PATH/gene_res.sh" "E: $(echo "$res" | jq -r ".message") b64: $(echo $text|base64)" $gateway)" http://127.0.0.1:4240/api/message
  else
    [[ -z "$(echo "$res" | jq -r ".text")" ]] && curl -s -XPOST -H 'Content-Type: application/json' -d "$(bash "$SH_PATH/gene_res.sh" "E: empty message" $gateway)" http://127.0.0.1:4240/api/message
  fi

}
}


  # if [[ "${text:0:6}" == ".note " ]]; then
#text=$(cmds $text)
#text=$(cmds $text 2>&1)
text=$(cmds $text 2>"$SH_PATH/error")
text=$(echo "$text"|sed 's/\r//g')
[[ -f "$SH_PATH/error" ]] && text_e=$(cat "$SH_PATH/error") && rm "$SH_PATH/error"

[[ -n "$text_e" ]] && text="$text
--
E: $text_e
"
text=$(echo "$text" | sed -r "s/\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[m|K]//g")

send_to_mt "$text"
# send_to_mt "E: $text_e"


