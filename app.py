from flask import Flask, render_template, request, redirect, url_for, send_file
import matplotlib.pyplot as plt
import pandas as pd
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    
    if file:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        return redirect(url_for('display_chart', filename=file.filename))

@app.route('/chart/<filename>')
def display_chart(filename):
    # Read CSV file into a DataFrame
    data = pd.read_csv(os.path.join(UPLOAD_FOLDER, filename))
    
    # Check the number of columns
    num_columns = data.shape[1]
    
    # Create charts based on the number of columns
    if num_columns == 1:
        plt.figure(figsize=(10, 6))
        plt.hist(data.iloc[:, 0], bins=10, color='g', alpha=0.7)
        plt.xlabel(data.columns[0])
        plt.ylabel('Frequency')
        plt.title(f'Histogram of {data.columns[0]}')
    elif num_columns == 2:
        plt.figure(figsize=(10, 6))
        plt.bar(data.iloc[:, 0], data.iloc[:, 1], color='g', width=0.72)
        plt.xlabel(data.columns[0])
        plt.ylabel(data.columns[1])
        plt.title(f'Bar Chart of {data.columns[0]} vs {data.columns[1]}')
    else:
        # For more than two columns, use a line chart for the first two columns
        plt.figure(figsize=(10, 6))
        for i in range(1, num_columns):
            plt.plot(data.iloc[:, 0], data.iloc[:, i], label=data.columns[i])
        plt.xlabel(data.columns[0])
        plt.ylabel('Values')
        plt.title(f'Line Chart of {data.columns[0]} vs Other Columns')
        plt.legend()
    
    # Save chart as an image file
    chart_path = os.path.join(UPLOAD_FOLDER, 'chart.png')
    plt.savefig(chart_path)
    plt.close()
    
    return send_file(chart_path, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
