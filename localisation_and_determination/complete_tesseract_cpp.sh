#!/bin/bash

cd tesseract_localiser
./setup.sh
./build/tesseract_localiser ../dataset ../dataset_tesseract_complete_l

cd tesseract_determiner
./setup.sh
./build/tesseract_determiner ../dataset_tesseract_complete_l ../dataset_tesseract_complete_cpp
