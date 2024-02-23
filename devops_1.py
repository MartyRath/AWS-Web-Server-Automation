#!/usr/bin/python3
# Author: Marty Rath
# Description: Python 3 program to automate the process of creating, 
#              launching and monitoring public-facing web servers in the Amazon cloud.


from create_instance import create_instance

instance = create_instance()

instance.wait_until_running()
instance.reload()
ip = instance.public_ip_address
print(ip)