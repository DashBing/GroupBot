#!/bin/bash
text="$1"
MAX_BYTES=${2:-1371}
# MAX_BYTES=${2:-1024}
if [[ $(echo -n "$text" | wc -c) -gt $MAX_BYTES ]]; then
  LP=${LP:-/var/www/dav/tmp}
  fn=$(date "+%Y%m%d_%H%M%S").txt
  SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}); pwd )}
  echo -ne "$text" >"$LP/${fn}" && echo "long msg: $(bash "$SH_PATH/file_to_ipfs.sh" "$LP/${fn}")" || { text="msg:\\n${text}"; echo "${text:0:MAX_BYTES}"; }
else
  echo "$text"
fi
