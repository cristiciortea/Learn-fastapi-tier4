#!/bin/bash

# ----------------------------------------------- function definitions ----------------------------------------------- #
: '
This function runs a command with a status check. It takes only one argument
that is a command itself or a function to be ran.
'
function run_cmd()  {
  # Gather arguments info
  arguments_number=${#}
  arguments_array=(" $@ ")

  # Check before running command
  echo ""
  if [ ${arguments_number} -gt 1 ]; then
    echo "[$(date -u +"%Y-%m-%d %H:%M:%S")]:[ERROR]: To many arguments given to the run_cmd function! It accepts only one."
    echo "[$(date -u +"%Y-%m-%d %H:%M:%S")]:[ERROR]: Number of arguments given: ${arguments_number}"

    # Show input args to the user
    for arg_nr in ${!arguments_array[*]}; do
      echo "ARG $((arg_nr+1)): ${arguments_array[arg_nr]}"

    done
    exit 1
  fi

  # Run given command and check status of ran command
  my_command=${1}
  echo "[$(date -u +"%Y-%m-%d %H:%M:%S")]:[ INFO]: Running command: ${my_command}"
  if ! output=$(${my_command}); then
    echo "[$(date -u +"%Y-%m-%d %H:%M:%S")]:[ERROR]: Command failed!: -->$1<--"
    echo "[$(date -u +"%Y-%m-%d %H:%M:%S")]:[ERROR]: Command output: ${output}"
  else
    echo "[$(date -u +"%Y-%m-%d %H:%M:%S")]:[ INFO]: Command ran successfully: -->$1<--"
    echo "[$(date -u +"%Y-%m-%d %H:%M:%S")]:[ INFO]: Command output: ${output}"
  fi
}

: '
This function builds fastapi application image using the Dockerfile located
in the docker folder. The image is built based on two environment variables
found in the .env file that are grabbed using grep combined with awk.
'
function build_fastapi_app_image() {
    local ENV_STATE
    local POETRY_VERSION
    ENV_STATE=$(grep ENV_STATE .env --max-count=1 | awk -F "=" '{print $2}' | awk '{print $1}')
    POETRY_VERSION=$(grep POETRY_VERSION .env --max-count=1 |  awk -F "=" '{print $2}')

    # docker build -t fastapi_learn:v0.4 . -f './docker/Dockerfile' --no-cache --build-arg ENV_STATE=dev --build-arg POETRY_VERSION=1.2.0
    # docker build -t fastapi-ltier2:v0.1 . -f './docker/Dockerfile' --network host --build-arg ENV_STATE=dev --build-arg POETRY_VERSION=1.2.0
    docker build -t fastapi-ltier2:v0.1 . -f './docker/Dockerfile' --network daskalos_default \
                                                                   --build-arg ENV_STATE="${ENV_STATE}"\
                                                                   --build-arg POETRY_VERSION="${POETRY_VERSION}"
}

: '
With this function you can start the fastapi container, but its recommended you start
it using docker-compose.
'
function start_fastapi_app() {
    docker run --name fastapi_learn -p 8000:8000 -d --rm -it fastapi_learn:v0.4 \
           /bin/bash -c 'poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000'
}

: '
This function can be used to kill all running docker containers.
'
function kill_docker_containers() {
    # shellcheck disable=SC2046
    docker kill $(docker ps -q)
}

: '
This function can be used to delete dangling images.
'
function remove_docker_dangling_images() {
    # shellcheck disable=SC2046
    docker container rm $(docker ps -a -q)
    # shellcheck disable=SC2046
    docker image rm $(docker images --filter "dangling=true" -q)
}

: '
This function builds the docker image app using docker-compose and the Dockerfile
stored in .
'
function build_app_using_docker_compose() {
    docker-compose -f docker/docker-compose.yml --env-file .env build --no-cache
}

: '
This function starts all the needed services for the application to run
using docker-compose.
'
function start_services_using_docker_compose() {
    docker-compose -f docker/docker-compose.yml --env-file .env --project-name fastapi-ltier2 up
}

# ------------------------------------------------------- main ------------------------------------------------------- #
run_cmd start_services_using_docker_compose
