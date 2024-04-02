#!/usr/bin/python3
# Author: Marty Rath
# Description: Adds monitoring.sh to ec2 instance and runs it.

def monitoring_commands(ip_address):
  script = f"""#!/bin/bash 
  scp -o StrictHostKeyChecking=no -i firstLabKey.pem monitoring.sh ec2-user@{ip_address}:.
  if [ $? -eq 0 ]; then
        echo "Monitoring script uploaded to instance"
    else
        echo "Failed to upload monitoring script" >&2
        exit 1
    fi

  ssh -i firstLabKey.pem ec2-user@{ip_address} 'chmod 700 monitoring.sh'
  if [ $? -eq 0 ]; then
    echo "Script permissions granted"
  else
    echo "Failed to grant script permissions" >&2
    exit 1
  fi
  
  ssh -i firstLabKey.pem ec2-user@{ip_address} './monitoring.sh' > monitoring.txt && cat monitoring.txt
  if [ $? -eq 0 ]; then
    echo "Monitoring details stored in monitoring.txt"
  else
    echo "Failed to run monitoring script" >&2
    exit 1
  fi
  """
  return script
