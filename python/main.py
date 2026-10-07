"""
Your visualisation entry point. Edit freely.

Run from the repository root:
    python python/main.py
"""
from __future__ import annotations

from challenge_io import DATA_DIR, load_camera, load_frames, load_trajectory
from solution import parse_cones


def main() -> None:
    cones = parse_cones(str(DATA_DIR / "track.csv"))
    print(f"Parsed {len(cones)} cones")

    # Task 2b inputs, if you need them:
    # camera = load_camera(DATA_DIR / "camera.json")
    # trajectory = load_trajectory(DATA_DIR / "trajectory.csv")
    # frames = load_frames(DATA_DIR / "frames.csv")

    # TODO: your visualisation here


if __name__ == "__main__":
    main()
