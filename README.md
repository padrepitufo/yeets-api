# YEETS API

Provides API endpoint and also provides CLI interface for yeets. This service
serves as an interface for the corresponding database.

## Building locally

Building supports specific targets for desired environment

```commandLine
docker build . -t api --target development
```

## API endpoints

Upon building the api is immediately available like so

```commandLine
docker-compose up
# and then flushed with
# docker-compose down
# docker volume rm yeets-api_api_db_vol
# docker-commpose build
# docker-compose up
```

You may access the API documentation from the swagger/open-api docs
that FastAPI generated probably here `http://localhost:8081/docs`

## CLI commands

Upon building the cli is immediately available like so

```commandLine
docker run -it api jane <commands>
```

## Running with local docker

```commandLine
docker run -it -p 127.0.0.1:8081:8000/tcp api
```

## Deploy to Prod

```
kubectl create ns develop
kubectl apply -f manifests/
```

## Port Forward

```
k -n develop port-forward deploy/yeetsapi 7070:8000
```
