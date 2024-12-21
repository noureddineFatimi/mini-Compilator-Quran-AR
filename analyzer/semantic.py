from .lexical import lexer, tokens  # Importer le lexer et les tokens
import ply.yacc as yacc
from .mini_dictionnaire import mini_dictionnaire
# Ordre attendu des versets
EXPECTED_VERSES = [
    "QUL HUWA ALLAHU AHADUN",
    "ALLAHU ALSSAMADU",
    "LAM YALID WALAM YOOLADU",
    "WALAM YAKUN LAHU KUFUWAN AHADUN"
]

V_arabe = {
    'QUL': 'قل',
    'HUWA':'هو',
    'ALLAHU':'الله',
    'AHADUN':'احد',
    'ALSSAMADU':'الصمد',
    'LAM':'لم',
    'YALID':'يلد',
    'WALAM':'ولم',
    'YOOLADU':'يولد',
    'YAKUN':'يكن',
    'LAHU':'له',
    'KUFUWAN':'كفوا'
}

# Fonction pour vérifier l'ordre des mots dans un verset
def check_verse_order(verse, expected_words):
    words = verse.split()
    if words != expected_words:

         # Traduire les mots en arabe en utilisant V_arabe
        translated_verse = ' '.join(V_arabe[word] for word in words if word in V_arabe)
        translated_expected = ' '.join(V_arabe[word] for word in expected_words if word in V_arabe)

        return False, f"  ترتيب الكلمات غير صحيح في الآية '{translated_verse}'، المتوقع: {translated_expected}"
    return True, None

# Fonction pour vérifier l'ordre des versets
def check_verses_order(input_verses):
    # Vérifier le nombre de versets avant l'ordre
    if len(input_verses) > len(EXPECTED_VERSES):
       return False, f"خطأ: عدد الآيات غير صحيح. المتوقع {len(EXPECTED_VERSES)} آية، لكن الموجود {len(input_verses)}."

    
    # Vérifier l'ordre des versets
    for i, verse in enumerate(input_verses):
        expected_words = EXPECTED_VERSES[i].split()
        valid, error_message = check_verse_order(verse, expected_words)
        
        if not valid:
            # Préciser quel verset est en erreur
            return False, f" خطأ في الآية رقم {i+1}: {error_message}."
  # Indiquer le numéro du verset avec l'erreur
    
    return True, "جميع الآيات تحترم الترتيب المتوقع."

# Reconstruction des versets à partir des tokens
def reconstruct_verses(tokens):
    input_verses = []
    current_verse = []
    for token in tokens:
        current_verse.append(token)
        # Si un verset est terminé (basé sur les mots de fin de chaque verset)
        if token in ['AHADUN', 'ALSSAMADU', 'YOOLADU', 'KUFUWAN']:
            input_verses.append(' '.join(current_verse))
            current_verse = []  # Réinitialiser pour le prochain verset

    # Vérification si le dernier verset est juste 'AHADUN' et fusion avec le précédent verset
    if len(input_verses) > 1:
        last_verse = input_verses[-1]
        second_last_verse = input_verses[-2]

        # Si le dernier verset est 'AHADUN' et que le verset précédent est 'WALAM YAKUN LAHU KUFUWAN', on fusionne
        if last_verse == 'AHADUN' and second_last_verse == 'WALAM YAKUN LAHU KUFUWAN':
            merged_verse = f"{second_last_verse} {last_verse}"
            input_verses[-2] = merged_verse  # Fusionner les deux versets
            input_verses.pop()  # Supprimer le verset 'AHADUN' maintenant fusionné

    return input_verses



# Analyse sémantique complète
def semantic_analysis(data):
    # Extraction des tokens (lexical)
    lexer.input(data)  # Passer les données au lexer
    tokens = [tok.type for tok in lexer]  # Extraire tous les tokens
    print("Tokens détectés par le lexer:", tokens)

    # Reconstruction des versets à partir des tokens
    input_verses = reconstruct_verses(tokens)

    print("Versets reconstruits :", input_verses)

    # Vérification de l'ordre des versets
    if len(input_verses) > len(EXPECTED_VERSES):
        return [f"خطأ: عدد الآيات غير صحيح. المتوقع {len(EXPECTED_VERSES)} آية، لكن الموجود {len(input_verses)}.", " "]

    valid, message = check_verses_order(input_verses)
    if not valid:
        return [message," "]

    if input_verses == []:
        return ["خطأ: ترتيب الكلمات غير صحيح أو الآية غير مكتملة", " "]

     # Si l'analyse est réussie, préparer les traductions
    translations = {"français": [], "anglais": [], "tamazight": []}
    for token in tokens:
        if token in mini_dictionnaire:
            for lang, translation in mini_dictionnaire[token].items():
                translations[lang].append(translation)

     # Fusionner les mots pour chaque langue
    for lang in translations:
        translations[lang] = " ".join(translations[lang])

    return ["النص الذي أدخلته صحيح.", translations]




# Test de l'analyseur sémantique
if __name__ == "__main__":
    data = "Qul huwa Allahu ahadun Allahu alssamadu  lam yalid walam yooladu walam yakun lahu kufuwan ahadun"
    result = semantic_analysis(data)
    print(result)
