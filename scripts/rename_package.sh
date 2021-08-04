#!/usr/bin/env bash
if [ -z "$1" ]
  then
    echo "Usage: rename.sh new_name"
    echo "Will rename the package to \"new_name\""
    exit 1
fi
# change working directory to project root
cd "$(dirname "$0")/.." || exit
# run rename script
python3 scripts/rename_package.py "$1"
