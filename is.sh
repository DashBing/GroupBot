#!/bin/bash
ai(){
curl -m 300 -s -XPOST -d "$*" 127.0.0.1:6000 || exit $?
echo
}

if [[ -z "$1" ]]; then
  echo ".is \$image_url"
# elif [[ "$2" == "on" ]]; then
#   :
else

  # echo "https://www.google.com/searchbyimage?&image_url=https://img1.acgvia.workers.dev/photos/file_1.jpg?&client=firefox-bd"
  echo "https://www.google.com/searchbyimage?&image_url=$(url)?&client=firefox-bd"
  # https://lens.google.com/uploadbyurl?url=https://img1.acgvia.workers.dev/photos/file_1.jpg
  echo "https://lens.google.com/uploadbyurl?url=$url"




fi
