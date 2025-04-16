# BreachCTF 2025 - Fraction Fun

- Author: Niral
- Flag: Breach{0n3_0f_c0nw4y5_7ur1n6_c0mpl373_w0nd3r5}



## Challenge Description

> My friend has created a fun game to play with fractions. He wants a particular output from the game. Can you find the correct input and crack the puzzle!
> [server](./server.py)
> [output](./output.txt)
> [code](./code.txt)

## Write up

Looking at server.py we find that it takes a number as input and then performs certain operations on it.
Finally it checks that the result of the operations must equal a particular number (final_output).

Let us go into the specifics of the code now:

```python
def execute(code, inp):
    values = code.split(" ")
    inp = int(inp)
    a = [int(i.split("/")[0]) for i in values]
    b = [int(i.split("/")[1]) for i in values]
    broken = False
    for _ in range(1000):
        changed = False
        for i in range(len(a)):
            if inp % b[i] == 0:
                inp = inp * a[i] // b[i]
                changed = True
        if not changed:
            broken = True
            break
    if not broken:
        print("Loop did not terminate in 1000 iterations!")
        return inp
    return inp
```

So the excecute function loops through the code, checking if the current value of the inp (initially the input) is divisible by b[i] if it is then input is changed to inp * a[i] / b[i].

This 'atomic' instruction can actually be reversed directly. 
Specifically we could loop through the reverse of the code, check if inp * b[i] is divisible by a[i]. If it is then set inp to inp * b[i] / a[i].

The following code segment does this:


```python
def execute_reverse(code, inp):
    values = code.split(" ")
    inp = int(inp)
    a = [int(i.split("/")[0]) for i in values]
    b = [int(i.split("/")[1]) for i in values]
    a = a[::-1]
    b = b[::-1]
    broken = False
    for _ in range(1000):
        changed = False
        for i in range(len(a)):
            if (inp * b[i]) % a[i] == 0:
                inp = inp * b[i] // a[i]
                changed = True
        if not changed:
            broken = True
            break
    if not broken:
        print("Loop did not terminate in 1000 iterations!")
        return inp
    return inp
```

Now to find the input that gives fin_output as its output we can simply run


```python
print(execute_reverse(code, fin_output))

# Check that this reversing works
assert(execute(code, execute_reverse(code, fin_output)) == fin_output)
```

The assertion passes and the value that's printed is the following:
```
859583601094064447752388276273759079492792499046350851378922618771547160802030329860897670972485616052135161182028125
```
We can give it to the server to get the flag.
