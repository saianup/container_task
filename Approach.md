# Approach and Methodology

## Problem Overview

The task is to autonomously guide a mobile robot into a shipping container, navigate inside it while maintaining a safe distance from the walls, reach the back wall, and exit the container.

The robot operates using **minimal sensing and computation**, relying only on **2D LiDAR data** for perception and a simple motion control strategy for navigation.

The solution was implemented and validated in **ROS2 and Gazebo Classic simulation**.

---

# Sensor Selection

## Why 2D LiDAR?

The environment in this task is **structured and geometrically simple**: a rectangular container with flat walls.

For such environments, a **2D LiDAR sensor provides sufficient information** to detect obstacles and estimate wall distances.

Advantages of 2D LiDAR include:

* Direct measurement of obstacle distance
* Low computational overhead
* Robust performance in low-texture environments
* Simpler data processing pipeline

The LiDAR scan directly provides the distance to surrounding obstacles in a horizontal plane, which is exactly the information required for wall detection and alignment.

---

## Why Not Depth Cameras?

Depth cameras provide dense 3D information, but they introduce several challenges:

### 1. Larger Data Size

Depth images contain thousands of pixels per frame.

Example:


640 × 480 depth image = 307,200 data points


In contrast, a typical 2D LiDAR scan contains only:


360 – 720 distance samples


This significantly reduces processing complexity.

---

### 2. Higher Processing Requirements

Depth camera data usually requires additional steps such as:

* point cloud generation
* filtering
* segmentation
* plane detection

These operations increase computational cost and latency.

For a simple wall-following task inside a container, such complexity is unnecessary.

---

### 3. Reliability in Structured Environments

Depth cameras may suffer from:

* reflective surfaces
* poor lighting conditions
* missing depth values

LiDAR sensors provide **more consistent range measurements**, making them better suited for this application.

---

# Perception Strategy

The robot extracts three key measurements from the LiDAR scan:


Left wall distance
Right wall distance
Front obstacle distance


These values are obtained by averaging small angular sectors of the LiDAR scan.

Example scan regions:


Left → 70% – 80% of scan
Right → 20% – 30% of scan
Front → center of scan


Averaging multiple beams improves measurement stability and reduces noise.

---

# Container Entrance Detection

Before reaching the container entrance, the robot operates in an open environment.

Therefore:


Left distance ≈ large value
Right distance ≈ large value


When the robot reaches the container opening, both walls become visible.

Entrance condition:


left_distance < threshold
AND
right_distance < threshold


This indicates that the robot has entered the container corridor.

---

# Centering Inside the Container

Once inside the container, the robot must remain centered between the two walls.

This is achieved by computing a **lateral error**:


error = left_distance − right_distance


If the robot is closer to the left wall:


left_distance < right_distance
error < 0


The robot then steers slightly to the right.

If the robot is closer to the right wall:


left_distance > right_distance
error > 0


The robot steers slightly to the left.

---

# Motion Control Strategy

A **Proportional (P) Controller** is used for heading correction.

Control law:


angular_velocity = -k * error


Where:


k = proportional gain


This controller was chosen because:

* The environment is static and predictable
* Only small heading corrections are required
* The robot moves at relatively low speeds
* The control objective is simple wall-centering

Using only a P controller keeps the system:


simple
stable
computationally efficient


Integral and derivative terms are unnecessary for this task.

---

# Back Wall Detection

The robot detects the end of the container using the front LiDAR measurement.

When the robot approaches the back wall:


front_distance < back_wall_threshold


The robot then switches from forward motion to reverse motion.

---

# Container Exit Detection

While reversing, the robot continues applying the centering controller to avoid drifting into the walls.

The robot determines it has exited the container when the walls disappear again:


left_distance > threshold
AND
right_distance > threshold


This indicates the robot has returned to the open environment.

At this point, the robot stops.

---

# Advantages of the Proposed Approach

The proposed solution provides several practical advantages:

### Simplicity

The algorithm relies only on simple geometric relationships between wall distances.

No complex perception algorithms are required.

---

### Computational Efficiency

The entire control strategy uses only a few LiDAR measurements and a proportional controller, making it suitable for real-time execution even on low-power hardware.

---

### Robustness

The method is robust in structured environments because:

* container walls provide clear geometric features
* LiDAR measurements are stable
* the control law continuously corrects heading deviations

---

# Limitations

The current approach assumes:

* a structured environment
* static walls
* a straight container corridor

In more complex environments, additional perception and navigation methods such as SLAM or path planning would be required.

---

# Conclusion

This project demonstrates that **simple perception and control strategies can effectively solve structured navigation problems**.

By using only:


2D LiDAR
simple wall-distance measurements
a proportional controller


the robot is able to:


detect the container entrance
enter the container
maintain a centered trajectory
reach the back wall
exit safely


The approach highlights how minimal sensing and control can achieve reliable autonomous navigation in constrained environments.
