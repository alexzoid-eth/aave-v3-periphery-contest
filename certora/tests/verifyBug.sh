#!/bin/bash

# Apply a bug, run prover and restore original file
# Run from the root git directory. Run without parameter to not apply any patches
# Examples:
#    ./certora/tests/verifyBug.sh certora --rule initializeCalledOnce
#    ./certora/tests/verifyBug.sh participants 2
#    ./certora/tests/verifyBug.sh participants 3 --rule initializeCalledOnce

if [ "$#" -lt 1 ]; then
    echo "Please provide the path as the first argument (either 'certora' or 'participants')."
    exit 1
fi

DIR_PATH="$1" # Capture the directory path from the first parameter
shift 1 # shift arguments to exclude the first one

MSG="[run] $@"
FILE_NAME="original"

# Check if the next argument is a bug number, else set to 'original'
if [[ $1 =~ ^[0-9]+$ ]]
then
  FILE_NAME="bug$1"
  shift 1  # shift arguments to exclude the first one (which is now the bug number)
  MSG="[prove $FILE_NAME] $@"
fi

PATCH_PATH="certora/tests/${DIR_PATH}/${FILE_NAME}.patch"

# If the patch file exists for the given path and filename
if [ -f "$PATCH_PATH" ]; then
    git apply "$PATCH_PATH"
    certoraRun certora/conf/verifyRewardsController_verified.conf --send_only --msg "${MSG}" "$@" # pass all other parameters to certoraRun
    git apply -R "$PATCH_PATH"
else
    echo "Patch file not found at $PATCH_PATH"
    exit 1
fi