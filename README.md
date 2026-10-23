=========================================
ASR700: Autonomous Systems and Robotics
=========================================

------------------------------------------------------------------------
1. SYSTEM & SOFTWARE REQUIREMENTS
------------------------------------------------------------------------
- Webots Version: Webots 2023b (or newer)
- Python Version: Python 3.10+ (Tested on Python 3.14)
- Hardware Requirements: 
    * Processor: Dual-core Intel/AMD x86-64 or modern ARM processor
    * Memory: Minimum 4 GB RAM
    * Graphics: OpenGL 3.3 compatible GPU

------------------------------------------------------------------------
2. PYTHON DEPENDENCIES
------------------------------------------------------------------------
The Python evaluation scripts require the following packages:
- pandas (for parsing CSV logs)
- matplotlib (for rendering 2D trajectory plots)

To install all dependencies, open your terminal or command prompt and run:
    pip install pandas matplotlib

------------------------------------------------------------------------
3. PROJECT DIRECTORY STRUCTURE
------------------------------------------------------------------------
ASR700_Assignment/
│
├── README.txt                             <-- Instructions file
├── ASR700_Final_Report.pdf                <-- Main assignment report
├── plot_trajectory.py                     <-- Matplotlib evaluation script
├── trajectory_evaluation.png              <-- Component A trajectory plot
├── swarm_trajectories.png                 <-- Component B trajectory plot
│
├── worlds/
│   └── ASR_world.wbt                      <-- Webots simulation arena
│
└── controllers/
    ├── Autonomous_navigation_controller/
    │   ├── Autonomous_navigation_controller.py
    │   └── robot_trajectory.csv           <-- Component A logged data
    │
    └── swarm_controller/
        ├── swarm_controller.py            <-- Component B swarm script
        ├── e-puck_1_trajectory.csv        <-- Swarm agent 1 trajectory dataset
        ├── e-puck_2_trajectory.csv        <-- Swarm agent 2 trajectory dataset
        └── e-puck_3_trajectory.csv        <-- Swarm agent 3 trajectory dataset

------------------------------------------------------------------------
4. INSTRUCTIONS TO RUN SIMULATION & GENERATE EVALUATION PLOTS
------------------------------------------------------------------------

STEP 1: Running the Webots Simulation
1. Launch Webots.
2. Open the world file: File -> Open World -> navigate to `worlds/ASR_world.wbt`.
3. To run Component A:
   - Ensure the robot in the scene has its controller set to `Autonomous_navigation_controller`.
4. To run Component B:
   - Ensure `e-puck_1`, `e-puck_2`, and `e-puck_3` have their controllers set to `swarm_controller`.
5. Click the "Play" button in Webots to begin simulation.
6. Allow the simulation to run for at least 15 to 30 seconds.
7. Click "Pause" or "Reset" to stop the simulation. The controllers will automatically update and save the `.csv` trajectory files.

Expected Runtime: 15 to 30 seconds of active simulation time.

STEP 2: Generating Trajectory Plots via Python
1. Open a terminal/command prompt in the root project folder (`ASR700_Assignment`).
2. Execute the trajectory plotting script:
       python plot_trajectory.py
3. A Matplotlib window will pop up showing the trajectory lines and starting markers for all agents, saving `swarm_trajectories.png` to the root folder.

========================================================================
