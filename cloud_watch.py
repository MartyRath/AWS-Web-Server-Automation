#!/usr/bin/python3

import boto3
from datetime import datetime, timedelta, timezone
import time

def run_cloud_watch(instance):
    cloudwatch = boto3.resource('cloudwatch')
    
    current_time = datetime.utcnow()
    result_time = current_time + timedelta(minutes=6)
    
    print(f"\nWelcome to CloudWatch. Monitoring details will be available at {result_time}")
    time.sleep(360)     # Wait 6 minutes to ensure we have some data
    
    # CPU Utilisation
    cpu_metric_iterator = cloudwatch.metrics.filter(Namespace='AWS/EC2',
                                                     MetricName='CPUUtilization',
                                                     Dimensions=[{'Name':'InstanceId', 'Value': instance.id}])

    cpu_metric = list(cpu_metric_iterator)[0]    # extract first (only) element

    cpu_response = cpu_metric.get_statistics(StartTime = current_time - timedelta(minutes=5),   # 5 minutes ago
                                             EndTime=current_time,                              # now
                                             Period=300,                                        # 5 min intervals
                                             Statistics=['Average'])

    print ("Average CPU utilization:", cpu_response['Datapoints'][0]['Average'], cpu_response['Datapoints'][0]['Unit'])