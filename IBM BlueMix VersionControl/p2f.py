from flask import Flask, render_template, redirect, url_for, request,make_response
from cloudant import cloudant
from base64 import b64encode,b64decode
import hashlib,os
import datetime
app = Flask(__name__)
PORT = int(os.getenv('PORT', 8080))
result=[]
result1=[]
result2=[]
#pip freeze > requirements.txt

@app.route('/',methods=['POST', 'GET'])
def index():

    return render_template("R:/index.html")


@app.route('/test', methods=['POST', 'GET'])
def checktextbox():
    quote=''
    now = datetime.datetime.now()
    #---------------------------------------------------------------------------------
    digest1=''
    digest3=''
    digest1encoded=''

    def md5_for_file(f, block_size=2 ** 20):
        md5 = hashlib.md5()
        while True:
            data = f.read(block_size)
            if not data:
                break
            md5.update(data.encode('utf8'))
        return md5.digest()
    #---------------------------------------------------------------------------------
    if request.method == 'POST':
        user = request.form['check']
        print user

        f = request.files['file']
        f_name=f.filename
       
        print f
       

        uploaded_file_content = b64encode(f.read())
        k=uploaded_file_content
        decoded_content=b64decode(k)
        #print 'decoded',decoded_content
        #print 'Encoded content',uploaded_file_content
        USERNAME = ''
        PASSWORD = ''
        with cloudant(USERNAME, PASSWORD,
                          url='') as client:

            
            my_db = client['my_database']
           
            i=0
            count=0
            versionno1=0
            flag = 1
            for document in my_db:
                print document

            fileexistscount=0
            for document in my_db:
                name = document['file_name']
                tail = name.split('.')
                namecheck=tail[0]+'.'+tail[1]
                print 'Namecheck',namecheck
                if (document['file_name'] == f_name or namecheck == f_name ) :
                    fileexistscount=fileexistscount+1
                    if len(tail)==2:
                        print tail[0], tail[1]

                    else:
                        print tail[0],tail[1],tail[2]
                        versionno=tail[2].split(' ')
                        versionno1=int(versionno[1])
                        count=count+1
                        print versionno1
                    #print 'NAme is ',name
#---------------------------------------------------------------------------------------------------------------------------------------
                if document['file_name']==f_name or namecheck==f_name:
                    fileexistscount = fileexistscount + 1
                    f1 = document.get_attachment(f_name, attachment_type='binary')



                    md51 = hashlib.md5()
                    md51.update(f1)
                    digest1 = md51.digest()
                    md52 = hashlib.md5()
                    md52.update(decoded_content)
                    digest2 = md52.digest()
                    digest3=digest2
                    digest3=b64encode(digest3)

                   
                    if(digest1 == digest2):
                        #print('File contents same,Already exists!')
                        flag=0
            if fileexistscount==0:
                print 'File nor file versions exists, so adding new file'
                quote='File nor file versions exists, so adding new file'
                md53 = hashlib.md5()
                md53.update(decoded_content)
                digest3 = md53.digest()
                digest3 = b64encode(digest3)
                data = {'file_name': f_name, 'version no':'','date and time':now.isoformat() , 'hashed_value': digest3, '_attachments': {f_name: {'data': uploaded_file_content}}}
                doc = my_db.create_document(data)

            if flag==1 and fileexistscount!=0:
                print 'Creating new version'
                quote='Creating new version'
                #for document in my_db:
                data = {'file_name': f_name+'.v '+str(count),'version no':count,'date and time':now.isoformat(), 'hashed_value': digest3, '_attachments': {f_name: {'data': uploaded_file_content}}}
                doc = my_db.create_document(data)
            elif flag==0 and fileexistscount>0:
                print ' Version already exists Sorry file cannot be uploaded'
                quote=' Version already exists Sorry file cannot be uploaded'
                #data = {'file_name': f_name, '_attachments': {f_name: {'data': uploaded_file_content}}}
                #doc = my_db.create_document(data)

#---------------------------------------------------------------------------------------------------------------------------------------------------
                
#----------------------------------------------------------------------------------------------------------------------------------------------------
            print count

    return  render_template("R:/next.html",quote=quote)
@app.route('/download', methods=['POST'])
def download():
    USERNAME = ''
    PASSWORD = ''
    with cloudant(USERNAME, PASSWORD,
                  url='') as client:

        my_db = client['my_database']
	file_name = request.form['filename']
	for document in my_db:
		if (document['file_name'] == file_name):
			f2=file_name.split('.')
			f3=f2[0]+'.'+f2[1]
			file = document.get_attachment(f3, attachment_type='binary')
			print file
			response = make_response(file)
			response.headers["Content-Disposition"] = "attachment; filename=%s"%file_name
			return response
		else:
			response = 'File not found'
	return response

@app.route('/delete', methods=['POST'])
def delete():
    USERNAME = ''
    PASSWORD = ''
    with cloudant(USERNAME, PASSWORD,
                  url='') as client:

        my_db = client['my_database']
        file_name = request.form['filename']
        for document in my_db:
            if document['file_name'] == file_name:
                #f2 = file_name.split('.')
                #f3 = f2[0] + '.' + f2[1]
                document.delete()
                return ("File found and deleted")
                #document.delete_attachment(file_name)
            else:
                return ('File not found')
    return 'File deleted'
	#return app.send_static_file('index.html')
#--------------------------------------------------------------------------------------------------------------------------------
@app.route('/listing', methods=['POST'])
def listing():
    result=[]
    result1=[]
    result2=[]
    USERNAME = '1'
    PASSWORD = ''
    with cloudant(USERNAME, PASSWORD,
                  url='') as client:
        my_db = client['my_database']
        for document in my_db:
            result.append(document['file_name'])
            result1.append(document['version no'])
            result2.append(document['date and time'])
        print ''
    return render_template("R:/result.html", result=result, result1=result1,result2=result2)

if __name__ == '__main__':
    #app.run(host='0.0.0.0',port=PORT,debug=True)
    app.run(debug=True)
