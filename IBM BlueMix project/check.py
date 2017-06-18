import swiftclient
from Crypto.Cipher import AES
import os,random,struct,time
class check:

    auth_url = ""
    password = ""
    project_id = ""
    user_id = ""
    region_name = 'dallas'
    conn=swiftclient.Connection(key=password,
                                authurl=auth_url,
                                auth_version='3',
                                os_options={"project_id": project_id, "user_id": user_id, "region_name": region_name})

 
    print ('Enter your choice :  1.Create Container 2.Encrypt File and upload 3.Download and decrypt 4.Details of files 5.Delete a remote file ')
    choice=input()
    if choice==1:
        name=input('Enter name of container')
        container_name = name
        conn.put_container(container_name)
    elif choice==2: #uploading to cloud
        Inputpath=input('Enter input path')
        Outputpath = input('Enter output path')
        def encrypt_file(key, in_filename, out_filename=None, chunksize=64 * 1024):

            if not out_filename:
                out_filename = in_filename + '.enc'

            iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
            encryptor = AES.new(key, AES.MODE_CBC, iv)
            filesize = os.path.getsize(in_filename)

            with open(in_filename, 'rb') as infile:
                with open(out_filename, 'wb') as outfile:
                    outfile.write(struct.pack('<Q', filesize))
                    outfile.write(iv)

                    while True:
                        chunk = infile.read(chunksize)
                        if len(chunk) == 0:
                            break
                        elif len(chunk) % 16 != 0:
                            chunk += ' ' * (16 - len(chunk) % 16)

                        outfile.write(encryptor.encrypt(chunk))

        encrypt_file("1234567812345678",Inputpath,Outputpath)
        time.sleep(10)
        fo = open(Outputpath, "r+")
        conn.put_object('project1', Outputpath, contents=fo.read())
        print('Uploaded encrypted file')
        fo.close()


    elif choice == 3: #fetching from cloud
        Inputpath2=input('Enter name of file to fetch from cloud')
        Outputpath2='R:\ xyz.txt'
        Outputpath3=input('Enter path to save file fetched from cloud ')
        print Inputpath2
       
        obj_tuple = conn.get_object('project1', Inputpath2)
        with open(Outputpath2, 'w') as my_hello:
            my_hello.write(obj_tuple[1])
        def decrypt_file(key, in_filename, out_filename=None, chunksize=24 * 1024):

            if not out_filename:
                out_filename = os.path.splitext(in_filename)[0]

            with open(in_filename, 'rb') as infile:
                origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
                iv = infile.read(16)
                decryptor = AES.new(key, AES.MODE_CBC, iv)

                with open(out_filename, 'wb') as outfile:
                    while True:
                        chunk = infile.read(chunksize)
                        if len(chunk) == 0:
                            break
                        outfile.write(decryptor.decrypt(chunk))
                    outfile.truncate(origsize)

        decrypt_file('1234567812345678',Outputpath2,Outputpath3)
        
    elif choice==4 :
        print('Details of Files')
        for data in conn.get_container('project1')[1]:
            print '{0}\t{1}\t{2}'.format(data['name'], data['bytes'], data['last_modified'])

    elif choice==5:

        s=input('Enter file name to be deleted')
        conn.delete_object('project1',s)
        print 'File deleted'
    else:
        print 'Wrong Choice'

    #------------------------------------------------------------------------------------------------------------------

    #IV = os.urandom(16)
    IV = 16 * '\x00'  # Initialization vector:
    mode = AES.MODE_CBC
    encryptor = AES.new(key, mode, IV=IV)

    text = 'hello'*16
    ciphertext = encryptor.encrypt(text)
    #print ciphertext

    decryptor = AES.new(key, mode, 16 * '\x00')
    plain = decryptor.decrypt(ciphertext)
    #print plain
#---------------------------------------------------------------------------------------------------------------------------------
def put(filename,conn):                                 #This code works for 10Mb total size of files
    for container in conn.get_account()[1]:
        for data in conn.get_container('project1')[1]:
            if (filename == data['name']):
                print "File already exists"

    size = os.path.getsize(filename)
    if (size <= 10000):
        with open(filename, 'r') as hello:
            conn.put_object('Cloud assignment 1', filename, hello.read(), content_type='text')
        print ("File list:")
        for container in conn.get_account()[1]:
            for data in conn.get_container('project1')[1]:
                print '-> {0}t size: {1}t date: {2}'.format(data['name'], data['bytes'], data['last_modified'])
    else:
        print("File is larger than limit")


