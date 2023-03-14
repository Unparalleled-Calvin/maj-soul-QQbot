#!/bin/bash

if [ "$1" == "start" ] ;
then
    nohup python script.py 1>/dev/null 2>&1 &
elif [ "$1" == "stop" ];
then
    ps aux | grep "python script.py" | grep -v grep | awk '{print $2}' | xargs kill
    ps aux | grep "go-cqhttp" | grep -v grep | awk '{print $2}' | xargs kill
elif [ "$1" == "help" ];
then
    echo "Usage:"
    echo "  start  start the service in the backend."
    echo "  stop   kill all existing related processes."
    echo "  help   print the usage."
else
    echo "error: no command $1. please use parameter help to check the usage."
fi
