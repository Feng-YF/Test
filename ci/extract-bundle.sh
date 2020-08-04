#!/bin/bash

set -x -e

SCRIPTS_DIR=$(dirname "${BASH_SOURCE[0]}")
BUNDLE_EXTENSION=${1:-"app"}

BUNDLE_DIRECTORY="$SCRIPTS_DIR/../bundle-to-test/ios"

APP_BUNDLE_ARCHIVE=`find "$BUNDLE_DIRECTORY" -name *.${BUNDLE_EXTENSION}.zip | head -n 1`
unzip -a "$APP_BUNDLE_ARCHIVE" -d "$BUNDLE_DIRECTORY"
