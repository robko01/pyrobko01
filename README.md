# Intro
Robko01 API library
This document is devoted to the way client software is installed, which communicates with the robot controller.

# Installation

## Environment

 - For better experience is good to have git client. This will will alow you to install easy from github this library. The link to the [git client](https://git-scm.com/download/win).

 - This script is written in Python 3.8.5. To [download](https://www.python.org/downloads/) it please visit official site of the Python and download [3.8.5](https://www.python.org/ftp/python/3.8.5/python-3.8.5.exe)


## Create a virtual environment (Optional)
 - Make virtual environment
```sh
python -m venv .venv
```

 - For Windows machines
```sh
.venv/bin/activate
```
 - For Linux or macOS machines:
```sh
source .venv/bin/activate
```

## Update the environment
 - Update the pip system
```bash
python -m pip install --upgrade pip 
```

## Install the library
 - Install the repository from link
```sh
python -m pip install git+https://github.com/robko01/pyrobko01.git#egg=robko01
```
 - You are ready for the first run.

## Install the library manually (optional)
 - Download the repository from [link](git+https://github.com/robko01/pyrobko01)

 - Install setuptools
```sh
python -m pip install setuptools
```

 - Unzip the downloaded repo.
 - Navigate to the unziped folder in terminal.
 - Install the package
```sh
python setup.py install
```
 - You are ready for the first run.

## First run
After installation, the script is ready for operation. This happens in the following way.

 - For Windows machines:
```sh
python -m robko01 --port COM<NUMBER> --task task_ui_qt
```
or
```sh
python -m robko01 --port COM<NUMBER> --task task_ui_tk
```

 - For Linux machines:
```sh
python3 -m robko01 --port /dev/ttyUSB<NUMBER> --task task_ui_qt
```
 - For macOS machines:
```sh
python3 -m robko01 --port /dev/cu.usbserial-1110 --task task_ui_qt
```

 - To approach the robot, it will be presented to the computer as a serial port.
 - The example is marked `COM5`, `/dev/ttyUSB0` or `/dev/cu.usbserial-1110`.
 - You need to find out which is the correct port for you by using the device manager.
 - The argument `--task` serves to indicate which program to execute the robot.

# Examples

## Example 1

In this example we will:

 - Create a controller.
 - Connect to the robot.
 - Do a simple motion.

```py
#!/usr/bin/env python
# -*- coding: utf8 -*-

from robko01.controllers.controller_factory import ControllerFactory

port = "COM1" # You should change it according to your setup.
cname = "orlin369"

# Controller
controller = ControllerFactory.create(port=port, cname=cname)

# Set the speed.
speed = 150

# Trajectory path.
trajectory = [ \
    [450, 0, 600, 0, -400, 0, 200, 0, -200, 0, 400, 0], \
    [0, 0, 0, 0, 0, 0, 110, 0, 110, 0, 0, 0], \
    [0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -100, 0], \
    [0, 0, -100, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
    [-900, 0, 0, 0, 0, 0, -200, 0, -200, 0, 0, 0], \
    [0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 100, 0], \
    [0, 0, -100, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
    [0, 0, 0, 0, 0, 0, 110, 0, 110, 0, 0, 0], \
    [450, 0, -600, 0, 400, 0, -220, 0, 180, 0, -400, 0] \
    ]

# Run trough trajectory points.
for position in trajectory:
    current_point = scale_speeds(position, speed)            
    controller.move_relative(current_point)
    current_point = controller.current_position()

# Wait the controller to end its last movement.
controller.wait_to_stop()

```

## Uninstall the library
In case you would like to remove the library use the fllowing command.

 - For Windows machines:
```sh
python -m pip uninstall robko01
```

 - For Linux machines:
```sh
python3 -m pip uninstall robko01
```

 - For NacOS machines:
```sh
python3 -m pip uninstall robko01
```

# Contributing

If you'd like to contribute to this project, please follow these steps:

1. Fork the repository on GitHub.
2. Clone your forked repository to your local machine.
3. Create a new branch for your changes: `git checkout -b my-new-feature`.
4. Make your modifications and write tests if applicable.
5. Commit your changes: `git commit -am 'Add some feature'`.
6. Push the branch to your forked repository: `git push origin my-new-feature`.
7. Create a pull request on the main repository.

We appreciate your contributions!

# License

This project is licensed under the GNU License. See the [GNU](http://www.gnu.org/licenses/) file for more details.
