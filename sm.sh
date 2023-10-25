#!/bin/bash
#send msg of tox(change port for other app) to matterbridge api


. "$SH_PATH/init_for_gmsm.sh"

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
  local text_en=$(bash "$SH_PATH/"gene_res.sh "$text" "$gateway" "$username")
  echo "sm.sh: text_en: $text_en" >> $LOG_FILE
# res=$(curl -m 9 -s -XPOST -H 'Content-Type: application/json' -d "$text_en" http://127.0.0.1:$api_port/api/message)
# curl -m 3 -s -XPOST -H 'Content-Type: application/json' -d "$text_en" http://127.0.0.1:$api_port/api/message || {
#   echo "sm.sh: send return code: $?" >> $LOG_FILE
#   export  >> $LOG_FILE
# echo curl -m 9 -s -XPOST -H 'Content-Type: application/json' -d "$text_en" http://127.0.0.1:$api_port/api/message >> $LOG_FILE
# } && echo "sm.sh: send return code: $?" >> $LOG_FILE
unset http_proxy https_proxy
curl -m 3 -s -XPOST -H 'Content-Type: application/json' -d "$text_en" http://127.0.0.1:$api_port/api/message
}

send(){
  local MAX_BYTES=1371
  # local MAX_BYTES=1024
  MAX_BYTES=$[MAX_BYTES-9-${#username}]
  local text=$1
  if [[ ${#text} -le $MAX_BYTES ]]; then
echo "sm.sh: the length of msg is ok: ${#text}:${text:0:10}..." &>> $LOG_FILE
    _send "$text"
    return $?
  fi
  echo "sm.sh: text is too long: ${#text}" &>> $LOG_FILE
  # shift
  local i=0
  local now=0
  local n=$[${#text}/MAX_BYTES]
  if [[ $[${#text}%MAX_BYTES] -ne 0 ]]; then
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
    if [[ "${tmp: -1}" != $'\n' ]]; then
      if [[ "${tmp: -1}" != $'\t' ]]; then
        # if [[ "${tmp: -1}" != " " ]]; then
          if [[ -n "$(echo "$tmp"|sed -e '$d' -e '/^ *$/d')" ]]; then
            tmp=$(echo "$tmp"|sed '$d')
            let now++
          fi
        # fi
      fi
    fi
    now=$[now+${#tmp}]

    let i++
    echo "send...$i/$n" &>> $LOG_FILE
    local res=$(_send "$tmp") || {
      if [[ -n "$res" ]]; then
        echo "$res"
      fi
      return $?
    }
# $i/$n" "$@" || return $?
    username=""
    if [[ $i -ge 9 ]]; then
      echo "fixme...$i/$n" &>> $LOG_FILE
      return 1
    fi
    sleep 0.5
  done
}

_push_err(){
  local res=$1
  if [[ "$(echo "$res" | jq ".message")" != "null" ]]; then
    date &>> $LOG_FILE
    echo "res :|$res|" >> $LOG_FILE
    msg=$(echo "$res" | jq ".message") && send "E: mt api res msg: $msg" && return $?
    # res=$(send "E: mt api: $res") && return $?
    if [[ "$(send "E: mt api: $msg res: $res" | jq ".message")" != "null" ]]; then
      if [[ "$(send "E: mt api: $msg res_b64: $(echo "$res"|base64)" | jq ".message")" != "null" ]]; then
        if [[ "$(send "E: can't send res to mt api: $msg" | jq ".message")" != "null" ]]; then
          if [[ "$(send "E: can't send res to mt api, msg_b64: $(echo "$msg"|base64)" | jq ".message")" != "null" ]]; then
            echo "E: can't send text and err msg to mt api: |$msg|$res|" >> $LOG_FILE
            if [[ "$(send "E: can't send res and err msg to mt api" | jq ".message")" != "null" ]]; then
              exit 1
            fi
          fi
        fi
      fi
    fi
  fi
}


push_err(){
  local res=$1

  if [[ -z "$res" ]]; then
    echo "res is empty" &>> $LOG_FILE
    return
  elif ! echo "$res" | jq ".message" &>/dev/null; then
    echo "E: $res" &>> $LOG_FILE
    res=$(send "$res") || {
      send "wtf: failed to send res"
    }
  elif [[ "$(echo "$res" | jq ".message")" != "null" ]]; then
    _push_err "$res"
    # send "E: $(echo "$res" | jq ".message")"
  else
    if [[ -z "$(echo "$res" | jq -r ".text")" ]]; then
      echo "the content of last msg is empty" &>> $LOG_FILE
      send "the content of last msg is empty"
    fi
  fi

}


# send "$text"
# exit 0

res=$(send "$text" 2>"$SH_PATH/error") && push_err "$res" || {
  e=$?
  echo "E: fail to send text(1)" &>> $LOG_FILE
# [[ -f "$SH_PATH/error" ]] && {
[[ -f "$SH_PATH/error" ]] && [[ -n "$(cat $SH_PATH/error)" ]] && {
  set -x
  send "$text" 2>"$SH_PATH/error" 1>"$SH_PATH/out"
  set +x
  r=$(cat "$SH_PATH/error") && rm "$SH_PATH/error"
  res=$(cat "$SH_PATH/out") && rm "$SH_PATH/out"
  echo "E: $r" &>> $LOG_FILE
  echo "res: $res" &>> $LOG_FILE
}
  # send "E: failed to send text: ${text:0:10}...|$e|$r"
  push_err "E: failed to send text: ${text:0:10}...|$e|$r"
}
# echo "res: $res"
# echo "json: $text"
# echo "res :|$res|" >> ~/tera/mt_msg.log

if [[ -n "$res" ]]; then
  push_err "$res"
fi
