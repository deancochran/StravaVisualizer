Hello there,

My name is Dean and this is my very chaotic and unoganized strava routes visualizer.

The project initially spared from me wanting to create some cool poster desings and provide users with the capablility to reciee some really cool personalized graphics that I made and found on the web. 

Through the developement of this project I have undoubtly made some very basic django mistakes and errors. However, I  have also been able to incorporate two separate api  applications into the project which authorize and process user information.

For the future goals of this project, I how to solve the following issues:
- computing user infomation when there are no values
    - current solution: choosing to not save data from activities
- fix landscapes absolute url to redirect to img of user landscapes
- update home page, update login, update strava auth, update signinout
- add about me page
-loading screen for downloads



## set up source
https://medium.com/@fceruti/setting-up-a-django-project-like-a-pro-a847a9867f9d


## influences
https://github.com/epsalt/d3-running-map

https://github.com/marcusvolz/strava

https://github.com/erik/derive

https://github.com/yihong0618/running_page

https://github.com/hozn/stravalib


Useful Commands

DROP SCHEMA public CASCADE;
CREATE SCHEMA public;

GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO public;

redis-server
celery -A conf worker --without-gossip --without-heartbeat --without-mingle -l info
celery -A conf beat -l info