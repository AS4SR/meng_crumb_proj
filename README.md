# MEng project, University of Cincinnati 2018

## Summary
This repository contains the whole project "The Application of STRIPS Planning Using PDDL to a CRUMB Project Robot", being used for Master of Engineering capstone in AS4SR lab at University of Cincinnati.

## Recommended OS/Programs

The software was developed and tested in:
 - Ubuntu 16.04 LTS
 - ROS Kinetic
 - Gazebo 7.12
 
## Installation

To install the current version of this repository to your machine, cd into your catkin workspace source directory and clone the repository:

```
git clone https://github.com/sharon50270/meng_crumb_proj
``` 
## Run the PDDL in Python Planner in Gazebo

### Launch the Gazebo file under meng_crumb_project package first
First scenario:
```
roslaunch meng_crumb_project crumb.launch
```

Second and third scenario:
```
roslaunch meng_crumb_project crumb_1.launch
```

### Rosrun file to generate the planner

```
cd script
```
First scenario:
```
rosrun meng_crumb_project turtlebot_wp_1.py
```
Second scenario:
```
rosrun meng_crumb_project turtlebot_wp_2.py
```
Third scenario:
```
rosrun meng_crumb_project turtlebot_wp_3.py
```

### Publish messages to different topic names to have the CRUMB to perform desired motions
First scenario:
```
rosrun meng_crumb_project action_publisher_1.py
```
Second and third scenario:
```
rosrun meng_crumb_project action_publisher_2&3.py
```

### Hardware setup
```
roslaunch turtlebot_bringup minimal.lauch
```
http://learn.turtlebot.com/2015/02/01/9/
