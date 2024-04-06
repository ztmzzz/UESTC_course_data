cmake_minimum_required(VERSION 3.22)
project(backup_tool)
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)
list(APPEND CMAKE_PREFIX_PATH "./Qt/6.4.0/gcc_64")
include_directories(.)
find_package(Qt6 COMPONENTS
        Core
        Gui
        Widgets
        REQUIRED)
add_executable(backup_tool
        backup.cpp file_info.h utils.h compress.cpp encrypt.h main.cpp mainwindow.cpp restore.cpp md5.cpp verify.h)
target_link_libraries(backup_tool
        Qt::Core
        Qt::Gui
        Qt::Widgets
        )



