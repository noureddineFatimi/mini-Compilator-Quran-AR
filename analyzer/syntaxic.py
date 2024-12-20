import ply.yacc as yacc
from .lexical import lexer, tokens  # Importer lexer et tokens

# Variables pour stocker les versets extraits
versets = []

# Règles de production pour le parser
def p_start_single(p):
    "start : V1"
    versets.append("QUL HUWA ALLAHU AHADUN")  # Ajouter le verset complet au résultat
    print("Structure syntaxique valide : V1.")

def p_start_two(p):
    "start : V1 V2"
    versets.append("QUL HUWA ALLAHU AHADUN")
    versets.append("ALLAHU ALSSAMADU")
    print("Structure syntaxique valide : V1 V2.")

def p_start_three(p):
    "start : V1 V2 V3"
    versets.append("QUL HUWA ALLAHU AHADUN")
    versets.append("ALLAHU ALSSAMADU")
    versets.append("LAM YALID WALAM YOOLADU")
    print("Structure syntaxique valide : V1 V2 V3.")

def p_start_four(p):
    "start : V1 V2 V3 V4"
    versets.append("QUL HUWA ALLAHU AHADUN")
    versets.append("ALLAHU ALSSAMADU")
    versets.append("LAM YALID WALAM YOOLADU")
    versets.append("WALAM YAKUN LAHU KUFUWAN AHADUN")
    print("Structure syntaxique valide : V1 V2 V3 V4.")

def p_V1(p):
    "V1 : قل هو الله أحد"
    pass

def p_V2(p):
    "V2 : الله الصمد"
    pass

def p_V3(p):
    "V3 : لم يلد ولم يولد"
    pass

def p_V4(p):
    "V4 : ولم يكن له كفوا أحد"
    pass


def p_error(p):
    print("Erreur syntaxique détectée.")

# Construire l'analyseur syntaxique
parser = yacc.yacc()

# Test de l'analyseur syntaxique
if __name__ == "__main__":
    data = "Qul huwa Allahu ahadun Allahu alssamadu lam yalid walam yooladu"
    lexer.input(data)  # Passer les données au lexer
    tokens = [tok.type for tok in lexer]  # Extraire tous les tokens
    print("Tokens détectés par le lexer:", tokens)
    
    parser.parse(data)  # Passer les données au parser
    print("Versets extraits :", versets)
