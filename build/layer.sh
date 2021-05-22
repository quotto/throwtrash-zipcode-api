#!/bin/bash
set -eo pipefail
rm -rf ./package/*
if [ ! -e "./package" ]; then
    mkdir ./package
fi
cd ./function
PIP_TARGET="../package" pipenv sync