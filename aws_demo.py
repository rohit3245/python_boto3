import boto3
import json


bucket_name = 'demo-bucket-rohit123'
region = 'us-east-2'

# 1. Create S3 client
s3 = boto3.client('s3', region_name='us-east-2')

# 2. Create the bucket
try:
    s3.create_bucket(
        Bucket='demo-bucket-rohit123',
        CreateBucketConfiguration={'LocationConstraint': 'us-east-2'}
    )
    print(" Bucket 'demo-bucket-rohit123' created.")
except s3.exceptions.BucketAlreadyOwnedByYou:
    print(" Bucket 'demo-bucket-rohit123' already exists and is owned by you.")
except s3.exceptions.BucketAlreadyExists:
    print(" Bucket 'demo-bucket-rohit123' already exists globally. Use a unique name.")
    exit()

# 3. Upload HTML files
try:
    s3.upload_file('index.html', 'demo-bucket-rohit123', 'index.html', ExtraArgs={'ContentType': 'text/html'})
    s3.upload_file('error.html', 'demo-bucket-rohit123', 'error.html', ExtraArgs={'ContentType': 'text/html'})
    print(" Uploaded index.html and error.html to 'demo-bucket-rohit123'.")
except Exception as e:
    print(f" Error uploading files: {e}")
    exit()

# 4. Enable static website hosting
try:
    s3.put_bucket_website(
        Bucket='demo-bucket-rohit123',
        WebsiteConfiguration={
            'IndexDocument': {'Suffix': 'index.html'},
            'ErrorDocument': {'Key': 'error.html'}
        }
    )
    print(" Static website hosting enabled on 'demo-bucket-rohit123'.")
except Exception as e:
    print(f" Error setting website configuration: {e}")
    exit()

# 5. Set public read bucket policy
bucket_policy = {
    "Version": "2012-10-17",
    "Statement": [{
        "Sid": "PublicReadGetObject",
        "Effect": "Allow",
        "Principal": "*",
        "Action": ["s3:GetObject"],
        "Resource": ["arn:aws:s3:::demo-bucket-rohit123/*"]
    }]
}

try:
    s3.put_bucket_policy(
        Bucket='demo-bucket-rohit123',
        Policy=json.dumps(bucket_policy)
    )
    print(" Public read policy applied to 'demo-bucket-rohit123'.")
except Exception as e:
    print(f" Error applying bucket policy: {e}")
    exit()

# 6. Print the website URL
website_url = "http://demo-bucket-rohit123.s3-website.us-east-2.amazonaws.com"
print(f"\n Website deployed at: {website_url}")
