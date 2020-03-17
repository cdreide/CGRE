# OCROnWebpages

install:
`` pipenv install . --dev ``

start shell:
`` pipenv shell ``

generate:
`` pipenv run python generate_html.py ``  
    => './html/font_family/font_size/font_style/layout.html'

render ( &save ):
`` pipenv run python render_html.py ``  
    => './dataset/font_family/font_size/font_style/layout.png'  
    => './dataset/font_family/font_size/font_style/layout.txt'  
        (contains words and their boxes in this format: // word\t(left,top,width,height)\n)  
        (first line contains path to the corresponding html file)

zip:
`` pipenv run python zip_dataset.py ``  
    => zips the 'dataset' directory with the same structure to 'dataset.zip'
