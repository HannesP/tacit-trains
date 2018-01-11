# tacit-trains

This is a rough Python adaption of a feature from J [(link)](http://www.jsoftware.com), called "verb trains". The construct normally known as functions is called verbs in J, and a train is formed by a sequence of such verbs.

## What is tacit programming?

I’ll quote Wikipedia:

> Tacit programming, also called point-free style, is a programming paradigm in which function definitions do not identify the arguments (or "points") on which they operate. Instead the definitions merely compose other functions, among which are combinators that manipulate the arguments.

### Is this useful?

Probably not directly. It’s meant to demonstrate a topic using familiar tools. Maybe (hopefully!) it could inspire somebody to approach problem solving differently.

## Forks

A fork is formed by three functions, and is itself a function. There are two flavours: unary and binary.

    fork(f, g, h)(y) ⇔ g(f(y), h(y))
    fork(f, g, h)(x, y) ⇔ g(f(x,y), h(x,y))

### Examples

The ubiquitous arithmetic mean:

```python
from operator import truediv as div
from tacit import fork

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

The other special case concerns something called *capping*. This makes `g` behave as a unary function, and is achieved by passing `f` as `None`. Example:

```python
def inv(x):
    return 1/x

parse_and_inv = fork(None, inv, int)
res = parse_and_inv('5') # 0.2
```
    
## Hooks

A hook is formed by two functions.

    hook(f, g)(y) ⇔ f(y, g(y))
    fork(f, g)(x, y) ⇔ f(x, g(y))

## Trains

A train is a way to string together a longer sequence of functions according to the following pattern:

    train(f, g) ⇔ hook(f, g)
    train(f, g, h) ⇔ fork(f, g, h)
    train(…, f, g, h) ⇔ train(…, fork(f, g, h))
    
### Example

A function to underline a string with dashes:

```python
from operator import add, mul
from tacit import train

underline = train(add, '\n', add, '-', mul, len)
print(underline('clackety-clack'))
```

Result:

    clackety-clack
    --------------

Equivalent, without using `train()`:

```python
from operator import add, mul
from tacit import fork, hook

to_line = fork('-', mul, len) # e.g. 'abcde' -> '-----'
newline = fork('\n', add, to_line) # e.g. '-----' -> '\n-----'
underline = hook(add, newline)
print(underline('clackety-clack'))
```