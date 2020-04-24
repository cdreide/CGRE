# OCROnWebpages

Pre:
    pyenv:
        ``https://github.com/pyenv/pyenv/wiki``
        (sudo apt-get update; sudo apt-get install --no-install-recommends make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev)
        ``pyenv install 3.7.2``
        ``pyenv local 3.7.2``

install:
`` pipenv install . --dev ``

start shell:
`` pipenv shell ``

generate:
`` pipenv run python generate_html.py ``
    => './html/font_family/font_size/font_style/layout.html'

render ( & save ):
`` pipenv run python render_html.py ``
    => './dataset/font_family/font_size/font_style/layout.png'  
    => './dataset/font_family/font_size/font_style/layout.txt'  
        (contains words and their boxes in this format: // word\t(left,top,width,height)\n)  
        (first line contains path to the corresponding html file)

zip:
`` pipenv run python zip_dataset.py ``
    => zips the 'dataset' directory with the same structure to 'dataset.zip'

evaluation:
`` pipenv run python evaluation.py ideal recognized``
    => evaluates the recognized dataset against the ideal
        True Positives 
        False Positives
        False Negatives
        Accuracy
        Precision
        Recall
        F1-Score
        (for respectively the localisation and the determination)
    => they need to have the same structure
    => results in 2 files:
        'evaluation_ideal_recognized.csv'
            (contains the )
        'evaluation_ideal_recognized.txt'


reset virtual env:
``pipenv --rm``
