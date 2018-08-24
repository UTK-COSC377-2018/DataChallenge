#!/bin/bash

com="./run.sh ${@:1}"

virtualenv cosc377
cd cosc377
source bin/activate

#pip install importlib
pip install -U sklearn
pip install -U nltk
pip install pandas==0.17.1
pip install beautifulsoup4

#pip install https://github.com/matplotlib/basemap/archive/v1.0.7rel.tar.gz

cd ..

${com}

deactivate
