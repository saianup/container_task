# Autonomous Container Entry using 2D LiDAR

## Overview

This project demonstrates a simple autonomous navigation strategy where a mobile robot detects a container entrance using a **2D LiDAR sensor**, enters the container, maintains its position inside, reaches the back wall, and exits safely.

The entire system is implemented and tested in **ROS2 + Gazebo Classic simulation**.

The goal of the project is to show how **minimal perception and control logic** can solve a structured navigation problem efficiently.



# Approach Summary

The robot uses only **2D LiDAR data** for perception and navigation.

The navigation logic is based on three simple observations from the LiDAR scan:


Left wall distance
Right wall distance
Front obstacle distance


### 1. Detecting the Container Entrance

Before entering the container, the environment is open.


Left distance ≈ infinite
Right distance ≈ infinite


As the robot approaches the container:


Left distance < threshold
Right distance < threshold


This indicates that the robot has detected the container walls and has entered the container.



### 2. Centering Inside the Container

Once inside the container, the robot keeps itself centered by maintaining equal distance from the left and right walls.

Control rule:


error = left_distance − right_distance
angular_velocity = −k * error


This simple proportional controller keeps the robot aligned with the center of the container while moving forward.



### 3. Detecting the Back Wall

The robot monitors the **front LiDAR distance**.


front_distance < threshold


This indicates the robot has reached the end of the container.

The robot then stops forward motion and begins reversing.



### 4. Exiting the Container

While reversing, the robot continues applying the same centering controller so it does not drift into the walls.

The robot determines it has exited when:


left_distance > threshold
right_distance > threshold


which indicates the container walls are no longer detected.

The robot then stops.



# Why 2D LiDAR?

A **2D LiDAR sensor** was chosen because:

* It provides sufficient information to detect walls and obstacles.
* It has lower computational cost compared to depth cameras.
* It is widely used in indoor robotics navigation.
* It enables a simple yet effective wall-following and centering strategy.

For a structured environment such as a container, **2D LiDAR alone is sufficient** to perform the task reliably.



# Implementation

The system consists of:

* **ROS2 (Humble)**
* **Gazebo Classic Simulation**
* **Custom AGV Robot Model**
* **2D LiDAR Sensor**
* **Python Navigation Node**



# Running the Simulation

### Terminal 1 – Launch Gazebo and Robot

```
ros2 launch agvrobot_description gazebo.launch.py
```



### Terminal 2 – Spawn the Container

```
ros2 run gazebo_ros spawn_entity.py
-file models/container/model.sdf
-entity container
-x 2 -y 0 -z 0
```



### Terminal 3 – Run the Navigation Node

```
python3 scripts/container_nav.py
```



# Expected Behaviour

The robot performs the following sequence:

1. Detects the container entrance
2. Enters the container
3. Centers itself between the walls
4. Moves forward until reaching the back wall
5. Reverses while maintaining alignment
6. Exits the container safely


# Demo

A demonstration video of the simulation can be found here:

**Video Link:**  
*(https://drive.google.com/file/d/11z1NkD_0yGiVycNIChGAIkqbu_-ecgPK/view?usp=sharing)*


# Key Advantages of the Approach

* Simple and robust
* Requires only a single sensor
* Low computational complexity
* Works reliably in structured environments
* Easy to implement and reproduce

