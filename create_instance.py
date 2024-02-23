#!/usr/bin/python3
# Author: Marty Rath
# Description: Python 3 program to create an ec2 instance.

import boto3
import time
from user_data_script import generate_user_data_script

def create_instance():
  ec2 = boto3.resource('ec2')
  
  # Ensure this is up to date
  ami_id = 'ami-0440d3b780d96b29d'
  
  # Using time to name instance
  local_time = time.localtime()
  format_time = time.strftime("%H%M", local_time)

  # Assign instance name
  instance_name = "Instance: " + format_time

  try:
    instance = ec2.create_instances(
    ImageId=ami_id,
    MinCount=1,
    MaxCount=1,
    InstanceType='t2.nano',
    KeyName='firstLabKey',
    SecurityGroups=['httpssh'],
    TagSpecifications=[{'ResourceType': 'instance', 'Tags': [{'Key': 'Name','Value': instance_name},]},],
    UserData=generate_user_data_script(instance_name))
    print ("Instance: " + instance[0].id + " has successfully been created")
    return instance[0]
  except Exception as e:
    print("Tip: Ensure ami_id and credentials are up-to-do", e)
    return None