import tarfile

tar = tarfile.open("sw/virtualenv-1.10.1.tar.gz")
tar.extractall()
tar.close()

import sys
import os

win32 = sys.platform.startswith('win')

if win32:
    os.system(r"%s virtualenv-1.10.1\virtualenv.py .venv" % sys.executable)
    os.system(r".venv\Scripts\python.exe install.py")
else:
    os.system("%s virtualenv-1.10.1/virtualenv.py .venv" % sys.executable)
    os.system(".venv/bin/python install.py")
