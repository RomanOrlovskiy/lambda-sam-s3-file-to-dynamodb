#!/bin/bash

if ! which sam ; then
  echo "sam not found"
  exit 1
fi

#if ! [ -n "$1" ] ; then
#    echo "Pass the directory with lambda application to be deployed as the first parameter"
#    exit 5
#fi
#
#cd $1

s3_bucket='rorlovskyi-lambda-sam-s3-file-to-dynamodb'
stack_name="s3-dynamodb"

set -x

if [ -d "tests" ]; then
    echo "Running tests ..."
    python3 -m pytest tests/ -v || exit $?
else
    echo "'tests' directory not found, skipping tests"
fi

echo "Building ..."
sam build || exit $?

echo "Packaging ..."
sam package \
  --output-template-file packaged.yaml \
  --s3-bucket $s3_bucket || exit $?

echo "Deploying ..."
sam deploy \
  --template-file packaged.yaml \
  --stack-name $stack_name \
  --capabilities CAPABILITY_IAM || exit $?