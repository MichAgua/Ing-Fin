#!/bin/bash

if [ -n "$(git status --porcelain)" ]; then
  git add .
  git commit -m "Auto update"
  git push
else
  echo "No changes to commit."
fi