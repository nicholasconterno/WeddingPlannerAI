from flask import Flask, request, jsonify, render_template
from main import converse_with_vendor, get_summary, get_next_step_for_bride

app = Flask(__name__)


@app.route("/")
def home():
    """
    Home page
    """
    return render_template("index.html")


@app.route("/query", methods=["POST"])
def query():
    """
    Query the AI model"""
    data = request.get_json()
    user_input = data.get("input_text")
    # get venfor email from the form
    vendor_email = data.get("vendor_email")
    response = converse_with_vendor(
        "sk-no-key-required",
        user_input,
        "wendyplanterweddings@gmail.com",
        "nqel uytt fzxn iqbr",
        vendor_email,
    )
    return jsonify({"output": response})


@app.route("/summary", methods=["GET"])
def summary():
    """
    Get the summary of the information gathered"""
    summary = get_summary("sk-no-key-required")
    return jsonify({"summary": summary})


@app.route("/next_step", methods=["GET"])
def next_step():
    """
    Get the next step for the bride based on the summary of the information gathered"""
    next_step = get_next_step_for_bride("sk-no-key-required")
    return jsonify({"next_step": next_step})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
