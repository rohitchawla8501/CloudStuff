from flask import Flask,render_template,request,flash
import time
from boto.s3.key import Key
from boto.s3.connection import S3Connection
app = Flask(__name__)
access_key=''
access_secret=''
conn = S3Connection(access_key,access_secret )
bucket=conn.get_bucket('buck8501')

@app.route('/',methods=['POST','GET'])
def login():
    return render_template('login.html')

@app.route('/f',methods=['POST','GET'])
def front():
    username=request.form['username']
    password=request.form['password']
    if username=='rohit' and password=='rohit':
        #flash("Check")
        return render_template('upload.html')
    else:
        return 'Not an Authorized USER!!'

@app.route('/upload',methods=['POST','GET'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        file_name = file.filename
        mimetype = file.content_type
        print mimetype
        # Upload a new file
        k = Key(bucket)
        k.key = file_name
        k.set_contents_from_string(file.read())
        #bucket.put_object(Key=file_name, Body=file.read())
        #flash("File uploaded successfully!!!")
    return ('Image uploaded')

@app.route('/download',methods=['POST','GET'])
def download():
    filename=request.form['filename']
    for f in bucket.get_all_keys():
        if(filename==f.key):
            f.get_contents_to_filename(filename+'.txt')
    return "done"
@app.route('/delete',methods=['POST','GET'])
def delete():
    filename=request.form['filename']
    for f in bucket.get_all_keys():
        if(filename==f.key):
            f.delete()
    return "done"
@app.route('/list',methods=['POST','GET'])
def list():
    result=[]
    for f in bucket.get_all_keys():
        result.append(f.key)

    return render_template('list.html',result=result)

if __name__ == '__main__':
    app.run(debug=True)
