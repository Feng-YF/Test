#!/bin/bash

./gradlew -Dplatform=android -Denv=cert -Dcountry=canada -Dlocale=en -Dbrowserstack=true -Dcucumber.options='--tags @pr-tests' test --tests CukeWipTest
