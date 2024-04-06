cmake_minimum_required(VERSION 3.26)
project(final)

set(CMAKE_CXX_STANDARD 17)

add_executable(final main.cpp
        utils.h
        threadPool.cpp
        threadPool.h
        sort.cpp
        sort.h
)
