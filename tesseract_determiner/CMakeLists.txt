cmake_minimum_required(VERSION 2.8)

project( tesseract_determiner )

find_package( OpenCV REQUIRED )

include_directories( ${OpenCV_INCLUDE_DIRS} )

add_executable( tesseract_determiner tesseract_determiner.cpp )

target_link_libraries( tesseract_determiner ${OpenCV_LIBS} tesseract lept)