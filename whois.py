import os
import sqlite3
from datetime import datetime
import ipaddress


#run who is on IPs and retrieve all 
def DatabaseCreation():
    connection = sqlite3.connect('assets.db')
    cursor = connection.cursor()
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS whois
              (IP TEXT, owner TEXT, CIDR TEXT, NETNAME TEXT, time TEXT)''')
    connection.commit()

def checkIP(address):
    try:
        ip = ipaddress.ip_address(address)
        return getHosting(address)
    except ValueError:
        return ['none','none','none'] 

def getHosting(ip):
    x = os.popen(f"whois {ip}").read().splitlines()
    hosting = 'none'
    netname = 'none'
    cidr = 'none'
    if ip == '0.0.0.0':
        return [hosting.strip(),cidr.strip(),netname.strip()]
    for i in x:
        if i.split(':')[0] == 'Organization':
            hosting = i.split(':')[1]
            #print("hosting: " + hosting)
        if i.split(':')[0] == 'CIDR':
            cidr = i.split(':')[1]
            #print("cide: " + cidr)
        if i.split(':')[0] == 'NetName':
            netname = i.split(':')[1]
            #print("netname: " + netname)
        if hosting != 'none' and cidr != 'none' and netname != 'none':
            return [hosting.strip(),cidr.strip(),netname.strip()]
    return [hosting.strip(),cidr.strip(),netname.strip()]

DatabaseCreation()
connection = sqlite3.connect('assets.db')
cursor = connection.cursor()
cursor.execute(f'SELECT hostname, IP from hosts')
rows = cursor.fetchall()

for row in rows:
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print(row[1].strip('\n'))
    data = checkIP(row[1].strip('\n'))
    print(data)
    cursor.execute(f"INSERT INTO whois(IP,owner,CIDR,NETNAME,time) VALUES(?,?,?,?,?)",(row[1].strip('\n'),data[0],data[1],data[2],dt_string,))
    connection.commit()
