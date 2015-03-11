huurspy
=


* For ubuntu 14.04 you will need to install:
>   sudo apt-get install python-dev libxml2-dev libxslt-dev zlib1g-dev libffi-dev libssl-dev python-pip  python-virtualenv virtualenvwrapper
   
* Install mongodb (use the 10gen repo)

* Create a virtual env

> mkvirtualenv huurspy

* Clone this repo

* Install the python dependencies:

> pip install -r requirements.txt


* Create run.sh

```
#!/bin/bash

source ~/.virtualenvs/huurspy/bin/activate
cd ~/huurspy
PUSHBULLET_KEY=xxx
PARMS="-s  $PUSHBULLET_KEY -a city=amsterdam"
spiders=`scrapy  list`
for spider in $spiders; do
	scrapy crawl $spider $PARMS -s LOG_FILE=scrapy.log -L INFO
done

deactivate
```

* Add run.rh to your cron.  For 5 minute interval it should be something like

> crontab -e 
> */5 * * * * /home/user/run.sh


Good luck!
