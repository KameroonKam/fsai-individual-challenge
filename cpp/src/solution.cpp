// Your solution goes here.
//
// Implement Task 1 and the Task 2 option you chose. Leave the other function
// throwing NotImplemented. You may add other source files (list them in
// CMakeLists.txt), but keep these three functions exactly as declared in
// include/challenge.hpp: the marking harness calls them through the runner.
//
// Check your work (from the repository root):
//     cmake -S cpp -B cpp/build && cmake --build cpp/build
//     ./cpp/build/runner all
#include "challenge.hpp"

// ---------------------------------------------------------------- Task 1
std::vector<Cone> parse_cones(const std::string& path) {
    (void)path;
    throw NotImplemented();
}

// ---------------------------------------------------------------- Task 2a
std::vector<Point2> plan_racing_line(const std::vector<Cone>& cones) {
    (void)cones;
    throw NotImplemented();
}

// ---------------------------------------------------------------- Task 2b
std::vector<Projection> project_cones(const std::vector<Cone>& cones,
                                      const Pose& pose,
                                      const Camera& camera) {
    (void)cones;
    (void)pose;
    (void)camera;
    throw NotImplemented();
}
