from antlr4 import *
if __name__ is not None and "." in __name__:
    from .rGexParser import rGexParser
else:
    from rGexParser import rGexParser
    
from regex import *

# This class defines a complete listener for a parse tree produced by rGexParser.
class Visitor(ParseTreeListener):

    def __init__(self):
        self.stack = []
        self.setStack = []
        self.number = 0

    # Enter a parse tree produced by rGexParser#regex.
    def enterRegex(self, ctx:rGexParser.RegexContext):
        pass    

    # Exit a parse tree produced by rGexParser#regex.
    def exitRegex(self, ctx:rGexParser.RegexContext):
        if ctx.regex()!=None:   
            rhs = self.stack.pop()
            lhs = self.stack.pop()
            self.stack.append( RegEx(ALTERNATION,lhs,rhs))


    # Enter a parse tree produced by rGexParser#regex2.
    def enterRegex2(self, ctx:rGexParser.Regex2Context):
        #if ctx.regex2()!=None:
            #print("concatenation")
        #else:
            #print("enter regex2")
        pass

    # Exit a parse tree produced by rGexParser#regex2.
    def exitRegex2(self, ctx:rGexParser.Regex2Context):
        if ctx.regex2()!=None:
            rhs = self.stack.pop()
            lhs = self.stack.pop()
            self.stack.append( RegEx(CONCATENATION,lhs,rhs))
        

    # Enter a parse tree produced by rGexParser#regex3.
    def enterRegex3(self, ctx:rGexParser.Regex3Context):
        #print("enter regex3")
        pass

    # Exit a parse tree produced by rGexParser#regex3.
    def exitRegex3(self, ctx:rGexParser.Regex3Context):
        pass


    # Enter a parse tree produced by rGexParser#kleene.
    def enterKleene(self, ctx:rGexParser.KleeneContext):
        #print("enter kleene")
        pass

    # Exit a parse tree produced by rGexParser#kleene.
    def exitKleene(self, ctx:rGexParser.KleeneContext):
        rgx = self.stack.pop()
        self.stack.append( RegEx(STAR,rgx))
        pass


    # Enter a parse tree produced by rGexParser#plus.
    def enterPlus(self, ctx:rGexParser.PlusContext):
        #print("enter plus")
        pass

    # Exit a parse tree produced by rGexParser#plus.
    def exitPlus(self, ctx:rGexParser.PlusContext):
        rgx = self.stack.pop()
        self.stack.append( RegEx(PLUS,rgx))
        pass


    # Enter a parse tree produced by rGexParser#qmark.
    def enterQmark(self, ctx:rGexParser.QmarkContext):
        #print("enter qmark")
        pass

    # Exit a parse tree produced by rGexParser#qmark.
    def exitQmark(self, ctx:rGexParser.QmarkContext):
        rgx = self.stack.pop()
        self.stack.append( RegEx(MAYBE,rgx))
        pass
        
    # Enter a parse tree produced by rGexParser#repeat.
    def enterRepeat(self, ctx:rGexParser.RepeatContext):
        #print("enter repeat")
        pass

    # Exit a parse tree produced by rGexParser#repeat.
    def exitRepeat(self, ctx:rGexParser.RepeatContext):
        if ctx.single()!=None:
            pass
        else:
            rgx = self.stack.pop()
            snd = self.setStack.pop()
            fst = self.setStack.pop()
            self.stack.append( RegEx(RANGE,rgx,(fst,snd)) )
    
    # Enter a parse tree produced by rGexParser#simple.
    def enterSingle(self, ctx:rGexParser.SingleContext):
        #print("enter repeat")
        pass

    # Exit a parse tree produced by rGexParser#repeat.
    def exitSingle(self, ctx:rGexParser.SingleContext):
        rgx = self.stack.pop()
        fst = self.setStack.pop()
        self.stack.append( RegEx(RANGE,rgx,(fst,fst)) )


    # Enter a parse tree produced by rGexParser#rest.
    def enterRepeatAtom(self, ctx:rGexParser.RepeatAtomContext):
        #print("enter atom")
        pass

    # Exit a parse tree produced by rGexParser#rest.
    def exitRepeatAtom(self, ctx:rGexParser.RepeatAtomContext):
        if ctx.number()!=None:
            pass
        else:
            self.setStack.append(-1)
        #print(self.setStack[-1])
        pass

    # Enter a parse tree produced by rGexParser#regex4.
    def enterRegex4(self, ctx:rGexParser.Regex4Context):
        #print("enter regex4")
        pass

    # Exit a parse tree produced by rGexParser#regex4.
    def exitRegex4(self, ctx:rGexParser.Regex4Context):
        #print("done regex4")
        pass


    # Enter a parse tree produced by rGexParser#anY.
    def enterAnY(self, ctx:rGexParser.AnYContext):
        #print("enter any")
        pass

    # Exit a parse tree produced by rGexParser#anY.
    def exitAnY(self, ctx:rGexParser.AnYContext):
        self.stack.append( RegEx(SYMBOL_ANY))
        pass


    # Enter a parse tree produced by rGexParser#paranthesis.
    def enterParanthesis(self, ctx:rGexParser.ParanthesisContext):
        #print("enter aranthesis")
        pass

    # Exit a parse tree produced by rGexParser#paranthesis.
    def exitParanthesis(self, ctx:rGexParser.ParanthesisContext):
        pass


    # Enter a parse tree produced by rGexParser#seT.
    def enterSeT(self, ctx:rGexParser.SeTContext):
        #print("enter set") 
        pass

    # Exit a parse tree produced by rGexParser#seT.
    def exitSeT(self, ctx:rGexParser.SeTContext):
        aux=self.setStack
        #print(aux)
        self.stack.append( RegEx(SYMBOL_SET,aux))
        self.setStack=[]
        pass


    # Enter a parse tree produced by rGexParser#setvals.
    def enterSetvals(self, ctx:rGexParser.SetvalsContext):
        #print("enter set vals")
        pass

    # Exit a parse tree produced by rGexParser#setvals.
    def exitSetvals(self, ctx:rGexParser.SetvalsContext):
        if ctx.continut()!=None:
            rgx = self.stack.pop()
            self.setStack.append(rgx.symbol)
        pass


    # Enter a parse tree produced by rGexParser#continut.
    def enterContinut(self, ctx:rGexParser.ContinutContext):
        #print("enter continut")
        if ctx.DIGIT()!=None:
            self.stack.append( RegEx(SYMBOL_SIMPLE,str(ctx.DIGIT())))
        if ctx.LALPHA()!=None:
            self.stack.append(  RegEx(SYMBOL_SIMPLE,str(ctx.LALPHA())))
        if ctx.HALPHA()!=None:
            self.stack.append( RegEx(SYMBOL_SIMPLE,str(ctx.HALPHA())))
        #print("continut done")
        pass

    # Exit a parse tree produced by rGexParser#continut.
    def exitContinut(self, ctx:rGexParser.ContinutContext):
        pass


    # Enter a parse tree produced by rGexParser#rangE.
    def enterRangE(self, ctx:rGexParser.RangEContext):
        #print("enter range")
        pass

    # Exit a parse tree produced by rGexParser#rangE.
    def exitRangE(self, ctx:rGexParser.RangEContext):
        self.setStack.append( (ctx.children[0].symbol.text,ctx.children[2].symbol.text))
        pass

    # Enter a parse tree produced by rGexParser#rangE.
    def enterNumber(self, ctx:rGexParser.NumberContext):
        #print("enter number")
        pass

    # Exit a parse tree produced by rGexParser#rangE.
    def exitNumber(self, ctx:rGexParser.NumberContext):
        if ctx.number()!=None:
            self.number = self.number*10+int( str(ctx.DIGIT()))
        else:
            self.number = self.number*10+int( str(ctx.DIGIT()))
            self.setStack.append(self.number)
            self.number = 0
        pass

