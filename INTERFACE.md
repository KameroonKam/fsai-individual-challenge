# Submission interface

Your code is run by a small program we provide, called the **runner**. It calls three functions that you
implement, checks what they return, and writes the results to `output/`. We use the same runner to mark
your submission, on the data in `data/` **and on a second track you haven't seen**. Don't hard-code
anything about this particular track.

Pick **one** language and work only in its folder. You can delete the other folder.

## The three functions

| Task | Python (`python/solution.py`) | C++ (`cpp/src/solution.cpp`) | Runner writes |
|---|---|---|---|
| 1 | `parse_cones(path)` | `parse_cones(path)` | `output/cones.csv` |
| 2a | `plan_racing_line(cones)` | `plan_racing_line(cones)` | `output/racing_line.csv` |
| 2b | `project_cones(cones, pose, camera)` | `project_cones(cones, pose, camera)` | `output/projections.csv` |

The exact signatures and return types are documented in `python/solution.py` and `cpp/include/challenge.hpp`.

- Implement Task 1 and the Task 2 option you chose. Leave the other one as it is (raising
  `NotImplementedError` / throwing `NotImplemented()`).
- For Tasks 2a and 2b the runner reads the cone file itself and passes you the cones in the same form your
  `parse_cones` returns. That way a mistake in Task 1 doesn't also cost you marks in Task 2.
- For Task 2b the runner reads `camera.json`, `trajectory.csv` and `frames.csv`, and calls
  `project_cones` once for each timestamp in `frames.csv`.

## Running it

From the repository root:

**Python** (3.10+)
```bash
pip install -r python/requirements.txt
python python/run.py all          # or: 1, 2a, 2b
```

**C++** (C++17, CMake 3.16+)
```bash
cmake -S cpp -B cpp/build
cmake --build cpp/build
./cpp/build/runner all            # or: 1, 2a, 2b
```

Each task prints `ok`, `not implemented`, `INTERFACE ERROR` (your function returned something the runner
can't use, and the message says what) or `CRASHED`.

## Files

| File | Yours to edit? |
|---|---|
| `python/solution.py`, `cpp/src/solution.cpp` | **Yes.** Implement the functions here. Add more files and modules as you like. |
| `python/main.py`, `cpp/src/main.cpp` | **Yes.** Your visualisation goes here, in whatever form you like. |
| `python/requirements.txt` | **Yes.** List every package you use. |
| `cpp/CMakeLists.txt` | **Yes**, above the "do not edit" line: add source files and libraries there. |
| `python/run.py`, `python/challenge_io.py` | No. We replace these with our own copies when marking. |
| `cpp/runner/run.cpp`, `cpp/include/challenge.hpp`, `cpp/include/challenge_io.hpp` | No. We replace these with our own copies when marking. |

You can use the helpers in `challenge_io` (Python) / `challenge_io.hpp` (C++) from your own code. They read
the Task 2b data files.

## Your README

Fill in `README.md`. In particular, tell us exactly how to run your visualisation.
