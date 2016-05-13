#!/bin/bash

# Updates the first line of config with the version number
# Run this after a commit where the commit ID should be updated.
CURRENT_VERSION="v0.1.0a-"
HASH="$(git log --pretty=format:'%h' -n 1)"
sed -i "1s/.*/__DataSTORM_Version__ = \'$CURRENT_VERSION${HASH}\'/" DataSTORM/config.py
git add DataSTORM/config.py
git commit -m "Update git hash tracking."
