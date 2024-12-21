import ply.lex as lex
import difflib  # Pour la suggestion de mots similaires

# Liste des mots clés à identifier
reserved = {
   'قل': 'QUL',
    'هو': 'HUWA',
    'الله': 'ALLAHU',
    'احد': 'AHADUN',
    'الصمد': 'ALSSAMADU',
    'لم': 'LAM',
    'يلد': 'YALID',
    'ولم': 'WALAM',
    'يولد': 'YOOLADU',
    'يكن': 'YAKUN',
    'له': 'LAHU',
    'كفوا': 'KUFUWAN'
}


# Définition des tokens (inclut les mots réservés)
tokens = list(reserved.values()) + ['ERROR']

def t_WORD(t):
    r'[a-zA-Z\u0600-\u06FF]+'  # Ajoute les caractères arabes (Unicode U+0600 à U+06FF)
    if t.value in reserved:
        t.type = reserved[t.value]  # Vérifie si le mot est réservé
    else:
        t.type = 'ERROR'  # Marque comme erreur si le mot n'est pas valide
    return t


def suggest_correction(word):
    suggestions = difflib.get_close_matches(word, reserved.keys(), n=3, cutoff=0.6)
    if not suggestions:
        return "لا توجد اقتراحات متوفرة."
    return '، '.join(suggestions)


# Ignorer les espaces et les nouvelles lignes
t_ignore = ' \t\n'

# Gérer les erreurs lexicales
def t_error(t):
    error_message = f"Caractère invalide: {t.value[0]} à la position {t.lexpos}. Le mot '{t.value}' n'est pas valide."
    
    # Suggérer des corrections en cas d'erreur
    correction = suggest_correction(t.value)
    
    # On ne renvoie pas un message d'erreur mais on effectue les suggestions
    print(f"{error_message} Suggestions: {correction}")
    t.lexer.skip(1)

lexer = lex.lex()

def analyze_lexical(input_data):
    errors = []
    lexer.input(input_data)
    
    for tok in lexer:
        if tok.type == 'ERROR':
            error_message = f"خطأ لغوي مكتشف: الكلمة '{tok.value}' غير صالحة," 
            suggestions = suggest_correction(tok.value)
            error_entry = f"{error_message} اقتراحات: {suggestions}"  # Pas de retour à la ligne ici
            errors.append(str(error_entry))  # On ajoute directement le message d'erreur à la liste
    
    # Retourner les erreurs sous forme de chaîne avec un seul retour à la ligne entre les erreurs
    return errors 
    # return "\n".join(errors) if errors else "Aucune erreur lexicale détectée."




if __name__ == "__main__":
    input = "Ql huwa allahu ahadun"
    print(analyze_lexical(input))
