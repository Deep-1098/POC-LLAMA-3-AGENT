from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


def generate_text_with_ollama(prompt, max_length=100):
    url = "http://127.0.0.1:11434/api/generate"
    data = {
        "model": "llama3.2",
        "prompt": prompt,
        "stream":False
    }
    
    try:
        response = requests.post(url, json=data)
        result = response.json()
        return result.get("response", "No response from the model.")
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"
    

@app.route('/text-generation', methods=['POST'])
def text_generation():
    topic = request.json.get('story')
    prompt = f"Write a story on {topic} In less than or equal to 50 words."
    generated_text = generate_text_with_ollama(prompt)
    return jsonify({"response": generated_text})


@app.route('/conversation', methods=['POST'])
def conversation():
    prompt = request.json.get('prompt')
    prompt += "In less than or equal to 50 words."
    generated_text = generate_text_with_ollama(prompt)
    return jsonify({"response": generated_text})


@app.route('/summarize', methods=['POST'])
def summarize():
    document = request.json.get('document')
    prompt = f"Summarize the following document in less than 50 words: {document}"
    generated_text = generate_text_with_ollama(prompt)
    return jsonify({"response": generated_text})


@app.route('/code-generation', methods=['POST'])
def code_generation():
    prompt = "Write a Python function that takes a list of numbers and returns the sum of all even numbers."
    generated_text = generate_text_with_ollama(prompt)
    return jsonify({"response": generated_text})


if __name__ == '__main__':
    app.run(debug=True)
