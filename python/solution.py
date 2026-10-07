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

# A cone as returned by Task 1: (side, x, y)
Cone = tuple[str, float, float]


# --------------------------------------------------------------------------- Task 1
def parse_cones(path: str) -> list[Cone]:
    """Read the cone file at `path` and return one (side, x, y) tuple per cone,
    in the order they appear in the file."""
    raise NotImplementedError


# --------------------------------------------------------------------------- Task 2a
def plan_racing_line(cones: list[Cone]) -> list[tuple[float, float]]:
    """Return your proposed racing line as a list of (x, y) points, in metres,
    in the order the car drives them."""
    raise NotImplementedError


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
