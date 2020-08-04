#!/usr/bin/env bash
set -e
top=$(dirname $0)
python3 -m venv ${top}/venv

${top}/venv/bin/python3 ${top}/venv/bin/pip3 install -q requests backoff

PYTHONWARNINGS="ignore:Unverified HTTPS request" $(dirname $0)/venv/bin/python $(dirname $0)/run-browserstack-parallel.py "$@"
