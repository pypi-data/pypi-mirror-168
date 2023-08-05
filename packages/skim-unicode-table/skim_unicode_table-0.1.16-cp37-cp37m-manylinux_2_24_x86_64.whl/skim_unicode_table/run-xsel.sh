#!/bin/bash

# get script's own location, which will also have all other executables
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

RUN_CMD="$SCRIPT_DIR/run.sh"

$RUN_CMD | awk '{ printf $1 }' | xsel -b
