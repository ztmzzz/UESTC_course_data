cmake_minimum_required(VERSION 3.22)
project(ls)
set(CMAKE_CXX_STANDARD 14)

include_directories(.)
add_executable(ls main.cpp)
target_link_libraries(ls)



