def numFromStr(inputStr):
    """Returns string with only numbers from input string."""
    outputStr = ""

    def checkSymbol(s, i):
        if s == i:
            return i

        return ""

    integers = [ "1", "2", "3", "4", "5", "6", "7", "8", "9", "0" ]
    for symbol in inputStr:
        for integer in integers:
            outputStr += checkSymbol(symbol, integer)

    return outputStr