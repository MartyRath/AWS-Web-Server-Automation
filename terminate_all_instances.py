#!/usr/bin/env python3
# Description: Terminates all running instances

import boto3

ec2 = boto3.resource('ec2')
for instance in ec2.instances.all():
  if instance.state['Name'] == "running":
    instance.terminate()