#!/bin/bash
# Publish the latest build as the current git tag or the value of the
#   environment variable $TAG

set -e

IMAGE_PREFIX="haxwithaxe/certdeploy"
TAG=${1:-${TAG:-$(git tag --points-at HEAD)}}

if [[ -z $TAG ]]; then
	echo No tag set. Either set the \$TAG environment variable or add a tag to HEAD. 1>&2
	exit 1
fi

echo Tagging ${IMAGE_PREFIX}-server as $TAG
docker image tag ${IMAGE_PREFIX}-server:latest ${IMAGE_PREFIX}-server:$TAG
echo Pushing ${IMAGE_PREFIX}-server latest and $TAG
docker image push ${IMAGE_PREFIX}-server:latest
docker image push ${IMAGE_PREFIX}-server:$TAG

echo Tagging ${IMAGE_PREFIX}-client as $TAG
docker image tag ${IMAGE_PREFIX}-client:latest ${IMAGE_PREFIX}-client:$TAG
echo Pushing ${IMAGE_PREFIX}-client latest and $TAG
docker image push ${IMAGE_PREFIX}-client:latest
docker image push ${IMAGE_PREFIX}-client:$TAG
