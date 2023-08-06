
print("Running __init__.py in karaml package")
import os
if not os.path.exists('KARaML_Tools'):
  os.mkdir('KARaML_Tools')
import gdown
gdown.download(id="14iuvYqoCWdUS_Adf3t1fBNS8tpOj-09Z", output='KARaML_Tools/karaml_setup.py')

#print("Import everything from karaml_tools.py")
#from .karaml_tools import *
