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

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

PATH = os.getcwd()

def run_program(file_name):
	process = subprocess.Popen([f'{PATH}\\{file_name}'],shell = True)
	process.wait()
	if process.returncode == 0:
		print("Success")
	else:
		print("Error")


if __name__ == "__main__":
	process = subprocess.Popen(['pip','install','-r','requirements.txt'],shell = True)
	process.wait()
	run_program("7zip_update.py")
	run_program("filezilla_update.py")
	run_program("notepad_update.py")
	run_program("totalcommander_update.py")
	
