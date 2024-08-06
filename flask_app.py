from flask import Flask, request, jsonify, render_template
from main import converse_with_vendor, get_summary, get_next_step_for_bride

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    data = request.get_json()
    user_input = data.get('input_text')
    
    response = converse_with_vendor("sk-no-key-required", user_input, 'wendyplanterweddings@gmail.com', 'nqel uytt fzxn iqbr', 'abneyjohnson0@gmail.com')
    return jsonify({'output': response})

@app.route('/summary', methods=['GET'])
def summary():
    summary = get_summary("sk-no-key-required")
    return jsonify({'summary': summary})

@app.route('/next_step', methods=['GET'])
def next_step():
    next_step = get_next_step_for_bride("sk-no-key-required")
    return jsonify({'next_step': next_step})

if __name__ == "__main__":
    app.run(debug=True)
