#! /bin/bash

IMG_TAG="eq-mock-api"

docker build -t $IMG_TAG .
docker run -d -p 8000:8000 $IMG_TAG