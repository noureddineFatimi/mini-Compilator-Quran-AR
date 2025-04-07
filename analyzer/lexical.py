import ply.lex as lex
import difflib

# Liste des tokens arabes basés sur des règles régulières
tokens = [
    'QUL', 'HUWA', 'ALLAHU', 'AHADUN', 'ALSSAMADU', 
    'LAM', 'YALID', 'WALAM', 'YOOLADU', 'YAKUN', 
    'LAHU', 'KUFUWAN', 'ERROR'
]

# Définir chaque token à l'aide d'une expression régulière
def t_QUL(t):
    r'قل'
    return t

def t_HUWA(t):
    r'هو'
    return t

def t_ALLAHU(t):
    r'الله'
    return t

def t_AHADUN(t):
    r'احد'
    return t

def t_ALSSAMADU(t):
    r'الصمد'
    return t

def t_LAM(t):
    r'لم'
    return t

def t_YALID(t):
    r'يلد'
    return t

def t_WALAM(t):
    r'ولم'
    return t

def t_YOOLADU(t):
    r'يولد'
    return t

def t_YAKUN(t):
    r'يكن'
    return t

def t_LAHU(t):
    r'له'
    return t

def t_KUFUWAN(t):
    r'كفوا'
    return t

# Si aucun token valide n'est trouvé
def t_WORD(t):
    r'[a-zA-Z\u0600-\u06FF]+'  # Accepte tout mot arabe ou anglais
    t.type = 'ERROR'  # Considéré comme une erreur
    return t

# Fonction pour suggérer des corrections
def suggest_correction(word):
    valid_tokens = ['قل', 'هو', 'الله', 'احد', 'الصمد', 'لم', 'يلد', 'ولم', 'يولد', 'يكن', 'له', 'كفوا']
    suggestions = difflib.get_close_matches(word, valid_tokens, n=3, cutoff=0.6)
    if not suggestions:
        return "لا توجد اقتراحات متوفرة."
    return '، '.join(suggestions)

# Ignorer les espaces, tabulations et nouvelles lignes
t_ignore = ' \t\n'

# Gestion des erreurs lexicales
def t_error(t):
    error_message = f"حرف غير صالح: {t.value[0]} في الموضع {t.lexpos}. الكلمة '{t.value}' غير صالحة."
    correction = suggest_correction(t.value)
    print(f"{error_message} اقتراحات: {correction}")
    t.lexer.skip(1)

# Construire l'analyseur lexical
lexer = lex.lex()

# Fonction pour analyser une entrée textuelle
def analyze_lexical(input_data):
    errors = []
    lexer.input(input_data)
    for tok in lexer:
        if tok.type == 'ERROR':
            error_message = f"خطأ لغوي مكتشف: الكلمة '{tok.value}' غير صالحة," 
            suggestions = suggest_correction(tok.value)
            error_entry = f"{error_message} اقتراحات: {suggestions}"  
            errors.append(str(error_entry))  
    return errors 

# Exemple principal
if __name__ == "__main__":
    input_data = "قل هو الله احد ولم يولد"
    errors = analyze_lexical(input_data)
    if errors:
        print("\n".join(errors))
    else:
        print("النص صالح لغوياً.")
