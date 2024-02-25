#!/usr/bin/python3
# Author: Marty Rath     
# Description: This Python program creates an s3 bucket, randomly named using uuid. Adapted from scripts made available in lab 4. 

import boto3
import uuid
import s3_website_config
import json

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

  # Adding image to bucket
  s3_website_config.get_image()
  image = 'logo.jpg'
  s3.Object(bucket_name, image).put(Body=open(image, 'rb'))

  # Making the bucket objects publicly accessible
  s3client = boto3.client("s3")
  s3client.delete_public_access_block(Bucket=bucket_name)

  # Get bucket policy from helper function in s3_website_config
  bucket_policy = s3_website_config.bucket_policy(bucket_name)
  # Setting policy to bucket
  s3.Bucket(bucket_name).Policy().put(Policy=json.dumps(bucket_policy))


create_bucket()