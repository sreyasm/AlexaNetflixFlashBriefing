#!/bin/bash
cd $(dirname $0)
rm -R deploy deploy.zip
mkdir deploy
cd deploy
pip install -r ../lambda-requirements.txt -t ./
cp ../lambda_function.py .
zip -r ../deploy.zip *
