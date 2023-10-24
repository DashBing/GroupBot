#!/bin/bash
#send msg of tox(change port for other app) to matterbridge api
# export SH_PATH=$(cd $(dirname ${BASH_SOURCE[0]}); pwd )
export SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}) || exit; pwd )}
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

_send(){
  local text=$1
# curl -m 2 -s -XPOST -H 'Content-Type: application/json' -d "$(bash "$SH_PATH/"gene_res.sh "$text" "$gateway" "$username")" http://127.0.0.1:$api_port/api/message || exit 0
curl -m 2 -s -XPOST -H 'Content-Type: application/json' -d "$(bash "$SH_PATH/"gene_res.sh "$text" "$gateway" "$username")" http://127.0.0.1:$api_port/api/message
}
send(){
  local MAX_BYTES=1371
  # local MAX_BYTES=1024
  MAX_BYTES=$[MAX_BYTES-5-${#username}]
  local text=$1
  if [[ ${#text} -le $MAX_BYTES ]]; then
    echo "sm.sh: the length of msg is ok: ${#text}" &>> $LOG_FILE
    _send "$@"
    return
  fi
  echo "sm.sh: text is too long: ${#text}" &>> $LOG_FILE
  shift
  local i=0
  local n=$[${#text}/MAX_BYTES]
  if [[ $[${#text}%MAX_BYTES] -ne 0 ]]; then
    let n++
  fi
  while true
  do
    if [[ $((i*MAX_BYTES)) -ge ${#text} ]]; then
      break
    fi
    echo "send...$i/$n" &>> $LOG_FILE
    tmp=${text:$((i*MAX_BYTES)):$MAX_BYTES}
    _send "$tmp
$i/$n" "$@" || return $?
    sleep 1
    let i++
  done
}

_push_err(){
  local res=$1
  if [[ "$(echo "$res" | jq ".message")" != "null" ]]; then
    date &>> $LOG_FILE
    echo "res :|$res|" >> $LOG_FILE
    msg=$(echo "$res" | jq ".message")
    res=$(send "E: mt api: $msg res: $res") 
    if [[ "$(send "E: mt api: $msg res: $res" | jq ".message")" != "null" ]]; then
      if [[ "$(send "E: mt api: $msg res_b64: $(echo "$res"|base64)" | jq ".message")" != "null" ]]; then
        if [[ "$(send "E: can't send res to mt api: $msg" | jq ".message")" != "null" ]]; then
          if [[ "$(send "E: can't send res to mt api, msg_b64: $(echo "$msg"|base64)" | jq ".message")" != "null" ]]; then
            echo "E: can't send text and err msg to mt api: |$msg|$res|" >> $LOG_FILE
            if [[ "$(send "E: can't send res and err msg to mt api" | jq ".message")" != "null" ]]; then
              :
            fi
          fi
        fi
      fi
    fi
  fi
}


push_err(){
  local res=$1

  if ! echo "$res" | jq ".message" &>/dev/null; then
    res=$(send "$res ") || {
      _push_err "failed to send: $res"
      exit 1
    }
    _push_err "$res"
  elif [[ "$(echo "$res" | jq ".message")" != "null" ]]; then
    _push_err "$res"
  else
    if [[ -z "$(echo "$res" | jq -r ".text")" ]]; then
      send "E: empty message"
    fi
  fi

}


res=$(send "$text" 2>"$SH_PATH/error") || {
  e=$?
# [[ -f "$SH_PATH/error" ]] && {
[[ -f "$SH_PATH/error" ]] && [[ -n "$(cat $SH_PATH/error)" ]] && {
  set -x
  send "$text" 2>"$SH_PATH/error" 1>"$SH_PATH/out"
  set +x
  r=$(cat "$SH_PATH/error") && rm "$SH_PATH/error"
  res=$(cat "$SH_PATH/out") && rm "$SH_PATH/out"
}
  push_err "E: failed to send text: $text|$e|$r"
  if [[ -n "$res" ]]; then
    push_err "$res"
  fi
  exit
}
# echo "res: $res"
# echo "json: $text"
# echo "res :|$res|" >> ~/tera/mt_msg.log
push_err "$res"




