# rezffa
Scrape results from FFA (Fédération Française d'Athlétisme)

### installation
Development stuff for installing some pip packages:

`[user@server][~] sudo apt install python3-dev libxml2-dev libxslt-dev python-dev`

##### clone project
`[user@server][~] git clone git@github.com:ldvc/rezffa.git`

##### virtualenv
Create folder for future venvs:
`[user@server][~] mkdir -p ~/.virtualenvs && cd ~/.virtualenvs`

Create venv:
`user@server][.virtualenvs] virtualenv -p python3 venv_rezffa`

Enable virtualenv:
`source ~/.virtualenvs/venv_rezffa/bin/activate`

Install dependencies: `pip install -r ~/github/rezffa/requirements.txt`

### usage
You can override default config by creating a local_config.py file.
```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 sw=4 ts=4 et:


# general
PATH = '/var/www/html/domain.tld/ffa/'
```
##### one-time run
Then, run `./rezffa.py -n 424242` (in virtualenv) to retrieve results for club with number 424242.

##### scheduling
Create a cron job for automatic retrieving twice a week (Mon and Thu for instance):
```
[user@server][~] cat /etc/cron.d/rezffa
# Use the hash sign to prefix a comment
# +---------------- minute (0 - 59)
# |  +------------- hour (0 - 23)
# |  |  +---------- day of month (1 - 31)
# |  |  |  +------- month (1 - 12)
# |  |  |  |  +---- day of week (0 - 7) (Sunday=0 or 7)
# |  |  |  |  |
# *  *  *  *  *  command to be executed
#--------------------------------------------------------------------------
  0 17 * * 1,4 user /home/user/.virtualenvs/venv_rezffa/bin/python ~user/github/rezffa/rezffa.py -n 424242 > /dev/null 2>&1
```
