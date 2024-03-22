from flask import Flask, render_template, request, jsonify
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier, plot_tree, export_text
import matplotlib.pyplot as plt
import numpy as np
import io
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/train', methods=['POST'])
def train_model():
    # Load Iris Dataset
    iris = load_iris()
    X, y = iris.data, iris.target
    
    # Train Decision Tree Classifier
    clf = DecisionTreeClassifier()
    clf.fit(X, y)
    
    # Visualize Decision Tree
    plt.figure(figsize=(20,10))
    plot_tree(clf, filled=True, feature_names=iris.feature_names, class_names=iris.target_names)
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    
    # Export Decision Tree as Text
    tree_text = export_text(clf, feature_names=iris.feature_names)
    
    return jsonify({'image': plot_url, 'text': tree_text})

if __name__ == '__main__':
    app.run(debug=True)
