#!/usr/bin/env python3

import json
import argparse
import urllib.request as urllib
import sys
import ssl

if __name__ == "__main__":
 parser = argparse.ArgumentParser(prog=sys.argv[0], description="Download an app from HockeyApp")
 parser.add_argument("--platform", help="ios or android")
 parser.add_argument("--token", help="HockeyApp API-Token with Full Access")
 parser.add_argument('--app-id', metavar='app_id', nargs='?', default='0', help='hockeyapp app id')
 args = parser.parse_args()

 ssl._create_default_https_context = ssl._create_unverified_context

 if args.platform == 'ios':
   extension = 'ipa'
 elif args.platform == 'android':
   extension = 'apk'
 else:
   print("Platform should be either ios or android")
   exit(1)

 q = urllib.Request('https://rink.hockeyapp.net/api/2/apps/' + args.app_id + '/app_versions')
 q.add_header('X-HockeyAppToken', args.token)
 versions_response = urllib.urlopen(q)
 versions = json.load(versions_response)
 latest_id = str(versions['app_versions'][0]['id'])

 app_url = 'https://rink.hockeyapp.net/api/2/apps/' + args.app_id + '/app_versions/' + latest_id + '?format=' + extension
 urllib.urlretrieve(app_url, args.app_id + '.' + extension)
