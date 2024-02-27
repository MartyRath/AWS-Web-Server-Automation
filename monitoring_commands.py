#!/usr/bin/python3
# Author: Marty Rath
# Description: Adds monitoring.sh to ec2 instance and runs it.

def monitoring_commands(ip_address):
  script = f"""#!/bin/bash 
  scp -o StrictHostKeyChecking=no -i firstLabKey.pem monitoring.sh ec2-user@{ip_address}:.
  echo "Monitoring script uploaded to instance"
  ssh -i firstLabKey.pem ec2-user@{ip_address} 'chmod 700 monitoring.sh'
  echo "Script permissions granted"
  ssh -i firstLabKey.pem ec2-user@{ip_address} './monitoring.sh' > monitoring.txt && cat monitoring.txt
  echo "Monitoring details stored in monitoring.txt"
  """
  return script