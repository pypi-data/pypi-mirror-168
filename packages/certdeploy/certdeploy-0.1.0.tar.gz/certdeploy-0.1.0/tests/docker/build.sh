#!/bin/bash

HERE=$(dirname $0)
DOCKER_TEST_ROOT=$(realpath $HERE)

set -ex

pushd $DOCKER_TEST_ROOT

docker-compose stop
docker-compose rm
docker-compose build

popd
