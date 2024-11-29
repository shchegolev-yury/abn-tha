#/bin/bash

if [ "$#" -ne 4 ]; then
  echo "Usage: $0 <repo_name> $1 <image_tag> $2 <project_name> $3 <environment>"
  exit 1
fi

REPO_NAME=$1
IMAGE_TAG=$2
PROJECT_NAME=$3
ENVIRONMENT=$4

ansible-playbook deploy.yml -e repo=$REPO_NAME -e image_tag=$IMAGE_TAG -e project_name=$PROJECT_NAME -e environment=$ENVIRONMENT