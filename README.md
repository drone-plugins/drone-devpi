# drone-devpi

[![Build Status](http://beta.drone.io/api/badges/drone-plugins/drone-devpi/status.svg)](http://beta.drone.io/drone-plugins/drone-devpi)
[![](https://badge.imagelayers.io/plugins/drone-devpi:latest.svg)](https://imagelayers.io/?images=plugins/drone-devpi:latest 'Get your own badge on imagelayers.io')

Drone plugin for publishing Python packages to a [devpi](http://doc.devpi.net/) index.

## Local Development

Set up [drone-cli](https://github.com/drone/drone-cli) and use it to run through ``.drone.yml``, much like Drone itself will:

```sh
drone exec
```

## Docker

Build the container using `make`:

```sh
make docker
```

### Example

```sh
docker run -i plugins/drone-devpi <<EOF
{
    "repo": {
        "clone_url": "git://github.com/drone/drone",
        "owner": "drone",
        "name": "drone",
        "full_name": "drone/drone"
    },
    "system": {
        "link_url": "https://beta.drone.io"
    },
    "build": {
        "number": 22,
        "status": "success",
        "started_at": 1421029603,
        "finished_at": 1421029813,
        "message": "Update the Readme",
        "author": "johnsmith",
        "author_email": "john.smith@gmail.com"
        "event": "push",
        "branch": "master",
        "commit": "436b7a6e2abaddfd35740527353e78a227ddcb2c",
        "ref": "refs/heads/master"
    },
    "workspace": {
        "root": "/drone/src",
        "path": "/drone/src/github.com/drone/drone"
    },
    "vargs": {
        "server": "http://devpi.example.com:3141/",
        "index": "guido/myindex",
        "username": "guido",
        "password": "secret"
    }
}
EOF
```
