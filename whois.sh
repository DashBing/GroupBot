#!/bin/bash

help(){
  echo "whosi
用法: .whois \$host"
}


{ [[ -z "$1" ]] || [[ "$1" == "help" ]]; } && help && exit 0

whois "$@"
