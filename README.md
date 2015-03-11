huurspy
=


* For ubuntu 14.04 you will need to install:
`` apt-get install python-dev libxml2-dev libxslt-dev zlib1g-dev libffi-dev libssl-dev python-pip  python-virtualenv virtualenvwrapper``
   
* Install mongodb (use the 10gen repo)

* Create a virtual env

``mkvirtualenv huurspy``

* Clone this repo

* Install the python dependencies:

``pip install -r requirements.txt``


* Create run.sh

```
#!/bin/bash

source ~/.virtualenvs/huurspy/bin/activate
cd ~/huurspy
PUSHBULLET_KEY=xxx
PARMS="-s $PUSHBULLET_KEY -a city=amsterdam -s LOG_FILE=scrapy.log -L INFO"
spiders=`scrapy  list`
for spider in $spiders; do
	scrapy crawl $spider $PARMS 
done

deactivate
```

* Add run.rh to your cron.  For 5 minute interval it should be something like

``crontab -e``
``*/5 * * * * /home/user/run.sh``


Good luck!

Todo
==
* Make the city a parameter for each scraper so we can iterate over a city list
* Better result filtering
* Better mongodb logic
