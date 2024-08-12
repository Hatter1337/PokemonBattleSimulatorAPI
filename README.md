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