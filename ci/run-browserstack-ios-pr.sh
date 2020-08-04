#!/bin/bash

./gradlew -Dplatform=ios -Denv=cert -Dcountry=canada -Dlocale=en -Dbrowserstack=true -Dtest.single=CukeWipTest -Dcucumber.options='--tags @pr-tests' test