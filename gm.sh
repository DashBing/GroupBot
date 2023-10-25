#!/bin/bash
#get msg for tox and run cmd
# export SH_PATH=$(cd $(dirname ${BASH_SOURCE[0]}); pwd )

set_log(){
export SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}) || exit; pwd )}
[[ -e "$SH_PATH/DEBUG" ]] && export LOG_FILE="$HOME/tera/mt.log" || export LOG_FILE=/dev/null
  busy=1
}

delete_raw(){
res=$(echo "$res" | jq 'del(.[].Extra.file[0].Data)') &>/dev/null || exit 0
  set_log
}

run_sh(){
  local ll=${1:-cmd.sh}
  local e=0
  rm "$SH_PATH/.ERROR"
  # echo bash "$SH_PATH/$ll" "$res" &>> $LOG_FILE
  bash "$SH_PATH/$ll" "$res" 1> "$SH_PATH/.STDOUT" 2> "$SH_PATH/.ERROR" || e=$?
  [[ -f "$SH_PATH/.ERROR" ]] && [[ -n "$(cat "$SH_PATH/.ERROR")" ]] && {
    bash "$SH_PATH/sm.sh" "C bot" "E: $?
$( cat "$SH_PATH/.STDOUT"
echo "---"
cat "$SH_PATH/.ERROR" )" 4240 &>> $LOG_FILE
  }

}
#res="[]"
# for cmd
res=$(curl -m 1 -s http://127.0.0.1:4240/api/messages) || exit 0
if [[ "$res" != "[]" ]]; then
  delete_raw
  run_sh
  run_sh msg_for_simplex.sh
  rm "$SH_PATH/.STDOUT"
  run_sh msg_for_tox.sh
  [[ -f "$SH_PATH/.STDOUT" ]] && [[ -n "$(cat "$SH_PATH/.STDOUT")" ]] && {
  cat "$SH_PATH/.STDOUT"
}
fi

# get msg from simplex
res=$(curl -m 1 -s http://127.0.0.1:4250) || exit 0
if [[ "$res" != "[]" ]]; then
  set_log
  run_sh sm_simplex.sh
fi


max=50 #3s
max2=80
min=2
if [[ "$busy" == "1" ]]; then
  busy=$min
else
export SH_PATH=${SH_PATH:-$(cd $(dirname ${BASH_SOURCE[0]}) || exit; pwd )}
  busy=$(cat "$SH_PATH/.BUSY")
  # busy=$[busy*2]
  if [[ $busy -ge $max2 ]]; then
    sleep 3
  elif [[ $busy -ge $max ]]; then
    busy=$[busy+1]
    busy2=$[(busy-max)*(busy-max)/30]
    sleep 0.2
    echo sleep2 $[busy2/10].$[busy2*10/10]
    sleep $[busy2/10].$[busy2*10/10]
  else
    busy=$[busy+1]
    sleep 0.2
  fi
  echo $busy 1>&2
  # sleep $[busy/10].$[busy%10]
fi

echo $busy > "$SH_PATH/.BUSY"


# nohup bash "$SH_PATH/bgm.sh" &>/dev/null &
