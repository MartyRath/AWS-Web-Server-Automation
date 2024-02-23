#!/usr/bin/python3
# Author: Marty Rath
# Description: Generates a user data script for an ec2 instance.

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
    echo "Here is your image stored on S3: <br> <img src="https://lab2bucket28jan.s3.amazonaws.com/sunflower.avif" width="500" height="500">" >> /var/www/html/index.html
    echo "</body></html>" >> /var/www/html/index.html
    """
    return script