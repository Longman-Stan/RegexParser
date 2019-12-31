from regex import *
import string

EMPTY_SET = 0
EMPTY_STRING = 1
SYMBOL = 2
STAR = 3
CONCATENATION = 4
ALTERNATION = 5

_SIMPLE_TYPES = {EMPTY_SET, EMPTY_STRING, SYMBOL}

def str_paranthesize(parent_type, re):
    if parent_type > re.type or parent_type == re.type and parent_type != STAR:
        return str(re)
    else:
        return "({!s})".format(str(re))
       
def normalize_to_tuple(e):
            """Allows us to sort sets containing both symbols and ranges

            This is needed in order to deterministically represent a symbol set
            as a string; namely all single characters first (in alphabetical
            order), followed by all ranges.

            """
            if isinstance(e, str):
                return (e, "")
            return e
    
def regex_to_reg(rgx):
    tp = rgx.type
    if tp == 0:
        return RegularExpression(EMPTY_STRING)
    if tp == 1:
        return RegularExpression(SYMBOL,rgx.symbol)
    if tp == 2:
        reg = RegularExpression(SYMBOL,'0')
        for i in range(1,10):
            reg = RegularExpression(ALTERNATION,reg,RegularExpression(SYMBOL,i))
        for i in string.ascii_lowercase:
            reg = RegularExpression(ALTERNATION,reg,RegularExpression(SYMBOL,i))
        for i in string.ascii_uppercase:
            reg = RegularExpression(ALTERNATION,reg,RegularExpression(SYMBOL,i))
        return reg
    if tp == 3:
        reg = RegularExpression(EMPTY_SET)
        for i in sorted(rgx.symbol_set, key=normalize_to_tuple):
            if isinstance(i,tuple):
                if i[0].isalpha():
                    for j in range(ord(i[0]),ord(i[1])+1):
                        if reg.type!=EMPTY_SET:
                            reg = RegularExpression(ALTERNATION,reg,RegularExpression(SYMBOL,chr(j)))
                        else:
                            reg = RegularExpression(SYMBOL,chr(j))
                else:
                    for j in range(int(i[0]),int(i[1])+1):
                        if reg.type!=EMPTY_SET:
                            reg = RegularExpression(ALTERNATION,reg,RegularExpression(SYMBOL,str(j)))
                        else:
                            reg = RegularExpression(SYMBOL,str(j))
            else:
                if reg.type!=EMPTY_SET:
                    reg = RegularExpression(ALTERNATION,reg,RegularExpression(SYMBOL,i))
                else:
                    reg = RegularExpression(SYMBOL,i)
        return reg
    if tp == 4:
        reg = regex_to_reg(rgx.lhs)
        return RegularExpression(ALTERNATION,reg,RegularExpression(EMPTY_STRING))
    if tp == 5:
        reg = regex_to_reg(rgx.lhs)
        return RegularExpression(STAR,reg)
    if tp == 6:
        reg = regex_to_reg(rgx.lhs)
        return RegularExpression(CONCATENATION,reg,RegularExpression(STAR,reg))
    if tp == 7:
        st = rgx.range[0]
        dr = rgx.range[1]
        i=0;
        base_reg = regex_to_reg(rgx.lhs)
        if st==-1:
            st=0
        reg = RegularExpression(EMPTY_STRING)
        while i<st:
            if reg.type!=EMPTY_STRING:
                reg= RegularExpression(CONCATENATION,reg,base_reg)
            else:
                reg = base_reg
            i+=1
        if dr==-1:
            if reg.type!=EMPTY_STRING:
                reg = RegularExpression(CONCATENATION,reg,RegularExpression(STAR,base_reg))
            else:
                reg = RegularExpression(STAR,base_reg)
        else:
            regaux=reg
            while i<dr:
                if reg.type!=EMPTY_STRING:
                    regaux = RegularExpression(CONCATENATION,regaux,base_reg)
                    reg = RegularExpression(ALTERNATION,reg,regaux)
                else:
                    regaux = base_reg
                    reg = regaux
                i+=1
        return reg
    if tp == 8:
        r1 = regex_to_reg(rgx.lhs)
        r2 = regex_to_reg(rgx.rhs)
        return RegularExpression(CONCATENATION,r1,r2)
    if tp == 9:
        r1 = regex_to_reg(rgx.lhs)
        r2 = regex_to_reg(rgx.rhs)
        return RegularExpression(ALTERNATION,r1,r2)
    
class RegularExpression(object):
    """Model a Regular Expression TDA

    The member "type" is always available, indicating the type of the
    RegularExpression. Its value dictates which other members (if any) are
    defined:

        - EMPTY_SET:
        - EMPTY_STRING:
        - SYMBOL: "symbol" is the symbol
        - STAR: "lhs" is the RegularExpression
        - CONCATENATION: "lhs" and "rhs" are the RegularExpressions
        - ALTERNATION: "lhs" and "rhs" are the RegularExpressions
    """
    
    def __init__(self, type, obj1=None, obj2=None):
        """Create a Regular Expression

        The value of the "type" parameter influences the interpretation of the
        other two paramters:

            - EMPTY_SET: obj1 and obj2 are unused
            - EMPTY_STRING: obj1 and obj2 are unused
            - SYMBOL: obj1 should be a symbol; obj2 is unused
            - STAR: obj1 should be a RegularExpression; obj2 is unused
            - CONCATENATION: obj1 and obj2 should be RegularExpressions
            - ALTERNATION: obj1 and obj2 should be RegularExpressions

        """
        self.type = type
        if type in _SIMPLE_TYPES:
            if type == SYMBOL:
                assert obj1 is not None
                self.symbol = obj1
        else:
            assert isinstance(obj1, RegularExpression)
            self.lhs = obj1
            if type == CONCATENATION or type == ALTERNATION:
                assert isinstance(obj2, RegularExpression)
                self.rhs = obj2

    def __str__(self):
        if self.type == EMPTY_SET:
            return "∅"
        elif self.type == EMPTY_STRING:
            return "ε"
        elif self.type == SYMBOL:
            return str(self.symbol)
        elif self.type == CONCATENATION:
            slhs = str_paranthesize(self.type, self.lhs)
            srhs = str_paranthesize(self.type, self.rhs)
            return slhs + srhs
        elif self.type == ALTERNATION:
            slhs = str_paranthesize(self.type, self.lhs)
            srhs = str_paranthesize(self.type, self.rhs)
            return slhs + "|" + srhs
        elif self.type == STAR:
            slhs = str_paranthesize(self.type, self.lhs)
            return slhs + "*"
        else:
            return ""

    def __mul__(self, rhs):
        """Concatenation"""
        if isinstance(rhs, str) and len(rhs) == 1:
            rhs = RegularExpression(SYMBOL, rhs)

        assert isinstance(rhs, RegularExpression)
        return RegularExpression(CONCATENATION, self, rhs)

    __rmul__ = __mul__

    def __or__(self, rhs):
        """Alteration"""
        if isinstance(rhs, str) and len(rhs) == 1:
            rhs = RegularExpression(SYMBOL, rhs)

        assert isinstance(rhs, RegularExpression)
        return RegularExpression(ALTERNATION, self, rhs)

    __ror__ = __or__

    def star(self):
        return RegularExpression(STAR, self)
