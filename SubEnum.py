#get all root domains from DB 
import subprocess
from tqdm import tqdm
from datetime import datetime 
import sqlite3
import os

def DatabaseCreation():
    connection = sqlite3.connect('assets.db')
    cursor = connection.cursor()
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS Subdomain
              (SubDomain TEXT, ROOT TEXT, time TEXT)''')
    connection.commit()

def amass(dns):
    #table = dns.split('.')[0]
    #out = subprocess.Popen(['amass', 'enum', '-passive','-d',dns], 
    #stdout=subprocess.PIPE, 
    #stderr=subprocess.STDOUT)
    #stdout,stderr = out.communicate()
    print(f"this is dns: {dns}")
    res = os.popen(f"sudo amass enum -passive -d {dns} -timeout 4 -dns-qps 500").read().splitlines()
        #-unique option in above command helps in fixing duplicates
    subname = []
    #for sub in tqdm(stdout.splitlines()):
    for sub in tqdm(res):
        #print(sub.decode("utf-8"))
        #subname.append(sub.decode("utf-8"))
        print(sub)
        subname.append(sub)
    return subname
        

def getRoot(hostname):
    y = hostname.split('.')
    x = [y[-2],y[-1]]
    return '.'.join(x)

def getIp(host):
    global ipcounter
    ip = os.popen(f"dig +noall +answer +short {host} | tail -n1").read()
    if ip == '':
        ip = "0.0.0.0"
    print(host + ":" + ip)
    return ip

def getRootDomains():
    connection = sqlite3.connect('assets.db')
    cursor = connection.cursor()
    cursor.execute(f'SELECT root from hosts')
    rows = cursor.fetchall()
    
    cursor.close()
    return rows 

DatabaseCreation()
connection = sqlite3.connect('assets.db')

#cursor.execute(f'SELECT * from DNSRoot')
#rows = cursor.fetchall()
#domains = ''''''
domains = getRootDomains()
domains = list(set(domains))
print(f"The output of getRootDomains is : {domains}")
cursor = connection.cursor()
for i in domains:
    print(str(i[0]))
    sublist = amass(str(i[0]).strip('\n'))
    for hostname in sublist:
        ip = getIp(hostname)
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        
        try:
            cursor.execute(f"INSERT INTO hosts(hostname,IP,root,searchstring,time) VALUES(?,?,?,?,?)",(hostname.strip(),ip.strip(),i,'Sub-domain enum',dt_string,))
            connection.commit()
        except:
            print(f"{hostname} is a duplicate (REMOVED)")
connection.close()

#domains = ['join.me','logmeinx.com','lastpass.com','citrixonline.com','nanorep.co','psdops.com','pinfall.ca','meldium.com','xively.io ','intel.com','appguru.com','joinme.com','logmeinusercontent.com','cubbyusercontent.com','xively.com','nopass.com','xmarks.com','lastpass-internal.io','zamurai.me ','zamurai.com','bold360.com','citrixsaassbe.net','nopassword.com','bold360ai.com','gotomypc.ca','pachube.com','xively.us','lastpass.ca','boldcenter.com ','nanorep.info ','stage-bold360.com','uber-electronics.com','xi-dev.com','logmein inc.','boldchat.com','co.uk','com.br','com.msg','co.za']
#code to fetch from hostnmae table and adding to different table
#cursor = connection.cursor()
#cursor.execute(f'SELECT hostname from hosts')
#rows = cursor.fetchall()
#for row in rows:
#    domain = getRoot(row[0])
#    #print(' '.join(domains))
#    if str(domain.strip(' ')) not in ''.join(domains):
#        #print(domain)
#        now = datetime.now()
#        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
#        domains.append(domain)
#        
#        print(domains)
#        sublist = amass(domain)
#        connection = sqlite3.connect('assets.db')
#        cursor = connection.cursor()
#        for name in sublist:
#            cursor.execute("INSERT INTO Subdomain(SubDomain,ROOT,time) VALUES(?,?,?)",(name,domain,dt_string,))
#            connection.commit()
#        
#        connection.close()
#print(domains)




#for j in domains:
#    x = os.popen(f"whois {j}").read().splitlines()
#    for i in x:
#        if i.split(':')[0] == 'Registrant Organization':
#            hosting = i.split(':')[1]
#            if 'GoTo' not in hosting and 'LogMeIn' not in hosting:
#                print(j)
            
