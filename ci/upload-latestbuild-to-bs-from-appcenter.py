#!/usr/bin/env python3

import urllib as urllib
import urllib.request as request
import sys
import ssl
import json
import argparse
import requests
import os
from requests.auth import HTTPBasicAuth

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog=sys.argv[0], description='Upload an app to Browser Stack from App Center')
    parser.add_argument("--token", help='App Center API-Token with Full Access')
    parser.add_argument('--owner-name', metavar='owner_name', help='Owner Name provided in app center URL')
    parser.add_argument('--app-name', metavar='app_name', help='App Name provided in app center URL')

args = parser.parse_args()

def getLatestReleaseId() :
    requestUrl = f"https://api.appcenter.ms/v0.1/apps/{args.owner_name}/{args.app_name}/releases?published_only=true&scope=tester"
    requestCall = request.Request(requestUrl)
    requestCall.add_header('accept', 'application/json')
    requestCall.add_header('X-API-Token', args.token)
    versions_response = request.urlopen(requestCall)
    versions = json.load(versions_response)
    return str(versions[0]['id'])

def getDownloadUrlForRelease(latest_release_id) :
    requestUrl = f"https://api.appcenter.ms/v0.1/apps/{args.owner_name}/{args.app_name}/releases/{latest_release_id}"
    requestCall = request.Request(requestUrl)
    requestCall.add_header('accept', 'application/json')
    requestCall.add_header('X-API-Token', args.token)
    details_response = request.urlopen(requestCall)
    details = json.load(details_response)
    return details['download_url']

def uploadAppCenterAppToBrowserStack(download_Url,latest_release_id) :
    upload_url = f"https://api-cloud.browserstack.com/app-automate/upload"
    payload = f'{{"url": "{download_Url}", "custom_id": "{latest_release_id}"}}'
    response = requests.post(
                             url=upload_url,
                             data=dict(data=payload),
                             verify=False,
                             auth=HTTPBasicAuth(os.getenv('BROWSERSTACK_USR'), os.getenv('BROWSERSTACK_PSW'))
                            )
    if not response.ok:
            response.raise_for_status()
    return response.json()['app_url']

# Step calls to Upload app
latest_release_id = getLatestReleaseId()
download_Url = getDownloadUrlForRelease(latest_release_id)
app_Url = uploadAppCenterAppToBrowserStack(download_Url,latest_release_id)
print(app_Url)
