#!/bin/bash

#export SH_PATH=$(cd $(dirname ${BASH_SOURCE[0]}); pwd )
# SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}); pwd )}
SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}) || exit; pwd )}

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
    if [[ "$gateway" == "gateway1" ]]; then
    # if true; then
      # if [[ "$username" != "O bot: " ]]; then
      if [[ "${username:0:2}" != "O " ]]; then
        if [[ "$gateway" != "gateway2" ]]; then
          URL=$(echo "$restmp" | jq -r ".Extra.file[0].URL")
          if [[ -z "$URL" || "$URL" == "null" ]]; then
            if [[ -z "$text" ]]; then
              continue
            else
              :
              #            [[ "$gateway" == "gateway1" ]] && echo -n "$(echo "$text" | sed "s/^/$username/g")"
              # [[ "$gateway" == "gateway1" ]] && echo -n "$(bash "$SH_PATH/change_long_text.sh" "$username$text")"
              # echo -n "$(bash "$SH_PATH/change_long_text.sh" "$username$text")"
            fi
          else
            text=".ipfs $URL only"
          fi
        fi
      fi
    fi


            # if [[ "$gateway" == "gateway1" ]]; then
            # if [[ -n "$gateway" ]]; then
            #   gateway=gateway11
            # fi


    # continue # run cmd by python: mybots.py. but not running now
    # ########################################################

    [[ "$username" == "C bot: " ]] && continue
    [[ "$username" == "C twitter: " ]] && continue
    # [[ $(echo "$text" | wc -l) -ne 1 ]] && continue
    username=$(echo "$username" | tail -n1 )

    # if [[ "$gateway" != "gateway2" && $(echo "$text" | wc -l) -eq 1 ]]; then
    if [[ $(echo "$text" | wc -l) -eq 1 ]]; then
      # if [[ "$gateway" == "gateway1" ]]; then
      #   gateway=gateway11
      # fi
      if [[ $(echo "$text" | grep -c -P "^https://(mobile\.)?twitter\.com/[a-zA-Z0-9_./?=&%-]+$") -eq 1 ]]; then
        text=".tw $text"
      # elif [[ $(echo "$text" | grep -c -P "^https://wtfipfs\.eu\.org/[a-zA-Z0-9_./?=%-]+$") -eq 1 ]]; then
      #   text=".ipfs $text only"
      elif [[ $(echo "$text" | grep -c -P "^http(s)?://[0-9a-zA-Z.-]+\.[a-zA-Z]+(:[0-9]+)?/?[\S]*(jpe?g|png|mp4|gif)$") -eq 1 ]]; then
        text=".ipfs $text only"
      elif [[ $(echo "$text" | grep -c -P "^http(s)?://[0-9a-zA-Z.-]+\.[a-zA-Z]+(:[0-9]+)?/?[\S]*$") -eq 1 ]]; then
        text=".type $text autocheck"
      elif [[ "$text" == "help" ]]; then
        # text=".help"
        nohup bash "$SH_PATH/bcmd.sh" "$gateway" "$username" ".help" "$restmp" &>/dev/null &
        sleep 3
      elif [[ "$text" == "ping" ]]; then
        text=".ping"
      fi
    fi
    # gateway=cmd
    nohup bash "$SH_PATH/bcmd.sh" "$gateway" "$username" "$text" "$restmp" &>/dev/null &

  fi

done
