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


def get_image(url, file_name):
  # Response from image url request
  response = requests.get(url)

  # Opens logo.jpg in write binary mode
  try:
    with open(file_name, "wb") as file:
      # Write the binary content from response to the file
      file.write(response.content)
      print("Success! Saved as: " + file_name)
  except Exception as e:
    print ("Issue downloading content", e)

get_image("http://devops.witdemo.net/logo.jpg", "image.jpg")
