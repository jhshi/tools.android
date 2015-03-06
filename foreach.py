#!/usr/bin/python

import argparse
import subprocess

parser = argparse.ArgumentParser()

parser.add_argument('exe', help='Executable to use. Must support devices and -s option to list and specify device.')
parser.add_argument('args', nargs=argparse.REMAINDER, help='Arguments.')

args = parser.parse_args()

devices = []
for line in subprocess.check_output('%s devices' % (args.exe), shell=True).split('\n'):
  line = line.strip()
  if len(line) > 0 and line[0].isdigit():
    devices.append(line.split()[0])

print '============================================'
print '%d devices detected: \n%s' % (len(devices), '\n'.join(devices))
print '============================================'

for d in devices:
  subprocess.check_call('%s -s %s %s' % (args.exe, d, ' '.join(args.args)), shell=True)
