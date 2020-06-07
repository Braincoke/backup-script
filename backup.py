#!/usr/bin/env python3

import yaml
import argparse
from string import Template
import sys
import os
import requests

# The config file can be an argument
parser = argparse.ArgumentParser()
parser.add_argument("--config", default="config.yaml", help="configuration file to load")
args = parser.parse_args()
config_file_path = args.config

# Read config
try:
  with open(config_file_path, 'r') as configfile:
    config = yaml.load(configfile)
except IOError:
  sys.exit(f'Config file {config_file_path} not found')

# Basic config checks
error_message = Template('YAML configuration missing $section info')

for section in ['healthchecks', 'restic', 'backup']:
  if section not in config:
    sys.exit(error_message.substitute(section=section))

# Load config
healthchecks = config['healthchecks']
with open(healthchecks['token'], 'r') as tokenfile:
  check_token = tokenfile.readline().rstrip('\n').rstrip('\r')
check_url = healthchecks['url'] + "/ping/" + check_token
restic = config['restic']
restic_repo = restic['repository']
restic_password_file = restic['password_file']
include_list = ''
exclude_list = ''
backup = config['backup']
if 'folders' in backup:
  include_list += ' '.join(backup['folders']) + ' '
if 'files' in backup:
  include_list += ' '.join(backup['files']) + ' '
if 'exclude_folders' in backup:
  for f in backup['exclude_folders']:
    exclude_list += ' --exclude="' + f + '"'
if 'exclude_files' in backup:
  for f in backup['exclude_files']:
    exclude_list += ' --exclude="' + f + '"'

# Ping start
try:
  requests.get(check_url + "/start")
except requests.exceptions.RequestException:
  # If the network request fails for any reason, we don't want
  # it to prevent the main job from running
  pass

# Run the backup
print(f"Backing up {include_list}")
print(exclude_list)
exit_code = os.system(f'/home/restic/bin/restic -r {restic_repo} -p {restic_password_file} backup {backup_list} {exclude_list}')

# Ping fail
if exit_code != 0:
  requests.get(check_url + "/fail")
else:
  # Ping end
  requests.get(check_url)

