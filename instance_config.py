#!/usr/bin/python3
# Author: Marty Rath
# Description: Generates a user data script for an ec2 instance.

import requests
import time

def generate_user_data_script(instance_name):
  script = f"""#!/bin/bash 
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
  echo "Your instance name is: {instance_name} <br>" >> /var/www/html/index.html
  echo "<hr>This instance is running in availability zone: " >> /var/www/html/index.html
  curl -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/placement/availability-zone >> /var/www/html/index.html
  echo "<hr>The instance ID is: " >> /var/www/html/index.html
  curl -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/instance-id >> /var/www/html/index.html
  echo "<hr>The instance type is: " >> /var/www/html/index.html
  curl -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/instance-type >> /var/www/html/index.html
  echo "<hr>Here is your image stored on S3: <br> <img src="logo.jpg">" >> /var/www/html/index.html
  echo "</body></html>" >> /var/www/html/index.html
  """
  return script

# Checks if instance website url returns code less than 400 using response.ok, i.e. if server is ready to access
def is_server_ready(url):
  try:
    response = requests.get(url)
    return response.ok
  except requests.RequestException:
    return False
  
# Loops is_server_ready until server responds True or until 100 seconds is up
def wait_until_server_ready(url):
  attempts = 20
  while attempts > 0:
    if is_server_ready(url):
      print("Server ready!")
      break # exits the loops
    attempts -= 1
    time.sleep(5)
  print("Server failed to load on time")