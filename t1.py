import sys


def codNRZI(input: str):
    print("nrzi")

def decodNRZI(input: str):
    print("nrzi")

def codManchester(input: str):
    print("manCoder")

def decodManchester(input: str):
    print("manDecoder")

def cod8b6t(input: str):
    print("manCoder")

def decod8b6t(input: str):
    print("manDecoder")

def main():
    if len(sys.argv) == 3:
        if sys.argv[0] == "codificador":
            if sys.argv[1] == "nrzi":
                codNRZI(sys.argv[2])

    else:
        print("Something went wrong with your input, please try again.")

if __name__ == "__main__":
    main()
