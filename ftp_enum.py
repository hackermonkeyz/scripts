#!/usr/bin/python3
import ftplib,os,sys,time,datetime,logging,argparse
from argparse import RawTextHelpFormatter

def checkpwd(ftp):
    logger.info("PWD: "+ftp.pwd())

def createTestFile(tf_name):
    write_f = open(tf_name,"w+")
    write_f.write("upload success")
    write_f.close()

def putShell(ftp, tf_name):
    send_f = open(tf_name,'rb')
    try:
        ftp.storbinary('STOR '+tf_name, send_f)
        logger.critical("\t\t\t[UPLOAD SUCCESS] in "+ ftp.cwd())
        input("\t\t\tPress any key to continue...")
    except Exception as e:
        logger.error(str(e) + "Unable to upload here.")
        send_f.close()

def downloadFiles(ftp, path, destination, ftab, ignore=None):
    try:
        ftp.cwd(path)
        checkpwd(ftp)   
        os.chdir(destination)
        creatDir(destination[0:len(destination)] + path)
        logger.info("Created: " + destination[0:len(destination)] + path)
    except Exception as e:
        logger.error(e)     
        pass
    except ftplib.error_perm:       
        logger.error("Could not change to " + path)
        sys.exit("Ending Application")
    
    filelist=ftp.nlst()
    for f in filelist:
        logger.info(ftab+path+f)

    ftab = "\t"+ftab
    for f in filelist:
        time.sleep(interval)
        try:
            ftp.cwd(path + f + "/")
            if ignore is not None:
                if f in ignore:
                    logger.warning("[!] Ignoring "+path+f)
                    continue
            else:              
                downloadFiles(ftp, path + f + "/", destination, ftab, ignore)

        except ftplib.error_perm:
            os.chdir(destination[0:len(destination)] + path)
            try:
                # logger.debug(os.path.join(destination + path, f) + " PWD: "+ftp.pwd())
                ftp.retrbinary("RETR " + path+ f, open(os.path.join(destination + path, f),"wb").write)
                logger.info("\t\t[DOWNLOADED]: " + f)
            except Exception as e:
                logger.warning("[!]: "+str(e)+" Unable to Download: " + f)
    return
    
def listFiles(ftp, path, destination, ftab, ftpput, ignore=None):
    try:
        ftp.cwd(path)
        checkpwd(ftp)
        if ftpput:
            putShell(ftp, tf_name)
    except OSError:     
        pass
    except ftplib.error_perm:       
        logger.error("Error: could not change to " + path)
        sys.exit("Ending Application")
    
    filelist=ftp.nlst()
    for f in filelist:
        logger.info(ftab+f)

    ftab = "\t"+ftab

    for f in filelist:
        time.sleep(interval)
        if ignore:
            if f in ignore:
                logger.warning("[!] Ignoring "+path+f)
                continue
        try:            
            ftp.cwd(path + f + "/")          
            listFiles(ftp, path + f + "/", destination, ftab, ftpput, ignore)
        except ftplib.error_perm:            
            pass

    return

def checkList(ignore, common):
    if ignore:
        result = ignore + list(set(common) - (set(ignore)))
    else:
        result = common

    return result

def creatDir(path):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except OSError as exc:
        logger.error("CreateDir: "+exc)


if __name__=="__main__":
    parser = argparse.ArgumentParser(description="""FTP enumerator - created by ibr0wse""",
                usage='%(prog)s [OPTIONS] -s FTPSERVER -d DESTINATION',
                formatter_class=RawTextHelpFormatter)

    parser.add_argument("-p", "--port", default="21", dest="port",
                        help="Set FTP port (default 21)")
    
    parser.add_argument("-b", "--source", default="/", dest="source",
                        help="The Source directory to Start at (default \"/\")")

    parser.add_argument("-u", "--user", default="anonymous", dest="user",
                        help="Username (default anonymous)")
    
    parser.add_argument("-pw", "--password", default="anonymous", dest="password",
                        help="Password (default anonymous)")

    parser.add_argument("-g", "--ftp-get", dest="ftpget", action="store_true",
                        help="Binary FTP GET download of all files and folders (excluding those you ignore). DEFAULT only lists the ftp structure")

    parser.add_argument("-t", "--test-ftp-upload", dest="ftpput", action="store_true",
                        help="Binary FTP PUT upload test of discovered directories (excluding those you ignore)")

    parser.add_argument("-i", "--ignore",  nargs="+", dest="ignore", help="Ignore a list of folders: -i \"Program Files\", \"Windows\", \"Users\"")
    
    parser.add_argument("-c", "--ignore-common", dest="common", action="store_true",
                        help="Ignore Common folders that may take up too much time")
    
    required = parser.add_argument_group('required arguments')

    required.add_argument("-s", "--server",  dest="host", type=str,required=True,
                    help="Host FTP server")

    required.add_argument("-d", "--dest",  dest="destination", type=str,required=True,
                        help="Location/Output name of directory to use or create if non existent for output and/or files")

    args = parser.parse_args()
    ################### argparse ######################
    host = args.host
    port = args.port
    user = args.user
    password = args.password
    destination = args.destination
    source = args.source
    ignore = args.ignore
    ign_common = args.common
    ftpget = args.ftpget
    ftpput = args.ftpput
    ################### argparse ######################
    common_dirs = ["Program Files (x86)", "Program Files", ]
    ################### logging ######################
    if not os.path.isabs(destination):
        creatDir(destination)
        logPath=os.getcwd()+"/"+destination
    else:
        logPath = destination
    timestr = time.strftime("%Y%m%d-%H%M%S")
    fileName = "ftp_enum_results-"+timestr
    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(levelname)s]  %(message)s",
        handlers=[
            logging.FileHandler("{0}/{1}.log".format(logPath, fileName)),
            logging.StreamHandler()
        ])
    logging.addLevelName(logging.INFO, '*')
    logger = logging.getLogger()
    interval = 0.05
    ################### logging ######################

    start_time = time.time()

    ftp = ftplib.FTP()
    ftp.connect(host,int(port))
    ftp.login(user,password)

    if ftpput:
        tf_name = "test_ftp.txt"
        createTestFile(tf_name)

    if ign_common:
        ignore = checkList(ignore, common_dirs)

    if ignore:
        logger.debug(ignore)
        if ftpget:
            downloadFiles(ftp, source, logPath, "\t-- ", ignore)
        else:
            listFiles(ftp, source, logPath, "\t-- ", ftpput, ignore)
    else:
        if ftpget:
            downloadFiles(ftp, source, logPath, "\t-- ")
        else:
            listFiles(ftp, source, logPath, "\t-- ", ftpput)

    ftp.quit()
    
    end_time = time.time()
    elapsed = end_time - start_time
    logger.info("[!] Completed in %s " % (str(datetime.timedelta(seconds=elapsed))))

