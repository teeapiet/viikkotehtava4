# Week 4

### The assignment asked to create a second Ubuntu server by copying the original server. I did this by creating Server B from a snapshot of Server A in CSC cPouta. 
### Also asked to set up automatic hourly backups, so I used Bash, rsync, SSH and cron to copy website files from Server A to Server B.
### Also had to configure MariaDB replication, so I set it up to automatically copy visitor counter changes from A to B. I made Server B's website read-only, so opening it does not increase the counter.

## A: http://195.148.23.163/viikko2/
## B: http://86.50.231.16/viikko4/
