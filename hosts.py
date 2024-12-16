import os
import argparse
import sqlite3
from datetime import datetime
#take a list of strings as search arguments and retrieve all hosts owned by us
#get the IP for all hosts found if not found add "not found"
#add data to DB table hosts(search_string, hostname, IP, time)
ipcounter = 0


def getHosts(search_string,filter):
    
    grep = "grep -v ',\|@\|(\|*'"
    query = f"SELECT distinct(lower(name_value)) FROM certificate_and_identities cai WHERE plainto_tsquery('certwatch', '{search_string}') @@ identities(cai.CERTIFICATE) AND cai.NAME_VALUE ILIKE ('%' || '.' || '%') LIMIT 10000;"
    cmd = f'psql -h crt.sh -p 5432 -P pager -t -c "{query}" -U guest certwatch | {grep}'
    if filter == search_string:
        grep2 = f"| grep '{filter}'"
        cmd = cmd + grep2
    urls = os.popen(cmd).read().split('\n')
    hosts = [i for i in urls if i]
    return hosts

def DatabaseCreation_hosts():
    connection = sqlite3.connect('assets.db')
    cursor = connection.cursor()
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS hosts
              (hostname TEXT NOT NULL UNIQUE, IP TEXT, root TEXT, searchstring TEXT, time TEXT)''')
    connection.commit()


def getIp(host):
    global ipcounter
    ip = os.popen(f"dig +noall +answer +short {host} | tail -n1").read()
    if ip == '':
        ip = "0.0.0.0"
    print(host + ":" + ip)
    ipcounter +=1
    return ip 

def updateDB(search_string,hostname,ip):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    connection = sqlite3.connect('assets.db')
    cursor = connection.cursor()
    x = hostname.split('.')
    global rootDomains
    if len(x) >= 2:
    	root = x[-2] + '.' + x[-1] ; root = root.strip(' ')

    try:
        cursor.execute(f"INSERT INTO hosts(hostname,IP,root,searchstring,time) VALUES(?,?,?,?,?)",(hostname.strip(),ip,root,search_string,dt_string,))
        cursor.execute(f"")
        connection.commit()
    except:
        print(f"{hostname} is a duplicate (REMOVED)")




DatabaseCreation_hosts()
# Initialize parser
parser = argparse.ArgumentParser()
# Adding optional argument
parser.add_argument("-F", "--file", help = "Enter file with comma seperated seach strings")
parser.add_argument("-s", "--search", help = "Enter seperated search strings")
parser.add_argument("-f", "--filter", help = "Use search string to filter the output as root domain")
# Read arguments from command line
args = parser.parse_args()
filter = 0

if args.search:
    search_strings = args.search.split(',')
    if args.filter:
        filter = args.filter
    for i in search_strings:
        hosts = getHosts(i,filter)
        for j in hosts:
            ip = getIp(j)
            updateDB(i,j,ip)
print(ipcounter)
