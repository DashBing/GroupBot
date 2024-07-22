#!/bin/bash



(

cd ~/bot

while true
do
vgp
tgp && bash init.sh && python3 -m tggpt && break
echo "restart ..."
sleep 5

done
)
