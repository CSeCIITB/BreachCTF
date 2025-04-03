from Encryptor import Encryptor, convertBinStrToStr
from SECRET import rules, FLAG
from jokes import jokes
import random


Timothy = Encryptor(rules)
Anthony = Encryptor(rules)

IV = "h9eunjhvbfhixmjvth7ewjswjhf9ko"  # Beep Bop Why Not
Timothy.initialize(IV, FLAG)

old, current = Timothy.iterate(1000)
running = 1
communicationType = 0
while running:
    print(
        "Welcome! What would you like to do?\n1: Encrypt something?\n2: Try fruitlessly to break the awesome encryption?\n3: Listen to a joke?\n4: Switch to binary input/output\n5: Switch to conentional input/output\n6: Exit\n"
    )

    data = input()
    if not data:
        print("Idk what u entered :(. BOOOOO^2. Goodbye!\n")
        break
    if data.strip() == "1":
        print("Enter something to encrypt:\n")
        data = input()
        if not data:
            print("Idk what u entered :((. BOOOOO. Goodbye!\n")
            running = 0
            break
        try:
            if communicationType == 1:
                try:

                    val = convertBinStrToStr(data[:-1])
                except Exception as e:
                    print("Bruh, I need a binary representation. Goodbye!\n")
                    running = 0
                    break
            else:
                val = data.strip()

            Anthony.initialize(IV, val)
            iterating = 1
            while iterating:
                print(
                    "How many times do u wanna iterate on it? (cumulative)\n"
                )
                data = input()
                try:
                    num = int(data.strip())
                except Exception as e:
                    print("Bruh, I need a number. Goodbye!\n")
                    running = 0
                    break
                if num > 10000:
                    print(
                        "Are u trying to kill me? Send a small number! I won't tolerate this. Goodbye\n"
                    )
                    running = 0
                    break
                Timothy.iterate(num)
                out = Timothy.getOutput(type=communicationType)
                print("Encrypted output:\n\n\n")
                print(out + "\n\n\n")
                print(
                    "\nContinue encryption iteration? (y/n) \n"
                )
                data =input()
                if data.strip() not in ["y", "n"]:
                    print(
                        "Idk what u entered :(((. BOOOOO. Goodbye!\n"
                    )
                    running = 0
                    break

                if data.strip() == "y":
                    continue
                else:
                    break

        except Exception as e:
            print(
                "Something went wrong! I aint dealing with that. Goodbye!\n"
            )
            # print(e)
            running=0
            break
    elif data.strip() == "2":
        print("Try to break the encryption:\n\n\n")
        print(
            Timothy.getOutput(type=communicationType)
            + "\n\n\n"
        )
        print(
            "To make it easier, I will give u the previous state as well!:\n\n\n"
        )
        print(
            Timothy.getOldOutput(type=communicationType)
            + "\n\n\n"
        )

    elif data.strip() == "3":
        joke = random.choice(jokes)
        print("Here's a joke for you:\n")
        print(joke + "\n\n")
    elif data.strip() == "4":
        communicationType = 1
        print("Switched to binary\n\n")
    elif data.strip() == "5":
        communicationType = 0
        print("Switched to conventional\n\n")
    elif data.strip() == "6":
        print("Fair winds, Traveler\n")
        running=0

        break
    else:
        print("Idk what u entered :(((( . BOOOOO. Goodbye!\n")
        break

