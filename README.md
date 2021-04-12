# ros_experiments
This repository consists of 15* experiments that can be realized on ROS Melodic and Ubuntu 18.04. All 15 experiments are realized on HAMER robot.
HAMER Github: https://github.com/hamerrobots.

# Experiments

Content of experiments are given as follows; 

1. Sensor reading and visualization and control of Robot with Keyboard
2. Creating a Labyrinth Environment and Adding Objects
3. Making the Robot Move Square
4. Patrol Application
5. Enabling Robot to Avoid Obstacle with Bug 0 Algorithm
6. Wall Follower Robot Application
7. Voice Controlled Robot Application
8. SLAM and Navigation Application
9. Autonomous Generation of the Environment Map ( frontier_exploration)
10. Common Mapping for Multiple Robot Systems (map_merge)
11. Multiple Route Planning Application with Genetic Algorithm
12. Visual Extraction of the Environment Map (rtabmap_ros)
13. Object Recognition Application in the Environment (find_object_2d)
14. Object Recognition with YOLOv3
15. Lane follower robot application

# Experiment 1

The first experiment is constructed to demonstrate how to read sensor data from the robot. 
- Launch HAMER robot on any map.
> $ roslaunch hamer_simulation hamer_gazebo_emptyworld.launch
- Launch HAMER RViz file.
> $ roslaunch hamer_simulation hamer_rviz.launch 
- Use Add button which is on the down left side of the RViz screen to add any sensor data.
- Run the below command to control HAMER through keyboard.
> $ rosrun hamer_teleop hamer_teleop.py

# Experiment 2
The main purpose of this experiment is to create a labyrinth environment in gazebo and add
objects to the created environment.

- Click on the edit tab on the upper left of the Gazebo window and select the Building Editor.
- In the window that opens, the tab on the left shows the objects, colors and coatings we can
use. Add walls according to the labyrinth perimeter you want from the Create walls section.
- Add desired objects such as windows, doors and stairs from the Add Features section.
- You can see the drawing area on the right. The added objects are seen and edited in this
section. Clicking on an object can be moved to the right or left, new objects can be added and
existing objects can be removed. The scale of this area can be seen at the bottom left of the
drawing area. Adjust this scale to desired using the middle mouse button.
- To edit the created objects, right click on the object and select the edit object section and edit
the dimensions of the walls from here.
- After the previously designed model is transferred to the Gazebo environment using the
drawing area, exit from the drawing area from the file tab that appears at the top left of the
screen, and the file is saved to turtlebot3_gazebo / models address.
- After this process is completed, the created model is ready for use. Try adding it to any project
using the insert tab on Gazebo.
 
# Experiment 3
The main purpose of this experiment is to introduce the students to linear and angular
movements in ROS environment.
- Launch HAMER with hamer_gazebo_emptyworld.launch file.
> $ roslaunch hamer_gazebo_emptyworld.launch
- Use the below command on another terminal.
> $ rosrun hamer_experiments hamer_square.py

# Experiment 4
The main purpose of this experiment is to introduce the students to linear and angular
movements in ROS environment.

- Launch HAMER with hamer_gazebo_emptyworld.launch file.
> $ roslaunch hamer_gazebo_emptyworld.launch
- Use the below command on another terminal.
> $ rosrun hamer_experiments hamer_patrol.py

# Experiment 5
The purpose of this experiments is to realize an object avoidance program for Turtlebot3 using
Bug 0 Algorithm.

- Launch HAMER with hamer_gazebo_maze.launch file.
> $ roslaunch hamer_gazebo_emptyworld.launch
- Use the below command on another terminal.
> $ rosrun hamer_experiments hamer_bug0.py

# Experiment 6
In this experiment, student will write a node for the HAMER. The node must be designed as, the robot should follow the walls and the distance between wall and robot’s corners must be printed on terminal unless there is no interrupt on the program.


- Launch HAMER with hamer_gazebo_emptyworld.launch file.
> $ roslaunch hamer_gazebo_emptyworld.launch
- Use the below command on another terminal.
> $ rosrun hamer_experiments hamer_follow_wall.py

# Experiment 7
The main purpose of this experiment is creating a Python script to control the HAMER with voice control.

- Launch HAMER with hamer_gazebo_emptyworld.launch file.
> $ roslaunch hamer_gazebo_emptyworld.launch
- Use the below command on another terminal.
> $ roslaunch hamer_experiments voice_control.launch
