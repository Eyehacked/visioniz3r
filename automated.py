import os
import argparse
from datetime import datetime
import pyfiglet
from termcolor import colored

def visioniz3r():
    ascii_art = pyfiglet.figlet_format("visioniz3r")
    colored_ascii = colored(ascii_art, 'green', attrs=['bold'])
    print(colored_ascii)

if __name__ == "__main__":
    visioniz3r()
#Initializa parser
parser = argparse.ArgumentParser()
#Adding options
parser.add_argument("-F", "--file", help = "enter file with comma seperated seach strings")
parser.add_argument("-s", "--search", help = "enter seperated search strings")
parser.add_argument("-f", "--filter", help = "use search string to filter the output as root domain")
parser.add_argument("-ns", "--noscan", action='store_true', help = "does not run the scanning functionality (passive mode)")
args = parser.parse_args()

if args.filter:
	os.popen(f"python hosts.py -f {args.filter}").read()
if args.search:
	print("---------------- Starting Hosts Scanning ---------------------")
	os.popen(f"python hosts.py -s {args.search}").read()
	print("---------------- Finished Hosts Scanning ---------------------")
	print("---------------- Starting Whois Scanning ---------------------")
	os.popen("python whois.py").read()
	print("---------------- Finished Whois Scanning ---------------------")
	print("---------------- Starting Sub-DomainEnum Scanning ---------------------")
	os.popen("python SubEnum.py").read()
	#os.popen("python subeumorg.py").read()
	print("---------------- Finished Sub-DomainEnum scanning ---------------------")
if args.noscan:
	print("No Scan Enabled!")
else:
	os.popen("python Scanner.py").read()
	print("---------------- finished port scanning ---------------------")
