#!/bin/bash

eval "$(ssh-agent -s)" &&
ssh-add -k ~/.ssh/id_rsa &&
cd /home/ubuntu/ECommerce-API
git pull

source ~/.profile
echo "$DOCKERHUB_PASS" | docker login --username $DOCKERHUB_USER --password-stdin
sudo docker stop numberforth
sudo docker rm numberforth
sudo docker rmi ilfarro/forth
sudo docker run -d --name numberforth -p 5000:5000 ilfarro/forth:latest