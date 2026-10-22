import csv
import math
from controller import Robot

# 1. Initialize Webots Robot instance FIRST
robot = Robot()
time_step = int(robot.getBasicTimeStep())
robot_name = robot.getName()

# 2. Initialize GPS device
gps = robot.getDevice("gps")
if gps:
    gps.enable(time_step)

# 3. Initialize Emitter and Receiver
emitter = robot.getDevice("emitter")
receiver = robot.getDevice("receiver")
if receiver:
    receiver.enable(time_step)

# 4. Initialize Motors
left_motor = robot.getDevice("left wheel motor")
right_motor = robot.getDevice("right wheel motor")
left_motor.setPosition(float("inf"))
right_motor.setPosition(float("inf"))
left_motor.setVelocity(0.0)
right_motor.setVelocity(0.0)

# 5. Initialize Distance Sensors
ds = []
for i in range(8):
    sensor = robot.getDevice(f"ps{i}")
    if sensor:
        sensor.enable(time_step)
        ds.append(sensor)

# 6. Setup CSV Data Logging (with line buffering to save data instantly)
log_filename = f"{robot_name}_trajectory.csv"
csv_file = open(log_filename, mode="w", newline="", buffering=1)
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["time", "x", "y"])

print(f"[{robot_name}] Swarm controller initialized successfully.")

# 7. Main Simulation Loop
start_time = robot.getTime()
while robot.step(time_step) != -1:
    current_time = robot.getTime() - start_time
    
    pos_x, pos_y = 0.0, 0.0
    if gps:
        pos = gps.getValues()
        pos_x, pos_y = pos[0], pos[1]

    csv_writer.writerow([round(current_time, 2), round(pos_x, 4), round(pos_y, 4)])

    message = f"{pos_x},{pos_y}"
    emitter.send(message.encode("utf-8"))

    peer_positions = []
    while receiver.getQueueLength() > 0:
        packet = receiver.getString()
        receiver.nextPacket()
        try:
            px, py = map(float, packet.split(","))
            if px != pos_x or py != pos_y:
                peer_positions.append((px, py))
        except ValueError:
            pass

    # Default speeds
    base_speed = 2.5
    left_speed = base_speed
    right_speed = base_speed

    # Check for obstacles / walls
    ds_vals = [s.getValue() for s in ds]
    surround_obstacle = any(val > 80.0 for val in ds_vals)

    if surround_obstacle:
        # If trapped in a corner (front sensors both high), reverse briefly to escape
        if ds_vals[0] > 100.0 and ds_vals[7] > 100.0:
            left_speed = -2.0
            right_speed = -2.0
        else:
            # Normal obstacle avoidance turn
            left_speed = 2.0
            right_speed = -2.0
    else:
        # Consensus and Aggregation behavior
        if peer_positions:
            avg_x = sum(p[0] for p in peer_positions) / len(peer_positions)
            avg_y = sum(p[1] for p in peer_positions) / len(peer_positions)
            
            # Calculate distance to cluster center
            dist_to_center = math.hypot(avg_x - pos_x, avg_y - pos_y)
            
            # If reached the group center, settle/stop instead of moving non-stop
            if dist_to_center < 0.2:
                base_speed = 0.0
            else:
                base_speed = 2.0

            left_speed = base_speed
            right_speed = base_speed

            dx = avg_x - pos_x
            if dx > 0.05:
                right_speed -= 0.3
            elif dx < -0.05:
                left_speed -= 0.3

    max_speed = 6.28
    left_speed = max(-max_speed, min(max_speed, left_speed))
    right_speed = max(-max_speed, min(max_speed, right_speed))

    left_motor.setVelocity(left_speed)
    right_motor.setVelocity(right_speed)

csv_file.close()