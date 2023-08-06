#!/bin/bash
#text=$(echo "$1" | sed 's/\\/\\\\/g' | sed 's/"/\\"/g')
#[[ $( echo "$text" | wc -l ) -gt 1 ]] && text=$(echo "$text" | awk '{printf "%s\\n", $0}' | sed "s/\\\\n$//g")


text=$1
text="$(echo "$text" | cut -d '\' --output-delimiter='\\' -f 1- )"

SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}); pwd )}
gateway=${2-gateway1}
username=${3-C bot}


wtf(){
echo "$1" | sed -e 's/\\/\\\\/g' -e 's/"/\\"/g' -e 's/\r/\\r/g' -e 's/\t/\\t/g' -e 's/\+/\\\+/g'
}

#text=$(bash "$SH_PATH/text2markdown.sh" "$text")

#text="$(echo "$text" | cut -d '"' --output-delimiter='\"' -f 1- | cut -d $'\t' --output-delimiter='\t' -f 1- | sed 's|\x1b||g' | sed -r "s/\x1B\[([0-9]{1,3}(;[0-9]{1,2})?)?[mGK]//g")"
# text="$(echo "$text" | ansi2txt | cut -d '"' --output-delimiter='\"' -f 1- | cut -d $'\t' --output-delimiter='\t' -f 1- )"

text=$(wtf "$text")
[[ $( echo "$text" | wc -l ) -gt 1 ]] && text=$(echo "$text" | awk '{printf "%s\\n", $0}' | sed "s/\\\\n$//g")

username=$(wtf "$username")

text=$(bash "$SH_PATH/change_long_text.sh" "$text" 4096)

#text=$( echo "$text"  | od -An -tx1 | sed 's/ /\\x/g' )
[[ -z "$text" ]] && exit 1
cat <<EOF
{"text":"bug ${text}","username":"${username}","gateway":"${gateway}"}
EOF
