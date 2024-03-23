import matplotlib
matplotlib.use('Agg')  # Use non-interactive Agg backend

from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from werkzeug.utils import secure_filename
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier, plot_tree, export_text
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import io
import base64
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'csv', 'xlsx'}
app.secret_key = 'your_secret_key_here'  # Needed for flash messaging

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/train', methods=['POST'])
def train_model():
    if 'file' in request.files:
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            data = pd.read_csv(filepath)
            X = data.iloc[:, :-1].values
            y = data.iloc[:, -1].values
    elif 'demo_dataset' in request.form and request.form['demo_dataset'] == 'iris':
        iris = load_iris()
        X, y = iris.data, iris.target
    else:
        return jsonify({'error': 'No valid dataset provided'}), 400

    clf = DecisionTreeClassifier()
    clf.fit(X, y)
    
    plt.figure(figsize=(20, 10))
    plot_tree(clf, filled=True)
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    
    tree_text = export_text(clf)
    
    return jsonify({'image': plot_url, 'text': tree_text})

if __name__ == '__main__':
    app.run(debug=True)
