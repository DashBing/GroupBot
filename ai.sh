#!/bin/bash
ai(){
curl -m 300 -s -XPOST -d "$*" 127.0.0.1:8889 || exit $?
echo
}

if [[ -z "$1" ]]; then
  echo ".ai \$str"
  echo "/AI \$str"
  echo
  echo "出现故障请对我说 reset"
  echo "嫌我的答案不可靠？可以试试bot命令，bot的温度是0"
  echo "model: text-davinci-003"
  echo "link: https://beta.openai.com/docs/models/overview"
# elif [[ "$2" == "on" ]]; then
#   :
else
# ai "$@"
ai "$*"
fi
