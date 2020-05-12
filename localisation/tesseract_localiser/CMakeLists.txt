cmake_minimum_required(VERSION 2.8)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)


project( tesseract_localiser )

find_package( OpenCV REQUIRED )

include_directories( ${OpenCV_INCLUDE_DIRS} )

add_executable( tesseract_localiser tesseract_localiser.cpp )

target_link_libraries( tesseract_localiser ${OpenCV_LIBS} tesseract lept)