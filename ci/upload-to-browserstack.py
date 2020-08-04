#!/usr/bin/env python3

import json
import argparse
import requests
import os
from requests.auth import HTTPBasicAuth
from requests.exceptions import RequestException
import sys
import backoff
import time


class HSBCProxyErrorException(Exception):
    """
    Exception to signal known HSBC proxy error
    """
    pass


def hsbc_proxy_issue_find_and_raise(content, status_code):
    """
    This function looks for very specific errors caused by the proxy, allowing for
    retries based on proxy issues outside of the in-place retries for all other issues.
    There are 2 issues that have popped up, daily, for the past weeks that this function
    filters and raises for retry - after a tuned sleep time.
    Known issues caught to retry on:
    1) ICAP operation - something went wrong with content filters
    2) Account is locked out - Still investigating this but 60s sleep time before retry gets us past this one
    """
    filter_text = \
        'For assistance, please contact your Local IT Support Desk regarding this message, ' \
        'relevant telephone/email details are available below.'
    if filter_text in content:
        if status_code == 503 and 'ICAP operation' in content:
            time.sleep(30)  # If ICAP protocol encountered sleep 30s
        elif status_code == 403 and 'Account is locked out.' in content:
            """
            60s sleep was chosen here to wait for the account lockout to unlock.
            Combined with backoff and max_retries=5, the total time this can try is 60s * 5 plus exponential backoff
            Once info has been gathered this param can be tuned further to minimize script execution time.
            """
            time.sleep(60)  # If account is locked out a usual wait time of 60s is required (based on tests)
        raise HSBCProxyErrorException


def raise_or_json(response):
    if not response.ok:
        if isinstance(response.content, (bytes, bytearray)):
            content = response.content.decode()
        else:
            content = response.content
        hsbc_proxy_issue_find_and_raise(content, response.status_code)  # filter out known proxy issues
        raise RuntimeError(
            f'JSONDecodeError or unexpected return caused failure uploading app. Browserstack returned: {content}'
        )
    return response.json()


# on_exception decorator is used to retry using exponential backoff when any requests exception is raised
# max_tries specifies the maximum number of calls to make to the target function before giving up
@backoff.on_exception(backoff.expo, RequestException, max_tries=10)         # retry for connection failure
@backoff.on_exception(backoff.expo, HSBCProxyErrorException, max_tries=10)  # retry for known proxy issues
def do_upload(app_id):
    upload_url = 'https://api-cloud.browserstack.com/app-automate/upload'
    response = requests.post(
        url=upload_url,
        files=dict(file=open(app_id, 'rb')),
        verify=False,
        auth=HTTPBasicAuth(os.getenv('BROWSERSTACK_USR'), os.getenv('BROWSERSTACK_PSW'))
    )
    json = raise_or_json(response)
    return json['app_url']


def parse_args():
    parser = argparse.ArgumentParser(prog=sys.argv[0], description="Upload an app to BrowserStack")
    parser.add_argument('--app-id', metavar='app_id', nargs='?', default='0', help='Name of the app')
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    app_url = do_upload(args.app_id)
    print(app_url)
