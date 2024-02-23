#!/usr/bin/python3
# Author: Marty Rath
# Description: This Python program creates an s3 bucket, named by input from. Adapted from scripts made available in lab 4. 

import boto3

def create_bucket(bucket_name):
  s3 = boto3.resource("s3")
  try:
    bucket = s3.create_bucket(Bucket=bucket_name)
    return bucket
  except Exception as e:
    print ("Issue creating bucket", e)
