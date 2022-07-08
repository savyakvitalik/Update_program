import requests
from datetime import date
from bs4 import BeautifulSoup
import urllib.request
import os
import platform
import shutil
import subprocess
import time
import ssl
###########################

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

###########################

PATH = os.getcwd()
URL = 'https://www.ghisler.com/download.htm'

def get_current_date():
    current_date = date.today()
    return current_date

def get_html(url):
    r = requests.get(url)
    return r

def get_html_text(url):
    r = requests.get(url)
    return r.text

def check_old_version_32bit_1():
    old_version = subprocess.check_output(['powershell.exe',"(Get-Item \"C:\\Program Files\\totalcmd\\TOTALCMD.EXE\").VersionInfo.FileVersion"], universal_newlines=True)
    return old_version
def check_old_version_64bit_1():
    old_version = subprocess.check_output(['powershell.exe',"(Get-Item \"C:\\Program Files\\totalcmd\\TOTALCMD64.EXE\").VersionInfo.FileVersion"], universal_newlines=True)
    return old_version
def check_old_version_32bit_2():
    old_version = subprocess.check_output(['powershell.exe',"(Get-Item \"C:\\Program Files (x86)\\totalcmd\\TOTALCMD.EXE\").VersionInfo.FileVersion"], universal_newlines=True)
    return old_version
def check_old_version_64bit_2():
    old_version = subprocess.check_output(['powershell.exe',"(Get-Item \"C:\\Program Files (x86)\\totalcmd\\TOTALCMD64.EXE\").VersionInfo.FileVersion"], universal_newlines=True)
    return old_version

def check_old_version():
    if(os.path.exists("C:\\Program Files\\totalcmd\\TOTALCMD.EXE")):
        old_version_1 = check_old_version_32bit_1()
    elif(os.path.exists("C:\\Program Files\\totalcmd\\TOTALCMD64.EXE")):
        old_version_1 = check_old_version_64bit_1()
    elif(os.path.exists("C:\\Program Files (x86)\\totalcmd\\TOTALCMD.EXE")):
        old_version_1 = check_old_version_32bit_2()
    elif(os.path.exists("C:\\Program Files (x86)\\totalcmd\\TOTALCMD64.EXE")):
        old_version_1 =check_old_version_64bit_2()

    if old_version_1[3] == ".":
        old_version_2 = old_version_1[0] + old_version_1[1] + old_version_1[2]
    else:
        old_version_2 = old_version_1[0] + old_version_1[1] + old_version_1[2] + old_version_1[3]
    old_version_3 = ''.join([old_version_2[i] for i in range(len(old_version_2)) if old_version_2[i] != "."])
    old_version_4 = ''.join([old_version_3[i] for i in range(len(old_version_3)) if old_version_3[i] != " "])
    old_version = ''.join([old_version_4[i] for i in range(len(old_version_4)) if old_version_4[i] != ","])
    return old_version

def check_new_version(html):
    soup = BeautifulSoup(html, 'html.parser')
    txt = soup.find("h3")
    txt1 = txt.text
    full_version = txt1.split(' ')
    version = full_version[9]
    new_version_1 = version[:-1]
    new_version = ''.join([new_version_1[i] for i in range(len(new_version_1)) if new_version_1[i] != "."])
    return new_version

def comparisons_version():
    old_version = int(check_old_version())
    new_version = int(check_new_version(get_html_text(URL)))
    if (new_version - old_version) == 0:
        return True
    else:
        return False

def get_download_link(html):
    soup = BeautifulSoup(html, 'html.parser')
    urls = []
    for link in soup.find_all('a'): 
        urls.append(link.get('href'))
    return urls[16]

def get_download_and_install_file(result_url):
    file = open(rf"{PATH}\Logs\Result-totalCommander-{get_current_date()}.txt", "w")
    if(os.path.exists("downloads")):
        shutil.rmtree("downloads")
    os.mkdir("downloads")
    Program_Name = f"{PATH}\\downloads\\TotalCommander.exe"
    file.write("Downloading...")
    with urllib.request.urlopen(result_url) as response, open(Program_Name, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
    file.write("\tSUCCESS\n")
    file.write("Installing...")
    process = subprocess.Popen([f'{PATH}\\downloads\\TotalCommander.exe', '/AHMGDU'])
    process.wait()
    file.write("\tSUCCESS\n")
    os.remove(f"{PATH}\\downloads\\TotalCommander.exe")
    shutil.rmtree("downloads")
    file.write("TotalCommander updated successful\n")

if __name__ == "__main__":
    file = open(rf"{PATH}\Logs\Result-totalCommander-{get_current_date()}.txt", "w")
    file.write("Error")
    file.close()
    if(os.path.exists("C:\\Program Files\\totalcmd\\TOTALCMD.EXE")) or (os.path.exists("C:\\Program Files\\totalcmd\\TOTALCMD64.EXE")):
        html = get_html(URL)
        if html.status_code == 200:
            if(comparisons_version()):
                file = open(rf"{PATH}\Logs\Result-totalCommander-{get_current_date()}.txt", "w")
                file.write("Successful\nNew version TotalCommander installed")
            else:
                result_url = get_download_link(get_html_text(URL))
                get_download_and_install_file(result_url)
        else:
            file = open(rf"{PATH}\Logs\Result-totalCommander-{get_current_date()}.txt", "w")
            file.write("Eror page\n")

    elif (os.path.exists("C:\\Program Files (x86)\\totalcmd\\TOTALCMD64.EXE")) or (os.path.exists("C:\\Program Files (x86)\\totalcmd\\TOTALCMD.EXE")):
        html = get_html(URL)
        if html.status_code == 200:
            if(comparisons_version()):
                file = open(rf"{PATH}\Logs\Result-totalCommander-{get_current_date()}.txt", "w")
                file.write("Successful\nNew version TotalCommander installed")
            else:
                result_url = get_download_link(get_html_text(URL))
                get_download_and_install_file(result_url)
        else:
            file = open(rf"{PATH}\Logs\Result-totalCommander-{get_current_date()}.txt", "w")
            file.write("Eror page\n")

    else:
        html = get_html(URL)
        if html.status_code == 200:
            result_url = get_download_link(get_html_text(URL))
            get_download_and_install_file(result_url)
        else:
            file = open(rf"{PATH}\Logs\Result-totalCommander-{get_current_date()}.txt", "w")
            file.write("Eror page\n")

    file.close()

