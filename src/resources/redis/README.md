# Redis
In this project, **[Redis](https://redis.io/)** is used to demonstrate caching techniques.

Deployed within an **EC2** instance via a `Dockerfile`, **Redis** serves as a dynamic cache to enhance the efficiency of data retrieval for frequently accessed information. 
This setup showcases how **Docker** can be leveraged to deploy database services, providing a hands-on example of containerization in action.

## Build and Push the Docker Image to ECR:
- Retrieve an authentication token and authenticate your Docker client to your registry. Use the AWS CLI:
  - `aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin {aws_account_id}.dkr.ecr.us-east-2.amazonaws.com`
- Build the Docker image:
  - `docker build --platform linux/amd64 -t pokemon-battle-similator-redis .`
- After the build completes, tag your image so you can push the image to this repository:
  - `docker tag pokemon-battle-similator-redis:latest {aws_account_id}.dkr.ecr.us-east-2.amazonaws.com/pokemon-battle-similator-redis:latest`
- Run the following command to push this image to your newly created AWS repository:
  - `docker push {aws_account_id}.dkr.ecr.us-east-2.amazonaws.com/pokemon-battle-similator-redis:latest`

## Deploy Redis to EC2 using CloudFormation:
```
aws cloudformation deploy \
  --stack-name pokemon-battle-similator-redis \
  --template-file resources/redis/redis.yaml \
  --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
  --region us-east-2 \
  --parameter-overrides \
    RedisPassword={redis-password}
```

## Connect to Redis:
- `redis-cli -h {ec2-elastic-ip} -p 6379 -a {redis-password}`