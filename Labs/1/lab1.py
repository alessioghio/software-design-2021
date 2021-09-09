from Worker import *

if __name__ == "__main__":
    print("Bienvenido!")
    
    """
    id = checkInput("numero de identificación", int)
    name = checkInput("nombre", str)
    lastName = checkInput("apellido", str)
    age = checkInput("edad", int)
    """
    # Dummy inputs for Worker class
    id = 12345678
    name = "Juan"
    lastName = "Perez"
    age = 38

    worker = Worker(id, name, lastName, age)
    print("---------------------------------")
    worker.printInfo()
    print("---------------------------------")

    # Calculate Withholdings
    worker.getWithholdingsInfo()
    worker.calculateWithholdings()

    # Ask if there are additional payments
    message = "Se deben considerar pagos adicionales? (1=Si,0=No): "
    while True:
        more_payments = checkInput(message, int)
        if more_payments == 1 or more_payments == 0:
            break
        else:
            print("Por favor ingrese 1 o 0, segun lo indicado.")
    
    if more_payments:
        # Calculate additional withholding
        worker.getExtraordinaryInfo()
        for month, extra in enumerate(worker.extra):
            if extra:
                worker.calculateExtraWithholdings(month+1)

    # Print withholdings
    print("-------------------------------------")
    for month, withholding in enumerate(worker.withholdings):
        print(f"Retencion del mes {worker.monthDict[month+1]}: {withholding:.2f}")
    print("-------------------------------------")