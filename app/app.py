
from flask import Flask, render_template, request
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from analyzer import analyze_lexical, semantic_analysis,log_error

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    lexical_errors = []
    semantic_result = []
    vailable=False
    translations = {}
    if request.method == "POST":
        user_input = request.form["input_text"]
        lexical_errors = analyze_lexical(user_input)
        if lexical_errors:
            result = ""
            log_error(lexical_errors)
        else:
            semantic_result = semantic_analysis(user_input)
            if "خطأ" in semantic_result[0]:
                result = semantic_result[0] 
                log_error(result)
            else:
                vailable=True
                result = semantic_result[0]
                translations = semantic_result[1]
    return render_template("index.html", result=result, lexical_errors=lexical_errors,vailable=vailable,translations=translations)

if __name__ == "__main__":
    app.run(debug=True)
