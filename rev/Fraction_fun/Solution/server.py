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


code = open("code.txt", "r").read()
fin_output = open("output.txt", "r").read()
code = str(code)
fin_output = int(fin_output)
while True:
    try:
        inp = int(input("Input your number: "))
        out = execute(code, inp)
        if out == int(fin_output):
            print("Correct!")
            print("Here is the flag: " + open("flag.txt", "r").read())
            break
        else:
            print("Incorrect!")
    except:
        print("Error!")
        break
