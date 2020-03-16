from cefpython3 import cefpython as cef
import os
from pathlib import Path
import sys
import numpy as np
import cv2
import htmlmin
import dominate
from dominate.tags import *
import lorem
import re
from enum import Enum

# test_html/font_family/font_size/font_style/layout

def main() -> None:
    print('generate_html called.')
    generator: Generator = Generator()
    generator.generate_html()

class Layout(Enum):
    center = 1
    left = 2
    top = 3
    wall_of_text = 4
    l_word_c_text = 5
    words = 6

class Generator(object):
    def __init__(self):
        self.save_directory: str = './html/'
        if not os.path.isdir(self.save_directory):
            os.mkdir(self.save_directory)

        self.font_families: [str] = ['arial', 'verdana', 'georgia']
        self.font_sizes: [str] = ['six', 'ten', 'sixteen']
        self.font_styles: [str] = ['normal', 'italic', 'bold', 'underline']
        self.layouts = [e for e in Layout]


    def generate_html(self):

        for font_family in self.font_families:
            for font_size in self.font_sizes:
                for font_style in self.font_styles:
                    for layout in self.layouts:

                        # Generate path
                        file_path: str = self.save_directory + font_family + "/" + font_size + "/" + font_style + "/" + layout.name
                        
                        # Generate content
                        words: [str] = [""]
                        sentences: [str] = [""]
                        paragraphs: [str] = [""]

                        for i in range(0, 9):
                            words.append(lorem.get_word())
                            sentences.append(lorem.get_sentence())
                            paragraphs.append(lorem.get_paragraph())

                        words.pop(0)
                        sentences.pop(0)
                        paragraphs.pop(0)

                        # Generate and save document
                        self.generate_file(
                            path=file_path,
                            words=words,
                            sentences=sentences,
                            paragraphs=paragraphs,
                            font_family=font_family,
                            font_size=font_size,
                            font_style=font_style,
                            layout=layout
                            )

    def generate_file(self, 
        path: str,
        words: [str]=[''],
        sentences: [str]=[''],
        paragraphs: [str]=[''],
        font_family: str='',
        font_size: str='',
        font_style: str='',
        layout: Layout=Layout.center
        ):
        doc = dominate.document(title='generated')

        with doc.head:
            link(rel='stylesheet', href=os.path.abspath('style.css'))
            script(type='text/javascript', src='script.js')

        with doc.body:
            with div(cls='grid' + ' ' + font_family + ' ' + font_size + ' ' + font_style):
                if layout == Layout.center:
                            div(cls='cell')
                            if paragraphs[0]:
                                with div(cls='cell'):
                                    p(paragraphs[0])
                            div(cls='cell')
                            div(cls='cell')
                            if paragraphs[1]:
                                with div(cls='cell'):
                                    p(paragraphs[1])
                            div(cls='cell')
                            div(cls='cell')
                            if paragraphs[2]:
                                with div(cls='cell'):
                                    p(paragraphs[2])
                            div(cls='cell')
                elif layout == Layout.left:
                            if paragraphs[0]:
                                with div(cls='cell'):
                                    p(paragraphs[0])
                            div(cls='cell')
                            div(cls='cell')
                            if paragraphs[1]:
                                with div(cls='cell'):
                                    p(paragraphs[1])
                            div(cls='cell')
                            div(cls='cell')
                            if paragraphs[2]:
                                with div(cls='cell'):
                                    p(paragraphs[2])
                            div(cls='cell')
                            div(cls='cell')
                elif layout == Layout.top:
                            if paragraphs[0]:
                                with div(cls='cell'):
                                    p(paragraphs[0])
                            if paragraphs[1]:
                                with div(cls='cell'):
                                    p(paragraphs[1])
                            if paragraphs[2]:
                                with div(cls='cell'):
                                    p(paragraphs[2])
                            div(cls='cell')
                            div(cls='cell')
                            div(cls='cell')
                            div(cls='cell')
                            div(cls='cell')
                            div(cls='cell')
                elif layout == Layout.wall_of_text:
                            if paragraphs[0]:
                                with div(cls='cell'):
                                    p(paragraphs[0])
                            if paragraphs[1]:
                                with div(cls='cell'):
                                    p(paragraphs[1])
                            if paragraphs[2]:
                                with div(cls='cell'):
                                    p(paragraphs[2])
                            if paragraphs[3]:
                                with div(cls='cell'):
                                    p(paragraphs[3])
                            if paragraphs[4]:
                                with div(cls='cell'):
                                    p(paragraphs[4])
                            if paragraphs[5]:
                                with div(cls='cell'):
                                    p(paragraphs[5])
                            if paragraphs[6]:
                                with div(cls='cell'):
                                    p(paragraphs[6])
                            if paragraphs[7]:
                                with div(cls='cell'):
                                    p(paragraphs[7])
                            if paragraphs[8]:
                                with div(cls='cell'):
                                    p(paragraphs[8])
                elif layout == Layout.l_word_c_text:
                            if words[0]:
                                with div(cls='cell'):
                                    p(words[0])
                            if paragraphs[0]:
                                with div(cls='cell'):
                                    p(paragraphs[0])
                            div(cls='cell')
                            if words[1]:
                                with div(cls='cell'):
                                    p(words[1])
                            if paragraphs[1]:
                                with div(cls='cell'):
                                    p(paragraphs[1])
                            div(cls='cell')
                            if words[2]:
                                with div(cls='cell'):
                                    p(words[2])
                            if paragraphs[2]:
                                with div(cls='cell'):
                                    p(paragraphs[2])
                            div(cls='cell')
                elif layout == Layout.words:
                            if words[0]:
                                with div(cls='cell'):
                                    p(words[0])
                            if words[1]:
                                with div(cls='cell'):
                                    p(words[1])
                            if words[2]:
                                with div(cls='cell'):
                                    p(words[2])
                            if words[3]:
                                with div(cls='cell'):
                                    p(words[3])
                            if words[4]:
                                with div(cls='cell'):
                                    p(words[4])
                            if words[5]:
                                with div(cls='cell'):
                                    p(words[5])
                            if words[6]:
                                with div(cls='cell'):
                                    p(words[6])
                            if words[7]:
                                with div(cls='cell'):
                                    p(words[7])
                            if words[8]:
                                with div(cls='cell'):
                                    p(words[8])

        out_path: str = ""

        try:
            out_path = re.search(r'(.*[\/])', path).group()
        except AttributeError:
            out_path = path
        print('out_path: ' + out_path)
        print('path: ' + path)
        print()
        Path(out_path).mkdir(parents=True, exist_ok=True)
        with open(path + '.html', 'w') as f:
            f.write(htmlmin.minify(doc.render(pretty=False), remove_empty_space=True))
        print('CREATED:  ' + path + '.html')

    def save_file(self, document: dominate.document, name: str) -> None:
        with open(self.save_directory + name + '.html', 'w') as f:
            f.write(document)
        print('CREATED:  ' + name + '.html')



if __name__ == '__main__':
    main()
