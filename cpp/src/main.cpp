// Your visualisation entry point. Edit freely.
//
// Build and run (from the repository root):
//     cmake -S cpp -B cpp/build && cmake --build cpp/build
//     ./cpp/build/visualise
#include <iostream>

#include "challenge.hpp"
#include "challenge_io.hpp"

int main() {
    const auto cones = parse_cones(challenge_io::kDataDir + "/track.csv");
    std::cout << "Parsed " << cones.size() << " cones\n";

    // Task 2b inputs, if you need them:
    // const auto camera = challenge_io::load_camera(challenge_io::kDataDir + "/camera.json");
    // const auto trajectory = challenge_io::load_trajectory(challenge_io::kDataDir + "/trajectory.csv");
    // const auto frames = challenge_io::load_frames(challenge_io::kDataDir + "/frames.csv");

    // TODO: your visualisation here
    return 0;
}
