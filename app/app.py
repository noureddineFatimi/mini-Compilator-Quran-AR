
from flask import Flask, render_template, request
import sys
import os

# Ajouter le répertoire racine du projet au PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Importer les fonctions depuis le package analyzer
from analyzer import analyze_lexical, semantic_analysis


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    lexical_errors = []
    semantic_result = []
    vailable=False
    translations = {}
        # Dans app.py
    if request.method == "POST":
        user_input = request.form["input_text"]
        
        # Vérification des erreurs lexicales
        lexical_errors = analyze_lexical(user_input)

        # Si lexical_errors contient des objets autres que des chaînes, on extrait les messages d'erreur
        if lexical_errors:
            
            result = ""

            #result = "Des erreurs lexicales ont été détectées.\n" + lexical_errors
            #lexical_errors = [str(error) for error in lexical_errors]  # Assurez-vous que lexical_errors est une liste de chaînes
            #result = "\n".join(lexical_errors)  # Afficher les erreurs lexicales si elles existent
        else:
            # Si l'analyse lexicale est réussie, faire l'analyse sémantique
            semantic_result = semantic_analysis(user_input)
            if "خطأ" in semantic_result[0]:
                result = semantic_result[0]  # Afficher l'erreur sémantique
            else:
                vailable=True
                result = semantic_result[0]
                translations = semantic_result[1]
               

    return render_template("index.html", result=result, lexical_errors=lexical_errors,vailable=vailable,translations=translations)

if __name__ == "__main__":
    app.run(debug=True)
