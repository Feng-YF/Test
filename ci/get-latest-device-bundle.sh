#!/bin/bash

set -x -e

SCRIPTS_DIR=$(dirname "${BASH_SOURCE[0]}")

BUNDLE_EXTENSION="ipa"
DOWNLOAD_DIRECTORY="$SCRIPTS_DIR/../bundle-to-test/ios"
JENKINS_JOB="job/mobilex-global/job/mobilex-global-ios/job/develop"

mkdir -p "$DOWNLOAD_DIRECTORY"



curl "https://build-mobile.systems.uk.hsbc/$JENKINS_JOB/lastSuccessfulBuild/artifact/*zip*/archive.zip" -o "$DOWNLOAD_DIRECTORY/device.zip"

unzip -a "$DOWNLOAD_DIRECTORY/device.zip" -d "$DOWNLOAD_DIRECTORY/"

APP_BUNDLE=`find "$DOWNLOAD_DIRECTORY" -name *.${BUNDLE_EXTENSION} | head -n 1`

mv $APP_BUNDLE "$DOWNLOAD_DIRECTORY/$(basename $APP_BUNDLE)"
