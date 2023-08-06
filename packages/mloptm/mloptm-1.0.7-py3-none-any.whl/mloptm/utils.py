import numpy as np
import sympy as sp
from sympy.parsing.sympy_parser import eval_expr
from mloptm.exceptions import ParsingExpressionError


def EvalExpr(f, variables):
    """
    Evaluate the expr f from string format to python function
    
    Parameters
    ----------
     - f (str) : the string representation of the function.
     - variabels (list) : the local variables of the function passed as list
     
    Returns
    -------
     - expr (func) : the function get evaluated.
     - symbols (list): the sympy symbols of the variables passed

    Raises
    ------
     - ParsingExpressionError : 
    """

    f = f.replace("^", "**")
    
    NUMPY_FUNCTIONS = {a: getattr(sp, a) for a in dir(sp)}

    symbols = sp.symbols(" ".join(variables))

    if not isinstance(symbols, (list, tuple)):
        symbols = [symbols]
    
    local_dict = {key: var for key, var in zip(variables, symbols)}
    
    expr = None
    
    try:
        expr = eval_expr(f, local_dict=local_dict, global_dict=NUMPY_FUNCTIONS)
    except Exception as e:
        raise ParsingExpressionError("error when parsing your expression,"\
                "please check the expression or the variables you are using.")
    
    return expr, symbols

