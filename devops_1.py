#!/usr/bin/python3
# Author: Marty Rath
# Description: Python 3 program to automate the process of creating, 
#              launching and monitoring public-facing web servers in the Amazon cloud.


from create_instance import create_instance
from create_bucket import create_bucket
from monitoring_commands import monitoring_commands
import subprocess

# Creates bucket and returns bucket name
bucket_name = create_bucket()

# Ensure this is up-to-date
ami_id = 'ami-0440d3b780d96b29d'
# Creates instance, inputting name as parameter to display bucket image
instance = create_instance(ami_id, bucket_name)

# Runs monitoring script, saving to monitoring.txt and displaying results
subprocess.run(monitoring_commands(instance.public_ip_address), shell=True)

