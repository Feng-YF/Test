#!/bin/bash

set -x -e

SCRIPTS_DIR=$(dirname "${BASH_SOURCE[0]}")

DOWNLOAD_DIRECTORY="$SCRIPTS_DIR/../bundle-to-test/ios"

mkdir -p "$DOWNLOAD_DIRECTORY"

curl https://build-mobile.systems.uk.hsbc/job/mobilex-global/job/mobilebanking-global-ios/job/develop/lastSuccessfulBuild/artifact/iOS/build/MobileXGlobalDebug.app.zip -o "$DOWNLOAD_DIRECTORY/simulator.zip"

unzip -a "$DOWNLOAD_DIRECTORY/simulator.zip" -d "$DOWNLOAD_DIRECTORY/"
