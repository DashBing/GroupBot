#!/bin/bash

#export SH_PATH=$(cd $(dirname ${BASH_SOURCE[0]}); pwd )
# SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}); pwd )}
SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}) || exit; pwd )}
#4247

send_msg_to_simplex(){
# get msg from simplex to mt
# curl -m 300 -s -XPOST -d "msg from mt" 127.0.0.1:4250
# res=$(curl -m 1 -s 127.0.0.1:4250) || exit 0
res=$(curl -m 2 -s -XPOST -d "$*"  127.0.0.1:4250) || exit 0
if [[ "$res" != "[]" ]]; then
  bash "$SH_PATH/sm_simplex.sh" "$msg"
fi
}


res=$1
i=0
for (( ; i < 4; i++)); do

  restmp=$(echo "$res" | jq ".[$i]")
  if [[ "$restmp" == "null" ]]; then
    break
  else
    text=$(echo "$restmp" | jq -r ".text")
    username=$(echo "$restmp" | jq -r ".username")
    gateway=$(echo "$restmp" | jq -r ".gateway")
    send_msg_to_simplex "$username: $text"
  fi

done
