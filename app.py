from flask import Flask, request, jsonify
from transformers import pipeline
import os

app = Flask(__name__)
summarizer = pipeline("summarization")

@app.route('/summarize', methods=['POST'])
def summarize():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Save the file temporarily
    file_path = os.path.join('uploads', file.filename)
    file.save(file_path)

    # Read the file and summarize
    with open(file_path, 'r') as f:
        text = f.read()
    
    summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
    
    # Clean up the uploaded file
    os.remove(file_path)

    return jsonify({'summary': summary[0]['summary_text']})

if __name__ == '__main__':
    app.run(debug=True)