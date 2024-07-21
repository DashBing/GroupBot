#!/bin/bash



(

cd ~/bot

while true; then
vgp
tgp && bash init.sh && python3 -m tggpt || break
echo "restart ..."
sleep 5

)
