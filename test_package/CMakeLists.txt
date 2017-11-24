project(example)
cmake_minimum_required(VERSION 2.8)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_executable(example example.cpp)
include_directories(${CONAN_INCLUDE_DIRS})
target_link_libraries(example ${CONAN_LIBS})