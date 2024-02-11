#!/usr/bin/python3
# Author: Marty Rath
# Description: Python 3 program to automate the process of creating, 
#              launching and monitoring public-facing web servers in the Amazon cloud.

# Imports
import boto3

####Variables for instance creation####
ec2 = boto3.resource('ec2')

# Must be up-to-date
ami_id = 'ami-0e731c8a588258d0d'

user_data_script = """#!/bin/bash 
  # apply any required patches to the operating system
  yum update -y
  yum install httpd -y
  systemctl enable httpd
  systemctl start httpd
  
  # Create IMDSv2 session token
  TOKEN=`curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600"`
  
  # Write metadata to index.html
  # Creates index.html and adds html and body
  echo "<html><body>" > /var/www/html/index.html
  echo "This instance is running in availability zone: " >> /var/www/html/index.html
  curl -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/placement/availability-zone >> /var/www/html/index.html
  echo "<hr>The instance ID is: " >> /var/www/html/index.html
  curl -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/instance-id >> /var/www/html/index.html
  echo "<hr>The instance type is: " >> /var/www/html/index.html
  curl -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/instance-type >> /var/www/html/index.html
  echo "</body></html>" >> /var/www/html/index.html
  """

new_instances = ec2.create_instances(
  ImageId=ami_id,
  MinCount=1,
  MaxCount=1,
  InstanceType='t2.nano',
  KeyName='firstLabKey',
  SecurityGroups=['httpssh'],
  TagSpecifications=[{'ResourceType': 'instance', 'Tags': [{'Key': 'Name','Value': 'Great'},]},],
  UserData=user_data_script)
print (new_instances[0].id)
