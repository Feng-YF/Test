#!/bin/bash

./gradlew -Dplatform=android -Denv=cert -Dcountry=india -Dlocale=en -Dbrowserstack=true -Dcucumber.options='--tags @bs-mauth' test --tests CukeWipTest

