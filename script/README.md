# Running a shell script inside a pod

## Create the script
Important using alpine docker image:

The script needs start with **#!/bin/sh** (instead of #/bin/bash).


## Build and load the docker image to kind nodes
```sh
cd script/
docker build -t adolfomaltez/script .
```

# Optional if using kind: Load docker image to nodes
```sh
kind load docker-image adolfomaltez/go-web-app:latest --name cluster
```

## Deploy the script pod inside the kubernetes cluster
```sh
kubectl apply -f deployment.yaml
```