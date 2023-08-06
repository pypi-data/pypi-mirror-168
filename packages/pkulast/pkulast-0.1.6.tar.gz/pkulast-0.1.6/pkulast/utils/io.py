import os
import sys

def ensure_dir(filename):
	""" Check if the dir of f exists, otherwise create it.
	"""
	directory = os.path.dirname(filename)
	if directory and not os.path.isdir(directory):
		os.mkdirs(directory)

def check_filename_exist(filename):
	if not os.path.exists(filename) or not os.path.isfile(filename):
		errmsg = ('File does not exist! Filename = ' + str(filename))
		raise IOError(errmsg)
	else:
		return True

def check_file_status(filepath, filesize):
    sys.stdout.write('\r')
    sys.stdout.flush()
    size = int(os.stat(filepath).st_size)
    percent_complete = (size/filesize)*100
    sys.stdout.write('%s %.2f %s' % (os.path.basename(filepath), percent_complete, '% Completed'))
    sys.stdout.flush()