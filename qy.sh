#!/bin/bash


SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}) || exit; pwd -P )}





_(){
  # curl -m 19 -s "http://api.qingyunke.com/api.php?key=free&appid=0&msg=$(bash "$SH_PATH/urlencode.sh" "$*")" || exit $?
  local res=$(curl -m 19 -s "http://api.qingyunke.com/api.php?key=free&appid=0&msg=$(bash "$SH_PATH/urlencode.sh" "$*")") && {

    local result=$(echo "$res"|jq -r ".result")
    if [[ "$result" = 0 ]]; then
      local content=$(echo "$res"|jq -r ".content")
      echo "$content"
    else
      echo "$res"
    fi

    return
    true
  } || exit $?
  echo
}


if [[ -z "$2" ]]; then
  echo "$1"
  echo "$1 \$str"
  echo "$1 \$str"
  echo '---'
  echo 'qingyunke.com'
# elif [[ "$2" == "on" ]]; then
#   :
else
  shift
  # ai "$@"
  _ "$*"
fi

