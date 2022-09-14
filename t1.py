import sys

def hexToBin(input):
    return bin(int(input, 16)).zfill(8)

def binToHex(input):
    return hex(int(input, 2))[2:]

def codNRZI(input):
    print(binToHex(input))

def decodNRZI(input):
    print("nrzi")

def codMan(input):
    print("manCoder")

def decodMan(input):
    print("manDecoder")

def cod8b6t(input):
    print("8b6t")

def decod8b6t(input):
    print("8b6t")

def cod6b8b(input):
    print("6b8b")

def decod6b8b(input):
    print("6b8b")   

def codhdb3(input):
    print("hdb3")

def decodhdb3(input):
    print("hdb3")

def main():
    if len(sys.argv) == 4:
        if sys.argv[1] == "codificador":
            if sys.argv[2] == "nrzi":
                codNRZI(sys.argv[3])
            elif sys.argv[2] == "mdif":
                codMan(sys.argv[3])
            elif sys.argv[2] == "8b6t":
                cod8b6t(sys.argv[3])
            elif sys.argv[2] == "6b8b":
                cod6b8b(sys.argv[3])
            elif sys.argv[2] == "hdb3":
                codhdb3(sys.argv[3])
            else:
                print("Error: coder input not valid")              
        elif sys.argv[1] == "decodificador":
            if sys.argv[2] == "nrzi":
                decodNRZI(sys.argv[3])
            elif sys.argv[2] == "mdif":
                decodMan(sys.argv[3])
            elif sys.argv[2] == "8b6t":
                decod8b6t(sys.argv[3])
            elif sys.argv[2] == "6b8b":
                decod6b8b(sys.argv[3])
            elif sys.argv[2] == "hdb3":
                decodhdb3(sys.argv[3])
            else:
                print("Error: decoder input not valid") 
    else:
        print("Something went wrong with your input, please try again.")

if __name__ == "__main__":
    main()
