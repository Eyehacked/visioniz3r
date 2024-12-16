import os
from datetime import datetime
import sqlite3
import ipaddress

single_ip = []
netnames = []
def DatabaseCreation():
    connection = sqlite3.connect('assets.db')
    cursor = connection.cursor()
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS scans
              (IP TEXT, NETNAME TEXT, ports TEXT, banners TEXT, whatweb TEXT, time TEXT)''')
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS ports
              (IP TEXT, port TEXT, time TEXT)''')
    connection.commit()
    connection.close()
def checkIP(address):
    global single_ip
    try:
        if address =='0.0.0.0':
            return {}
        ip = ipaddress.ip_address(address)
        if address not in ' '.join(single_ip):
            print(f"added {address} to list of single IPs")
            single_ip.append(address)
        #return massScanner(address)
        
    except ValueError:
        return {} 

#use masscan
def massScanner(ip):

    scan = os.popen(f'sudo masscan {ip} --top-ports --banners -oL -  --rate 4000').read().splitlines()
    data = {}
    for i in scan:
        print(i)
        if i != '# end' and i != '#masscan':
            if i.split()[3] not in data.keys():
                data.update({i.split()[3] : {'ports' : [], 'banners': []}})
            if 'open' in i:
                data[i.split()[3]]['ports'].append(i.split()[2])
            elif 'banner' in i:
                for j in range(len(i.split())):
                    if j >= 6:
                        if len(i.split()[6]) < 100:    
                            data[i.split()[3]]['banners'].append(i.split()[j])
    return data

def whatWeb(host):

    return os.popen(f'whatweb {host} --color=never --no-errors').read()
    

## 
os.system("touch start-time")
DatabaseCreation()
connection = sqlite3.connect('assets.db')
cursor = connection.cursor()
cursor.execute(f'SELECT IP, CIDR, NETNAME from whois')
rows = cursor.fetchall()
block = []
connection.close()

for row in rows:
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print(dt_string)
    print(row[0].strip('\n'))
    print(row[2])
    if "GOTO" in row[2] or "VC-GF-1" in row[2] or "JIVEC-GLOBAL" in row[2] or "JIVECOMMUNICATIONS" in row[2]:
        #log the block so we dont scan it multple times
        if row[2] not in '  '.join(block):
            print("GOTO-BLOCK")
            print(row[2])
            block.append(row[2])
            data = massScanner(row[1])
            connection = sqlite3.connect('assets.db')
            cursor = connection.cursor()
            fingerprint = "none"
            for keys in data:
                x = ' '.join(data[keys]['ports'])
                if '80' in ' '.join(data[keys]['ports']) or '443' in ' '.join(data[keys]['ports']):
                    fingerprint = whatWeb(keys)
                z = ' '.join(data[keys]['banners'])
                print(x)
                print(z)
                y = data[keys]['ports']
                cursor.execute("INSERT INTO scans(IP,NETNAME,ports,banners,whatweb,time) VALUES(?,?,?,?,?,?)",(keys.strip('\n'),row[2],x,z,fingerprint,dt_string,))
                connection.commit()
                for p in y:
                    cursor.execute("INSERT INTO ports(IP,port,time) VALUES(?,?,?)",(keys.strip('\n'),p,dt_string,))
                    connection.commit()
        connection.close()
        #print(keys + ' has ' + ' '.join(data[keys]['ports']))
    else:   
        data = checkIP(row[0].strip('\n'))
        netnames.append(row[2])
    print(data)
    

print(block)
print("starting the single IP scan")
print(len(single_ip))
print('-------------------------------------------------------------------')
connection = sqlite3.connect('assets.db')
cursor = connection.cursor()
ip_list = ' '.join(single_ip)
data2 = massScanner(ip_list)

counter = 0

for keys in data2:
    x = ' '.join(data2[keys]['ports'])
    fingerprint = "none"
    if '80' in ' '.join(data2[keys]['ports']) or '443' in ' '.join(data2[keys]['ports']):
        fingerprint = whatWeb(keys)
    z = ' '.join(data2[keys]['banners'])
    print(x)
    print(z)
    y = data2[keys]['ports']
    cursor.execute("INSERT INTO scans(IP,NETNAME,ports,banners,whatweb,time) VALUES(?,?,?,?,?,?)",(keys.strip('\n'),netnames[counter],x,z,fingerprint,dt_string,))
    for p in y:
        cursor.execute("INSERT INTO ports(IP,port,time) VALUES(?,?,?)",(keys.strip('\n'),p,dt_string,))
    counter += 1
connection.commit()
connection.close()
