
print("Welcome to the KARaML Tools package (version 0.0.22)")

def respond():
    return "Response from karaml_tools.py" 

INSTALL_PATH = '/content/KARaML_Tools'

import os
INITIAL_DIR = os.getcwd()
if not os.path.exists(INSTALL_PATH):
  os.mkdir(INSTALL_PATH )
os.chdir(INSTALL_PATH )

import subprocess
subprocess.run(["pip", "-q", "install", "gdown"])
import gdown
gdown.download(id='14iuvYqoCWdUS_Adf3t1fBNS8tpOj-09Z', quiet=True)
from karaml_setup import *
os.chdir(INITIAL_DIR)
