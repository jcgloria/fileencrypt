import boto3
import json
credentials = json.loads(open('env.json').read())
s3 = boto3.client('s3', aws_access_key_id=credentials['aws_access_key_id'], aws_secret_access_key=credentials['aws_secret_access_key'], region_name=credentials['region'])

dir = "juan-mybucket/wasaaa/"
bucketName = dir.split("/")[0]
route = dir.split("/", 1)[1]
files = s3.list_objects(Bucket=bucketName, Prefix=route)['Contents']
for f in files:
    print(f['Key'])

print(route)





