import matplotlib
matplotlib.use('Agg')  # Use non-interactive Agg backend

from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from werkzeug.utils import secure_filename
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier, plot_tree, export_text, _tree
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import io
import base64
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'csv', 'xlsx'}
app.secret_key = 'your_secret_key_here'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def tree_to_o1js(tree, feature_names):
    tree_ = tree.tree_
    feature_name = [
        feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]
    feature_names = [f.replace(" ", "_")[:-5] for f in feature_names]

    js_snippet = ["const DecisionTree = ZkProgram({",
                  "    name: 'DecisionTree',",
                  "    publicOutput: Field,",
                  "methods: {",
                  "    predict: {",
                  "        privateInputs: [{}],".format(", ".join(["Field"] * len(feature_names))),
                  "        method({}): Field {{".format(", ".join(feature_names))]

    def recurse(node, depth):
        indent = "    " * (depth+2)
        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            name = feature_name[tree_.feature[node]]
            threshold = tree_.threshold[node]

            if depth == 1:
                js_snippet.append("{}return Provable.if({}.lessThan(Field({})), ".format(indent, name, int(np.round(threshold * 100,0))))
            else:
                js_snippet.append("{}Provable.if({}.lessThan(Field({})), ".format(indent, name, int(np.round(threshold * 100,0))))
            recurse(tree_.children_left[node], depth + 1)
            js_snippet.append("{}, ".format(indent))
            recurse(tree_.children_right[node], depth + 1)
            if depth == 1:
                js_snippet.append("{});".format(indent))
            else:
                js_snippet.append("{})".format(indent))
        else:
            js_snippet.append("{}Field({})".format(indent, np.argmax(tree_.value[node])))

    recurse(0, 1)
    js_snippet += ["        },",
                   "    },",
                   "},",
                   "});"]
    
    return "\n".join(js_snippet)

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
    js_tree = tree_to_o1js(clf, feature_names=iris['feature_names'] if 'iris' in request.form.values() else data.columns[:-1])
    
    return jsonify({'image': plot_url, 'text': tree_text, 'js_tree': js_tree})

if __name__ == '__main__':
    app.run(debug=True)
