import ply.lex as lex
import difflib

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

tokens = list(reserved.values()) + ['ERROR']

def t_WORD(t):
    r'[a-zA-Z\u0600-\u06FF]+'  
    if t.value in reserved:
        t.type = reserved[t.value]  
    else:
        t.type = 'ERROR'  
    return t

def suggest_correction(word):
    suggestions = difflib.get_close_matches(word, reserved.keys(), n=3, cutoff=0.6)
    if not suggestions:
        return "لا توجد اقتراحات متوفرة."
    return '، '.join(suggestions)

t_ignore = ' \t\n'

def t_error(t):
    error_message = f"Caractère invalide: {t.value[0]} à la position {t.lexpos}. Le mot '{t.value}' n'est pas valide."
    correction = suggest_correction(t.value)
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
            error_entry = f"{error_message} اقتراحات: {suggestions}"  
            errors.append(str(error_entry))  
    return errors 

if __name__ == "__main__":
    input = "Ql huwa allahu ahadun"
    print(analyze_lexical(input))
