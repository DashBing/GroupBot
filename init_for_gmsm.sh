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
