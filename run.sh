#!/bin/bash

U=`whoami`
PUSHBULLET_KEY="xxx"

source /home/${U}/.virtualenvs/huurspy/bin/activate
cd /home/${U}/huurspy
CITIES="amsterdam amstelveen zandaam hilversum haarlem den-haag leiden"
spiders=`scrapy  list`
for city in $CITIES; do
        for spider in $spiders; do
                PARMS="-s PUSHBULLET_KEY=${PUSHBULLET_KEY} -a city=$city"
                scrapy crawl $spider $PARMS -s LOG_FILE=scrapy-$spider.log -L INFO  &
                sleep 2
        done
done
deactivate