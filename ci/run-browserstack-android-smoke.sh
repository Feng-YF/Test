#!/bin/bash

./gradlew -Dplatform=android -Denv=cert -Dcountry=$1 -Dlocale=en -Dbrowserstack=true -Dtest.single=CukeWipTest -Dcucumber.options=" --tags @smoke-tests-${1}" test
