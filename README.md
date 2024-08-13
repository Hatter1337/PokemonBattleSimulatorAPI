# PokemonBattleSimulatorAPI
![Python 3.12](https://img.shields.io/badge/python-3.12-green.svg) 
![SAM](https://img.shields.io/badge/SAM-v1.120.0-blue.svg)
![Powertools for AWS Lambda](https://img.shields.io/badge/Powertools%20for%20AWS%20Lambda-v2.43.0-blue.svg)

REST API written in Python, powered by **[AWS SAM](https://aws.amazon.com/serverless/sam/)** and **[Powertools for AWS Lambda](https://docs.powertools.aws.dev/lambda/python/latest/)**.

**SAM** template file is located in the root directory: `template.yaml` together with configuration file `samconfig.toml`.

**PokemonBattleSimulatorAPI** is a lightweight and efficient REST API designed to simulate Pokémon battles, 
deployed on AWS using Serverless Application Model (SAM) and enhanced with AWS Lambda Powertools. 
Leveraging data from **[PokéAPI](https://pokeapi.co/)**, it calculates battle outcomes based on Pokémon stats like HP, Attack, Defense, and Speed. 
This project demonstrates serverless architecture, offering scalable and cost-effective solutions for real-time Pokémon battle simulations.

**Note:** `swagger.yml` and Postman collection are located in the `/doc` directory.

## Project structure
- `/docs` - API documentation with swagger file
- `/src` - Source code
  - `/lambda` - Code base related to Lambda functions
    - `/functions` - Lambda functions
      - `/{name}` - Specific Lambda function with `handler.py` 
    - `/tests` - Unit tests for all Lambda functions
  - `/layers` - Code base related to Lambda layers
    - `/{name}_layer` - Lambda layer with `requirements.txt` and common code 
    - `/tests` - Unit tests for all Lambda layers
  - `/resources` - AWS resources configuration with CloudFormation
  - `template.yaml` - SAM template file with API resources: API Gateway, Lambda functions, etc.
  - `samconfig.toml` - SAM configuration file with environment variables and parameters
  - `docker-compose.yaml` - Docker Compose configuration for local development
  - `run-local-api.sh` - Script to run SAM application locally in Docker

## Deploy to your AWS account
- First of all, you need to have an AWS account and AWS CLI installed on your machine.
- Clone this repository and navigate to the root directory.
- Rename S3 bucket in the `/src/resources/s3.yaml` and `samconfig.toml` (lines: 18, 30), because S3 Bucket names must be unique.
- Create AWS resources from `/src/resources` directory using AWS CLI and CloudFormation (details in `src/resources/README.md`).
- Deploy Serverless application using **SAM CLI**:
```bash
$ sam build
$ sam deploy --config-env dev --profile {your-aws-profile}
```

## Run locally using **SAM**:
- Configure your AWS CLI with the necessary credentials, for your AWS profile, before running SAM commands.
- Ensure Docker is running for `sam local start-api` to simulate the Lambda environment.
- Run the following commands to build and start the API locally:
```bash
$ sam build
$ sam local start-api --port 8000 --profile {your-aws-profile}
```

You also can use Dokcer Compose to run the application locally:
- Change the AWS profile name in `run-local-api.sh`.
- Grant execution rights to the script: `$ chmod +x run-local-api.sh`
- `$ docker-compose up`
