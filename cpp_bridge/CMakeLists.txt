cmake_minimum_required(VERSION 3.15)
project(studyboard_cpp_bridge VERSION 1.0.0 LANGUAGES CXX)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Compiler flags
if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
    add_compile_options(-Wall -Wextra -O3 -march=native)
elseif(MSVC)
    add_compile_options(/W4 /O2)
endif()

# Find Python
find_package(Python3 COMPONENTS Interpreter Development REQUIRED)

# Include directories
include_directories(
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${Python3_INCLUDE_DIRS}
)

# Create shared library
add_library(studyboard_bridge SHARED
    bridge.cpp
)

target_link_libraries(studyboard_bridge
    ${Python3_LIBRARIES}
)

# Set output properties
set_target_properties(studyboard_bridge PROPERTIES
    PREFIX ""
    OUTPUT_NAME "studyboard_bridge"
    POSITION_INDEPENDENT_CODE ON
)

# Installation
install(TARGETS studyboard_bridge
    LIBRARY DESTINATION lib
    RUNTIME DESTINATION bin
)

install(FILES bridge.h
    DESTINATION include/studyboard
)

# Build message
message(STATUS "Building STUDYBOARD C++ Bridge")
message(STATUS "Python3 found: ${Python3_VERSION}")
message(STATUS "Compiler: ${CMAKE_CXX_COMPILER_ID}")