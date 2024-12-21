from .lexical import lexer, tokens 
import ply.yacc as yacc
from .mini_dictionnaire import mini_dictionnaire

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

def check_verse_order(verse, expected_words):
    words = verse.split()
    if words != expected_words:
        translated_verse = ' '.join(V_arabe[word] for word in words if word in V_arabe)
        translated_expected = ' '.join(V_arabe[word] for word in expected_words if word in V_arabe)
        return False, f"  ترتيب الكلمات غير صحيح في الآية '{translated_verse}'، المتوقع: {translated_expected}"
    return True, None

def check_verses_order(input_verses):
    if len(input_verses) > len(EXPECTED_VERSES):
       return False, f"خطأ: عدد الآيات غير صحيح. المتوقع {len(EXPECTED_VERSES)} آية، لكن الموجود {len(input_verses)}."
    for i, verse in enumerate(input_verses):
        expected_words = EXPECTED_VERSES[i].split()
        valid, error_message = check_verse_order(verse, expected_words) 
        if not valid:
            return False, f" خطأ في الآية رقم {i+1}: {error_message}."    
    return True, "جميع الآيات تحترم الترتيب المتوقع."

def reconstruct_verses(tokens):
    input_verses = []
    current_verse = []
    for token in tokens:
        current_verse.append(token)
        if token in ['AHADUN', 'ALSSAMADU', 'YOOLADU', 'KUFUWAN']:
            input_verses.append(' '.join(current_verse))
            current_verse = []  
    if len(input_verses) > 1:
        last_verse = input_verses[-1]
        second_last_verse = input_verses[-2]
        if last_verse == 'AHADUN' and second_last_verse == 'WALAM YAKUN LAHU KUFUWAN':
            merged_verse = f"{second_last_verse} {last_verse}"
            input_verses[-2] = merged_verse  
            input_verses.pop()  
    return input_verses

def semantic_analysis(data):
    lexer.input(data)  
    tokens = [tok.type for tok in lexer] 
    print("Tokens détectés par le lexer:", tokens)
    input_verses = reconstruct_verses(tokens)
    print("Versets reconstruits :", input_verses)
    if len(input_verses) > len(EXPECTED_VERSES):
        return [f"خطأ: عدد الآيات غير صحيح. المتوقع {len(EXPECTED_VERSES)} آية، لكن الموجود {len(input_verses)}.", " "]
    valid, message = check_verses_order(input_verses)
    if not valid:
        return [message," "]
    if input_verses == []:
        return ["خطأ: ترتيب الكلمات غير صحيح أو الآية غير مكتملة", " "]
    translations = {"français": [], "anglais": [], "tamazight": []}
    for token in tokens:
        if token in mini_dictionnaire:
            for lang, translation in mini_dictionnaire[token].items():
                translations[lang].append(translation)
    for lang in translations:
        translations[lang] = " ".join(translations[lang])
    return ["النص الذي أدخلته صحيح.", translations]

if __name__ == "__main__":
    data = "Qul huwa Allahu ahadun Allahu alssamadu  lam yalid walam yooladu walam yakun lahu kufuwan ahadun"
    result = semantic_analysis(data)
    print(result)
