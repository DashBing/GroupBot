#!/bin/bash


export LOG_FILE=${LOG_FILE:-/dev/null}

# echo cmd start >> ~/tera/mt_msg.log
#export SH_PATH=$(cd $(dirname ${BASH_SOURCE[0]}); pwd )
# SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}); pwd )}
SH_PATH=${SH_PATH:-$(cd $(dirname "${BASH_SOURCE[0]}") || exit; pwd )}

send_msg_to_simplex(){
# get msg from simplex to mt
# curl -m 300 -s -XPOST -d "msg from mt" 127.0.0.1:4250
# res=$(curl -m 1 -s 127.0.0.1:4250) || exit 0
res=$(curl -m 5 -s -XPOST -d "$*"  127.0.0.1:4250) || exit 0
if [[ "$res" != "[]" ]]; then
  bash "$SH_PATH/sm_simplex.sh" "$res" &>> $LOG_FILE
fi
}



bcmd(){
  local text=$1

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
      continue
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
    [[ -z "${username}" ]] && continue
  fi
  nohup bash "$SH_PATH/bcmd.sh" "$gateway" "$username" "$text" "$restmp" "$qt_text" &


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

    [[ "${username:0:2}" == "C " ]] || {
      bcmd "$text" &>> $LOG_FILE
    }


    if [[ "$gateway" == "test" ]]; then
      # echo 2 > "$SH_PATH/.BUSY"
      rm "$SH_PATH/.BUSY"
    elif [[ "$gateway" == "gateway1" ]]; then
    # if true; then
      URL=$(echo "$restmp" | jq -r ".Extra.file[0].URL")
      if [[ -z "$URL" || "$URL" == "null" ]]; then
        if [[ -z "$text" ]]; then
          continue
        else
          #            [[ "$gateway" == "gateway1" ]] && echo -n "$(echo "$text" | sed "s/^/$username/g")"
          # [[ "$gateway" == "gateway1" ]] && echo -n "$(bash "$SH_PATH/change_long_text.sh" "$username$text")"
          # echo -n "$(bash "$SH_PATH/change_long_text.sh" "$username$text")"
          # echo "$(bash "$SH_PATH/change_long_text.sh" "$username$text")"
          msg="$(bash "$SH_PATH/change_long_text.sh" "$username$text")"
        fi
      else
        # if [[ "$gateway" == "gateway1" ]]; then
        if [[ -n "$gateway" ]]; then
          Comment=$(echo "$restmp" | jq -r ".Extra.file[0].Comment")
          if [[ -z "$Comment" ]]; then
#              echo -n "$username$text$URL"
            # echo -n "$(bash "$SH_PATH/change_long_text.sh" "$username$text $URL")"
            # echo "$(bash "$SH_PATH/change_long_text.sh" "$username$text $URL")"
            msg="$(bash "$SH_PATH/change_long_text.sh" "$username$text $URL")"
          else
            # text="$username$Comment: $URL"
            # echo -n "$(bash "$SH_PATH/change_long_text.sh" "$username$text$Comment: $URL")"
            # echo "$(bash "$SH_PATH/change_long_text.sh" "$username$text$Comment: $URL")"
            msg="$(bash "$SH_PATH/change_long_text.sh" "$username$text$Comment: $URL")"
          fi
        fi
      fi
      if [[ -n "$msg" ]]; then
        if [[ "${username:0:2}" != "S " ]]; then
          # bash "$SH_PATH/run_sh.sh" "[$restmp]" msg_for_simplex.sh
          # send_msg_to_simplex "$username$text"
          send_msg_to_simplex "$msg"
        fi
        # if [[ "$username" != "O bot: " ]]; then
        if [[ "${username:0:2}" != "O " ]]; then
          echo "$msg"
        fi
      fi
    fi








  fi

done
