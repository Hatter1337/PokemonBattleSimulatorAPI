#!/bin/sh

sam build

sam local start-api \
  --profile {your-aws-profile} \
  --container-host host.docker.internal \
  --skip-pull-image \
  --host 0.0.0.0 \
  --port 8000 \
  --container-host-interface 0.0.0.0