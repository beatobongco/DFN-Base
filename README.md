# Fig-Flask-Nginx

Simple template for creating flask apps running behind gunicorn and nginx,
containerized in fig and docker.

This repo was created for learning purposes and for future reference.

## How to run

1. `fig build`
2. (run for development - Werkzeug) `fig up -d`
3. (run for prod - gunicorn) `fig -f fig-prod.yml up -d`

`fig logs web` Check out the logs of flask or gunicorn
`fig rm [container name]` When things go weird try removing container and then using `fig up` again.

## Explanation

### Dockerfile

```
FROM python:2.7-onbuild
```

A special image that copies your `requirements.txt` to `/usr/src/app` and the executes
`pip install requirements.txt`

```
COPY . /usr/src/app
WORKDIR /usr/src/app
RUN pip install -r requirements.txt
```

If you choose to use a python image without -onbuild you need to include the above.

`FROM` - which Docker image you will use

`COPY` [host path] [container path] - copies directory contents from host path to container path. Faster than ADD because ADD can be used to copy and extract zipped files from URLs

`WORKDIR`- set the pwd in the container

`RUN` - run stuff based on where you are (WORKDIR)

### fig.yml

We will use `fig.yml` for development.

`build: web`

This tells fig to build the `Dockerfile` inside the `/web` directory on your host machine.

```
  ports:
    - 80:1337
```

Exposes ports [host machine]:[container]. So `port 1337` inside the container will be exposed as `port 80` on your host machine.

```
  volumes:
    - web:/usr/src/app
```

Docker volumes are used to save and share data among containers.
We want our app to be inside a volume so that when we make changes to our Flask app, we don't need to fig build again.

[Learn more about volumes here](https://docs.docker.com/userguide/dockervolumes/)

`command: python app.py`

`command` tells fig to run a command (duh). What you should note is that this is influenced by your Dockerfile's `WORKDIR` or you can influence this by your fig.yml's `working_dir`

### fig-prod.yml

We will use this `.yml` file for production. Note that when we use `fig-prod.yml`, we will need to use `fig stop && fig start` for changes to the flask app to be reflected. This is because gunicorn needs to be restarted.

You'll notice there's a new service called `nginx`. This is our HTTP server for production.

```
nginx:
  image: nginx:latest
  ports:
    - 80:80
    - 443:443
  links:
    - web:web
  volumes:
    - nginx.conf:/etc/nginx/nginx.conf:ro
```

`image` - pulls a Docker image and uses it.

`links` - link to containers in another service. It actually writes the IP address of the target container to `etc/hosts/` of the current container so in this case, our nginx container will have the IP address of our web service which can be accessed at `http://web` and its port 5000 for example at `http://web:5000`

`volumes` - we'll put the configuration file for nginx in the correct place in our nginx container `/etc/nginx/nginx.conf` `:ro` means `read-only`

### Notes on fig

`fig up` basically runs your instructions in your `fig.yml` file i.e. creates the instances, volumes, command, workdir
`fig stop && start` - use this when the contents of your volumes are updated i.e. when using gunicorn and you updated your flask app
`fig -f yourfig.yml` - run different fig.yml files


