from flask import Flask, render_template, request, send_file
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/train_and_plot', methods=['POST'])
def train_and_plot():

    plot_path = 'path_to_generated_plot.png'
    
    return send_file(plot_path, mimetype='image/png')
