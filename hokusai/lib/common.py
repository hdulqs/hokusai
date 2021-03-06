import os
import sys
import signal
import string
import random
import json

from subprocess import call, check_call, check_output, Popen, STDOUT

import yaml

from botocore import session as botosession

from termcolor import cprint

from hokusai.lib.config import config
from hokusai.lib.exceptions import CalledProcessError

CONTEXT_SETTINGS = {
  'terminal_width': 10000,
  'max_content_width': 10000,
  'help_option_names': ['-h', '--help']
}

EXIT_SIGNALS = [signal.SIGHUP, signal.SIGINT, signal.SIGQUIT, signal.SIGPIPE, signal.SIGTERM]

VERBOSE = False

AWS_DEFAULT_REGION = 'us-east-1'

def smart_str(s, newline_before=False, newline_after=False):
  if newline_before:
    s = '\n' + s
  if newline_after:
    s = s + '\n'
  if isinstance(s, unicode):
      return unicode(s).encode("utf-8")
  elif isinstance(s, int) or isinstance(s, float):
      return str(s)
  return s

def print_smart(msg, newline_before=False, newline_after=False):
  print(smart_str(msg, newline_before, newline_after))

def print_green(msg, newline_before=False, newline_after=False):
  cprint(smart_str(msg, newline_before, newline_after), 'green')

def print_red(msg, newline_before=False, newline_after=False):
  cprint(smart_str(msg, newline_before, newline_after), 'red')

def print_yellow(msg, newline_before=False, newline_after=False):
  cprint(smart_str(msg, newline_before, newline_after), 'yellow')

def set_verbosity(v):
  global VERBOSE
  VERBOSE = v or config.always_verbose

def get_verbosity():
  global VERBOSE
  return VERBOSE

def verbose(msg):
  if VERBOSE: print_yellow("==> hokusai exec `%s`" % msg, newline_after=True)
  return msg


def returncode(command):
  return call(verbose(command), stderr=STDOUT, shell=True)

def shout(command, print_output=False):
  if print_output:
    return check_call(verbose(command), stderr=STDOUT, shell=True)
  else:
    return check_output(verbose(command), stderr=STDOUT, shell=True)

def shout_concurrent(commands, print_output=False):
  if print_output:
    processes = [Popen(verbose(command), shell=True) for command in commands]
  else:
    processes = [Popen(verbose(command), shell=True, stdout=open(os.devnull, 'w'), stderr=STDOUT) for command in commands]

  return_codes = []
  try:
    for p in processes:
      return_codes.append(p.wait())
  except KeyboardInterrupt:
    for p in processes:
      p.terminate()
    return_codes = [1 for p in processes]
  return return_codes

def k8s_uuid():
  uuid = []
  for i in range(0,5):
    uuid.append(random.choice(string.lowercase))
  return ''.join(uuid)

def clean_string(str):
  return str.lower().replace('_', '-')

def get_region_name():
  # boto3 autodiscovery
  _region = botosession.get_session().get_config_variable('region')
  if _region:
    return _region
  # boto2 compatibility
  if os.environ.get('AWS_REGION'):
    return os.environ.get('AWS_REGION')
  return AWS_DEFAULT_REGION
