def reflex(f):
    def q(x):
        return f(x,x)
    return q

def passive(f):
    def q(x,y):
        return f(y,x)
    return q

def constant(y):
    def f(*x):
        if len(x) > 2:
            raise Exception
        return y
    return f

def bond(a,b):
    def q(x):
        if callable(a):
            return a(x,b)
        elif callable(b):
            return b(a,x)
        return q
	return q