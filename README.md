# tacit-trains

This is a rough Python adaption of a feature from J [(link)](http://www.jsoftware.com), called "verb trains". The construct normally known as functions is called verbs in J, and a train is formed by a sequence of such verbs.

## What is tacit programming?

I’ll quote Wikipedia:

> Tacit programming, also called point-free style, is a programming paradigm in which function definitions do not identify the arguments (or "points") on which they operate. Instead the definitions merely compose other functions, among which are combinators that manipulate the arguments.

### Is this useful?

Probably not directly. It’s meant to demonstrate a topic using familiar tools. Maybe (hopefully!) it could inspire somebody to approach problem solving differently.

## Tacit utilities

Defined in `tacit.utils`:

    reflex(f)(x) ⇔ f(x, x)
    passive(f)(x, y) ⇔ f(y, x)

    bond(f, y)(x) ⇔ f(x, y)
    bond(x, f)(y) ⇔ f(x, y)
    
    constant(c)(x[, y]) ⇔ c
    left(x, y) ⇔ x
    right(x, y) ⇔ y

## Forks

A fork is formed by three functions, and is itself a function. There are two flavours: unary and binary.

    fork(f, g, h)(y) ⇔ g(f(y), h(y))
    fork(f, g, h)(x, y) ⇔ g(f(x, y), h(x, y))

### Examples

The ubiquitous arithmetic mean:

```python
from operator import truediv as div
from tacit.trains import fork

avg = fork(sum, div, len)
res = avg([1, 7, 2, 2, 9]) # 4.2
```

Notice the syntactic similarity to English – `fork(sum, div, len)` and “*sum* *div*ided by *len*gth”. No x is mentioned!

### Advanced

There are two special cases. When `f` isn't callable, i.e. when it’s a value rather than a function, it's treated as a constant function. Example:

```python
from operator import add
sum_plus_10 = fork(10, add, sum)
res = sum_plus_10([1,2,3]) # 16
```

The other special case concerns something called *capping*. This makes `g` behave as a unary function, and is achieved by passing `f` as `None`.

    fork(None, g, h)(y) ⇔ g(h(y))
    fork(None, g, h)(x, y) ⇔ g(h(x,y))

Example:

```python
def inv(x):
    return 1/x

parse_and_inv = fork(None, inv, int)
res = parse_and_inv('5') # 0.2, equivalent to inv(int('5'))
```
    
## Hooks

A hook is formed by two functions.

    hook(f, g)(y) ⇔ f(y, g(y))
    fork(f, g)(x, y) ⇔ f(x, g(y))

## Trains

A train is a generalisation of hooks and forks. According to the below pattern, any non-zero number of functions can be stringed together to recursively form a train.

    train(f) ⇔ f
    train(f, g) ⇔ hook(f, g)
    train(f, g, h) ⇔ fork(f, g, h)
    train(…, f, g, h) ⇔ train(…, train(f, g, h))
    
### Example

A function to underline a string with dashes:

```python
from operator import add, mul
from tacit.trains import train

underline = train(add, '\n', add, '-', mul, len)
print(underline('clackety-clack'))
```

Result:

    clackety-clack
    --------------

Equivalent, without using `train()`:

```python
from operator import add, mul
from tacit.trains import fork, hook

to_line = fork('-', mul, len) # e.g. 'abcde' -> '-----'
prepend_newline_to_line = fork('\n', add, to_line) # e.g. '-----' -> '\n-----'
underline = hook(add, prepend_newline_to_line)
print(underline('clackety-clack'))
```

### Longer example

This example demonstrates composing a function to calculate the sample standard deviation using a train of simple functions.

```python
from tacit.trains import train
from tacit.utils import passive, reflex

from operator import add, sub, mul, truediv as div
from math import sqrt

std = train(None, sqrt, train(-1, add, len), passive(div), None, sum, None, reflex(mul), train(sub, sum, div, len))