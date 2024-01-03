from flask import Flask, render_template, request, redirect, url_for
from compresor import compress
from decompresor import decoder
import os
import sys

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compress', methods=['POST'])
def compress_file():
    file = request.files['file']
    max_search = int(request.form['max_search'])
    
    compressed_filename = compress(file, max_search)
    original_size = os.path.getsize(file.filename)
    compressed_size = os.path.getsize(compressed_filename)
    compression_percentage = round(((original_size - compressed_size) / original_size) * 100, 2)

    return render_template('index.html', compression_percentage=compression_percentage)

@app.route('/decompress', methods=['POST'])
def decompress_file():
    compressed_file = request.files['compressed_file']
    max_search = int(request.form['max_search_decompress'])

    output_filename = "decompressed_output.txt"

    decoder(compressed_file, output_filename, max_search)

    return render_template('index.html', output_filename=output_filename)


if __name__ == '__main__':
    app.run(debug=True)
