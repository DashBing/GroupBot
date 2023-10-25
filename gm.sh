#!/bin/bash
#get msg for tox and run cmd
# export SH_PATH=$(cd $(dirname ${BASH_SOURCE[0]}); pwd )

set_log(){
export SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}) || exit; pwd )}
[[ -e "$SH_PATH/DEBUG" ]] && export LOG_FILE="$HOME/tera/mt.log" || export LOG_FILE=/dev/null
  busy=1
}

delete_raw(){
res=$(echo "$res" | jq 'del(.[].Extra.file[0].Data)') &>/dev/null || exit 0
  set_log
}

send_err(){
  local ll=${1:-cmd.sh}
  echo bash "$SH_PATH/$ll" "$res" &>> $LOG_FILE
  bash "$SH_PATH/$ll" "$res" 1> "$SH_PATH/.STDOUT" 2> "$SH_PATH/.ERROR"
  local text=$(cat "$SH_PATH/.STDOUT"
  echo "---"
  cat "$SH_PATH/.ERROR")
  bash "$SH_PATH/$ll" "C bot" "$text" 4240 &>> $LOG_FILE

}
send_err2(){
  local ll=${1:-cmd.sh}
  bash "$SH_PATH/$ll" "$res" &>> $LOG_FILE || {
    send_err "$ll"
  }
}



res=$(curl -m 1 -s http://127.0.0.1:4241/api/messages) || exit 0
if [[ "$res" != "[]" ]]; then
  delete_raw
bash "$SH_PATH/msg_for_tox.sh" "$res" 2>> $LOG_FILE || {
  send_err msg_for_tox.sh
}
fi

max=30 #3s
min=2
if [[ "$busy" == "1" ]]; then
  busy=$min
else
export SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}) || exit; pwd )}
  busy=$(cat "$SH_PATH/.BUSY")
  # busy=$[busy*2]
  busy=$[busy+1]
  if [[ $busy -ge $max ]]; then
    busy=$max
    echo max 1>&2
  else
    echo $busy 1>&2
  fi
  sleep $[busy/10].$[busy%10]
fi

echo $busy > "$SH_PATH/.BUSY"


nohup bash "$SH_PATH/bgm.sh" &>/dev/null &
