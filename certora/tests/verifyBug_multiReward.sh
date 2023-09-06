#!/bin/bash

# Apply a bug, run prover and restore original file
# Run from the root git directory. Run without bug's number parameter to not apply any patches
# Examples:
#    ./certora/tests/verifyBug_multiReward.sh participants 2
#    ./certora/tests/verifyBug_multiReward.sh participants 3 --rule initializeCalledOnce

if [ "$#" -lt 1 ]; then
    echo "Please provide the path as the first argument (either 'certora' or 'participants')."
    exit 1
fi

DIR_NAME="$1" # Capture the directory path from the first parameter
shift 1 # shift arguments to exclude the first one
MSG="[run] $@"

# Check if the next argument is a bug number
if [[ $1 =~ ^[0-9]+$ ]]
then
  FILE_NAME="bug$1_multiReward"
  shift 1 
  MSG="[prove ${DIR_NAME}/$FILE_NAME] $@"
fi

PATCH_PATH="certora/tests/${DIR_NAME}/${FILE_NAME}.patch"

# If the patch file exists than apply and restore a bug
if [ -f "$PATCH_PATH" ]; then
  git apply "$PATCH_PATH"
  certoraRun certora/conf/verifyRewardsController_multiReward_verified.conf --send_only --msg "${MSG}" "$@" # pass all other parameters to certoraRun
  git apply -R "$PATCH_PATH"
else
  # Run without patching 
  certoraRun certora/conf/verifyRewardsController_multiReward_verified.conf --send_only --msg "${MSG}" "$@" 
fi

