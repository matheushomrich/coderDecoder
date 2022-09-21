import sys

# functions to support code
def hexToBin(input):
    return bin(int(input, base = 16))[2:].zfill(16)

def binToHex(input):
    return hex(int(input, 2))[2:]

def loadMap(csv, toggle):
    result = {}

    try:
        file = open(csv, 'r')

        for line in file:
            infos = line.split(",")
            if not toggle:
                #codificacao
                result[infos[0]] = infos[1][:-1]
            else:
                #decodificacao
                result[infos[1][:-1]] = infos[0]

        return result


    except:
        print('error')

def invert(inputBin):
    result = ""

    for i in range(0, len(inputBin)):
        if inputBin[i] == '-':
            result += '+'
        elif inputBin[i] == '+':
            result += '-'
        else:
            result += '0'
    

# techniques
def codNRZI(input):

    binInput = str(hexToBin(input))

    currentSignal = "-"
    codedSignal = ""

    for i in range(0, len(binInput)):
        if binInput[i] == '1':
            if currentSignal == '-':
                currentSignal = '+'
            else:
                currentSignal = '-'
        codedSignal += currentSignal
    
    return codedSignal

def decodNRZI(input):

    currentSignal = "-"
    decodedSignal = ""

    for i in range(0, len(input)):
        if input[i] != currentSignal:
            decodedSignal += '1'
            if currentSignal == '-':
                currentSignal = '+'
            else:
                currentSignal = '-'
        else:
            decodedSignal += '0'

    return binToHex(decodedSignal)

def codMan(input):
    
    binInput = str(hexToBin(input))

    currentSignal = "-"

    nextSignals = ""
    codedSignal = ""

    for i in range(0, len(binInput)):
        if binInput[i] == '0':
            if currentSignal == '-':
                nextSignals = '+-'
                currentSignal = '-'
            else:
                nextSignals = '-+'
                currentSignal = '+'
        elif currentSignal == '-':
            nextSignals = '-+'
            currentSignal = '+'
        else:
            nextSignals = '+-'
            currentSignal = '-'
        codedSignal += nextSignals

    return codedSignal

def decodMan(input):
    previousSignal = '-'
    decodedSignal = ""
    signalA = ''
    signalB = ''

    for i in range(0, len(input), 2):
        signalA = input[i]
        signalB = input[i + 1]

        if signalA == signalB:
            return "Error"
        
        if previousSignal == '-':
            if signalA == '+':
                decodedSignal += '0'
            else:
                decodedSignal += '1'
        else:
            if signalA == '+':
                decodedSignal += '1'
            else:
                decodedSignal += '0'
        previousSignal = signalB
    
    return binToHex(decodedSignal)

#BUG falta digitos no final
def cod8b6t(input):
    map = loadMap("8b6t.csv", False)
    inputBin = hexToBin(input)
    codedSignal = ""
    aux = 0

    countPositiveTotal = 0
    countNegativeTotal = 0

    for i in range(8, len(inputBin), 8):
        substring = inputBin[aux:i]
        codedSubstring = map.get(substring)

        countPosSubs = 0
        countNegSubs = 0

        for j in range(5):
            if codedSubstring[j] == '-':
                countNegSubs += 1
            elif codedSubstring[j] == '+': 
                countPosSubs += 1
        
        if not countPositiveTotal == countNegativeTotal:
            normal = abs((countPositiveTotal + countPosSubs) - (countNegativeTotal + countNegSubs))
            inverted = abs((countPositiveTotal + countNegSubs) - (countNegativeTotal + countPosSubs))

            if inverted < normal:
                codedSubstring = invert(codedSubstring)
                a = countPosSubs
                countPosSubs = countNegSubs
                countNegSubs = a

        codedSignal += codedSubstring
        countNegativeTotal += countNegSubs
        countPositiveTotal += countPosSubs
        aux = i

    return codedSignal


# BUG falta 2 digitos no final 
def decod8b6t(input):

    map = loadMap("8b6t.csv", True)
    decodedString = ""
    aux = 0

    if not len(input) % 6 == 0:
        return "error"
    
    for i in range(6, len(input), 6):
        substring = input[aux:i]
        decodedSubstring = map.get(substring)

        if decodedSubstring == None:
            substring = invert(substring)
            decodedSubstring = map.get(substring)
            if decodedSubstring == None:
                return "error"
        
        decodedString += decodedSubstring
        aux = i

    return binToHex(decodedString)


#BUG faltam digitos
def cod6b8b(input):
    binInput = str(hexToBin(input))
    codedSginal = ""
    aux = 0

    for i in range(6, len(binInput), 6):
        subs = binInput[aux:i] 
        positiveCounter = 0
        negativeCounter = 0
        disp = 0

        for j in range(0, 6):
            if subs[j] == '0':
                negativeCounter += 1
            else:
                positiveCounter += 1
            
        disp = positiveCounter - negativeCounter
        if disp == 0:
            codedSginal += "10" + subs
        if disp == 2:
            codedSginal += "00" + subs
        if disp == -2:
            codedSginal += "11" + subs
        aux = i
    return codNRZI(binToHex(codedSginal))

# BUG resultado aleatorio F
def decod6b8b(input):
    inputBin = decodNRZI(input)
    inputBin = hexToBin(inputBin)

    decodedString = ""
    aux = 0

    if not len(inputBin) % 8 == 0:
        return "Erro"
    for i in range(8, len(inputBin), 8):
        subString = inputBin[aux:i]
        countPositive = 0
        countNegative = 0
        for j in range(7):
            if subString[j] == '+':
                countPositive += 1
            else:
                countNegative += 1
        decodedString += subString[2:8]
        aux = i
    
    return binToHex(decodedString)

# BUG so imprime +-+-+-+-+
def codhdb3(input):
    inputBin = hexToBin(input)

    currentViolation = '+'
    currentInfo = '+'
    violation = 0

    flag = False

    codedSignal = ""

    for i in range(0, len(inputBin)):
        if inputBin[i] == '0':
            violation = 1

            if not (i + 3) >= len(inputBin):
                for j in range(1, 3):
                    if inputBin[i + j] == '0':
                        violation += 1
                    else:
                        break
            
            if violation == 4:
                if currentInfo == currentViolation or (not currentInfo == currentViolation and flag):
                    codedSignal += currentViolation + "00" + currentViolation
                else:
                    codedSignal += "000" + currentViolation
                
                if currentViolation == '+':
                    currentViolation = '-'
                else:
                    currentViolation = '+'

                flag = True

                i += violation - 1
                violation = 0
            else:
                i += violation - 1
                violation -= 1
        else:
            codedSignal += currentInfo

            if currentInfo == '+':
                currentInfo = '-'
            else:
                currentInfo = '+'

            flag = True

    return codedSignal


# TODO not tested 
def decodhdb3(input):
    
    decodedString = ""
    lastInFBit = '0'
    zeroSequence = 0
    violation = False

    for i in range(0, len(input)):
        if input[i] == '0':
            decodedString += '0'
            zeroSequence += 1
        elif violation or (lastInFBit == input[i] and zeroSequence == 3):
            decodedString += '0'
            violation = False
            zeroSequence = 0
        else:
            signal = True
            if len(input) > i + 3:
                for j in range(2):
                    if not input[i + j] == '0':
                        signal = False
                        break
                if not input[i + 3] == input[i]:
                    signal = False
            else:
                signal = False
            if signal:
                decodedString += '0'
                violation = True
            else:
                if input[i] == lastInFBit:
                    return "Erro"
                decodedString += '1'
            zeroSequence = 0
    
    return binToHex(decodedString)



def main():
    if len(sys.argv) == 4:
        if sys.argv[1] == "codificador":
            if sys.argv[2] == "nrzi":
                print(codNRZI(sys.argv[3]))
            elif sys.argv[2] == "mdif":
                print(codMan(sys.argv[3]))
            elif sys.argv[2] == "8b6t":
                print(cod8b6t(sys.argv[3]))
            elif sys.argv[2] == "6b8b":
                print(cod6b8b(sys.argv[3]))
            elif sys.argv[2] == "hdb3":
                print(codhdb3(sys.argv[3]))
            else:
                print("Error: coder input not valid")              
        elif sys.argv[1] == "decodificador":
            if sys.argv[2] == "nrzi":
                print(decodNRZI(sys.argv[3]))
            elif sys.argv[2] == "mdif":
                print(decodMan(sys.argv[3]))
            elif sys.argv[2] == "8b6t":
                print(decod8b6t(sys.argv[3]))
            elif sys.argv[2] == "6b8b":
                print(decod6b8b(sys.argv[3]))
            elif sys.argv[2] == "hdb3":
                print(decodhdb3(sys.argv[3]))
            else:
                print("Error: decoder input not valid") 
    else:
        print("Something went wrong with your input, please try again.")

if __name__ == "__main__":
    main()
