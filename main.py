import requests
from os.path import abspath, dirname, join
from datetime import date
from bs4 import BeautifulSoup
import urllib.request
import os
import platform
import shutil
import subprocess
import time
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

BASE_DIR = dirname(abspath(__file__))
Repository_name = 'https://github.com/savyakvitalik/Update_program.git'

def zabbix_check(main_list_error,list_error):
	if(os.path.exists("Zabbix")):
		pass
	else:
		os.mkdir("Zabbix")
	for word in main_list_error:
		if word == "Error":
			file = open(rf"{BASE_DIR}\Zabbix\program_update.txt", "w")
			file.write(f"{list_error}")
			file.close()
		else:
			file = open(rf"{BASE_DIR}\Zabbix\program_update.txt", "w")
			file.write("True")
			file.close()
	

def run_program(file_name,main_list_error,list_error):
	if(os.path.exists("Logs")):
		pass
	else:
		os.mkdir("Logs")
	process = subprocess.Popen([f'{BASE_DIR}\\{file_name}'],shell = True)
	process.wait()
	if process.returncode == 0:
		print("Success")
	else:
		main_list_error.append("Error")
		list_error.append(f"Error in {file_name}")
		print("Error")


if __name__ == "__main__":
	main_list_error = [""]
	list_error = ["Errors: "]
	process_pip_install = subprocess.Popen(['pip','install','-r','requirements.txt'],shell = True)
	process_pip_install.wait()
	process_git_pull = subprocess.Popen(['git','pull',f'{Repository_name}'],shell = True)
	process_git_pull.wait()
	file_names = ['7zip_update.py','filezilla_update.py','notepad_update.py','totalcommander_update.py']
	for name in file_names:
		run_program(name,main_list_error,list_error)

	zabbix_check(main_list_error,list_error)
