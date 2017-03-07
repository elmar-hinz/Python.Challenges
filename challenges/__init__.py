from os.path import dirname, realpath

version_file = realpath(dirname(dirname(__file__))) + '/version.txt'
with open(version_file) as f:
    __version__ = f.read().strip()
