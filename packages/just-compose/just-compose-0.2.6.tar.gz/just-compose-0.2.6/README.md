## Just Compose

A script to run the entire pipeline.

### Installation

```bash
pip3 install just_compose
jcompose --help # Should print something
```

### How to deploy crow

```bash
# This repo implements health checks
cd ~/crow2/src
git clone https://gitlab.ciirc.cvut.cz/hajekric/observations

# Rebuild
cd ~/crow2
colcon build --symlink-install

# This repo contains example configurations
cd ~/
git clone https://gitlab.ciirc.cvut.cz/hajekric/just-compose.git
cd examples
jcompose just-compose_ros.yaml # Should start the pipeline
```

### How to write a service

If you don't have your own, create `tutorial.yaml` with this content:

```yaml
pre:
  - cd ~/crow2
  - source /opt/ros/eloquent/setup.bash
  - source install/setup.bash

post:
  - echo "Job finished"

services:

  crow_vision_ros2:
    working_dir: ~/crow2
    command: ros2 launch crow_vision_ros2 all_cameras.launch.py
    tags: [ vision, camera ]
```

1. Figure out the following
 - Service name ( for identification, must be unique )
 - Command(s) to run the service
    - Make sure to also find out the working dir of the service
 - If you want healtcheck:
    - Find out what is the name of your ROS node
2. Insert the following into the config file, into the **`services` part**

```yaml
   <service_name>:
     working_dir: <working_dir>
     command: <command>
     healthcheck: ros2 run observations check_alive -n <node_name> # Ignore this line if you dont have a health check
     tags: [<tag1>, <tag2>] # Ignore this line if you dont have any tags ( alternative names )
```

3. You may now run this service with `jcompose tutorial.yaml --jobs <service_name>` or `jcompse tutorial.yaml --jobs <any of the tags>`

### Technical details

#### YAML

The main configuration file contains the following structure:

```yaml
pre:
  - echo This hook runs before each job and each healthcheck

post:
  - echo This hook runs after each job

services:
  
  crow_vision_ros2: # The name of the service. Is used for printing and identification
    working_dir: ~/crow2 # Command is `cd`-ed to this directory before execution
    command: ros2 launch crow_vision_ros2 all_cameras.launch.py # The service command
    tags: [ vision ] # Tags used for identification

  crow_object:
    working_dir: ~/crow2
    commands:
      - echo Multiline commands are also available
      - ros2 launch crow_vision_ros2 crow_object.launch.py
    tags: [ vision ]

  ...

```