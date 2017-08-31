# tl.py : Very Basic CLI time logger for gtimelog
=================================================

## introduction
This is just a simple script that I did more or less as a
python assignment to help me keep track of my work under
gtimelog.

## Scripts

* tl.py        : Main script to register tasks
* weekly_tl.py : Weekly report
* rep_tl.py    : Category report
* tl_sum.py    : Summary report for a single task

## Syntax

### tl.py

This is the main script responsible for logging the time into the gtimelog
logfile.

    usage: tl.py [-h] [-c] [-t CATEGORY] [-r] [-l LOGFILE] [task [task ...]]

    positional arguments:
      task                  category | category : task title

    optional arguments:
      -h, --help            show this help message and exit
      -c, --list-categories
                            list available task categories
      -t CATEGORY, --list-tasks CATEGORY
                            list available tasks for a given category
      -r, --raw             produce raw output (without pretty formatting)
      -l LOGFILE, --logfile LOGFILE
                            Path to the gtimelog logfile to be use

### weekly_tl.py

This script provides a weekly summary of all the work done.

    usage: weekly_tl.py [-h] [-l LOGFILE] [-u USER] [-n] [-m]

    optional arguments:
      -h, --help            show this help message and exit
      -l LOGFILE, --logfile LOGFILE
                            Path to the gtimelog logfile to be use
      -u USER, --user USER  User Identification to be used for report
      -n, --no-time         Print weekly report without spent time
      -m, --minutes         Print weekly report with spent time in minutes

### rep_tl.py

This script will list a summary of the different tasks done, time spent on it
and percentage of the total time spent.

    usage: rep_tl.py [-h] [-l LOGFILE]

    optional arguments:
      -h, --help            show this help message and exit
      -l LOGFILE, --logfile LOGFILE
                        Path to the gtimelog logfile to be use

### tl_sum.py

This calculates the total time spent on a task.

    usage: tl_sum.py [-h] [-c] [-t CATEGORY] [-r] [task [task ...]]

    positional arguments:
      task                  category | category : task title

    optional arguments:
      -h, --help            show this help message and exit
      -c, --list-categories
                            list available task categories
      -t CATEGORY, --list-tasks CATEGORY
                            list available tasks for a given category
      -r, --raw             produce raw output (without pretty formatting)
