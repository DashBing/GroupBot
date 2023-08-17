#!/bin/bash
#get msg for tox and run cmd
# export SH_PATH=$(cd $(dirname ${BASH_SOURCE[0]}); pwd )

#res="[]"
res=$(curl -m 2 -s http://127.0.0.1:4240/api/messages) || exit 0
if [[ "$res" != "[]" ]]; then
res=$(echo "$res" | jq 'del(.[].Extra.file[0].Data)') &>/dev/null || exit 0
export SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}) || exit; pwd )}
# [[ -e "$SH_PATH/DEBUG" ]] && export DEBUG=true
[[ -e "$SH_PATH/DEBUG" ]] && export LOG_FILE="$HOME/tera/mt.log" || export LOG_FILE=/dev/null
echo bash "$SH_PATH/cmd.sh" "$res" &>> $LOG_FILE
bash "$SH_PATH/cmd.sh" "$res" &>> $LOG_FILE
# date >> ~/tera/mt_msg.log
# echo "cmd res :|$res|" >> ~/tera/mt_msg.log
fi
# echo "gm" >> ~/tera/mt_msg.log
res=$(curl -m 2 -s http://127.0.0.1:4241/api/messages) || exit 0
if [[ "$res" != "[]" ]]; then
res=$(echo "$res" | jq 'del(.[].Extra.file[0].Data)') &>/dev/null || exit 0
res=$(bash "$SH_PATH/msg_for_tox.sh" "$res" 2>&1)
echo -n "$res"
export SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}) || exit; pwd )}
[[ -e "$SH_PATH/DEBUG" ]] && export LOG_FILE="$HOME/tera/mt.log" || export LOG_FILE=/dev/null
# bash "$SH_PATH/msg_for_tox.sh" "$res" &>> $LOG_FILE
echo bash "$SH_PATH/msg_for_tox.sh" "$res" &>> $LOG_FILE
echo "$res" >> $LOG_FILE
fi

