import ply.yacc as yacc
from .lexical import lexer, tokens 

versets = []

def p_start_single(p):
    "start : V1"
    versets.append("QUL HUWA ALLAHU AHADUN")  
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

parser = yacc.yacc()

if __name__ == "__main__":
    data = "Qul huwa Allahu ahadun Allahu alssamadu lam yalid walam yooladu"
    lexer.input(data) 
    tokens = [tok.type for tok in lexer]  
    print("Tokens détectés par le lexer:", tokens)
    parser.parse(data)  
    print("Versets extraits :", versets)
