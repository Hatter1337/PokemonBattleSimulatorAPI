## Deploy DynamoDB tables using CloudFormation:
```
aws cloudformation deploy \
  --stack-name ede-demo-pokemon-dynamodb-dev \
  --template-file src/resources/dynamodb/dynamodb.yaml \
  --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
  --region eu-central-1
```
