# FS-AI 2026 Individual Challenge: Kamron Khusainov

> Replace everything in this file with your own write-up. See `INTERFACE.md` for how the code is run.

**Task chosen:** 2a (path planning) 
**Language:** Python

## How to run my visualisation

```bash
pip install -r python/requirements.txt
python python/run.py all
python python/main.py
```

## Task 1

### Reading the cones:

`parse_cones(path)` reads the CSV with pandas and returns one `(side, x, y)` tuple per cone, in file order, for example `("blue", 34.752, -19.546)`. `itertuples(index=False, name=None)` gives plain tuples without the row number or column names.
The given track has 127 cones: 64 blue, 59 yellow and 4 big orange (start/finish).
By FS-UK conventions blue cones are left, and yellow - are right.


## Task 2

## 2A - Path planning! 
### Step 1: gates and the centreline

For each blue cone I find the nearest yellow cone. I call the line between them a **gate**: the car has to pass through every gate. The middle of each gate gives one point of the centreline.
There are fewer yellow cones (59) than blue (64), so a few yellow cones are the nearest partner of two blue cones. That is fine, because every gate still has its own blue end.


### Step 2: a smooth curve through the points

As was suggested in the given PDF instruction file, I join the points with a periodic cubic spline (`scipy.interpolate.splprep` with `s=0, per=True`):

- `s=0` makes the curve pass exactly through every point.
- `per=True` joins the end back to the start smoothly, because the track is a loop.

I then sample the spline at 500 evenly spaced positions around the lap, about 0.6 m apart. I used a spline rather than straight lines because straight segments have a sharp turn at every join, so every cone would look like a corner.


### Step 3: how sharp each part of the line is

Curvature measures how sharply the line turns, and equals 1 / radius: 0 on a straight, large in a hairpin. I get it from the spline's first and second derivatives:

```
curvature = |x'y'' - y'x''| / (x'^2 + y'^2)^1.5
```

The tightest corner on the centreline has curvature 0.150, which is a radius of 6.7 m.



### Step 4: the car model (lap simulator)

I treat the car as a single point with three limits: tyre grip, acceleration and braking.

**Corner speed.** To follow a curve the car needs a sideways acceleration of `v^2 x curvature`, and the tyres can give at most `GRIP x g`. So the fastest speed at each point is

```
v_corner = sqrt(GRIP x g / curvature), capped at TOP_SPEED
```

**Accelerating and braking.** The car cannot change speed instantly, so I go around the lap twice more, using `v^2 = u^2 + 2as`:

- Forward pass: the speed at the next point can be at most `sqrt(v^2 + 2 x ACCEL x d)`, where `d` is the distance to it. This makes the car build speed gradually after a corner.
- Backward pass: the speed at each point can be at most `sqrt(v_next^2 + 2 x BRAKE x d)`. This makes the car start braking before a corner.

Each pass runs twice so the speed at the end of the lap carries over the start line (a flying lap :) ).

**Lap time.** Each of the 499 small pieces takes `distance / average speed`. The lap time is the sum.


### Step 5: moving the line

Each point of the line can only slide along its own gate:

```
point = blue + a x (yellow - blue)
```

`a = 0` is on the blue cone, `a = 1` is on the yellow cone and `a = 0.5` is the centreline. So the whole line is just one number per gate (64 numbers), and the optimiser searches for the best 64 numbers.

**Keeping the car on the track.** The point is the centre of the car, so it has to stay at least half the car width plus a margin (0.75 + 0.2 = 0.95 m) away from each cone. I turn that into a fraction of each gate's width, so on this track each `a` is limited to roughly 0.22 to 0.78, depending on how wide the gate is. If a gate is ever narrower than 1.9 m, the limit is capped so the car simply drives through the middle.


### Step 6: Calculating best time

**Two stages.** Both use `scipy.optimize.minimize`.

1. **Smoothest line.** Starting from the centreline, minimise the total bending, `sum(curvature^2)`. Squaring makes one sharp bend cost more than the same turn spread over a wide arc. Result: 12.42 s.
2. **Fastest line.** Starting from the smoothest line, minimise the lap time from the simulator. Result: 12.31 s.

The final line does what a driver would do: it stays wide before a corner, moves towards the inside cones in the middle of it and drifts back out afterwards. 


## How I got here

These are the main decisions, in the order I made them.

1. **Centreline first.** Nearest-cone midpoints plus a spline gave a simple, working line and a baseline lap time (13.48 s) to compare against.
2. **Point mass instead of a bicycle model.** The optimiser runs the lap simulator about 25,000 times, so it had to be fast and have few parameters. A point mass still captures the main trade-off: a wider corner allows more speed. A bicycle model is the next step.
3. **Limits based on the car's width.** My first version let each point go from 0.1 to 0.9 of the gate. On a 3.5 m wide track, 0.1 puts the car's centre 35 cm from a cone, with half the car (75 cm) over it. I changed the limits to use the car's width plus a margin.
4. **Lap time alone got stuck, so I added a first stage.** Optimising lap time directly from the centreline only reached 12.76 s, and every `a` stayed between 0.47 and 0.54. Moving one point on its own makes a small kink, which slows the car, so the optimiser never found that moving a whole corner together helps. Minimising bending first moves whole corners at once and gives the lap time stage a much better starting point.

## Assumptions

From my search I found basic student car specifications, which I used as assumptions

| Parameter | Value | Reason |
|---|---|---|
| Units | metres | the lap length (305 m) and corner radii fit a Formula Student track |
| GRIP | 1.5 | typical friction for racing slicks |
| ACCEL | 8.0 m/s^2 | rough figure for an electric FS car |
| BRAKE | 12.0 m/s^2 | cars brake harder than they accelerate |
| TOP_SPEED | 30 m/s | about 108 km/h |
| CAR_WIDTH | 1.5 m | typical FS car |
| MARGIN | 0.2 m | extra space between the car and the cones |

I also assume that:
- the cones in the file are listed in driving order,
- blue cones mark the left edge and yellow cones the right (from FS-UK),
- the track is a closed loop,


## Limitations and what I'd do with more time
- **Grip is not shared.** The model allows full braking and full cornering at the same moment. Real tyres share their grip between the two (the friction circle), so the next step is to limit the combined acceleration.
- **No aerodynamics or power curve.** Downforce would raise corner speeds, and real acceleration drops at higher speed.
- **Point mass, not a bicycle model.** A bicycle model would add steering angle, and check that the line can actually be driven.
- **Not guaranteed to be the best line.** Each stage stops when it stops improving or after a fixed number of evaluations, so the result is a good line, not a proven optimum.
- **Cone order and direction.** The cones must be in driving order. If a file lists them the other way round, the line is planned and returned in reverse. A fix would be to sort the cones along the track and check the direction using the rule that blue is on the left.
- **Cone pairing.** Nearest-cone pairing assumes the cones are fairly evenly spaced on both sides. With very uneven spacing, a gate could cross the track at an angle.
