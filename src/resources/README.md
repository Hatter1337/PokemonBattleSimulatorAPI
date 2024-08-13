Deploy application resources:
- **S3 Buckets** using CloudFormation (to Dev):
```
aws cloudformation deploy \
  --stack-name ede-demo-pokemon-sam-s3 \
  --template-file src/resources/s3.yaml \
  --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
  --region eu-central-1
```

- **DynamoDB tables** using CloudFormation (to Dev):
```
aws cloudformation deploy \
  --stack-name ede-demo-pokemon-dynamodb-dev \
  --template-file src/resources/dynamodb.yaml \
  --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
  --region eu-central-1
```
