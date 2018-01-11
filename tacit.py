def fork(f,g,h):
    if f is None:
        def q(*x):
            if len(x) == 1:
                return g(h(x[0]))
            elif len(x) == 2:
                return g(h(x[0],x[1]))
            else:
                raise
        return q
    elif not callable(f):
        def q(*x):
            if len(x) == 1:
                return g(f, h(x[0]))
            elif len(x) == 2:
                return g(f, h(x[0],x[1]))
            else:
                raise
        return q
    else:
        def q(*x):
            if len(x) == 1:
                return g(f(x[0]), h(x[0]))
            elif len(x) == 2:
                return g(f(x[0],x[1]), h(x[0],x[1]))
            else:
                raise
        return q

def hook(f,g):
    def q(*x):
        if len(x) == 1:
            return f(x[0], g(x[0]))
        elif len(x) == 2:
            return f(x[0], g(x[1]))
        else:
            raise
    return q

def train(*fs):
    while len(fs) >= 3:
        rem, head = fs[:-3], fs[-3:]
        fs = rem + (fork(*head),)
    if len(fs) == 2:
        return hook(*fs)
    else:
        return fs[0]