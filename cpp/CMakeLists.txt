cmake_minimum_required(VERSION 3.16)
project(fsai_individual_challenge CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release)
endif()

# ----------------------------------------------------------------- your code
# Add any extra source files to the `solution` library, and any third-party
# libraries you use, e.g.
#   find_package(Eigen3 REQUIRED)    -> target_link_libraries(solution PUBLIC Eigen3::Eigen)
#   find_package(OpenCV REQUIRED)    -> target_link_libraries(solution PUBLIC ${OpenCV_LIBS})
add_library(solution
  src/solution.cpp
)
target_include_directories(solution PUBLIC include)
target_compile_definitions(solution PUBLIC CHALLENGE_REPO_ROOT="${CMAKE_CURRENT_SOURCE_DIR}/..")

# Your visualisation program (src/main.cpp)
add_executable(visualise src/main.cpp)
target_link_libraries(visualise PRIVATE solution)

# ----------------------------------------------------------------- do not edit below
# The runner is what we use to mark your submission.
add_executable(runner runner/run.cpp)
target_link_libraries(runner PRIVATE solution)
