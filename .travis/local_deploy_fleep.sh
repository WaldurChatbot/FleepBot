#!/bin/bash

NAME="FleepBot"
DIRECT="fleepbot"
SCRIPT="fleepbot.py"

# we are working on the assumption that the remote server already has cloned this repo
cd ${NAME}
git checkout master
git pull

# install requirements
sudo pip install -r requirements.txt --upgrade

# kill process if running
[ -f pid ] && kill `cat pid`

# start process
cd ${DIRECT}
nohup python3.5 ${SCRIPT} > /dev/null 2>&1 & echo $! > ../pid
echo "Started ${DIRECT}/${SCRIPT}"

sleep 5

PID=`cat ../pid`

if ps -p ${PID} > /dev/null
then
   echo "${NAME} is running with pid ${PID}"
   exit 0
else
   echo "${NAME} is not running"
   exit 100
fi
