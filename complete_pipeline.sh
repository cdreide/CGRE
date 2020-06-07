#!/bin/bash

echo 'Pipeline started.'
### Preperation ###
mkdir -p results

### Creation ###
echo '### Creation ###'
cd ./dataset/creation
echo '# Generating'
pipenv run python main.py -i ../styleCrawling/resources/urls_us -o ../../results -b

### Recognition ###
echo '### Recognition ###'

## Localisation
echo '## Localisation'
cd ../../recognition/localisation/tesseract_localiser
./setup.sh
./build/tesseract_localiser ../../results/dataset ../../results/dataset_tesseract_localised

## Determination on ideal
echo '## Determination on ideal'
cd ../../determination/tesseract_determiner
./setup.sh
./build/tesseract_determiner ../../results/dataset ../../results/dataset ../../results/dataset_tesseract_determiner

## Determination on localised (complete)
echo '## Determination on localised (complete)'
./build/tesseract_determiner ../../results/dataset ../../results/dataset_tesseract_localised ../../results/dataset_tesseract_complete

## Evaluation
echo '## Evaluation'
cd ../../../evaluation
echo '# Determination'
pipenv run python evaluation.py ../results/dataset ../results/dataset_tesseract_determiner/ -cp 0.5 -lt 2
echo '# Localised (complete)'
pipenv run python evaluation.py ../results/dataset ../results/dataset_tesseract_complete/ -cp 0.5 -lt 2
