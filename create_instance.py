#!/usr/bin/python3
# Author: Marty Rath
# Description: Python 3 program to create an ec2 instance.

import boto3
import time
import instance_config
import webbrowser

def create_instance(ami_id, bucket_name):
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
    UserData=instance_config.generate_user_data_script(instance_name, bucket_name))
    print ("Instance created")
    
    instance = instance[0]
    instance.monitor()  # Enables detailed monitoring on instance (1-minute intervals)
    instance.wait_until_running()
    instance.reload()
    print("Instance running")
    public_ip = instance.public_ip_address
    url = f'http://{public_ip}/'
    # Checks if server is ready before attempting to open
    instance_config.wait_until_server_ready(url)
    # Setting to append to not overwrite bucket url
    with open("mrath-websites.txt", "a") as file:
      file.write(url)
    webbrowser.open_new_tab(url)
    print ("Instance: " + instance.id + " has successfully been created")
    return instance
  except Exception as e:
    print("Ensure ami_id and credentials are up-to-date. Error: ", e)
