#!/bin/bash


export LOG_FILE=${LOG_FILE:-/dev/null}
export LOG=${LOG:-$HOME/mt.log}

# echo cmd start >> ~/tera/mt_msg.log
#export SH_PATH=$(cd $(dirname ${BASH_SOURCE[0]}); pwd )
# SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}); pwd )}
SH_PATH=${SH_PATH:-$(cd $(dirname "${BASH_SOURCE[0]}") || exit; pwd )}

send_msg_to_simplex(){
# [[ -e "$SH_PATH/DEBUG" ]] && set -x
# [[ -e "$SH_PATH/DEBUG" ]] && set +x
# get msg from simplex to mt
# curl -m 300 -s -XPOST -d "msg from mt" 127.0.0.1:4250
# res=$(curl -m 1 -s 127.0.0.1:4250) || exit 0
 # &>> $LOG_FILE
echo "send to sx: $*" &>> $LOG_FILE
echo "send to sx: $*" &>> $LOG
res=$(curl -m 2 -s -XPOST -d "$*"  127.0.0.1:4250) || return 1
echo "got from sx: $res" &>> $LOG_FILE
if [[ "$res" != "[]" ]]; then
  bash "$SH_PATH/sm_simplex.sh" "$res" &>> $LOG
fi
echo "send to sx end: $*" &>> $LOG_FILE
echo "send to sx end: $*" &>> $LOG
}



bcmd(){
  local text=$1
  local username=$2

  # [[ "$username" == "C bot: " ]] && continue
  # [[ "$username" == "C xmppbot: " ]] && continue
  # [[ "$username" == "C titlebot: " ]] && continue
  # [[ "$username" == "C twitter: " ]] && continue
  # [[ $(echo "$text" | wc -l) -ne 1 ]] && continue
qt_text=$(echo "$username" | sed '/^> /!d' | sed 's/^> //')
[[ -n "$qt_text" ]] && qt_text="
$qt_text"
  username=$(echo "$username" | tail -n1 )
  account=$(echo "$restmp" | jq -r ".account")

  # if [[ "$gateway" != "gateway2" && $(echo "$text" | wc -l) -eq 1 ]]; then
  if [[ $(echo "$text" | wc -l) -eq 1 ]]; then
    # if [[ "$gateway" == "gateway1" ]]; then
    #   gateway=gateway11
    # fi
    if [[ "$text" == "ping" ]]; then
      text=".ping"
    elif [[ -z "${username}" ]]; then
      # continue
      return 0
    elif [[ "$text" == "help" ]]; then
      # text=".help"
      nohup bash "$SH_PATH/bcmd.sh" "$gateway" "$username" ".help" "$restmp" &>/dev/null &
      sleep 3
    elif [[ $(echo "$text" | grep -c -P "^https://(mobile\.)?twitter\.com/[a-zA-Z0-9_./?=&%-]+$") -eq 1 ]]; then
      :
      # text=".tw $text" # not work because of fordiben by twitter
    # elif [[ $(echo "$text" | grep -c -P "^https://wtfipfs\.eu\.org/[a-zA-Z0-9_./?=%-]+$") -eq 1 ]]; then
    #   text=".ipfs $text only"
    elif [[ $(echo "$text" | grep -c -P "^http(s)?://[0-9a-zA-Z.-]+\.[a-zA-Z]+(:[0-9]+)?/?[\S]*(jpe?g|png|mp4|gif)$") -eq 1 ]]; then
      text=".ipfs $text only"
    elif [[ $(echo "$text" | grep -c -P "^http(s)?://[0-9a-zA-Z.-]+\.[a-zA-Z]+(:[0-9]+)?/?[\S]*$") -eq 1 ]]; then
      text=".type $text autocheck"
    fi
  else
    # [[ -z "${username}" ]] && continue
    [[ -z "${username}" ]] && return 0
  fi
  nohup bash "$SH_PATH/bcmd.sh" "$gateway" "$username" "$text" "$restmp" "$qt_text" 2>> $LOG 1>> $LOG_FILE &
}

#[[ "$(echo "$res" | jq ".[0]")" != "null" ]] && bash "$SH_PATH/cmd.sh" "$res"
#
# echo "cmd > arg: $*" >> /tmp/cmd.log

res=$1
i=0
for (( ; i < 4; i++)); do
  restmp=$(echo "$res" | jq ".[$i]")
  if [[ "$restmp" == "null" ]]; then
    break
  else
echo "start to check restmp: $restmp" &>> $LOG_FILE
    text=$(echo "$restmp" | jq -r ".text")
#    echo "$text" | sed '/^[^>]/,$d'
#    text=$(echo "$text" | sed '/^[^>]/,$!d')
    username=$(echo "$restmp" | jq -r ".username")

#    username="$(echo "$text" | head -n1 | cut -s -d ":" -f1 ): "
#    text=$(echo "$text" | cut -d" " -f3-)
#    text="${text:${#username}}"
    gateway=$(echo "$restmp" | jq -r ".gateway")
  # continue # run cmd by python: mybots.py. but not running now
  # ########################################################

    [[ "${username:0:2}" != "C " ]] && [[ "${username: -5}" != "bot: " ]] && bcmd "$text" "$username"

    # continue


    if [[ "$gateway" == "test" ]]; then
      # echo 2 > "$SH_PATH/.BUSY"
      if [[ -e "$SH_PATH/.BUSY" ]]; then
        rm "$SH_PATH/.BUSY"
      fi
    elif [[ "$gateway" == "gateway1" ]]; then
      URL=$(echo "$restmp" | jq -r ".Extra.file[0].URL")
      if [[ -z "$URL" || "$URL" == "null" ]]; then
        if [[ -z "$text" ]]; then
          continue
        else
          msg=$(bash "$SH_PATH/change_long_text.sh" "$username$text")
        fi
      else
        if [[ -n "$gateway" ]]; then
          Comment=$(echo "$restmp" | jq -r ".Extra.file[0].Comment")
          if [[ -z "$Comment" ]]; then
            msg=$(bash "$SH_PATH/change_long_text.sh" "$username$text $URL")
          else
            msg=$(bash "$SH_PATH/change_long_text.sh" "$username$text$Comment: $URL")
          fi
        fi
      fi
      if [[ -n "$msg" ]]; then
        if [[ "${username:0:2}" != "S " ]]; then
          :
          # bash "$SH_PATH/run_sh.sh" "[$restmp]" msg_for_simplex.sh
          # send_msg_to_simplex "$username$text"
          send_msg_to_simplex "$msg" 2>> $LOG 1>> $LOG_FILE
        fi
        # if [[ "$username" != "O bot: " ]]; then
        if [[ "${username:0:2}" != "O " ]]; then
echo "send to tox: $msg" &>> $LOG_FILE
          echo "$msg"
        fi
      fi
    fi



  fi

done
# [[ -e "$SH_PATH/DEBUG" ]] && set -x

# [[ -e "$SH_PATH/DEBUG" ]] && set +x






