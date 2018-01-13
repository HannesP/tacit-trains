def reflex(f):
    def g(x):
        return f(x,x)
    return g

def passive(f):
    def g(x,y):
        return f(y,x)
    return g

def constant(y):
    def f(*x):
        if len(x) > 2:
            raise Exception
        return y
    return f

def bond(a,b):
    def g(x):
        if callable(a):
            return a(x,b)
        elif callable(b):
            return b(a,x)
        return g
    return g

def left(*x):
	if len(x) == 0 or len(x) > 2:
		raise Exception
	return x[0]

def right(*x):
	if len(x) == 0 or len(x) > 2:
		raise Exception
	return x[-1]