#!/bin/bash
#send msg of tox to matterbridge api

text=$2
[[ -z "$text" ]] && exit 1
#source /tmp/init.sh
SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}) || exit; pwd )}

# export SH_PATH=$(cd $(dirname ${BASH_SOURCE[0]}); pwd )
username=$1
[[ "$username" == "bot" || "$username" == "ToxBot" ]] && exit 0


[[ -z "$username" ]] && username="null"
username="$(echo "$username" | sed 's/\\/\\\\/g' | sed 's/"/\\"/g')"

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

#api_port=${3:-4242}
api_port=${3:-4241}
gateway=${4-gateway1}
curl -m 2 -s -XPOST -H 'Content-Type: application/json' -d "$(bash "$SH_PATH/"gene_res.sh "$text" "$gateway" "$username")" http://127.0.0.1:$api_port/api/message || exit 0

