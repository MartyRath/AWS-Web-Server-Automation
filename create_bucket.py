#!/usr/bin/python3
# Author: Marty Rath     
# Description: Creates an s3 bucket, randomly named using uuid. Adapted from scripts made available in lab 4. 

import boto3
import bucket_config
import webbrowser

def create_bucket():
  # Naming the bucket with six random characters and mrath
  bucket_name = bucket_config.create_bucket_name()
  s3 = boto3.resource("s3")
  try:
    # Creates the bucket
    bucket = s3.create_bucket(Bucket=bucket_name)
    print("Bucket created")
    # Configures website
    bucket_config.configure_website(s3, bucket_name)
    # Gets the bucket policy
    bucket_policy = bucket_config.create_bucket_policy(bucket_name)
    # Clears default "block all public access" setting and sets policy
    bucket_config.set_bucket_policy_and_access(s3, bucket_name, bucket_policy)
    print("Bucket access & policy set")
    # Download image locally
    bucket_config.download_image()
    image = 'logo.jpg'
    # Upload image to bucket
    s3.Object(bucket_name, image).put(Body=open(image, 'rb'), ContentType='image/jpeg')
    print("Image added to bucket")
    # Creates index.html with image
    bucket_config.create_index(bucket_name, image)
    # Upload index.html to bucket
    s3.Object(bucket_name, "index.html").put(Body=open("index.html", 'rb'), ContentType='text/html')
    print("index.html added to bucket")
    print("Bucket: " + bucket_name + " successfully created")
    url = f"http://{bucket_name}.s3-website-us-east-1.amazonaws.com"
    
    # Setting to write mode, will overwrite any data.
    with open("mrath-websites.txt", "w") as file:
      file.write(url + "\n")
    webbrowser.open_new_tab(url)
    return bucket_name
  except Exception as e:
    print (f"Issue creating bucket: {e}")
