#!/usr/bin/env python3

import json
import argparse
import urllib.request as urllib
import sys
import ssl

if __name__ == "__main__":
 parser = argparse.ArgumentParser(prog=sys.argv[0], description="Download an app from App Center")
 parser.add_argument("--token", help="App Center API-Token with Full Access")
 parser.add_argument("--platform", help="ios or android")
 parser.add_argument('--owner-name', metavar='owner_name', nargs='?', default='0', help=' owner name')
 parser.add_argument('--app-name', metavar='app_name', nargs='?', default='0', help=' app id')

 args = parser.parse_args()

# Handle extension for build platform
 if args.platform == 'ios':
   extension = 'ipa'
 elif args.platform == 'android':
   extension = 'apk'
 else:
   print("Platform should be either ios or android")
   exit(1)

# Call to retrieve latest release id
 q = urllib.Request('https://api.appcenter.ms/v0.1/apps/' + args.owner_name + '/' + args.app_name + '/recent_releases')
 q.add_header('accept', 'application/json')
 q.add_header('X-API-Token', args.token)
 versions_response = urllib.urlopen(q)
 versions = json.load(versions_response)
 latest_id = str(versions[0]['id'])

# Call to retrieve latest release details
 q = urllib.Request('https://api.appcenter.ms/v0.1/apps/' + args.owner_name + '/' + args.app_name + '/releases/' + latest_id)
 q.add_header('accept', 'application/json')
 q.add_header('X-API-Token', args.token)
 details_response = urllib.urlopen(q)
 details = json.load(details_response)
 download_url = details['download_url']

# Call to download app
 urllib.urlretrieve(download_url, args.app_name + '.' + extension)
