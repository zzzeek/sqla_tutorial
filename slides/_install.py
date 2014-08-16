import pip
import os

path = os.path.abspath("sw")
assert os.path.exists(path)
pip.main(["install", "-r", "requirements.txt", "--no-index", "--upgrade", "-f", "file://%s" % path])

