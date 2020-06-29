#!/bin/bash

echo 'Pipeline started.'
### Preperation ###
mkdir -p results

### Creation ###
echo '### Creation ###'
cd ./dataset/creation
echo '# Generating'
pipenv run python main.py -i ../styleCrawling/resources/urls_us -o ../../results -t 3 -b -v

### Recognition ###
echo '### Recognition ###'

## Localisation
echo '## Localisation'
cd ../../recognition/localisation/
./setup.sh
./build/localiser ../../results/dataset ../../results/dataset_tesseract_localised

## Determination on ideal
echo '## Determination on ideal'
cd ../determination/
./setup.sh
./build/determiner ../../results/dataset ../../results/dataset ../../results/dataset_tesseract_determiner

## Determination on localised (complete)
echo '## Determination on localised (complete)'
./build/determiner ../../results/dataset ../../results/dataset_tesseract_localised ../../results/dataset_tesseract_complete

## Evaluation
echo '## Evaluation'
cd ../../evaluation
# echo '# Determination'
# pipenv run python evaluation.py ../results/dataset ../results/dataset_tesseract_determiner/ -cp 0.6 -lp 0.7 -o ../results/evaluation_determiner
# echo '# Localised (complete)'
# pipenv run python evaluation.py ../results/dataset ../results/dataset_tesseract_complete/ -cp 0.6 -lp 0.7 -o ../results/evaluation_complete

echo '# Determination'
# pipenv run python evaluate_combinations.py ../results/dataset ../results/dataset_tesseract_determiner/ -o ../results/evaluation_determiner
echo '# Localised (complete)'
pipenv run python evaluate_combinations.py ../results/dataset ../results/dataset_tesseract_complete/ -o ../results/evaluation_complete
