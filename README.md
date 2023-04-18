# FilEncrypt
A web-based, client-side file encryption and decryption service using AES integrated with AWS S3. The application is written in Python using [Flask](https://flask.palletsprojects.com/en/2.2.x/) and the AWS SDK for Python ([Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)). The UI components used are from [FastBootstrap](https://fastbootstrap.com/).

### Installation
#### 1. Set AWS credentials in `env.json`
```json
{
    "aws_access_key_id": "<Access Key ID>",
    "aws_secret_access_key": "<Secret Access Key>",
    "region": "<region>"
}
```
The AWS credentials should have the following permissions:
- s3:PutObject
- s3:GetObject
- s3:ListAllMyBuckets
- s3:ListBucket
            
#### 2. Install dependencies
```bash
pip3 install -r requirements.txt
```
#### 3. Run the flask application
```bash
flask --app app run
```
