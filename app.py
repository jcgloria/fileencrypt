from flask import Flask, render_template, redirect, abort, request, send_file
from flask_cors import CORS
import boto3
import json
import encrypt_utils
import os

app = Flask(__name__)
CORS(app)

credentials = json.loads(open('env.json').read())
s3 = boto3.client('s3', aws_access_key_id=credentials['aws_access_key_id'], aws_secret_access_key=credentials['aws_secret_access_key'], region_name=credentials['region'])

# Get the list of buckets
bucketList = []
for bucket in s3.list_buckets()['Buckets']:
    bucketList.append(bucket['Name'])
if len(bucketList) > 0:
    currentBucket = bucketList[0]
else:
    currentBucket = ""

# Get the list of keys
keyList = []
files = os.listdir("./keys")
for file in files:
    if file.endswith(".key"):
        keyList.append(file)
if len(keyList) > 0:
    currentKey = keyList[0]
else:
    currentKey = ""

@app.route('/')
def index():
    return redirect("/" + currentBucket + "/")

@app.route('/settings')
def settings():
    return render_template('settings.html', keyList=keyList, currentKey=currentKey)

@app.route("/upload", methods=['GET', 'POST'])
def upload():
    msg = ""
    if request.method == 'POST':
        route = request.form['route']
        bucket = request.form['bucket']
        file = request.files['file']
        key = request.form['formKey']
        file_data = file.read()
        success = handle_uploaded_file(file_data, key, bucket, route)
        if success:
            return redirect("/" + currentBucket + "/")
        else:
            msg = "Error uploading file"

    return render_template('upload.html', currentBucket=currentBucket, bucketList=bucketList, keyList=keyList, currentKey=currentKey, message=msg)

@app.route("/downloadRequest", methods=['POST'])
def downloadRequest():
    body = request.get_json()
    bucket = body['bucket']
    key = body['key']
    file = s3.get_object(Bucket=bucket, Key=key)
    fileName = key.split("/")[-1] # remove the path
    fileName = fileName.replace(".encrypted", "") # remove the encrypted extension
    if 'encryption_key' not in file['Metadata']:
        return json.dumps({"error": "No encryption key was defined in file"}), 500
    try:
        key = file['Metadata']['encryption_key']
        decrypted = encrypt_utils.decrypt("./keys/" + key, file['Body'].read())
    except Exception as e:
        return json.dumps({"error": "Encryption key was not found in local computer"}), 500
    with open('./client_files/' + fileName, 'wb') as f:
        f.write(decrypted)
    return json.dumps({"file": fileName}), 200

@app.route("/downloadFile")
def downloadFile():
    # get the get params
    file = request.args.get('file')
    return send_file('./client_files/'+file, as_attachment=True)

@app.route('/<path:dirPath>')
def any_route(dirPath):
    files = get_objects_by_dir(dirPath)
    if files == 404:
        abort(404)
    return render_template('index.html', files=files, bucketList=bucketList, currentBucket=currentBucket, dir_string=dirPath)

@app.route('/generateKey', methods=['GET','POST'])
def generateKey():
    if request.method == 'GET':
        return redirect("/settings")
    else:
        keyName = request.form['keyName']
        encrypt_utils.generateKey("./keys/" + keyName + ".key")
        keyList.append(keyName + ".key")
        return render_template('settings.html', keyList=keyList, currentKey=currentKey, message="Key generated successfully")

@app.route('/importKey', methods=['GET','POST'])
def importKey():
    if request.method == 'GET':
        return redirect("/settings")
    else:
        keyName = request.form['keyName']
        keyString = request.form['keyString']
        encrypt_utils.importKey("./keys/" + keyName + ".key", keyString)
        keyList.append(keyName)
        return render_template('settings.html', keyList=keyList, currentKey=currentKey, message="Key imported successfully")

def get_objects_by_dir(dir):
    dirs = dir.split("/")
    bucketName = dirs[0]
    if bucketName not in bucketList: # Bucket exists?
        return 404
    global currentBucket
    currentBucket = bucketName # Set the current bucket
    # remove empty strings
    dirs = list(filter(None, dirs))
    if len(dirs) == 1: # User only wants the bucket root
        objects = s3.list_objects(Bucket=bucketName)
        if 'Contents' in objects:
            return parseObjects(objects['Contents'], "")
        else:
            return []
    route = dir.split("/", 1)[1] # User wants a specific directory in a bucket.
    try:
        s3.head_object(Bucket=bucketName, Key=route) # does the directory exist?
    except:
        return 404
    objects = s3.list_objects(Bucket=bucketName, Prefix=route)
    if 'Contents' in objects:
        return parseObjects(objects['Contents'], route)
    else:
        return []

def parseObjects(objects, route):
    results = []
    for object in objects:
        result = {}
        if object['Key'] == route:
            continue
        result['name'] = object['Key']
        result['size'] = convert_size(object['Size'])
        result['lastModified'] = object['LastModified'].strftime("%B %d, %Y, %I:%M %p")
        result['isFolder'] = object['Key'].endswith("/")
        if result['name'].startswith(route) and result['isFolder']:
            result['name'] = result['name'].replace(route, "")
        results.append(result)
    results.sort(key=lambda x: x['isFolder'], reverse=True)
    return results

def handle_uploaded_file(f, key, bucket, route):
    if route[0] == "/":
        route = route[1:]
    try:
        encrypted = encrypt_utils.encrypt("./keys/" + key, f)
        s3.put_object(Body=encrypted, Bucket=bucket, Key=route+'.encrypted', Metadata={'encryption_key': key})
        return True
    except Exception as e:
        print(e)
        return False

def convert_size(size_bytes):
    units = ["Bytes", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(units)-1:
        size_bytes /= 1024
        i += 1
    if int(size_bytes) == size_bytes:
        return f"{int(size_bytes)} {units[i]}"
    else:
        return f"{size_bytes:.2f} {units[i]}"