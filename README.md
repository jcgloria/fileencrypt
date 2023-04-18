# FilEncrypt
A web-based, client-side file encryption and decryption file manager integrated with AWS S3. Encryption keys are purely stored in the user's machine and are never sent to AWS. 

- The web application framework used is [Flask](https://flask.palletsprojects.com/en/2.2.x/).
- The integration with AWS S3 is done using the AWS SDK for Python [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html). 
- The UI components used are from [FastBootstrap](https://fastbootstrap.com/).
- The encryption is done using Advanced Encryption Standard (AES) with the Fernet library from [cryptography](https://cryptography.io/en/latest/fernet/).

### Installation
#### 1. Set AWS credentials in a new file `env.json` in the root directory of the project. The file should contain the following:
```json
{
    "aws_access_key_id": "<Access Key ID>",
    "aws_secret_access_key": "<Secret Access Key>",
    "region": "<region>"
}
```
The steps to create these credentials can be found [here](https://docs.aws.amazon.com/powershell/latest/userguide/pstools-appendix-sign-up.html). An AWS account is required to create these credentials. The region can be any of the [AWS regions](https://docs.aws.amazon.com/general/latest/gr/rande.html). Example: `eu-west-2` (London). 

The user associated to the AWS credentials can have administrator access for simplicity. If specific permissions want to be applied then the user should have a policy with the following actions:

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