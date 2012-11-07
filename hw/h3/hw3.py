"""
Programming Assignment 2
Handed out: 11/5/12
Due back: 11/14/12 by midnight
"""
import copy

class Polynomial(dict):
    """
    An instance of our class represents a specific polynomial in
    a single variable x, e.g. 3x^2 -11x + 10. In our example, the
    polynomial has three terms: 3x^2 (algebraically, this is 3*x*x)
    with coefficient 3 and exponent 2, the term -11x with coeffcient
    -11 and exponent 1, and the constant term 10 (with exponent 0
    and coefficient 10). Thus, each term of the polynomial
    has a unique, non-negative integer exponent and a corresponding
    integer coefficient.  This mapping is implemented by making our
    Polynomial class, a subclass of the builtin dict class (for
    dictionaries): the exponents are the keys and the coeffcients, the
    corresponding values. Only the terms with non-zero coefficients
    are maintained at any time. 

    Methods of the class support the usual algebraic operations for
    polynomials: binary addition, subtraction, and multiplication (by
    scalars and polynomials). The class also supports evaluation of
    instances at specific values of x. Finally, the class implements the
    first derivative of the polynomial with respect to x (from calculus).
    This is obtained by forming a polynomial as follows:

    * the derivative of the constant term is zero
    * the derivative of a term of the form c*x^n is equal to c*n*x^(n-1)

    For instance, the derivative of  2x^2 -10 -3x^3 is the polynomial 4x -9x^2.  
    """

    # this function is already implemented: do not change it!!
    def __init__(self, s=""):
        """Initialize the polynomial from a string respresentation

        The string is parsed to convert it to a representation
        that associates exponents (keys) with coefficients (values).

        s: string representing a polynomial

        >>> list(sorted(P0.items()))
        []
        >>> list(sorted(P1.items()))
        [(0, -10), (2, 2), (3, -3)]
        >>> list(sorted(P2.items()))
        [(0, 10), (1, -11)]
        """
        super()
        if s: 
            import re
            term = re.compile(r"""\s*                              # initial white space
                                                  ([+-]?[0-9]+)             # coefficient pattern group
                                                  \s*                               # intermediate white space
                                                  (x(\^([0-9]+))?)?      # optional exponent group
                                                  \s*                               # trailing white space""",
                              re.VERBOSE)
            while s:
                t = term.match(s)
                coeff = int(t.group(1))
                if t.group(4):                            # explicit exponent
                    expo = int(t.group(4))
                elif t.group(2):                        # implicit exponent (1)
                    expo = 1
                else:
                    expo = 0                              # constant term
                if coeff != 0:
                    self[expo] = coeff
                s = s[t.span(0)[1]:]

    def degree(self):
        """Return the largest exponent in any term of the polynomial

        >>> P0.degree()
        0
        >>> P1.degree()
        3
        """
        if not self.items():
            return 0
        else:
            return sorted(self.items(), reverse=True)[0][0]

    def __repr__(self):
        """Return a nice string representation of the polynomial

        Terms appear in decreasing order of exponent. The
        constant term, if zero, is only returned as part of the
        representation only if the polynomial itself is the zero
        polynomial. Each term is separated from its previous
        term by exactly one space. The sign of the leading term
        is omitted if the coefficient is non-negative. 

        >>> P0
        0
        >>> P1
        -3x^3 +2x^2 -10
        >>> P2
        -11x +10
        """
        terms = []
        for exp, coeff in sorted(self.items(), reverse=True):
            if exp == 0:
                terms.append("{:+}".format(coeff))
            elif exp == 1:
                terms.append("{:+}x".format(coeff))
            else:
                terms.append("{:+}x^{}".format(coeff, exp))
        if not terms:
            terms = ["0"]
        return " ".join(terms)

    def addTerm(self, expo, coeff):
        """Add a term to the polynomial with given coefficient and exponent

        coeff: integer
        expo: non-negative integer
        >>> P3.addTerm(1,11)
        >>> list(P3.items())
        [(0, 10)]
        """
        if expo in self:
            self[expo] += coeff
        else:
            self[expo] = coeff
        # Remove any keys where value (coefficient) is 0
        for k, v in list(self.items()):
            if v == 0:
                del self[k]
    
    def __add__(self,other):
        """Returns the polynomial obtained by adding self with other.

        other - a Polynomial object

        >>> P1+P2
        -3x^3 +2x^2 -11x
        >>> P = P2+P1
        >>> list(sorted(P.items()))
        [(1, -11), (2, 2), (3, -3)]
        """
        return Polynomial()

    def __mul__(self, other):
        """Returns the polynomial obtained by multiplying self with other.

        other - either an integer (scalar) or a Polynomial object

        >>> P1*0
        0
        >>> Q = P1*P2
        >>> Q
        33x^4 -52x^3 +20x^2 +110x -100
        >>> list(sorted(Q.items()))
        [(0, -100), (1, 110), (2, 20), (3, -52), (4, 33)]
        """
        return Polynomial()

    # this function is already implemented: do not change it!!
    def __rmul__(self, scalar):
        """Returns the polynomial obtained by multiplying it to a scalar

        >>> 3*P2
        -33x +30
        """
        return Polynomial()

    def __sub__(self,other):
        """Returns the polynomial obtained by subtracting other from self.

        other - a Polynomial object

        >>> P2 - P1
        3x^3 -2x^2 -11x +20
        >>> P = P2 - P1
        >>> list(sorted(P.items()))
        [(0, 20), (1, -11), (2, -2), (3, 3)]
        """
        return Polynomial()
    
            
    def __call__(self, x):
        """Return the result of evaluating the polynomial at x

        x: integer

        >>> P0(4)             # evaluate polynomial P0 at x=4
        0
        >>> P1(4)             # evaluate polynomial P1 at x=4
        -170
        >>> P2(1)
        -1
        """
        return 0

    def derivative(self):
        """Return the first derivative

        >>> P1.derivative()
        -9x^2 +4x
        >>> list(sorted(P1.derivative().items()))
        [(1, 4), (2, -9)]
        """
        result = Polynomial()
        [result.addTerm(exp - 1, coeff * exp) for exp, coeff in self.items()]
        return result


# Do not modify anything below this line!!!

P0 = Polynomial()
P1 = Polynomial('2x^2 -10 -3x^3 ')
P2 = Polynomial('10-11x')
P3 = copy.deepcopy(P2)

if __name__=="__main__":
    import doctest
    doctest.testmod()

