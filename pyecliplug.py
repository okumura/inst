#!/usr/bin/python

import sys
import os
import glob
from subprocess import *
import re

APP = 'org.eclipse.update.core.standaloneUpdate'

def get_search_command(path, url):
	return [
            'java', '-jar', path, 
            '-application', APP,
            '-command', 'search',
            '-from', url]

def get_install_command(path, url, featureId, version):
	return [
            'java', '-jar', path, 
            '-application', APP,
            '-command', 'install',
            '-featureId', featureId,
            '-version', version,
            '-from', url]

def get_launcher():
    if not os.environ.has_key('ECLIPSE_ROOT'):
        raise NameError, 'please define "ECLIPSE ROOT" environemt variable.'
    
    ECLIPSE_ROOT = os.environ['ECLIPSE_ROOT']
    LAUNCHER_GLOB = 'plugins/org.eclipse.equinox.launcher_*.jar'
    files = glob.glob(os.path.join(ECLIPSE_ROOT, LAUNCHER_GLOB))
    if len(files) == 1:
        return files[0]
    else:
        raise NameError, 'equinox launcher not found.'

def search(update_url):
	launcher = get_launcher()
	cmd = get_search_command(launcher, update_url)
	return Popen(cmd, stdout=PIPE).communicate()[0]

def get_feature_version(update_url, featureId):
	p = re.compile('"(.+)" (.+) (.+)')
	for line in search(update_url).splitlines():
		m = p.match(line)
		if m != None and m.group(2) == featureId:
			return m.group(3)

def install(update_url, featureId):
	version = get_feature_version(update_url, featureId)
	if version != None:
		launcher = get_launcher()
		cmd = get_install_command(launcher, update_url, featureId, version)
		return Popen(cmd, stdout=PIPE).communicate()[0]

def main():
    if len(sys.argv) <= 2:
        print 'usage: '
        print '	pyecliplug.py search <update_url>'
        print '	pyecliplug.py install <update_url> <featureId>'
    elif sys.argv[1] == 'search':
        print search(sys.argv[2])
    elif sys.argv[1] == 'install':
        print install(sys.argv[2], sys.argv[3])

if __name__ == "__main__":
	main()
