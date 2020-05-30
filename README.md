# Simple restic backup script

This is a simple backup script written in Python 3 and relying on [restic](https://github.com/restic/restic) to perform backups.
This script assumes that you have set up a user `restic` on your system and the restic binary file is in `/home/restic/bin/`. You can always change it in the script if you wish.
It also relies on an instance [healthchecks.io](https://healthchecks.io/) to monitor the script execution.

## Usage

Set up a cron job as the user restic with `crontab -e`.
Example of a cron job running every day at 23:00:

~~~bash
0 23 * * * python3 /home/restic/backup.py --config config.yaml
~~~

## Configuration file

The configuration is in YAML and expects 3 sections:

- **backup**: lists the folders and files to backup (absolute paths only)
- **restic**: defines the repository to backup to and the file holding the password to this repository
- **healthchecks**: defines the healthchecks server url and token