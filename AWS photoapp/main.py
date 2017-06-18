from flask import Flask, render_template, url_for, request, session, redirect
from pymongo import MongoClient
import flask
import boto
from boto.s3.key import Key
from boto.s3.connection import S3Connection, Location
from werkzeug.utils import secure_filename
import os
import datetime

UPLOAD_FOLDER = './static/img/'
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']
app = Flask(__name__)
app.secret_key = ''
app.config['SESSION_TYPE'] = 'filesystem'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('user'))

    return render_template('index.html')


@app.route('/user', methods=['POST', 'GET'])
def user():
    client = MongoClient('')
    db = client.photoapp
    users = db.users
    if 'logout' in request.form:
        session.pop('username', None)
        return redirect(url_for('index'))
    if request.method == 'POST':
        if 'file' not in request.files:
            flask.flash('No file part')
            return redirect(url_for('user'))
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flask.flash('No selected file')
            return redirect(url_for('user'))
        if file and allowed_file(file.filename):
            flask.flash(file.filename)
            filename = secure_filename(file.filename)
            addr = session['username'] + str(datetime.datetime.now()) + filename
            access_key = ''
            access_secret = ''
            conn = S3Connection(access_key, access_secret)
            bucket = conn.get_bucket('')
            k = Key(bucket)
            k.key = addr
            k.set_contents_from_filename(file.filename)
            k.make_public()
            login_user = users.find_one({'name': session['username']})
            current_images = []
            if 'images' in login_user:
                current_images = login_user['images']
            if len(current_images) >= 30:
                flask.flash('Limited exceeded')
                return redirect(url_for('user'))

            current_images.append(''+addr)
            users.update({"name": session['username']}, {'$set': {'images': current_images}})
            flask.flash('Image Uploaded')

    return render_template('user.html')


@app.route('/images', methods=['POST', 'GET'])
def images():
    client = MongoClient('')
    db = client.photoapp
    users = db.users
    all_users = users.find()
    comments = db.comments
    all_images = []
    for user in all_users:
        if 'images' in user:
            for image in user['images']:
                image_comments = comments.find_one({'image': image})
                all_images.append([image, image_comments])

    return render_template('dispImg.html', all_images=all_images)


@app.route('/addcomment', methods=['POST'])
def addcomment():
    client = MongoClient('')
    db = client.photoapp
    comments = db.comments
    image = request.form['image']
    comment_text = request.form['comment']
    time = datetime.datetime.now()

    image_comment = comments.find_one({'image': image})
    current_comments = []
    if image_comment:
        if 'comments' in image_comment:
            current_comments = image_comment['comments']
    current_comments.append([time, session['username'], comment_text])
    comments.update({"image": image}, {'$set': {'comments': current_comments, "image": image}}, True)
    return redirect(url_for('images'))


@app.route('/myimages', methods=['GET'])
def myimages():
    client = MongoClient('')
    db = client.photoapp
    users = db.users
    login_user = users.find_one({'name': session['username']})
    my_images = []
    if 'images' in login_user:
        my_images = login_user['images']
    return render_template('myimage.html', my_images=my_images)


@app.route('/delimages', methods=['POST'])
def delimages():
    client = MongoClient('')
    db = client.photoapp
    users = db.users
    login_user = users.find_one({'name': session['username']})
    my_images = []
    delimg = request.form['image']
    if 'images' in login_user:
        my_images = login_user['images']

    my_images.remove(delimg)
    users.update({'name': session['username']}, {'$set': {'images': my_images, 'name': session['username']}}, True)
    return render_template('myimage.html', my_images=my_images)


@app.route('/login', methods=['POST'])
def login():
    client = MongoClient('')
    db = client.photoapp
    users = db.users
    login_user = users.find_one({'name': request.form['username']})

    if login_user:
        if (request.form['pass'].encode('utf-8')) == login_user[
            'password'].encode('utf-8'):
            session['username'] = request.form['username']
            return redirect(url_for('index'))

    return 'Invalid username/password combination'


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        client = MongoClient('')
        db = client.photoapp
        users = db.users
        existing_user = users.find_one({'name': request.form['username']})

        if existing_user is None:
            hashpass = (request.form['pass'].encode('utf-8'))
            users.insert({'name': request.form['username'], 'password': hashpass})
            session['username'] = request.form['username']
            return redirect(url_for('index'))

        return 'That username already exists!'

    return render_template('register.html')


if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)
