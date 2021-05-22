#!/bin/bash
set -eo pipefail
aws cloudformation package --template-file template.yml --s3-bucket $ARTIFACT_BUCKET --output-template-file out.yml
aws cloudformation deploy --template-file out.yml --stack-name throwtrash-zipcode-api --role-arn ${CFN_ROLE_ARN} --capabilities CAPABILITY_NAMED_IAM --profile lambda_deployer --region ap-northeast-1