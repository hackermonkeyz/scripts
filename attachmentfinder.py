#!/usr/bin/python3
import glob,os,shutil,sys
#  find . -type f | perl -ne 'print $1 if m/\.([^.\/]+)$/' | sort -u
#  put all extensions into an array

extensions = [ "7z",
    "doc",
    "docx",
    "jpg",
    "jpeg",
    "eml",
    "emz",
    "gif",
    "htm",
    "ics",
    "mht",
    "mso",
    "p7m",
    "PDF",
    "pdf",
    "PNG",
    "png",
    "PPTX",
    "pptx",
    "rtf",
    "sif",
    "tiff",
    "txt",
    "xls",
    "XLS",
    "xlsx",
    "XLSX"]

def getattachments(directory):
    for ext in extensions:
        for filename in glob.iglob(directory+'/**/*.'+ext, recursive=True):
            print(ext+":")
            
            # print(filename+"\n")
            directory = os.getcwd()+"/"+ext+"_files"
            if not os.path.exists(directory):
                os.makedirs(directory)
                
            with open(directory+"/"+ext+"_files.txt", "a") as f:
                print(filename)
                shutil.copy2(filename, directory)
                f.write(filename+"\n")

if __name__ == "__main__":
    getattachments(sys.argv[1])