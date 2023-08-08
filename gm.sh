#!/bin/bash
#get msg for tox and run cmd
# export SH_PATH=$(cd $(dirname ${BASH_SOURCE[0]}); pwd )
SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}) || exit; pwd )}

#res="[]"
res=$(curl -m 2 -s http://127.0.0.1:4240/api/messages) || exit 0
if [[ "$res" != "[]" ]]; then
res=$(echo "$res" | jq 'del(.[].Extra.file[0].Data)') &>/dev/null || exit 0
bash "$SH_PATH/cmd.sh" "$res"
# date >> ~/tera/mt_msg.log
# echo "cmd res :|$res|" >> ~/tera/mt_msg.log
fi
# echo "gm" >> ~/tera/mt_msg.log
res=$(curl -m 2 -s http://127.0.0.1:4241/api/messages) || exit 0
if [[ "$res" != "[]" ]]; then
res=$(echo "$res" | jq 'del(.[].Extra.file[0].Data)') &>/dev/null || exit 0
bash "$SH_PATH/msg_for_tox.sh" "$res"
fi

