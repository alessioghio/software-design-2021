def getTypeName(input_type):
    typesDict = {"int": "numero",
                 "float": "numero",
                 "str": "palabra"}
    typeName = typesDict[input_type.__name__]
    return typeName

def isFloat(value):
    try:
        float(value)
        return True
    except:
        return False

def checkInput(input_string, input_type):
    while True:
        user_input = input(input_string)
        if user_input.isnumeric() or isFloat(user_input):
            if input_type == int:
                user_input = int(user_input)
            else:
                user_input = float(user_input)
        if isinstance(user_input, input_type):
            break
        else:
            print(f"Por favor ingrese un/a {getTypeName(input_type)}")
    return user_input