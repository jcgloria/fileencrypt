# FilEncrypt
### Development in Progress

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
