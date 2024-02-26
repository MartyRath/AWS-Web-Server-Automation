#!/usr/bin/python3
# Author: Marty Rath
# Description: This configures all requirements for the s3 bucket.
# Functions: 
# create_bucket_name
# download_image
# create_bucket_policy
# set_bucket_policy_and_access
# configure_website
# create_index

import boto3
import requests
import uuid
import json

# Returns 6 random characters using uuid. Used to name bucket.
def create_bucket_name():
  # Getting a uuid of random characters
  random_uuid = uuid.uuid4()
  # Splicing down to 6 characters and converting to string
  bucket_name = str(random_uuid)[:6] + "mrath" 
  return bucket_name

# Gets the image at url and names it logo.jpg
def download_image():
  # Response from image url request
  response = requests.get("http://devops.witdemo.net/logo.jpg")

  # Opens logo.jpg in write binary mode
  try:
    with open("logo.jpg", "wb") as file:
      # Write the binary content from response to the file
      file.write(response.content)
      print("Downloaded: " + "logo.jpg")
  except Exception as e:
    print ("Issue downloading image", e)

# Creates the bucket policy for the input bucket name
def create_bucket_policy(bucket_name):
  bucket_policy = {
  "Version": "2012-10-17",
  "Statement": 
  [{
    "Sid": "PublicReadGetObject",
    "Effect": "Allow",
    "Principal": "*",
    "Action": ["s3:GetObject"],
    "Resource": f"arn:aws:s3:::{bucket_name}/*"}]}
  return bucket_policy

# Sets the bucket policy and sets access to public
def set_bucket_policy_and_access(s3, bucket_name, bucket_policy):
  s3client = boto3.client("s3")
  s3client.delete_public_access_block(Bucket=bucket_name)
  # Sets the bucket policy
  s3.Bucket(bucket_name).Policy().put(Policy=json.dumps(bucket_policy))

# Configures website
def configure_website(s3, bucket_name):
  website_configuration = {
  'ErrorDocument': {'Key': 'error.html'},
  'IndexDocument': {'Suffix': 'index.html'},}
  bucket_website = s3.BucketWebsite(bucket_name)
  bucket_website.put(WebsiteConfiguration=website_configuration)

# Create an index page, add image from bucket, and save it index.html locally
def create_index(bucket_name, image):
  index = f'''<html><body><img src="https://{bucket_name}.s3.amazonaws.com/{image}">
  </body></html>
  '''
  with open('index.html', 'w') as file:
    file.write(index)