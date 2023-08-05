#!/usr/bin/env python3

# AORT - All in One Recon Tool
# Author: D3Ext
# Github: https://github.com/D3Ext/AORT
# Website: https://d3ext.github.io

# Libraries
try:
    import requests
    import sys
    import re
    import socket
    import json
    import argparse
    import platform
    import dns.zone
    import warnings
    import dns.resolver
    import pydig
    from time import sleep
    import os
    import urllib3
except:
    print(c.YELLOW + "\n[" + c.RED + "-" + c.YELLOW + "] ERROR requirements missing try to install the requirements: pip3 install -r requirements.txt" + c.END)
    sys.exit(0)

# Output Colours
class c:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    UNDERLINE = '\033[4m'

# Banner Function
def banner():
    print(c.YELLOW + '                _____                   ')
    print('             .-"     "-.                ')
    print('            / o       o \               ')
    print('           /   \     /   \              ')
    print('          /     )-"-(     \             ')
    print('         /     ( 6 6 )     \            ')
    print('        /       \ " /       \           ')
    print('       /         )=(         \    - By D3Ext')
    print('      /   o   .--"-"--.   o   \         ')
    print('     /    I  /  -   -  \  I    \        ')
    print(' .--(    (_}y/\       /\y{_)    )--.    ')
    print('(    ".___l\/__\_____/__\/l___,"    )   ')
    print(' \                                 /    ')
    print('  "-._      o O o O o O o      _,-"     ')
    print('      `--Y--.___________.--Y--\'        ')
    print('         |==.___________.==|            ')
    print('         `==.___________.==\'           ' + c.END)

    print(c.BLUE + "\nPython version: " + c.GREEN + platform.python_version() + c.END)
    print(c.BLUE + "Current OS: " + c.GREEN + platform.system() + " " + platform.release() + c.END)

    internet_check = socket.gethostbyname(socket.gethostname())

    if internet_check == "127.0.0.1":
        if platform.system() == "Windows":
            print(c.BLUE + "Internet connection: " + c.RED + "-" + c.END)
        else:
            print(c.BLUE + "Internet connection: " + c.RED + "✕" + c.END)
    else:
        if platform.system() == "Windows":
            print(c.BLUE + "Internet connection: " + c.GREEN + "+" + c.END)
        else:
            print(c.BLUE + "Internet connection: " + c.GREEN + "✔" + c.END)

    print(c.BLUE + "Target: " + c.GREEN + domain + c.END)

# Argument parser Function
def parseArgs():

    p = argparse.ArgumentParser(description="AORT - All in One Recon Tool")
    p.add_argument("-d", "--domain", help="domain to search its subdomains", required=True)
    p.add_argument("-o", "--output", help="file to store the scan output", required=False)
    p.add_argument('-t', '--token', help="api token of hunter.io to discover mail accounts and employees", required=False)
    p.add_argument("-p", "--portscan", help="perform a fast and stealthy scan of the most common ports", action='store_true', required=False)
    p.add_argument("-a", "--axfr", help="try a domain zone transfer attack", action='store_true', required=False)
    p.add_argument("-m", "--mail", help="try to enumerate mail servers", action='store_true', required=False)
    p.add_argument('-e', '--extra', help="look for extra dns information", action='store_true', required=False)
    p.add_argument("-n", "--nameservers", help="try to enumerate the name servers", action='store_true', required=False)
    p.add_argument("-i", "--ip", help="it reports the ip or ips of the domain", action='store_true', required=False)
    p.add_argument('-6', '--ipv6', help="enumerate the ipv6 of the domain", action='store_true', required=False)
    p.add_argument("-w", "--waf", help="discover the WAF of the domain main page", action='store_true', required=False)
    p.add_argument("-s", "--subtakeover", help="check if any of the subdomains are vulnerable to Subdomain Takeover", action='store_true', required=False)
    p.add_argument("-r", "--repos", help="try to discover valid repositories and s3 servers of the domain (still improving it)", action='store_true', required=False)
    p.add_argument("-c", "--check", help="check active subdomains and store them into a file", action='store_true', required=False)
    p.add_argument("--enum", help="stealthily enumerate and identify common technologies", action='store_true', required=False)
    p.add_argument("--whois", help="perform a whois query to the domain", action='store_true', required=False)
    p.add_argument("--wayback", help="find useful information about the domain and his different endpoints using The Wayback Machine and other services", action="store_true", required=False)
    p.add_argument("--all", help="perform all the enumeration at once (best choice)", action='store_true', required=False)
    p.add_argument("--quiet", help="don't print the banner", action='store_true', required=False)
    p.add_argument("--version", help="display the script version", action='store_true', required=False)

    return p.parse_args()

# Nameservers Function 
def ns_enum(domain):
    print(c.BLUE + "\n[" + c.END + c.GREEN + "+" + c.END + c.BLUE + "] Trying to discover valid name servers...\n" + c.END)
    sleep(0.2)

    """
    Query to get NS of the domain
    """

    data = pydig.query(domain, 'NS')

    if data:
        for ns in data:
            l = len(ns)
            ns = ns[:l-1]
            print(c.YELLOW + ns + c.END)
    else:
        print(c.YELLOW + "Unable to enumerate" + c.END)

# IPs discover Function
def ip_enum(domain):
    print(c.BLUE + "\n[" + c.END + c.GREEN + "+" + c.END + c.BLUE + "] Discovering IPs of the domain...\n" + c.END)
    sleep(0.2)

    """
    Query to get ips
    """

    data = pydig.query(domain, 'A')

    if data:
        for ip in data:
            print(c.YELLOW + ip + c.END)
    else:
        print(c.YELLOW + "Unable to enumerate" + c.END)

# Extra DNS info Function
def txt_enum(domain):
    print(c.BLUE + "\n[" + c.END + c.GREEN + "+" + c.END + c.BLUE + "] Enumerating extra DNS information...\n" + c.END)
    sleep(0.2)

    """
    Query to get extra info about the dns
    """

    data = pydig.query(domain, 'TXT')

    if data:
        for info in data:
            print(c.YELLOW + info + c.END)
    else:
        print(c.YELLOW + "Unable to enumerate" + c.END)

# Function to discover the IPv6 of the target
def ipv6_enum(domain):
    print(c.BLUE + "\n[" + c.END + c.GREEN + "+" + c.END + c.BLUE + "] Getting ipv6 of the domain...\n" + c.END)
    sleep(0.2)

    """
    Query to get ipv6
    """

    data = pydig.query(domain, 'AAAA')
    
    if data:
        for info in data:
            print(c.YELLOW + info + c.END)
    else:
        print(c.YELLOW + "Unable to enumerate" + c.END)

# Mail servers Function
def mail_enum(domain):
    print(c.BLUE + "\n[" + c.END + c.GREEN + "+" + c.END + c.BLUE + "] Finding valid mail servers...\n" + c.END)
    sleep(0.2)

    """
    Query to get mail servers
    """

    data = pydig.query(domain, 'MX')

    if data:
        for mail_output in data:
            mail_data = []
            mail_output = mail_output.split(' ')
            if len(mail_output) == 1:
                mail_servers = mail_output[0]
                mail_data.append(mail_servers)
            else:
                mail_output = mail_output[1]
                l = len(mail_output)
                mail_servers = mail_output[:l-1]
                mail_data.append(mail_servers)
            print(c.YELLOW + mail_data[0] + c.END)
    else:
        print(c.YELLOW + "Unable to enumerate" + c.END)

# Domain Zone Transfer Attack Function
def axfr(domain):
    print(c.BLUE + "\n[" + c.END + c.GREEN + "+" + c.END + c.BLUE + "] Starting Domain Zone Transfer attack...\n" + c.END)
    sleep(0.2)

    """
    Iterate through the name servers and try an AXFR attack on everyone
    """

    ns_answer = dns.resolver.resolve(domain, 'NS')
    for server in ns_answer:
        ip_answer = dns.resolver.resolve(server.target, 'A')
        for ip in ip_answer:
            try:
                zone = dns.zone.from_xfr(dns.query.xfr(str(ip), domain))
                for host in zone:
                    print(c.YELLOW + "Found Host: {}".format(host) + c.END)
            except Exception as e:
                print(c.YELLOW + "NS {} refused zone transfer!".format(server) + c.END)
                continue

# Modified function from https://github.com/Nefcore/CRLFsuite WAF detector script <3
def wafDetector(domain):
    
    """
    Get WAFs list in a file
    """

    r = requests.get("https://raw.githubusercontent.com/D3Ext/AORT/main/utils/wafsign.json")
    f = open('wafsign.json', 'w')
    f.write(r.text)
    f.close()

    with open('wafsign.json', 'r') as file:
        wafsigns = json.load(file)

    print(c.BLUE + "\n[" + c.END + c.GREEN + "+" + c.END + c.BLUE + "] Discovering active WAF on the main web page...\n" + c.END)
    sleep(1)
    
    """
    Payload to trigger the possible WAF
    """

    payload = "../../../../etc/passwd"

    try:

        """
        Check the domain and modify if neccessary 
        """

        if domain.endswith("/") and domain.startswith("https://"):
            response = requests.get(domain + payload, verify=False)

        elif domain.endswith("/") and not domain.startswith("https://"):
            response = requests.get('https://' + domain + payload, verify=False)

        elif not domain.endswith("/") and domain.startswith("https://"):
            response = requests.get(domain + '/' + payload, verify=False)
        
        elif not domain.endswith("/") and not domain.startswith("https://"):
            response = requests.get('https://' + domain + '/' + payload, verify=False)

    except:
        print(c.YELLOW + "An error has ocurred" + c.END)

        try:
            os.remove('wafsign.json')
        except:
            pass
    
        return None

    code = str(response.status_code)
    page = response.text
    headers = str(response.headers)
    cookie = str(response.cookies.get_dict())

    """
    Check if WAF has blocked the request
    """

    if int(code) >= 400:
        bmatch = [0, None]
        for wafname, wafsign in wafsigns.items():
            total_score = 0
            pSign = wafsign["page"]
            cSign = wafsign["code"]
            hSign = wafsign["headers"]
            ckSign = wafsign["cookie"]
            if pSign:
                if re.search(pSign, page, re.I):
                    total_score += 1
            if cSign:
                if re.search(cSign, code, re.I):
                    total_score += 0.5
            if hSign:
                if re.search(hSign, headers, re.I):
                    total_score += 1
            if ckSign:
                if re.search(ckSign, cookie, re.I):
                    total_score += 1
            if total_score > bmatch[0]:
                del bmatch[:]
                bmatch.extend([total_score, wafname])

        if bmatch[0] != 0:
            print(c.YELLOW + bmatch[1] + c.END)
        else:
            print(c.YELLOW + "WAF not detected or doesn't exists" + c.END)
    else:
        print(c.YELLOW + "An error has ocurred or unable to enumerate" + c.END)

    try:
        os.remove('wafsign.json')
    except:
        pass

# Use the token
def crawlMails(domain, api_token):

    print(c.BLUE + "\n[" + c.GREEN + "+" + c.BLUE + "] Discovering valid mail accounts and employees..." + c.END)

    """
    Use the api of hunter.io with your token to get valid mails
    """

    sleep(1)
    api_url = f"""https://api.hunter.io/v2/domain-search?domain={domain}&api_key={api_token}"""
    r = requests.get(api_url)
    response_data = json.loads(r.text)
    domain_name = domain.split(".")[0]
    print()

    file = open(f"{domain_name}-mails-data.txt", "w")
    file.write(r.text)
    file.close()

    counter = 0
    for value in response_data["data"]["emails"]:

        if value["first_name"] and value["last_name"]:
            counter = 1
            print(c.YELLOW + value["first_name"] + " " + value["last_name"] + " - " + value["value"] + c.END)
        else:
            counter = 1
            print(c.YELLOW + value["value"] + c.END)

    if counter == 0:
        print(c.YELLOW + "\nAny mails or employees found" + c.END)
    else:
        print(c.YELLOW + "\nMore mail data stored in " + domain_name + "-mails-data.txt" + c.END)

# Function to check subdomain takeover
def subTakeover(all_subdomains):

    """
    Iterate through all the subdomains to check if anyone is vulnerable to subdomain takeover
    """
    
    vuln_counter = 0
    print(c.BLUE + "\n[" + c.GREEN + "+" + c.BLUE + "] Checking if any subdomain is vulnerable to takeover\n" + c.END)
    sleep(1)
    
    for subdom in all_subdomains:
        try:
            sleep(0.05)
            resquery = dns.resolver.resolve(subdom, 'CNAME')
            
            for resdata in resquery:
                resdata = (resdata.to_text())
                
                if subdom[-8:] in resdata:
                    r = requests.get("https://" + subdom, allow_redirects=False)
    
                    if r.status_code == 200:
                        vuln_counter += 1
                        print(c.YELLOW + subdom + " appears to be vulnerable" + c.END)

                else:
                    pass

        except KeyboardInterrupt:
            sys.exit(c.RED + "\n[!] Interrupt handler received, exiting...\n" + c.END)
        except:
            pass
    
    if vuln_counter <= 0:
        print(c.YELLOW + "Any subdomain is vulnerable" + c.END)

# Function to enumerate github and cloud
def cloudgitEnum(domain):

    print(c.BLUE + "\n[" + c.END + c.GREEN + "+" + c.END + c.BLUE + "] Finding valid git repositories or services\n" + c.END)

    """
    Check if an github account or a repository the same name exists 
    """

    r = requests.get("https://" + domain + "/.git/")
    if r.status_code == 200 or r.status_code == 403 or r.status_code == 500:
        print(c.YELLOW + "Git repository found: https://" + domain + "/.git/ - " + str(r.status_code) + " status code" + c.END)

    r = requests.get("https://" + domain + "/.dev/")
    if r.status_code == 200 or r.status_code == 403 or r.status_code == 500:
        print(c.YELLOW + "Possible dev directory found: https://" + domain + "/.dev/ - " + str(r.status_code) + " status code" + c.END)

    r = requests.get("https://" + domain + "/dev/")
    if r.status_code == 200 or r.status_code == 403 or r.status_code == 500:
        print(c.YELLOW + "Possible dev directory found: https://" + domain + "/dev/ - " + str(r.status_code) + " status code" + c.END)

    r = requests.get("https://github.com/" + domain.split(".")[0])
    if r.status_code == 200:
        print(c.YELLOW + "Github account found: https://github.com/" + domain.split(".")[0] + " - " + str(r.status_code) + " status code" + c.END)

    r = requests.get("https://gitlab.com/" + domain.split(".")[0])
    if r.status_code == 200:
        print(c.YELLOW + "Gitlab account found: https://gitlab.com/" + domain.split(".")[0] + " - " + str(r.status_code) + " status code" + c.END)

# Wayback Machine function
def wayback(domain):

    print(c.BLUE + "\n[" + c.END + c.GREEN + "+" + c.END + c.BLUE + "] Using The Wayback Machine to discover endpoints" + c.END)

    """
    URL to query info
    """

    wayback_url = f"http://web.archive.org/cdx/search/cdx?url=*.{domain}/*&output=json&fl=original&collapse=urlkey"
    
    """
    Get information from Wayback Machine
    """
    try:
        r = requests.get(wayback_url, timeout=20)
        results = r.json()
        results = results[1:]
    except KeyboardInterrupt:
        sys.exit(c.RED + "\n[!] Interrupt handler received, exiting...\n" + c.END)
    except:
        pass
        
    domain_name = domain.split(".")[0]

    try:
        os.remove(f"{domain_name}-wayback.txt")
    except:
        pass

    for result in results:

        """
        Save data to a file
        """

        file = open(f"{domain_name}-wayback.txt", "a")
        file.write(result[0] + "\n")

    
    """
    Get URLs and endpoints from URLScan
    """

    try:
        r = requests.get(f"https://urlscan.io/api/v1/search/?q=domain:{domain}", timeout=20)

        myresp = json.loads(r.text)
        results = myresp["results"]

        for res in results:
            url = res["task"]["url"]

            file = open(f"{domain_name}-wayback.txt", "a")
            file.write(url + "\n")
    except:
        pass

    print(c.YELLOW + f"\nInformation stored in {domain_name}-wayback.txt" + c.END)

#def createReport(domain):

    #file = open()

# Query the domain
def whoisLookup(domain):

    print(c.BLUE + "\n[" + c.END + c.GREEN + "+" + c.END + c.BLUE + "] Performing Whois lookup..." + c.END)

    import whois
    sleep(1.2)

    try:
        w = whois.whois(domain) # Two different ways to avoid a strange error
    except:
        w = whois.query(domain)
    try:
        print(c.YELLOW + f"\n{w}" + c.END)
    except:
        print(c.YELLOW + "\nAn error has ocurred or unable to whois " + domain + c.END)

# Function to thread when probing active subdomains
def checkStatus(subdomain, file):

    try:
        r = requests.get("https://" + subdomain, timeout=2)

        if r.status_code:
            file.write("https://" + subdomain + "\n")
    except:
        pass

# Check status function
def checkActiveSubs(domain,doms):

    global file

    import threading

    print(c.BLUE + "\n[" + c.END + c.GREEN + "+" + c.END + c.BLUE + "] Probing active subdomains..." + c.END)

    if len(doms) >= 100:
        option = input(c.YELLOW + "\nThere are a lot of subdomains to check, (+100) do you want to check all of them [y/n]: " + c.END)
        
        if option == "n" or option == "no":
            sleep(0.2)
            return

    """
    Define filename
    """
    domain_name = domain.split(".")[0]
    file = open(f"{domain_name}-active-subs.txt", "w")
    
    """
    Iterate through all subdomains in threads
    """
    for subdomain in doms:
        t = threading.Thread(target=checkStatus, args=(subdomain,file))
        t.start()

    sleep(4)

    print(c.YELLOW + f"\nActive subdomains stored in {domain_name}-active-subs.txt" + c.END)

# Check if common ports are open
def portScan(domain):

    print(c.BLUE + "\n[" + c.END + c.GREEN + "+" + c.END + c.BLUE + "] Scanning most common ports on " + domain + "\n" + c.END)

    """
    Define ports array
    """

    ports = [21,22,23,25,26,43,53,69,80,81,88,110,389,443,445,636,873,2049,3000,3001,3306,4000,4040,5000,5001,5985,5986,8000,8001,8080,8081,27017]

    """
    Iterate through the ports to check if are open
    """

    for port in ports:

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.50)
        result = sock.connect_ex((domain,port))
    
        if result == 0:
            print(c.YELLOW + "Port " + str(port) + " - OPEN" + c.END)

        sock.close()

# Perform basic enumeration
def basicEnum(domain):

    print(c.BLUE + "\n[" + c.END + c.GREEN + "+" + c.END + c.BLUE + "] Performing some basic enumeration...\n" + c.END)

    """
    Use python-Wappalyzer
    """

    try:
        from Wappalyzer import Wappalyzer, WebPage

        wappalyzer = Wappalyzer.latest()
        webpage = WebPage.new_from_url('https://' + domain)
        info = wappalyzer.analyze_with_versions(webpage)

        print(c.YELLOW + json.dumps(info, sort_keys=True, indent=4) + c.END)
    except:
        print(c.YELLOW + "\nAn error has ocurred or unable to enumerate" + c.END)

# Main Domain Discoverer Function
def SDom(domain,filename):
    
    print(c.BLUE + "\n[" + c.END + c.GREEN + "+" + c.END + c.BLUE + "] Discovering valid subdomains using passive techniques...\n" + c.END)
    sleep(0.1)

    global doms
    doms = []

    """
    Get valid subdomains with a request to crt.sh
    """
    try:
        r = requests.get("https://crt.sh/?q=" + domain + "&output=json", timeout=20)
        formatted_json = json.dumps(json.loads(r.text), indent=4)
        crt_domains = sorted(set(re.findall(r'"common_name": "(.*?)"', formatted_json)))

        # Only append new valid subdomains
        for dom in crt_domains:
            if dom.endswith(domain) and dom not in doms:
                doms.append(dom)

    except KeyboardInterrupt:
        sys.exit(c.RED + "\n[!] Interrupt handler received, exiting...\n" + c.END)
    except:
        pass
              
    """
    Get subdomains from AlienVault
    """
    try:
        r = requests.get(f"https://otx.alienvault.com/api/v1/indicators/domain/{domain}/passive_dns", timeout=20)
        alienvault_domains = sorted(set(re.findall(r'"hostname": "(.*?)"', r.text)))

        # Only append new valid subdomains
        for dom in alienvault_domains:
            if dom.endswith(domain) and dom not in doms:
                doms.append(dom)
    
    except KeyboardInterrupt:
        sys.exit(c.RED + "\n[!] Interrupt handler received, exiting...\n" + c.END)
    except:
        pass
                
    """
    Get subdomains from Hackertarget
    """
    try:
        r = requests.get(f"https://api.hackertarget.com/hostsearch/?q={domain}", timeout=20)
        hackertarget_domains = re.findall(r'(.*?),', r.text)
        
        # Only append new valid subdomains
        for dom in hackertarget_domains:
            if dom.endswith(domain) and dom not in doms:
                doms.append(dom)
                
    except KeyboardInterrupt:
        sys.exit(c.RED + "\n[!] Interrupt handler received, exiting...\n" + c.END)
    except:
        pass
                
    """
    Get subdomains from RapidDNS
    """
    try:
        r = requests.get(f"https://rapiddns.io/subdomain/{domain}", timeout=20)
        rapiddns_domains = re.findall(r'target="_blank".*?">(.*?)</a>', r.text)

        # Only append new valid subdomains
        for dom in rapiddns_domains:
            if dom.endswith(domain) and dom not in doms:
                doms.append(dom)
                
    except KeyboardInterrupt:
        sys.exit(c.RED + "\n[!] Interrupt handler received, exiting...\n" + c.END)
    except:
        pass
    """
    Get subdomains from Riddler
    """
    try:
        r = requests.get(f"https://riddler.io/search/exportcsv?q=pld:{domain}", timeout=20)
        riddler_domains = re.findall(r'\[.*?\]",.*?,(.*?),\[', r.text)

        # Only append new valid subdomains
        for dom in riddler_domains:
            if dom.endswith(domain) and dom not in doms:
                doms.append(dom)
                
    except KeyboardInterrupt:
        sys.exit(c.RED + "\n[!] Interrupt handler received, exiting...\n" + c.END)
    except:
        pass
    """
    Get subdomains from ThreatMiner
    """
    try:
        r = requests.get(f"https://api.threatminer.org/v2/domain.php?q={domain}&rt=5", timeout=20)
        raw_domains = json.loads(r.content)
        threatminer_domains = raw_domains['results']
        
        # Only append new valid subdomains
        for dom in threatminer_domains:
            if dom.endswith(domain) and dom not in doms:
                doms.append(dom)
    except KeyboardInterrupt:
        sys.exit(c.RED + "\n[!] Interrupt handler received, exiting...\n" + c.END)
    except:
        pass

    """
    Get subdomains from URLScan
    """
    try:
        r = requests.get(f"https://urlscan.io/api/v1/search/?q={domain}", timeout=20)
        urlscan_domains = sorted(set(re.findall(r'https://(.*?).' + domain, r.text)))
    
        # Only append new valid subdomains
        for dom in urlscan_domains:
            dom = dom + "." + domain
            if dom.endswith(domain) and dom not in doms:
                doms.append(dom)
                
    except KeyboardInterrupt:
        sys.exit(c.RED + "\n[!] Interrupt handler received, exiting...\n" + c.END)
    except:
        pass
                
    if filename != None:
        f = open(filename, "a")
    
    if doms:

        """
        Iterate through the subdomains and check the lenght to print them in a table format
        """

        print(c.YELLOW + "+" + "-"*47 + "+")
        for value in doms:
    
            if len(value) >= 10 and len(value) <= 14:
                l = len(value)
                print("| " + value + "    \t\t\t\t|")
                if filename != None:
                    f.write(value + "\n")

            if len(value) >= 15 and len(value) <= 19:
                l = len(value)
                print("| " + value + "\t\t\t\t|")
                if filename != None:
                    f.write(value + "\n")

            if len(value) >= 20 and len(value) <= 24:
                l = len(value)
                print("| " + value + "   \t\t\t|")
                if filename != None:
                    f.write(value + "\n")
    
            if len(value) >= 25 and len(value) <= 29:
                l = len(value)
                print("| " + value + "\t\t\t|")
                if filename != None:
                    f.write(value + "\n")

            if len(value) >= 30 and len(value) <= 34:
                l = len(value)
                print("| " + value + " \t\t|")
                if filename != None:
                    f.write(value + "\n")

            if len(value) >= 35 and len(value) <= 39:
                l = len(value)
                print("| " + value + "   \t|")
                if filename != None:
                    f.write(value + "\n")

            if len(value) >= 40 and len(value) <= 44:
                l = len(value)
                print("| " + value + " \t|")
                if filename != None:
                    f.write(value + "\n")

        """
        Print summary
        """
        print("+" + "-"*47 + "+" + c.END)
        print(c.YELLOW + "\nTotal discovered sudomains: " + str(len(doms)) + c.END)

        """
        Close file if "-o" parameter was especified
        """

        if filename != None:
            f.close()
            print(c.BLUE + "\n[" + c.GREEN + "+" + c.BLUE + "] Output stored in " + filename)
    else:
        print(c.YELLOW + "Any subdomain discovered through SSL transparency" + c.END)

# Check if the given target is active/real
def checkDomain(domain):

    try:
        addr = socket.gethostbyname(domain)
    except:
        print(c.YELLOW + "\nTarget doesn't exists or is down" + c.END)
        sys.exit(1)

# Program workflow starts here
if __name__ == '__main__':

    urllib3.disable_warnings()
    
    # If --version is passed
    if "--version" in sys.argv:
        print("\nSDomDiscover v1.0 - By D3Ext")
        print("Contact me: <d3ext@proton.me>\n")
        sys.exit(0)

    parse = parseArgs()

    # Check domain format
    dom_format = parse.domain.split(".")
    if len(dom_format) != 2:
        print(c.YELLOW + "\nInvalid domain format, example: domain.com" + c.END)
        sys.exit(0)

    warnings.simplefilter('ignore')

    # If --output is passed
    if parse.output:
        store_info=1
        filename = parse.output
    else:
        filename = None

    global domain

    domain = parse.domain
    checkDomain(domain)

    """
    If --all is passed do all enumeration processes
    """
    if parse.domain and parse.all:

        if domain.startswith('https://'):
            domain = domain.split('https://')[1]

        if domain.startswith('http://'):
            domain = domain.split('http://')[1]

        try:

            if not parse.quiet:
                banner()

            SDom(domain,filename)
            portScan(domain)
            ns_enum(domain)
            axfr(domain)
            mail_enum(domain)
            ip_enum(domain)
            ipv6_enum(domain)
            txt_enum(domain)
            whoisLookup(domain)
            basicEnum(domain)
            cloudgitEnum(domain)
            wafDetector(domain)
            checkActiveSubs(domain,doms)
            wayback(domain)
            subTakeover(doms)

            if parse.token:
                crawlMails(domain, parse.token)
            else:
                print(c.BLUE + "\n[" + c.GREEN + "-" + c.BLUE + "] No API token provided, skipping email crawling" + c.END)

            try:
                file.close()
            except:
                pass

        except KeyboardInterrupt:
            sys.exit(c.RED + "\n[!] Interrupt handler received, exiting...\n" + c.END)

        sys.exit(0)

    """
    Enter in this part if the --all isn't passed
    """
    if parse.domain:

        domain = parse.domain

        if domain.startswith('https://'):
            domain = domain.split('https://')[1]

        if domain.startswith('http://'):
            domain = domain.split('http://')[1]
        
        try:

            if not parse.quiet:
                banner()

            SDom(domain,filename)
    
            """
            Check the passed arguments via command line
            """

            if parse.portscan:
                portScan(domain)
        
            if parse.nameservers:
                ns_enum(domain)

            if parse.axfr:
                axfr(domain)
    
            if parse.mail:
                mail_enum(domain)

            if parse.ip:
                ip_enum(domain)

            if parse.ipv6:
                ipv6_enum(domain)

            if parse.extra:
                txt_enum(domain)

            if parse.whois:
                whoisLookup(domain)

            if parse.enum:
                basicEnum(domain)

            if parse.repos:
                cloudgitEnum(domain)

            if parse.waf:
                wafDetector(domain)

            if parse.check:
                checkActiveSubs(domain,doms)

            if parse.wayback:
                wayback(domain)

            if parse.subtakeover:
                subTakeover(doms)

            if parse.token:
                crawlMails(domain, parse.token)
    
        except KeyboardInterrupt:
            sys.exit(c.RED + "\n[!] Interrupt handler received, exiting...\n" + c.END)


