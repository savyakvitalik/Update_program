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
#This url adress need change
URL = 'https://download.filezilla-project.org/client/FileZilla_3.60.2_win64_sponsored2-setup.exe'


#Fuction for get current date
def get_current_date():
    current_date = date.today()
    return current_date

#Fuction for get download file
def get_download_and_install_file():
    file = open(rf"{PATH}\Logs\Result-filezilla-{get_current_date()}.txt", "w")
    if(os.path.exists("downloads")):
        shutil.rmtree("downloads")
    os.mkdir("downloads")
    Program_Name = f"{PATH}\\downloads\\filezilla.exe"
    file.write("Downloading...")
    with urllib.request.urlopen(URL) as response, open(Program_Name, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
    file.write("\tSUCCESS\n")
    file.write("Installing...")
    process = subprocess.Popen([f'{PATH}\\downloads\\filezilla.exe', '/S'])
    process.wait()
    file.write("\tSUCCESS\n")
    os.remove(f"{PATH}\\downloads\\filezilla.exe")
    shutil.rmtree("downloads")
    file.write("Filezilla updated successful\n")

#Fuction installing program
def get_download_file():
    file = open(rf"{PATH}\Logs\Result-filezilla-{get_current_date()}.txt", "w")
    if(os.path.exists("downloads")):
        shutil.rmtree("downloads")
    os.mkdir("downloads")
    Program_Name = f"{PATH}\\downloads\\filezilla.exe"
    file.write("Downloading...")
    with urllib.request.urlopen(URL) as response, open(Program_Name, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
    file.write("\tSUCCESS\n")

#Fuction to check old version program
def check_old_version():
    old_version_1 = subprocess.check_output(['powershell.exe',"(Get-Item \"C:\\Program Files\\FileZilla FTP Client\\filezilla.exe\").VersionInfo.FileVersion"], universal_newlines=True)
    old_version_2 = ''.join([old_version_1[i] for i in range(len(old_version_1)) if old_version_1[i] != "."])
    old_version_3 = ''.join([old_version_2[i] for i in range(len(old_version_2)) if old_version_2[i] != " "])
    old_version_4 = ''.join([old_version_3[i] for i in range(len(old_version_3)) if old_version_3[i] != ","])
    old_version = old_version_4[:4]
    return old_version

#Fuction to check new version program
def check_new_version():
    get_download_file()
    new_version_1 = subprocess.check_output(['powershell.exe',f"(Get-Item \"{PATH}\\downloads\\filezilla.exe\").VersionInfo.FileVersion"], universal_newlines=True)
    new_version = ''.join([new_version_1[i] for i in range(len(new_version_1)) if new_version_1[i] != "."])
    os.remove(f"{PATH}\\downloads\\filezilla.exe")
    shutil.rmtree("downloads")
    return new_version

#Fuction to comparing old and new date
def comparisons_version():
    old_version = int(check_old_version())
    new_version = int(check_new_version())
    if (new_version - old_version) == 0:
        return True
    else:
        return False


if __name__ == "__main__":
    file = open(rf"{PATH}\Logs\Result-filezilla-{get_current_date()}.txt", "w")
    file.write("Error")
    file.close()
    if(os.path.exists("C:\\Program Files\\FileZilla FTP Client\\filezilla.exe")):
        if (comparisons_version()):
            file = open(rf"{PATH}\Logs\Result-filezilla-{get_current_date()}.txt", "w")
            file.write("Successful\nNew version Filezilla installed")
        else:
            get_download_and_install_file()
    else:
        get_download_and_install_file()
    file.close()
