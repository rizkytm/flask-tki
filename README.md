# Youtube Comment Summary Analysis

## Introduction

> Youtube comment summary analysis merupakan sistem information retrieval yang menghasilkan kalimat summary dari kumpulan komentar pada link youtube. Sistem ini menerima input berupa link video youtube dengan, kemudian me-retrive komentar yang ada pada link tersebut untuk diolah dengan algoritma summarization dan  mengeluarkan output berupa top-10 kalimat yang menjelaskan summary dari kumpulan komentar tersebut. Selain hasil summary,akan dihasilkan output lain berupa grafik wordcloud, 2-gram bar graph, dan 3-gram pie-chart.


## Installation

> Install flask :
    
    mkdir test :

    cd test
    pip install flask
    python app.py

    dependency yang diinstall:

    pip install flask-mysql
    pip install flask-wtf
    pip install passlib

> install Anaconda :
    
    https://conda.io/docs/download.html

> install package via anaconda :

    conda install -c anaconda gensim
    conda install -c plotly plotly 
    conda install -c conda-forge wordcloud

> Tutorial run via flask (linux) :

    export FLASK_APP=app.py
    export FLASK_DEBUG=true
    flask run
