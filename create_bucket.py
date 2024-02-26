#!/usr/bin/python3
# Author: Marty Rath     
# Description: This Python program creates an s3 bucket, randomly named using uuid. Adapted from scripts made available in lab 4. 

import boto3
import bucket_config
import json

def create_bucket():
  # Naming the bucket with six random characters and mrath
  bucket_name = bucket_config.get_random_characters() + "mrath"
  s3 = boto3.resource("s3")
  try:
    # Creates the bucket
    bucket = s3.create_bucket(Bucket=bucket_name)
    # Clear default "block all public access" setting
    s3client = boto3.client("s3")
    s3client.delete_public_access_block(Bucket=bucket_name)
    # Gets the bucket policy
    bucket_policy = bucket_config.bucket_policy(bucket_name)
    # Sets the bucket policy
    s3.Bucket(bucket_name).Policy().put(Policy=json.dumps(bucket_policy))
    print("Bucket policy set")
    # Adding image to bucket
    bucket_config.get_image()
    image = 'logo.jpg'
    s3.Object(bucket_name, image).put(Body=open(image, 'rb'))
    print("Image added to bucket")
    print("Bucket: " + bucket_name + " successfully created")
    return bucket
  except Exception as e:
    print (f"Issue creating bucket: {e}")


create_bucket()