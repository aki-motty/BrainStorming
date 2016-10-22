#coding: UTF-8
a = 4
def getVarName( var, symboltable, error=None ) :
    """
    Return a var's name as a string.\nThis funciton require a symboltable(returned value of globals() or locals()) in the name space where you search the var's name.\nIf you set error='exception', this raise a ValueError when the searching failed.
    """
    for k,v in symboltable.iteritems() :
        if id(v) == id(var) :
            return k
    else :
        if error == "exception" :
            raise ValueError("Undefined function is mixed in subspace?")
        else:
            return error

print (getVarName(a,locals()))