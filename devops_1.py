#!/usr/bin/python3
# Author: Marty Rath
# Description: Python 3 program to automate the process of creating, 
#              launching and monitoring public-facing web servers in the Amazon cloud.


from create_instance import create_instance
from create_bucket import create_bucket


ami_id = 'ami-0440d3b780d96b29d'

create_bucket()
create_instance(ami_id)


