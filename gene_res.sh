#!/bin/bash
#text=$(echo "$1" | sed 's/\\/\\\\/g' | sed 's/"/\\"/g')
#[[ $( echo "$text" | wc -l ) -gt 1 ]] && text=$(echo "$text" | awk '{printf "%s\\n", $0}' | sed "s/\\\\n$//g")


text=$1
text="$(echo "$text" | cut -d '\' --output-delimiter='\\' -f 1- )"

SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}); pwd )}
gateway=${2-gateway1}
username=${3-C bot}


wtf(){
# echo "$1" | sed -e 's/\\/\\\\/g' -e 's/"/\\"/g' -e 's/\r/\\r/g' -e 's/\t/\\t/g' -e 's/+/\\+/g'
# echo "$1" | sed -e 's/\\/\\\\/g' -e 's/"/\\"/g' -e 's/\r/\\r/g' -e 's/\t/\\t/g' -e 's/-/\\-/g'
# echo "$1" | sed -e 's/\\/\\\\/g' -e 's/"/\\"/g' -e 's/\r/\\r/g' -e 's/\t/\\t/g'

echo "$1" | sed -e 's/\\/\\\\/g' -e 's/"/\\"/g' -e 's/\r//g' -e 's/\t/\\t/g' | sed -r "s/\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[m|K]//g"
}

#text=$(bash "$SH_PATH/text2markdown.sh" "$text")

#text="$(echo "$text" | cut -d '"' --output-delimiter='\"' -f 1- | cut -d $'\t' --output-delimiter='\t' -f 1- | sed 's|\x1b||g' | sed -r "s/\x1B\[([0-9]{1,3}(;[0-9]{1,2})?)?[mGK]//g")"
# text="$(echo "$text" | ansi2txt | cut -d '"' --output-delimiter='\"' -f 1- | cut -d $'\t' --output-delimiter='\t' -f 1- )"

echo "g0 :|$text|" >> ~/tera/mt_msg.log
text=$(wtf "$text")
echo "g1 :|$text|" >> ~/tera/mt_msg.log
[[ $( echo "$text" | wc -l ) -gt 1 ]] && text=$(echo "$text" | awk '{printf "%s\\n", $0}' | sed "s/\\\\n$//g")
echo "g2 :|$text|" >> ~/tera/mt_msg.log

username=$(wtf "$username")

text=$(bash "$SH_PATH/change_long_text.sh" "$text" 4096)
echo "g3 :|$text|" >> ~/tera/mt_msg.log

cat <<EOF>>~/tera/mt_msg.log
$(date)
{"text":"${text}","username":"${username}","gateway":"${gateway}"}
EOF

#text=$( echo "$text"  | od -An -tx1 | sed 's/ /\\x/g' )
# [[ -z "$text" ]] && exit 1
cat <<EOF
{"text":"${text}","username":"${username}","gateway":"${gateway}"}
EOF

