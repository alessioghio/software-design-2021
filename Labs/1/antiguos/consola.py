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
        user_input = input(f"Por favor ingrese su/s {input_string}: ")
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

class Worker():
    def __init__(self, id, name, lastName, age):
        self.id = int(id)
        self.name = name.capitalize()
        self.lastName = lastName.capitalize()
        self.age = int(age)
    
    def getTaxInfo(self):
        remuneration = checkInput("remuneracion", float)
        while True:
            month = checkInput("mes de inicio", int)
            if month > 12 or month < 1:
                print("Por favor ingrese un numero de mes valido")
            else:
                break
        extraPays = checkInput("pagos adicionales", float)
        gratification = checkInput("gratificacion", float)
        self.remuneration = remuneration
        self.month = month
        self.extraPays = extraPays
        self.gratification = gratification

    def printInfo(worker):
        print(f"Numero de identificacion: {worker.id}")
        print(f"Nombre: {worker.name} {worker.lastName}")
        print(f"Edad del trabajador: {worker.age}")

if __name__ == "__main__":
    print("Bienvenido!")
    
    id = checkInput("numero de identificación", int)
    name = checkInput("nombre", str)
    lastName = checkInput("apellido", str)
    age = checkInput("edad", int)

    worker = Worker(id, name, lastName, age)
    worker.printInfo()

    worker.getTaxInfo()

    print(f"Renumeración mensual: {worker.remuneration}")
    print(f"Mes inicial: {worker.month}")

# Escenarios
"""
Caso 1:
Ingreso mensual de 1000
Adicional: 0
mes = 1

respuesta
enero
febrero
--------------------------------
Caso 2:
Ingreso mensual de 5000
Adicional: 0
mes = 1

respuesta
enero
febrero
--------------------------------
Caso 3
Ingreso mensual de 5000
Adicional: 10,000 en Junio
mes = 1

respuesta
enero
febrero
--------------------------------
Caso 4:
Ingreso mensual de 5000
Adicional: 0
mes = 9

respuesta
enero
febrero
--------------------------------
Caso 5:
Ingreso mensual de 5000
Adicional: 10,000
mes = 7

respuesta
enero
febrero
"""