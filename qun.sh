#!/bin/bash

# set -x

SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}) || exit; pwd )}

my_encode_old() {
  # [[ $( echo "$text" | wc -l ) -gt 1 ]] && text=$(echo "$text" | awk '{printf "%s\\n", $0}' | sed "s/\\\\n$//g")

  if [[ $(echo "$@" | wc -l) -le 1 ]]; then
    #    text="$(printf "%q" "${@}")"
    text=$(printf "%q" "${*}")
  else
    text=$(printf "%q" "${*}")
    #text="${text:2}"
    text="${text#\$\'}"
    text="${text%\'}"
    text=$(echo "$text" | cut -d '"' --output-delimiter='\"' -f 1-)
  fi
  cat <<EOF
$text
EOF

}

my_encode() {

  local text="$1"
  text=$(echo "$text" | cut -d '\' --output-delimiter='\\' -f 1-)
  text=$(echo "$text" | cut -d '"' --output-delimiter='\"' -f 1-)
  [[ $(echo "$text" | wc -l) -gt 1 ]] && text=$(echo "$text" | awk '{printf "%s\\n", $0}' | sed "s/\\\\n$//g")
  # echo -e "$text"
  cat <<EOF
$text
EOF

}

my_decode() {
  echo -e "$1"
}


get_jid(){
  # cat | grep -G -o ": .*"
  # cat | sed -r 's/.*: ([^ ]+)($| .*)/\1/1'
  cat | sed -r 's/(^|\s)(\S+@\S+)($|\s)/\2/1'
}

get_jid2(){
  # cat | grep -G -o ": .*"
  # cat | sed -r 's/.*: ([^ ]+)($| .*)/xmpp:\1?join/1'
  cat | sed -r 's/(^|\s)(\S+@\S+)($|\s)/xmpp:\2?join/1'
}

add() {

  local username=$1
  local text=$2
  text=$(echo "$text"|sed 's/^> //')

  local jid=$(echo "$text"|get_jid|head -n1)


  if grep -q -F "$jid" "$NOTE_FILE"; then
    if echo "$jid" | grep -q -G '^xmpp:.*?join$'; then
      jid=$(echo "$jid" |sed -r 's/^(xmpp:)(.*)(\?join)$/\2/1')
    fi

    if echo "$text"| head -n1 | awk '{print $1}'|grep -q -F "@"; then
      :
    else
      line_num=$(echo "$text" | grep -n -F "$jid" | cut -d ':' -f1 | head -n1)
      text=$(echo "$text" |sed -r $line_num's/(^.*\s+)(\S+@\S+)($|\s+.*$)/\1\3/1')
      text="$jid $text"
    fi
    line_num=$(grep -n -F "$jid" "$NOTE_FILE" | cut -d ':' -f1 | head -n1)
    line=$(sed -n "${line_num}p" "$NOTE_FILE")
    echo "已存在: $line"
  else
    echo "$username$text" >>"$NOTE_FILE" && echo "已添加: $text" || echo "E: $?"
  fi
}

del() {
  # if [[ -z "$2" ]]; then
  local text=$1
  # else
  #   local tag=$1
  #   local text=$2
  # fi
  # text=$(echo "$text" | cut -d '\' --output-delimiter='\\' -f 1-)
  # [[ $( echo "$text" | wc -l ) -gt 1 ]] && text=$(echo "$text" | awk '{printf "%s\\n", $0}' | sed "s/\\\\n$//g")
  # line_num=$(grep -n -G "^$text\$" "$NOTE_FILE" | cut -d ':' -f1 | head -n1)
  # line_num=$(grep -n -F "$text" "$NOTE_FILE" | cut -d ':' -f1 | head -n1)
  # if echo "$text"|grep -q -P '^\d+$'; then
  #   line_num=$text
  # else
    # line_num=$(grep -n -G "^$tag" "$NOTE_FILE" | grep -F "$text" | cut -d ':' -f1 | head -n1)
    line_num=$(grep -n -F "$text" "$NOTE_FILE" | cut -d ':' -f1 | head -n1)
  # fi
  # echo num$line_num
  # read -p ok?
  if [[ -n "$line_num" ]]; then
    line=$(sed -n "${line_num}p" "$NOTE_FILE")
    sed -i "${line_num}d" "$NOTE_FILE" && echo "已删除: $line" || echo "E: $?"
    # sed -i "${line_num}d" "$NOTE_FILE" && echo "已删除: $text" || echo "E: $?"
  else
    echo "没找到: $text"
  fi
}

list_tags() {
  #  cat "$NOTE_FILE" | cut -d ' ' -f1 |sort -n |awk '{if($0!=line)print; line=$0}'
  # local tags=$(cat "$NOTE_FILE" | cut -d ' ' -f1 | sort -n | uniq)
  # echo $tags
  # echo "all tag:"
  # cat "$NOTE_FILE"| sed -r 's/.*: [^ ]+(( +#[^\s])+)/\1/1'| sed -r 's/ /\n/g' | sort -n | uniq
  cat "$NOTE_FILE"| sed -r 's/.*: [^ ]+( .*$)/\1/1'|grep -o -P '#[^\s]+' | sort -n | uniq
}


print_help(){
  echo "群组列表整理
用法:
.note [add] \$text
.note list
.note tag
.note del \$text
.note help

备份: https://github.com/liqsliu/bot/blob/master/qun.txt
源码: https://github.com/liqsliu/bot/blob/master/qun.sh"

}

log_msg(){
  echo
  echo
  date
  echo "#### $1 ####"
  shift
  # echo "msgText, msgUsername, inAccount, inProtocol, inChannel, inGateway, inEvent, outAccount, outProtocol, outChannel, outGateway, outEvent"
  local i=0
  for i in "$@"
  do
    echo -n "|$i|"
  done
  echo
  echo "#### end ####"
}


shorter(){
text=$(echo "$text" | sed -r '1s/^\s*\S+\s*//' )
}


# date >> ~/tera/mt_msg.log
# echo "$*" >> ~/tera/mt_msg.log
log_msg note "$@" >> $LOG_FILE
#
NOTE_FILE="$SH_PATH/qun.txt"

username=$1
username=$(my_encode "$1")
text="$2"
[[ -z "$text" ]] && print_help && exit 0
text_1=$(echo "$text"|head -n1)
cmd_1=$(echo "$text_1" | awk '{print $1}' )
cmd_2=$(echo "$text_1" | awk '{print $2}' )

case "${cmd_1}" in
help)
  print_help
  exit 0
  ;;
tag)
  du -h "$NOTE_FILE"
  list_tags
  exit 0
  ;;
list)
  cmd=list
  shorter
  ;;
add)
  cmd=add
  shorter
  ;;
del)
  cmd=del
  shorter
  ;;
delete)
  cmd=delete
  shorter
  ;;
*)
  cmd=add
  ;;
esac
text=$(my_encode "$text")

[[ -z "$text" ]] && [[ "$cmd" != "list" ]] && echo '内容不能为空' && exit 0

case "${cmd}" in
list)
  # echo "$tag"
  # my_decode "$(grep -G "^$tag " "$NOTE_FILE" | cut -d" " -f2- | sed 's/^/\n/g')"
  # my_decode "$(grep -n -F "$tag " "$NOTE_FILE" | cut -d" " -f2- | sed 's/^/\n/g')"
  # my_decode "$(grep -n -F "$tag " "$NOTE_FILE" | sed -r 's|:#[^ ]+ |%|1')"
  if [[ "$cmd_2" == "jid" ]]; then
    echo jid
    cat "$NOTE_FILE" | get_jid2
  elif [[ "$cmd_2" == "jidonly" ]]; then
    echo jid only
    cat "$NOTE_FILE" | get_jid
  elif [[ "$cmd_2" == "full" ]]; then
    echo full
    my_decode "$(cat "$NOTE_FILE")"
  else
    echo jid only
    cat "$NOTE_FILE" | get_jid
  fi
  ;;
add)
  add "$username" "$text"
  ;;
del)
  del "$username$text"
  ;;
delete)
  del "$text"
  ;;
*)
  add "$username$text"
  ;;
esac
