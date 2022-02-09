# API

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
docker run -it api
```

## CLI commands

Upon building the cli is immediately available like so

```commandLine
docker run -it api jane <commands>
```

## Running with local docker

```commandLine
docker run -it -p 127.0.0.1:8080:8000/tcp api
```
