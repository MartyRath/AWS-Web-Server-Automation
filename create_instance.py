#!/usr/bin/python3
# Author: Marty Rath
# Description: Python 3 program to create an ec2 instance.

import boto3
import time
from user_data_script import generate_user_data_script
import webbrowser

def create_instance(ami_id):
  ec2 = boto3.resource('ec2')
  
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
    
    instance = instance[0]
    instance.wait_until_running()
    instance.reload()
    time.sleep(30)
    print("Instance running")
    public_ip = instance.public_ip_address
    url = f'http://{public_ip}/'
    # Setting to append to not overwrite bucket url
    with open("mrath-websites.txt", "a") as file:
      file.write(url)
    webbrowser.open_new_tab(url)
  except Exception as e:
    print("Ensure ami_id and credentials are up-to-date. Error: ", e)
