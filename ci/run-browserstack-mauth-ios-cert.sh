#!/bin/bash

./gradlew -Dplatform=ios -Denv=certOne -Dcountry=india -Dlocale=en -Dbrowserstack=true -Dtest.single=CukeWipTest -Dcucumber.options='--tags @bs-mauth' test --tests CukeWipTest
