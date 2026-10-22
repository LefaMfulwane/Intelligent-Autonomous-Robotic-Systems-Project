import math
import csv
from controller import Robot

TIME_STEP = 32
MAX_SPEED = 6.28

class WaypointNavigationController:
    def __init__(self):
        print("INFO: Initializing Waypoint Navigation Controller...")
        self.robot = Robot()
        
        # Motors
        self.left_motor = self.robot.getDevice('left wheel motor')
        self.right_motor = self.robot.getDevice('right wheel motor')
        self.left_motor.setPosition(float('inf'))
        self.right_motor.setPosition(float('inf'))
        self.left_motor.setVelocity(0.0)
        self.right_motor.setVelocity(0.0)
        
        # GPS
        self.gps = self.robot.getDevice('gps')
        if self.gps:
            self.gps.enable(TIME_STEP)
            print("INFO: GPS enabled successfully.")
            
        # Proximity Sensors
        self.sensors = []
        for i in range(8):
            s = self.robot.getDevice(f'ps{i}')
            if s:
                s.enable(TIME_STEP)
                self.sensors.append(s)
                
        # Define Planned Waypoints (x, y) for the robot to visit
        self.waypoints = [
            [0.4, 0.4],   # Waypoint 1
            [0.4, -0.4],  # Waypoint 2
            [-0.4, -0.4], # Waypoint 3
            [-0.4, 0.4]   # Waypoint 4
        ]
        self.current_waypoint_index = 0
        
        # Data Logging for Evaluation
        self.logged_x = []
        self.logged_y = []

    def run(self):
        print("INFO: Starting waypoint navigation loop...")
        try:
            while self.robot.step(TIME_STEP) != -1:
                # 1. Get current GPS position
                if self.gps:
                    pos = self.gps.getValues()
                    curr_x, curr_y = pos[0], pos[1]
                    self.logged_x.append(curr_x)
                    self.logged_y.append(curr_y)
                else:
                    break

                # 2. Check if we reached the current waypoint (within 0.08m tolerance)
                target = self.waypoints[self.current_waypoint_index]
                distance = math.sqrt((target[0] - curr_x)**2 + (target[1] - curr_y)**2)
                
                if distance < 0.08:
                    print(f"REACHED Waypoint {self.current_waypoint_index + 1}: {target}")
                    self.current_waypoint_index += 1
                    if self.current_waypoint_index >= len(self.waypoints):
                        print("INFO: All waypoints completed! Saving trajectory data...")
                        self.save_trajectory_to_csv()
                        break

                # 3. Simple proportional steering toward the target waypoint
                desired_angle = math.atan2(target[1] - curr_y, target[0] - curr_x)
                
                # Approximate heading control (For full orientation, compass can be added; 
                # here we drive forward and correct based on obstacle sensors or simple mixing)
                sensor_values = [s.getValue() for s in self.sensors]
                obstacle_detected = sensor_values[0] > 80.0 or sensor_values[7] > 80.0

                if obstacle_detected:
                    # Obstacle avoidance override
                    self.left_motor.setVelocity(MAX_SPEED * 0.4)
                    self.right_motor.setVelocity(-MAX_SPEED * 0.4)
                else:
                    # Move towards target
                    base_speed = MAX_SPEED * 0.5
                    self.left_motor.setVelocity(base_speed)
                    self.right_motor.setVelocity(base_speed)
                    
        except Exception as e:
            print(f"CRASH in main loop: {e}")

    def save_trajectory_to_csv(self):
        """Saves logged GPS coordinates to a CSV file for Matplotlib plotting."""
        filename = "robot_trajectory.csv"
        with open(filename, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["x", "y"])
            for x, y in zip(self.logged_x, self.logged_y):
                writer.writerow([x, y])
        print(f"SUCCESS: Trajectory saved to {filename} for your report graphs.")

if __name__ == "__main__":
    controller = WaypointNavigationController()
    controller.run()