"""
Your visualisation entry point. Edit freely.

Run from the repository root:
    python python/main.py
"""
from __future__ import annotations

from challenge_io import DATA_DIR, load_camera, load_frames, load_trajectory
from solution import parse_cones, solve

import matplotlib.pyplot as plt
import numpy as np

def main() -> None:
    cones = parse_cones(str(DATA_DIR / "track.csv"))
    print(f"Parsed {len(cones)} cones")

    # Task 2b inputs, if you need them:
    # camera = load_camera(DATA_DIR / "camera.json")
    # trajectory = load_trajectory(DATA_DIR / "trajectory.csv")
    # frames = load_frames(DATA_DIR / "frames.csv")

    # TODO: 
    plan = solve(cones)

    # results
    saved = plan["base_time"] - plan["race_time"]
    print(f"centreline: {plan['base_time']:.2f} s, slowest {plan['base_speed'].min():.1f} m/s")
    print(f"smoothest line: {plan['smooth_time']:.2f} s, slowest {plan['smooth_speed'].min():.1f} m/s")
    print(f"racing line: {plan['race_time']:.2f} s, slowest {plan['race_speed'].min():.1f} m/s")
    print(f"saved: {saved:.2f} s ({100 * saved / plan['base_time']:.1f}%)")

    blue, yellow = plan["blue"], plan["yellow"]
    big_orange = np.array([[x, y] for side, x, y in cones if side == "big_orange"])

    #figure 1: the track with the centreline and the racing line
    plt.figure(figsize=(10, 7))
    plt.scatter(blue[:, 0], blue[:, 1], c="blue", s= 10, label="blue cones")
    plt.scatter(yellow[:, 0], yellow[:, 1], c="gold", s= 10, label="yellow cones")
    plt.scatter(big_orange[:, 0], big_orange[:, 1], c="orange", s=40, label="start/finish")
    plt.plot(plan["base_x"], plan["base_y"], c="grey", linestyle="dashed", label="centreline")
    plt.plot(plan["race_x"], plan["race_y"], c="red", label="racing line")
    plt.legend()
    plt.title(f"Centreline {plan['base_time']:.2f} s, racing line {plan['race_time']:.2f} s")
    plt.axis("equal")  #helps a screen to not stretch the map and cone points
    plt.xlabel("x (m)")
    plt.ylabel("y (m)")
    plt.tight_layout()  #stops labels being cut off

    # figure 2: speed around the lap
    plt.figure(figsize=(19, 4))
    plt.plot(plan["base_speed"], c="grey", label="centreline")
    plt.plot(plan["race_speed"], c="red", label="racing line")
    plt.xlabel("point number")
    plt.ylabel("speed (m/s)")
    plt.legend()
    plt.title("Speed around the lap")
    plt.tight_layout()

    plt.show()



if __name__ == "__main__":
    main()
