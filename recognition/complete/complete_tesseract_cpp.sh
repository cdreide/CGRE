#!/bin/bash

cd ../localisation/tesseract_localiser
./setup.sh
./build/tesseract_localiser ../../../results/dataset ../../../results/dataset_tesseract_l

cd ../../determination/tesseract_determiner
./setup.sh
./build/tesseract_determiner ../../../results/dataset_tesseract_complete_l ../../../results/dataset_tesseract_complete_d
