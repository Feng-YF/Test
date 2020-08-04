#!/usr/bin/env python3

import os
import subprocess
import sys
import argparse

if __name__ == "__main__":

  parser = argparse.ArgumentParser(prog=sys.argv[0], description="Start an browserstacklocal server and run some tests, ensuring that the server process is stopped at the end.")
  parser.add_argument('--test_script', metavar='test_script', nargs='?', default='run-browserstack-tests', help='test script to run, e.g. "run-tests-ios-cert" will run the "run-tests-ios-cert.sh" script in the same directory as run-browserstack-local.py')
  args = parser.parse_args()

  scriptsDir = os.path.dirname(os.path.realpath(__file__))
  proc = subprocess.Popen(['BrowserStackLocal', '--key', os.getenv('BROWSERSTACK_PSW'), '--pac-file', scriptsDir + '/proxy1.pac', '--force-local'])
  try:
    print("started browserstacklocal process with pid {0}".format(proc.pid))
    subprocess.check_call(f'{scriptsDir}/{args.test_script}.sh')
  except subprocess.CalledProcessError as err:
    retcode, cmd = err.args
    sys.exit(retcode)
  finally:
    if proc.poll() is None:
      print("Killing browserstacklocal process with pid {0}".format(proc.pid))
      proc.kill()
      print("Done.")