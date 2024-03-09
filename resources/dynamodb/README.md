Deploy DynamoDB tables using CloudFormation:
```
aws cloudformation deploy \
  --stack-name pokemon-battle-similator-dynamodb-dev \
  --template-file resources/dynamodb/dynamodb.yaml \
  --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
  --region us-east-2
```
