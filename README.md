# Foodie

## Setup

1. `git clone https://github.com/dansheikh/foodie.git $HOME/Downloads/`
2. `git clone http://github.com/dansheikh/docks.git $HOME/Downloads/`
3. Within the "Sandbox" directory of the "docks" clone, execute: `docker build -t foodie -f ubuntu/Dockerfile .`
4. Start container (in daemon mode) with: `docker run --rm -t -d -P -p 5432:5432 -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -v $HOME/Downloads/foodie:/home/dev/Projects/foodie foodie`
5. Connect to running container with: `docker exec -u dev -it [container id] env TERM=xterm /bin/bash -l`
6. Launch application with: `/home/dev/Projets/foodie/app.py [options]`

_Note_: To view options run `/home/dev/Projects/foodie/app.py [-h | --help]`

## Minimum Requirements
* Python (Version 3.6.0)
* Python Libraries:
    * Requests (Version 2.12.4)