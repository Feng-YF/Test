#!/bin/bash
usage="$(basename "$0") [-h] [APPPATH] [AVAILABLEENVIRONMENTS (STRING ARRAY)] -- Script that will setup the entity bundle with necessary information.
It will set all the available environments inside the bundle.

where:
    -h  show the help text
    APPPATH - .app path
    AVAILABLEENVIRONMENTS - environments to setup as available on the bundle. {EX: mock, mock_api, sct, mct, cert, prod}"

while getopts 'h' option; do
  case "$option" in
    h) echo "$usage"
       exit
       ;;
  esac
done

APPPATH=$1; shift
AVAILABLEENVIRONMENTS=("$@")

echo "---------------------------------Set available environments on Bundles---------------------------------"

copyPlistArrayValuesForKey () {
    KEY=$1; shift
    OUTPUT=$1; shift
    ENVIRONMENTS=("$@")

    CNTSOURCE=0
	for i in "${ENVIRONMENTS[@]}"; do
		((CNTSOURCE++))
	done
	echo "number of values source = $CNTSOURCE"
	DESTINY=$(/usr/libexec/PlistBuddy -c "Print :$KEY" $OUTPUT)
	exitCodeDestiny=$?
	DESTINY=$($DESTINY | sed -e 1d -e '$d')
	CNTDESTINY=0
	if [ $exitCodeDestiny -eq 0 ]; then
		for i in "${DESTINY[@]}"; do
			((CNTDESTINY++))
		done
	fi
	/usr/libexec/PlistBuddy -c "Add :$KEY array" $OUTPUT

	echo "number of values destiny = $CNTDESTINY"
	STARTINDEX=$(($CNTDESTINY))
	FINALINDEX=$(($CNTDESTINY + CNTSOURCE))

	echo "StartIndex=$STARTINDEX    FinalIndex=$FINALINDEX"
	for (( i = $STARTINDEX; i < $FINALINDEX; i++ )); do
		/usr/libexec/PlistBuddy -c "Add :$KEY:$i string" $OUTPUT
		/usr/libexec/PlistBuddy -c "Set :$KEY:$i ${ENVIRONMENTS[$i]}" $OUTPUT
	done
}

if [ -z "$AVAILABLEENVIRONMENTS" ]; then
	echo "All environments will be available"
else
	for filename in $APPPATH/*.bundle; do
		echo $filename
		BUNDLEINFO="/$filename/Info.plist"
		/usr/libexec/PlistBuddy -c "Delete :availableEnvironments" $BUNDLEINFO
		copyPlistArrayValuesForKey "availableEnvironments" $BUNDLEINFO ${AVAILABLEENVIRONMENTS[@]}
	done
fi

echo "Completed"


