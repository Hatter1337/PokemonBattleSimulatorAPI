# Data Lambda Layer

Data Layer designed to facilitate interaction with caching solutions, offering two clients: 
- one for [Redis](https://redis.io/) and another 
- for [Amazon DynamoDB](https://aws.amazon.com/dynamodb/).

This architectural choice enables a direct comparison between **Redis's** in-memory caching capabilities and the robust, 
scalable data storage provided by **DynamoDB**. 

For scenarios demanding even quicker data access within **DynamoDB**, I consider the **[DynamoDB Accelerator (DAX)](https://aws.amazon.com/dynamodb/dax/)** an essential enhancement. 
**DAX** introduces in-memory caching to significantly expedite read operations.

It's important to mention that while database-level caching can lead to noticeable performance boosts, AWS provides an alternative caching mechanism through **[API Gateway](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-caching.html)**. 
This approach can optimize response times by caching end-point responses, potentially making the implementation of specific caching clients redundant.