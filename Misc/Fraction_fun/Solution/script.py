import numpy as np

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


code = open("code.txt", "r").read()
fin_output = open("output.txt", "r").read()
code = str(code)
fin_output = int(fin_output)
print(execute_reverse(code, fin_output))

# Check that this reversing works
assert(execute(code, execute_reverse(code, fin_output)) == fin_output)