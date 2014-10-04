#!/usr/bin/python

import re
import argparse
import subprocess

DEFAULT_BUFFER = 'main'
DEFAULT_ROTATE_COUNT = 100
DEFAULT_ROTATE_SIZE = 256
DEFAULT_FORMAT = 'threadtime'

parser = argparse.ArgumentParser()
parser.add_argument('--device', help="Device serial number to run logcat on.")
parser.add_argument('-b', '--buffer', default=DEFAULT_BUFFER, help="Loads an alternate log buffer for viewing, such as events or radio. The main buffer is used by default.")
parser.add_argument('-c', '--clear', action='store_true', help="Clears (flushes) the entire log and exits.")
parser.add_argument('-d', '--dump', action='store_true', help="Dumps the log to the screen and exits.")
parser.add_argument('-g', '--size', action='store_true', help="Prints the size of the specified log buffer and exits.")
parser.add_argument('-s', '--silent', action='store_true', help="Sets the default filter spec to silent.")
parser.add_argument('-v', '--format', default=DEFAULT_FORMAT, help="Sets the output format for log messages. The default is brief format.")
parser.add_argument('filters', nargs='*', help="Logcat filters. Python regex is supported.")

args = parser.parse_args()

def call(cmd):
  proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1)
  for line in iter(proc.stdout.readline, ''):
    print line[:-1]
  proc.kill()

if args.clear:
  call(['adb', 'logcat', '-c'])
  exit()

if args.size:
  call(['adb', 'logcat', '-g'])
  exit()

if args.format != DEFAULT_FORMAT:
  print "Only support %s format for now." % (DEFAULT_FORMAT)
  exit()


class FilterRule(object):
  ANDROID_LOG_LEVELS = {'*': 0, 'V': 0, 'D': 1, 'I':2, 'W': 3, 'E': 4, 'F': 5, 'S': 6}

  def __init__(self, tag, level):
    super(FilterRule, self).__init__()
    if level not in FilterRule.ANDROID_LOG_LEVELS:
      raise Exception("Invalid log level: %s" % (level))
    self.level = FilterRule.ANDROID_LOG_LEVELS[level]
    # shortcut * to match all tags
    if tag == '*':
      tag = '.*'
    try:
      self.tag = re.compile(tag)
    except:
      print "Invalid tag regex: %s" % (tag)
      raise
    self.rule = "%s:%s" % (tag, level)

  def match(self, tag):
    return self.tag.match(tag) is not None

  def should_print(self, tag, level):
    assert self.match(tag)
    return FilterRule.ANDROID_LOG_LEVELS[level] >= self.level

  def __str__(self):
    return str(self.__dict__)


g_filter_rules = []
for filter in args.filters:
  parts = filter.split(':')
  if len(parts) < 2:
    print "Invalid filter rule %s" % (filter)
    exit()
  level = parts[-1]
  tag = ':'.join(parts[:-1])
  g_filter_rules.append(FilterRule(tag, level))


# default rule comes last
if args.silent:
  g_filter_rules.append(FilterRule('.*', 'S'))
else:
  g_filter_rules.append(FilterRule('.*', '*'))


def should_print(line):
  global g_filter_rules

  parts = line.split()
  level = parts[4]
  tag = ' '.join(parts[5:]).split(':')[0]

  for filter in g_filter_rules:
    if filter.match(tag):
      return filter.should_print(tag, level)

  return True

cmd = ['adb']
if args.device is not None :
  cmd += ['-s', args.device]
cmd += ['logcat', '-v', args.format, '-b', args.buffer]
if args.dump:
  cmd += ['-d']

try:
  proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1)
  for line in iter(proc.stdout.readline, ''):
    line = line[:-1]
    if should_print(line):
      print line
except KeyboardInterrupt:
  proc.kill()
