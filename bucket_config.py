#!/usr/bin/python3
# Author: Marty Rath
# Description: This bucket needs to contain at least two items:
''' o An image which we will make available at http://devops.witdemo.net/logo.jpg. Your
Python program should download this image and then upload it to your newly-created
bucket. The image at this URL will change from time to time, so your code will need to
handle this in a generic manner.
o A web page called index.html which displays the image - e.g. using <img> tag.
Configure the S3 bucket for static website hosting so that the image can be accessed with a URL
of the form http://bucket-name.s3-website-us-east-1.amazonaws.com (note that index and image
file names are not in the URL, just the bucket name '''

import boto3
import requests
import uuid

# Returns 6 random characters using uuid
def get_random_characters():
  # Getting a uuid of random characters
  random_uuid = uuid.uuid4()
  # Splicing down to 6 characters and converting to string
  random_characters = str(random_uuid)[:6] 
  return random_characters

# Gets the image at url and names it logo.jpg
def get_image():
  # Response from image url request
  response = requests.get("http://devops.witdemo.net/logo.jpg")

  # Opens logo.jpg in write binary mode
  try:
    with open("logo.jpg", "wb") as file:
      # Write the binary content from response to the file
      file.write(response.content)
      print("Retrieved image saved as: " + "logo.jpg")
  except Exception as e:
    print ("Issue downloading image", e)

# Sets the bucket policy for the input bucket name
def bucket_policy(bucket_name):
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
