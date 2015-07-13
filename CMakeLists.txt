cmake_minimum_required(VERSION 2.8)
project(PPS_utils)

set(CAEN_LOCATION "/usr/lib")
set(GCC_COMPILE_FLAGS "-Wall -fPIC -O2")
add_definitions(${GCC_COMPILE_FLAGS})

file(GLOB sources ${PROJECT_SOURCE_DIR}/src/*.cpp)
add_library(src_lib OBJECT ${sources})
include_directories("${PROJECT_SOURCE_DIR}/include/")

# WebSocket
#add_subdirectory(${PROJECT_SOURCE_DIR}/external)
#include_directories("${PROJECT_SOURCE_DIR}/external")

#add_executable(ppsRun main.cpp $<TARGET_OBJECTS:src_lib> $<TARGET_OBJECTS:ws_lib>)
#add_executable(listener listener.cpp $<TARGET_OBJECTS:src_lib> $<TARGET_OBJECTS:ws_lib>)

# Here have tests
#add_subdirectory(test EXCLUDE_FROM_ALL)

# CAEN stuff
add_library(caen SHARED IMPORTED)
set_property(TARGET caen PROPERTY IMPORTED_LOCATION "${CAEN_LOCATION}/libCAENVME.so")
set(CMAKE_CXX_FLAGS "-DLINUX")
#set(CMAKE_CXX_LINK_FLAGS "-lCAENVME -Wl")
set(CMAKE_CXX_LINK_FLAGS "-lCAENVME")

add_executable(readreg read_register.cpp $<TARGET_OBJECTS:src_lib> $<TARGET_OBJECTS:ws_lib>)
add_executable(readevs read_outputbuf.cpp $<TARGET_OBJECTS:src_lib> $<TARGET_OBJECTS:ws_lib>)
add_executable(writereg write_register.cpp $<TARGET_OBJECTS:src_lib> $<TARGET_OBJECTS:ws_lib>)
add_executable(vmesysreset vme_system_reset.cpp $<TARGET_OBJECTS:src_lib> $<TARGET_OBJECTS:ws_lib>)
add_executable(vmebridge BridgeVME.cpp $<TARGET_OBJECTS:src_lib> $<TARGET_OBJECTS:ws_lib>)
#add_library(readtdcteg SHARED src/ReadTDCRegister.cpp)
target_link_libraries(readreg caen)
#target_link_libraries(readtdcreg caen)
