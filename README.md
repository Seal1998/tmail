Tmail
======
### Script that's managed telegram messages delivering through command line interface
---------------------------

#### Quick overview:

- #### Use it in cron jobs:
		0 0 * * * echo "daily report" | tmail -a /var/log/nginx/access.log
- #### Send notification in scripts:
		#!/bin/bash
		./very_important_backup.sh
		if [ $? -ne 0 ]; then
			echo "Backup failed" | tmail -s "$(date)" -c 123456
		fi

------------------
Why this piece of software is even exist
===============
Telegram is my everyday in use software. And for me its very comfortable to resieve notifications in it about state of my server, logs and so on. Of course it cant handle some important information for security reasons, but its perfectly suited for every day reports, programs states, system state, alarms etc.
When I wrote this script I was inspired by utility named "mail" which can work with STDIN, manage attachments and many more, sending all this stuff to recipient email box. Becouse of it easy in use interface I desided to iplement this functional with help of telegram API and Python!

*TODO*:
- command line args
- functionality
- installation
