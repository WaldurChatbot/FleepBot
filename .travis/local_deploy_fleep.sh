#!/bin/bash

# the target should already have cloned this repo
cd FleepBot

# if supplied argument is 'dev', use develop branch
if [ ! -z $1 ]; then
    if [ $1 == "dev" ]; then
        git checkout develop
    else
        git checkout master
    fi
else
    git checkout master
fi

git pull

# install requirements
sudo pip install -r requirements.txt --upgrade

# kill all python processes
[ -f pid ] && kill `cat pid`

# start processes
cd fleepbot
nohup python3.5 fleepbot.py > /dev/null 2>&1 & echo $! > ../pid
echo "Started fleep bot"

sleep 5

if ps -p `cat ../pid` > /dev/null
then
   echo "`cat ../pid` is running"
   exit 0
else
   echo "Fleep bot is not running"
   exit 100
fi
