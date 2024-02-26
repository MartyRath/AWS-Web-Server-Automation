#!/usr/bin/python3
# Deletes all s3 buckets and their contents

import boto3

def delete_all_buckets():
  s3 = boto3.resource('s3')
  try:
    # Iterate through all buckets
    for bucket in s3.buckets.all():
      # Delete all objects in the bucket first
      bucket.objects.all().delete()
      # Then delete the bucket itself
      bucket.delete()
      print(f"Bucket '{bucket.name}' deleted successfully.")
  except Exception as e:
    print(f"Failed to delete buckets: {e}")

delete_all_buckets()