#!/bin/bash

set -x -e

SCRIPTS_DIR=$(dirname "${BASH_SOURCE[0]}")

DOWNLOAD_DIRECTORY="$SCRIPTS_DIR/../bundle-to-test/android"

mkdir -p "$DOWNLOAD_DIRECTORY"

cd "$DOWNLOAD_DIRECTORY" && { curl -O https://build-mobile.systems.uk.hsbc/job/mobilex-global/job/mobilebanking-global-android/job/develop/lastSuccessfulBuild/artifact/Android/app/build/outputs/apk/indiaCertSecure/debugProguard/india-cert-2.[1-50].0-secure-debugProguard.apk; cd -; }
