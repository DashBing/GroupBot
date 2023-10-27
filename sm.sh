#!/bin/bash
#send msg of tox(change port for other app) to matterbridge api

export SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}) || exit; pwd )}
MAX_BYTES=1371 #tox


export LOG="$HOME/mt.log"
[[ -e "$SH_PATH/DEBUG" ]] && export LOG_FILE=$LOG || export LOG_FILE=/dev/null

LOG_FILE_E="$LOG"

username=$1
text=$2
# [[ "$username" == "bot" || "$username" == "ToxBot" ]] && exit 0
#api_port=${3:-4242}
api_port=${3:-4241}
gateway=${4-gateway1}
[[ -z "$username" ]] && username="null"

[[ -z "$text" ]] && exit 1
#source /tmp/init.sh


# if [[ "${username:0:2}" == "C " ]]
# then
#   :
# elif [[ "${username:0:2}" == "T " ]]
# then
#   :
# else
#   :
#   username="O $username"
# fi

# touch /tmp/test_sm.sh
# echo "$*" > /tmp/test_sm.sh.txt

wtf1(){
  local text=$1
text="$(echo "$text" | cut -d '\' --output-delimiter='\\' -f 1- )"
echo "$text"
}
wtf(){
  local text=$1
text="$(echo "$text" | cut -d '\' --output-delimiter='\\' -f 1- )"
  text=$(echo "$text" | sed -e 's/\\/\\\\/g' -e 's/"/\\"/g' -e 's/\r//g' -e 's/\t/\\t/g' | sed -r "s/\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[m|K]//g")
[[ $( echo "$text" | wc -l ) -gt 1 ]] && text=$(echo "$text" | awk '{printf "%s\\n", $0}' | sed "s/\\\\n$//g")
echo "$text"
}

gene_res(){
local text=$1
local gateway=${2-gateway1}
local username=${3-C bot: }
# text=$(bash "$SH_PATH/change_long_text.sh" "$text" 4096)
# text=$(bash "$SH_PATH/change_long_text.sh" "$text" 1371)
cat <<EOF
{"text":"${text}","username":"${username}","gateway":"${gateway}"}
EOF
}

  # local e=$?
    # {
    # echo "E: $e"
    # echo "fail to send msg to mt: $text"
    # echo "username: $username"
    # echo "gateway: $gateway"
    # echo "api_port: $api_port"
    # # echo "export:"
    # # export
    #
    # } &>> $LOG
__send(){
  local text=$1
  local msg=$(gene_res "$text" "$gateway" "$username")
  unset http_proxy https_proxy
  curl -m 8 -s -XPOST -H 'Content-Type: application/json' -d "$msg" http://127.0.0.1:$api_port/api/message || {
  return $?
  }
}

_send(){
  local text=$1

local res=$(__send "$text" 2>"$SH_PATH/error") && {

  if [[ "$(echo "$res" | jq ".message")" != "null" ]]; then
    __send "E: $(echo "$res" | jq ".message")|${text:0:64}" 2>> $LOG 1>> $LOG
  else
    if [[ -z "$(echo "$res" | jq -r ".text")" ]]; then
      echo "the content of last msg is empty" &>> $LOG
      __send "the content of last msg is empty"
    fi
  fi

} || {
  e=$?
  echo "E: fail to send text(1)" &>> $LOG
  [[ -f "$SH_PATH/error" ]] && [[ -n "$(cat $SH_PATH/error)" ]] && {
    set -x
    __send "$text (E: $e)" 2>"$SH_PATH/error" 1>"$SH_PATH/out"
    ee=$?
    set +x
    err=$(cat "$SH_PATH/error") && rm "$SH_PATH/error"
    out=$(cat "$SH_PATH/out") && rm "$SH_PATH/out"
    # echo "E: $e" &>> $LOG
    # echo "err: $err" &>> $LOG
    # echo "out: $out" &>> $LOG
    # echo "res: $res" &>> $LOG
      echo "E: $e
text=$text
error=$err
out=$out
res=$res
" >> $LOG
    if [[ "$ee" -ne 0 ]]; then
      # echo "E: $e|$ee|$err|$out|${text:0:64}...$res" 2>> $LOG 1>> $LOG
      __send "E: $e|$ee|$err|${text:0:15}" 2>> $LOG 1>> $LOG
      __send "D: $res|$out" 2>> $LOG 1>> $LOG
    fi

  }
}

}




send(){
  # local MAX_BYTES=1371
  # local MAX_BYTES=1024
  local ulength=$(echo -n "$username"|wc -c)
  local MAX_BYTES=$[MAX_BYTES-9-ulength]
  local text=$1
  # text=$(wtf1 "$text")
  text_en=$(wtf "$text")
  local length=$(echo -n "$text_en"|wc -c)
  # if [[ ${#text} -le $MAX_BYTES ]]; then
  if [[ $length -le $MAX_BYTES ]]; then
echo "sm.sh: the length of msg is ok: $length:${text:0:256}..." &>> $LOG
    _send "$text_en"
    return $?
  fi
  echo "sm.sh: text is too long: $length:${text:0:128}..." &>> $LOG
  # shift
  local i=0
  local now=0
  local n=$[length/MAX_BYTES]
  if [[ $[length%MAX_BYTES] -ne 0 ]]; then
    let n++
  fi
  while true
  do
    # now=$[i*MAX_BYTES]
    # if [[ $((i*MAX_BYTES)) -ge ${#text} ]]; then
    if [[ $now -ge ${#text} ]]; then
      return 0
      break
    fi
    tmp=${text:$now:$MAX_BYTES}
    tmp0=$tmp
    local need_1=0
    while true
    do
      if [[ "${tmp: -1}" != $'\n' ]]; then
        if [[ "${tmp: -1}" != $'\t' ]]; then
          # if [[ "${tmp: -1}" != " " ]]; then
            if [[ -n "$(echo "$tmp"|sed -e '$d' -e '/^ *$/d')" ]]; then
              tmp=$(echo "$tmp"|sed '$d')
              need_1=1
            fi
          # fi
        fi
      fi
      tmp1=$(wtf "$tmp")
      # if [[ ${#tmp1} -gt $MAX_BYTES ]]; then
      if [[ $(echo -n "$tmp1"|wc -c) -gt $MAX_BYTES ]]; then
        tmp=${tmp::-1}
        if [[ $need_1 -eq 1 ]]; then
              need_1=0
        fi
      else
        break
      fi
    done
    if [[ $need_1 -eq 1 ]]; then
      let now++
    fi
    now=$[now+${#tmp}]

    let i++
    echo "send...$i/$n" &>> $LOG

    _send "$tmp1" || {
      return $?
    }

    # sleep 1
    username=""
    if [[ $i -ge 16 ]]; then
      echo "E: msg is too long, stop sending...$i/$n" &>> $LOG
      _send "E: msg is too long, stop sending, now $i/$n" &>> $LOG
      return 1
    fi
  done
}







username=$(wtf "$username")


send "$text"
exit $?

t=0
res=$(send "$text" 2>"$SH_PATH/error") && push_err "$res" || {
  e=$?
  let t++
  echo "E: fail to send text(1)" &>> $LOG
# [[ -f "$SH_PATH/error" ]] && {
[[ -f "$SH_PATH/error" ]] && [[ -n "$(cat $SH_PATH/error)" ]] && {
  set -x
  send "$text (E: $e)" 2>"$SH_PATH/error" 1>"$SH_PATH/out"
  set +x
  err=$(cat "$SH_PATH/error") && rm "$SH_PATH/error"
  out=$(cat "$SH_PATH/out") && rm "$SH_PATH/out"
  echo "E: $e" &>> $LOG
  echo "err: $err" &>> $LOG
  echo "out: $out" &>> $LOG
  echo "res: $res" &>> $LOG
#   echo "E: $e
# fail to run cmd
# text=$text
# error=$err
# out=$out
# " >> $LOG
[[ -n "$err" ]] && {
  let t++
}

}
  # send "E: failed to send text: ${text:0:10}...|$e|$r"
}
# echo "res: $res"
# echo "json: $text"
# echo "res :|$res|" >> ~/tera/mt_msg.log
[[ $t -eq 2 ]] && {
push_err "E: $e: ${text:0:64}...|$r|$res" 2>> $LOG 1>> $LOG_FILE
}

if [[ -n "$res" ]]; then
  push_err "$res" 2>> $LOG 1>> $LOG_FILE
fi
