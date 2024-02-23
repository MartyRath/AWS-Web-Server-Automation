#!/usr/bin/python3
# Author: Marty Rath
# Description: This Python program creates an s3 bucket, named by input from. Adapted from scripts made available in lab 4. 

import boto3
import uuid

def get_random_characters():
  # Getting a uuid of random characters
  random_uuid = uuid.uuid4()
  # Splicing down to 6 characters and converting to string
  random_characters = str(random_uuid)[:6] 
  return random_characters

def create_bucket():
  bucket_name = get_random_characters() + "mrath"
  s3 = boto3.resource("s3")
  try:
    bucket = s3.create_bucket(Bucket=bucket_name)
    print("Bucket: " + bucket_name + " successfully created")
    return bucket
  except Exception as e:
    print ("Issue creating bucket", e)

create_bucket()
