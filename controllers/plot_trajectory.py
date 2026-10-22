import pandas as pd
import matplotlib.pyplot as plt

robots = ['e-puck_1', 'e-puck_2', 'e-puck_3']

plt.figure(figsize=(8, 8))

data_found = False

for robot in robots:
    filename = f"controllers/swarm_controller/{robot}_trajectory.csv"
    try:
        df = pd.read_csv(filename)
        print(f"--- {robot} ---")
        print(df.head())  # Prints first few rows to terminal
        
        if df.empty or (df['x'].max() == 0 and df['y'].max() == 0):
            print(f"Warning: {filename} contains only zeros or is empty.")
            continue
            
        plt.plot(df['x'], df['y'], label=f"{robot} Trajectory", linewidth=2)
        plt.scatter(df['x'].iloc[0], df['y'].iloc[0], marker='o', s=100, label=f"{robot} Start")
        data_found = True
    except Exception as e:
        print(f"Could not read {filename}: {e}")

plt.title("Multi-Agent Swarm Trajectories (ASR700 Component B)")
plt.xlabel("X Position (meters)")
plt.ylabel("Y Position (meters)")
plt.axhline(0, color='grey', linestyle='--', linewidth=0.5)
plt.axvline(0, color='grey', linestyle='--', linewidth=0.5)
plt.grid(True)
plt.legend()
plt.show()