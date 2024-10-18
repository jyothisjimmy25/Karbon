from flask import Flask, request, render_template, redirect, url_for
import os
import json
from model import analyze_financials

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        return redirect(url_for('results', filepath=filename))

@app.route('/results')
def results():
    filepath = request.args.get('filepath')
    with open(filepath, 'r') as f:
        data = json.load(f)
    results = analyze_financials(data)
    
    if 'error' in results:
        return render_template('error.html', error_message=results['error'])
    
    return render_template('results.html', results=results)

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
