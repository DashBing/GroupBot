#!/bin/bash


export SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}) || exit; pwd )}
[[ -e "$SH_PATH/DEBUG" ]] && export LOG_FILE="$HOME/tera/mt.log" || export LOG_FILE=/dev/null
# [[ -e "$SH_PATH/DEBUG" ]] && export LOG_FILE="$HOME/mt.log" || export LOG_FILE=/dev/null



# SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}); pwd )}
# LP=${LP:-/var/www/dav/tmp}
LP=${LP:-$HOME/tera/tmp}
#DOMAIN=${DOMAIN:-liuu.tk}
DOMAIN=$(cat $SH_PATH/DOMAIN)
MAX_SHARE_FILE_SIZE=${MAX_SHARE_FILE_SIZE:-64000000}

GP=${GP:-$HOME/bot/note}



export http_proxy="http://127.0.0.1:6080"
export https_proxy="http://127.0.0.1:6080"











if [[ $(echo "$1" | grep -c -P "^http(s)?://[0-9a-zA-Z.-]+\.[a-zA-Z]+(:[0-9]+)?/?[\S]*(txt)$") -eq 1 ]]; then
  URL=$2
  file_path=$(bash "$SH_PATH/link_to_file.sh" "$1" "only")
  if [[ -f "$file_path" ]]; then
    if file -i "$file_path"| grep -q "text/plain"; then
      fs=$(du -b "$file_path"|cut -f1)
      if $fs -le 512000 ]]; then
        fn=${URL##*/}
        if [[ -f "$GP/$fn" ]]; then
          fn=$(date "+%Y%m%d_%H%M%S")"_$fn".txt
        fi
        cp "$file_path" "$GP/$fn"
      else
        echo "E: too big"
      fi
    else
      echo "E: txt only"
    fi
  else
    echo "E: no $file_path"
  fi
else
  fn=$(date "+%Y%m%d_%H%M%S").txt
  echo "$*" > "$GP/$fn"
fi


if [[ -n "fn" ]]; then
bash -i -c "
cd $GP
cd ..
bash init.sh
tgpp
" &>/dev/null
echo https://github.com/liqsliu/bot/blob/master/note/"$fn"
else
echo error
fi



      # if [[ "$ft" == "text/plain" ]] && [[ $fs -le 512000 ]]; then
      #   :
      # fi
