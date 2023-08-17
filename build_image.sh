#!/bin/bash

set -e
docker build -t jck53416/eq-mock-api:latest .
docker push jck53416/eq-mock-api:latest