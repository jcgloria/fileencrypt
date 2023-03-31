from flask import Flask, render_template, redirect, abort, request, send_file
from flask_cors import CORS
import boto3
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

credentials = json.loads(open('env.json').read())
s3 = boto3.client('s3', aws_access_key_id=credentials['aws_access_key_id'], aws_secret_access_key=credentials['aws_secret_access_key'], region_name=credentials['region'])

# Get the list of buckets
bucketList = []
for bucket in s3.list_buckets()['Buckets']:
    bucketList.append(bucket['Name'])

currentBucket = bucketList[0]

@app.route('/')
def index():
    return redirect("/" + currentBucket + "/")

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        route = request.form['route']
        bucket = request.form['bucket']
        file = request.files['file']
        file_data = file.read()
        handle_uploaded_file(file_data, bucket, route)
        return redirect("/" + currentBucket + "/")
    else:
        return render_template('upload.html', currentBucket=currentBucket, bucketList=bucketList)

@app.route("/downloadRequest", methods=['POST'])
def downloadRequest():
    body = request.get_json()
    bucket = body['bucket']
    key = body['key']
    file = s3.get_object(Bucket=bucket, Key=key)
    # save file to disk
    fileName = key.split("/")[-1] #remove directories if any
    with open('./client_files/' + fileName, 'wb') as f:
        f.write(file['Body'].read())
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
    print("FILES")
    return render_template('index.html', files=files, bucketList=bucketList, currentBucket=currentBucket, dir_string=dirPath)

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
    #organize results. Place folders first
    results.sort(key=lambda x: x['isFolder'], reverse=True)
    return results

def handle_uploaded_file(f, bucket, route):
    if route[0] == "/":
        route = route[1:]
    s3.put_object(Body=f, Bucket=bucket, Key=route)

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