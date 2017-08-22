#!/bin/bash

export APPSERVER_CFG=./runtime/config/dev
export TEST_VARIABLE=exists

echo "Beginning test execution..."
echo ""

if coverage run --include="./src/*" -m unittest discover src; then
  coverage report -m
else
  exit 1
fi