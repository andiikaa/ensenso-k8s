#!/bin/bash
docker buildx build \
  --platform linux/amd64 \
  -t registry.code.wabo.run/andre.kuehnert/enenso:latest \
  --push \
  .