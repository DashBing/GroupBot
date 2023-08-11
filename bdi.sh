#!/bin/bash
SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}) || exit; pwd )}
bdi(){
curl -m 300 -s -XPOST -d "$*" 127.0.0.1:6002 || exit $?
echo
}

if [[ -z "$1" ]]; then
  echo ".ai \$str"
  echo ".bd \$str #有上下文"
  echo ".bdi [-notr] \$image_url\n\$str"
  echo "--"
  echo "link: https://github.com/EvanZhouDev/bard-ai"
  echo "link: https://bard.google.com/"
# elif [[ "$2" == "on" ]]; then
#   :
elif [[ "$1" = "-notr" ]]; then
shift
bdi "$*"
else
# bdi "what is it?
url=$(echo "$*"|grep -o -P '^\s*\S+\s*'|grep -o -P '\S+')
if [[ -z "$url" ]]; then
  echo "url? $url"
else
text=$(echo "$*" | sed -r 's|^\s*\S+\s*||g')
bdi "$url
$(bash "$SH_PATH/trans.sh" -brief :en "$text")
Please answer in Chinese."
fi
fi
