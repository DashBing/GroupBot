#!/bin/bash
#send msg from simplex to mt


send_msg_mt(){
text=$(echo "$1"|cut -d' ' -f2)
username=$(echo "$1"|cut -d':' -f1)
bash "$SH_PATH/sm.sh" "$username" "$text" 4247
}

tmp=$1
while true
do
  if [[ -z "$tmp" ]]; then
    break
  else
    msg=$(echo "$tmp" | sed '/^SPLIT_FOR_MT$/,$d')
    send_msg_mt "$msg"
  fi
  tmp=$(echo "$tmp" | sed '1,/^SPLIT_FOR_MT$/d')
done
