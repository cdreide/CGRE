#! /bin/bash

echo 'Pipeline started.'
pipenv run python generate_html.py
pipenv run python render_html.py
pipenv run python dataset_to_csv.py
#pipenv run python zip_dataset.py