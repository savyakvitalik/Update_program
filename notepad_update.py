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
url_text = 'https://notepad-plus-plus.org/'

def get_current_date():
    current_date = date.today()
    return current_date

#Function of getting html text
def get_html(url, params=None):
    r = requests.get(url,params=params)
    return r
#Function of checking old version notepad++
def check_old_version():
    old_version_1 = subprocess.check_output(['powershell.exe',"(Get-Item \"C:\\Program Files\\Notepad++\\notepad++.exe\").VersionInfo.FileVersion"], universal_newlines=True)
    old_version = ''.join([old_version_1[i] for i in range(len(old_version_1)) if old_version_1[i] != "."])
    return old_version

#Function of checking new version notepad++ and write to file
def check_new_version(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find('p', class_='library-desc')
    txt = items.text
    new_version_1 = txt[17:]
    new_version = ''.join([new_version_1[i] for i in range(len(new_version_1)) if new_version_1[i] != "."])       
    return new_version

#Fuction to comparing old and new date
def comparisons_version():
    html_1 = get_html(url_text)
    old_version = int(check_old_version())
    new_version = int(check_new_version(html_1.text))
    if (new_version - old_version) == 0:
        return True
    else:
        return False

#Function of getting url page
def get_download_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    urls = []
    for link in soup.find_all('a'): 
        urls.append(link.get('href'))
    url_download = urls[2]
    download_page = url_text + url_download
    return download_page

#Function of getting url download
def get_url_download(html):
    soup = BeautifulSoup(html, 'html.parser')
    urls = []
    for link in soup.find_all('a'):
        urls.append(link.get('href')) 
    url_download = urls[12]
    return url_download

#Fuction for get download file and install program
def get_download_and_install_file(result_url):
    file = open(rf"{PATH}\Logs\Result-notepad-{get_current_date()}.txt", "w")
    if(os.path.exists("downloads")):
        shutil.rmtree("downloads")
    os.mkdir("downloads")
    Program_Name = f"{PATH}\\downloads\\notepad++.exe"
    file.write("Downloading...")
    with urllib.request.urlopen(result_url) as response, open(Program_Name, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
    file.write("\tSUCCESS\n")
    file.write("Installing...")
    process = subprocess.Popen([f'{PATH}\\downloads\\notepad++.exe', '/S'])
    process.wait()
    file.write("\tSUCCESS\n")
    os.remove(f"{PATH}\\downloads\\notepad++.exe")
    shutil.rmtree("downloads")
    file.write("Notepad++ install successful\n")

if __name__ == "__main__":
    file = open(rf"{PATH}\Logs\Result-notepad-{get_current_date()}.txt", "w")
    file.write("Error")
    file.close()
    #Check of exist notepad++
    if(os.path.exists("C:\\Program Files\\Notepad++\\notepad++.exe")):
        html_1 = get_html(url_text)   
        if(html_1.status_code) == 200:
            if(comparisons_version()):
                file = open(rf"{PATH}\Logs\Result-notepad-{get_current_date()}.txt", "w")
                file.write("Successful\nNew version notepad++ installed")
            else:
                url_page = get_download_page(html_1.text)
                html_2 = get_html(url_page)
                if(html_2.status_code) == 200:
                    result_url = get_url_download(html_2.text)
                    get_download_and_install_file(result_url)
                else:
                    file = open(rf"{PATH}\Logs\Result-notepad-{get_current_date()}.txt", "w")
                    file.write("Eror second page\n")
        else:
            file = open(rf"{PATH}\Logs\Result-notepad-{get_current_date()}.txt", "w")
            file.write("Eror first page\n")
    else:
        html_3 = get_html(url_text)  
        if(html_3.status_code) == 200:
            url_page = get_download_page(html_3.text)
            html_4 = get_html(url_page)
            if(html_4.status_code) == 200:
                result_url = get_url_download(html_4.text)
                get_download_and_install_file(result_url)
            else:
                file = open(rf"{PATH}\Logs\Result-notepad-{get_current_date()}.txt", "w")
                file.write("Eror second page\n")
        else:
            
            file.write("Eror first page\n")
    file.close()

