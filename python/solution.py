"""
Your solution goes here.

Implement Task 1 and the Task 2 option you chose. Leave the other function
raising NotImplementedError. You may add as many other functions, modules and
files as you like, but keep these three function names and signatures: the
marking harness calls them through run.py.

Check your work with:
    python python/run.py all
"""
from __future__ import annotations
import numpy as np
import pandas as pd 
from scipy.interpolate import splprep, splev
from scipy.optimize import minimize


# A cone as returned by Task 1: (side, x, y)
Cone = tuple[str, float, float]

# car specifications 
GRIP = 1.5  # how well tyres hold the road
ACCEL = 8.0 # m/s^2
BRAKE = 12.0 # m/s^2
TOP_SPEED = 30.0 # m/s
G = 9.81 #gravity, m/s^2
CAR_WIDTH = 1.5   # m
MARGIN = 0.2   # m, extra space between the side of the car and a cone



# --------------------------------------------------------------------------- Task 1
def parse_cones(path: str) -> list[Cone]:
    """Read the cone file at `path` and return one (side, x, y) tuple per cone,
    in the order they appear in the file."""

    cone_pos = pd.read_csv(path)
    # make each row of csv as a tuple
    cone_tuples = list(cone_pos.itertuples(index=False, name=None))
    return cone_tuples


# --------------------------------------------------------------------------- Task 2a
def plan_racing_line(cones: list[Cone]) -> list[tuple[float, float]]:
    """Return your proposed racing line as a list of (x, y) points, in metres,
    in the order the car drives them."""
    plan = solve(cones)
    # the last spline point is the same place as the first, so it is left out
    return [(float(x), float(y)) for x, y in zip(plan["race_x"][:-1], plan["race_y"][:-1])]

def solve(cones):
    # fetching x,y positions of each cone, and store them as an array
    blue = np.array([[x, y] for side, x, y in cones if side == "blue"])
    yellow = np.array([[x, y] for side, x, y in cones if side == "yellow"])

    # find the borders, i.e. path and assigning a yellow cone for each blue cone  
    path, partners = find_gates(blue, yellow)

    # make_path receives list "across" with param values (from 0 to 1), which say where the car crosses that gate. Returns an array of track points. 
    def make_path(across):
        points = []
        for i in range(len(blue)):
            b = blue[i]                  
            y = partners[i]              
            p = b + across[i] * (y - b)  # go part of the way from b to y
            points.append(p)
        return np.array(points)

    
    def lap_time(across):
        points = make_path(across)
        return run_paths(points)[0]

    def bend(across):
        points = make_path(across)
        return total_bend(points)

    #find centreline
    base_time, base_x, base_y, base_speed = run_paths(path)

    # keep the whole car (plus a margin) inside the cones at every gate
    gate_width = np.linalg.norm(partners - blue, axis=1) #axis=1 means “do it separately for each row”
    keep_clear = (CAR_WIDTH / 2 + MARGIN) / gate_width  # part of each gate the car's centre must not enter
    keep_clear = np.minimum(keep_clear, 0.5)             # a very narrow gate leaves only the middle
    limits = []
    for l in keep_clear:  # l = the off-limits fraction for one gate, e.g. 0.24
        limits.append((l, 1 - l))    # add the pair (lowest allowed, highest allowed), e.g. (0.24, 0.76)


    start = np.full(len(blue), 0.5)
    #stage 1: the smoothest line (least bending), starting from the centreline
    smooth = minimize(bend, start, bounds=limits)
    smooth_time, smooth_x, smooth_y, smooth_speed = run_paths(make_path(smooth.x))

    # stage 2: fine-tune the smooth line for the lowest lap time
    result = minimize(lap_time, smooth.x, bounds=limits)
    best = result.x
    race_time, race_x, race_y, race_speed = run_paths(make_path(best))


    return {
        "blue": blue, "yellow": yellow,
        "base_time": base_time, "base_x": base_x, "base_y": base_y, "base_speed": base_speed,
        "smooth_time": smooth_time, "smooth_speed": smooth_speed,
        "race_time": race_time, "race_x": race_x, "race_y": race_y, "race_speed": race_speed,
    }
 


def find_gates(blue, yellow):
    # algorithm below finds midpoints between two closest of cones (blue & yellow)
    path = []      # store the Midpoint Path
    partners = []  # store the values of each yellow cone that is closest to blue cone
    for b in blue:
        difference = yellow - b
        str_line_array = np.linalg.norm(difference, axis=1)
        smallest = np.argmin(str_line_array)  # returns position
        y = yellow[smallest]
        partners.append(y)
        mid_point = (b + y) / 2
        path.append(mid_point)
    return np.array(path), np.array(partners)


def total_bend(pts):
    # same spline and curvature as in run_paths
    loop = np.vstack([pts, pts[0]])
    spline, midpoint_range = splprep([loop[:, 0], loop[:, 1]], s=0, per=True)
    lap_progress = np.linspace(0, 1, 500)
    dx, dy = splev(lap_progress, spline, der=1)
    ddx, ddy = splev(lap_progress, spline, der=2)
    curvature = np.abs(dx*ddy - dy*ddx)/(dx**2 + dy**2)**1.5
    # squared, so one sharp bend counts more than several gentle ones
    return np.sum(curvature**2)



def run_paths(pts):
    loop = np.vstack([pts, pts[0]])
    # splprep - spline parametric representation = the stored description(formula) of a smooth curve, where x and y each depend on a progress number(midpoint_range on the track - how far away is it from start to end (0 to 1))
    spline, midpoint_range = splprep([loop[:, 0], loop[:, 1]], s=0, per=True)
    lap_progress = np.linspace(0, 1, 500) 
    # splev - spline evaluation = takes given spline, put the values of lap_progress, returns x and y values of that curve.
    inter_x, inter_y = splev(lap_progress, spline)


    # find how fast can the car go in the corner
    # curvature = how sharply the path bends (1 / radius)
    dx, dy = splev(lap_progress, spline, der=1)
    ddx, ddy = splev(lap_progress, spline, der=2)
    curvature = np.abs(dx*ddy - dy*ddx)/(dx**2 + dy**2)**1.5

    safe_curv = np.maximum(curvature, 1e-6)
    #how fast the tyres allow at that sharpness
    corner_speed = np.sqrt(GRIP * G / safe_curv) 
    corner_speed = np.minimum(corner_speed, TOP_SPEED)

    # distance between neighbouring points
    step_x = np.diff(inter_x)
    step_y = np.diff(inter_y)
    distance = np.sqrt(step_x**2 + step_y**2)

    speed = corner_speed.copy()

    # forward pass - the car can only gain speed at ACCEL
    for lap in range(2):
        for i in range(len(distance)):
            #find the speed for each dot: v^2 = u^2 + 2as
            reach = np.sqrt(speed[i]**2 + 2 * ACCEL * distance[i])
            # initial speed at the next point is min of(reach: what the engine allows or speed[i+1]: what the tyres allow at the next dot.)
            speed[i+1] = min(reach, speed[i + 1])
        speed[0] = speed[-1]

    # backward pass: the car can only lose speed at BRAKE
    for lap in range(2):
        for i in reversed(range(len(distance))):
            allowed = np.sqrt(speed[i+1]**2 + 2 * BRAKE * distance[i])
            speed[i] = min(speed[i], allowed)
        speed[-1] = speed[0]

    avg_speed = (speed[:-1] + speed[1:]) / 2
    lap_time = np.sum(distance / avg_speed)
    return lap_time, inter_x, inter_y, speed


# --------------------------------------------------------------------------- Task 2b
def project_cones(cones: list[Cone],
                  pose: tuple[float, float, float],
                  camera: dict) -> list[tuple[int, float, float]]:
    """Return (cone_index, u, v) for every cone visible to the camera when the
    car is at `pose` = (x, y, yaw).

    cone_index is the cone's 0-based position in `cones`; (u, v) is the
    centre of the cone's base in pixels. `camera` is camera.json as a dict
    (see challenge_io.load_camera)."""
    raise NotImplementedError
