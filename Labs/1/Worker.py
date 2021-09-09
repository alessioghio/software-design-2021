from utils import *

class Worker():
    def __init__(self, id, name, lastName, age):
        self.id = int(id)
        self.name = name.capitalize()
        self.lastName = lastName.capitalize()
        self.age = int(age)
        # Default values
        self.month_entry = 1
        self.RNA = 0
        self.withholdings = [0,0,0,0,0,0,0,0,0,0,0,0]
        self.extra = [0,0,0,0,0,0,0,0,0,0,0,0]
        # Constants for withholding calculations
        self.UIT = 4300
        self.divisions = {  1: 12, 2: 12, 3: 12, 4: 9,
                5: 8, 6: 8, 7: 8, 8: 5,
                9: 4, 10: 4, 11: 4, 12: 1
            }
        self.monthDict = {   1: "Enero", 2: "Febrero", 3: "Marzo",
                4: "Abril", 5: "Mayo", 6: "Junio",
                7: "Julio", 8: "Agosto", 9: "Setiembre",
                10: "Octubre", 11: "Novimebre", 12: "Diciembre"
            }
    
    def printInfo(worker):
        print(f"Numero de identificacion: {worker.id}")
        print(f"Nombre completo: {worker.name} {worker.lastName}")
        print(f"Edad del trabajador: {worker.age}")
    
    # Get Withholdings calculations inputs
    def getWithholdingsInfo(self):
        # Monthly Remuneration
        message = "Por favor ingrese su remuneracion mensual: "
        remuneration = checkInput(message, float)
        self.remuneration = remuneration
        # Month at which the employee starts working
        message = "Por favor ingrese el numero de mes de inicio laboral: "
        while True:
            month_entry = checkInput(message, int)
            if month_entry > 12 or month_entry < 1:
                print("Por favor ingrese un numero de mes valido.")
            else:
                break
        self.month_entry = month_entry
        # Remuneration at previous company
        message = "Por favor ingrese su remuneracion total anterior (si aplica, si no ingrese 0): "
        previous_remuneration = checkInput(message, float)
        self.previous_remuneration = previous_remuneration
        # Withholdings at previous company
        self.previous_withholdings = [0,0,0,0,0,0,0,0,0,0,0,0]
        if previous_remuneration:
            print("Ahora por favor inserte las retenciones mensuales anteriores: ")
            for i in range(1, month_entry):
                self.previous_withholdings[i-1] = checkInput(f"{self.monthDict[i]}: ", float)
    
    def getExtraordinaryInfo(self):
        # Additional extraordinary pays
        print("Por favor inserte montos extraordinarios adicionales segun el mes al que corresponden: ")
        for i in range(self.month_entry, 12+1):
            self.extra[i-1] = checkInput(f"{self.monthDict[i]}: ", float)

    # Calculate stretches ("tramos") limits
    def getStrecthesLimits(self, stretches_nums):
        stretches_limits = []
        for i in range(1, len(stretches_nums)):
            stretches_limits.append((stretches_nums[i]-stretches_nums[i-1])*self.UIT)
        return stretches_limits
    
    # Divide into the calculated stretches
    def divideIntoStrecthes(self, RNA, stretches_limits):
        stretches = []
        total_stretch = 0
        for stretch_lim in stretches_limits:
            if RNA < total_stretch + stretch_lim:
                break
            total_stretch += stretch_lim
            stretches.append(stretch_lim)
        stretches.append(RNA-total_stretch)
        return stretches
    
    # Calculate tax rate per stretch
    def calculateProyectedTax(self, stretches, stretches_rates):
        if len(stretches_rates) != 5:
            raise Exception(f"Invalid number of rates. The number of tax rates must be 5.")
        proyected_tax = 0
        for i in range(len(stretches)):
            proyected_tax += stretches[i]*stretches_rates[i]
        return proyected_tax
    
    def calculateReduction(self, entry_month, prev_withholdings):
        reduction = 0
        if entry_month >= 3:
            total_months = entry_month - 1
            for i in range(total_months):
                reduction += prev_withholdings[i]
        return reduction

    def calculateWithholding(self, entry_month, proyected_tax, prev_withholdings, divisions):
        # withholding = (tax - reduction) / division
        reduccion = self.calculateReduction(entry_month, prev_withholdings)
        division = divisions[entry_month]
        retencion_mensual = (proyected_tax - reduccion) / division
        return retencion_mensual

    def calculateWithholdings(self):
        # -- STEP 1: Calculate RBA -- #
        remaining_months = 12 - self.month_entry + 1 # Entry month is included
        # Calculate gratifications
        jul_grat = 0
        if self.month_entry < 6:
            jul_grat += self.remuneration / 6 * (6 - self.month_entry) # First month of work is not considered
            dec_grat = self.remuneration
        else:
            dec_grat = self.remuneration / 6 * (12 - self.month_entry) # First month of work is not considered
        # Remuneracion Bruta Anual (RBA)
        RBA = self.remuneration*remaining_months + jul_grat + dec_grat + self.previous_remuneration
        # Calculate extraordinary bonuses
        BONUS_PERCENTAGE = 9/100
        jul_extra_bonus = BONUS_PERCENTAGE*jul_grat
        dec_extra_bonus = BONUS_PERCENTAGE*dec_grat
        RBA += jul_extra_bonus + dec_extra_bonus

        # -- STEP 2: 7 UIT deduction -- #
        if RBA > self.UIT*7:
            # Remuneracion Neta Anual (RNA)
            RNA = RBA - self.UIT*7
            self.RNA = RNA
        else:
            print("No esta sujeto a retenciones de quinta categoria.")
            return # withholding does not get calculated

        # -- STEP 3: Calculate Proyected Tax -- #
        stretches_nums = [0, 5, 20, 35, 45]
        stretches_limits = self.getStrecthesLimits(stretches_nums)
        stretches = self.divideIntoStrecthes(RNA, stretches_limits)
        stretches_rates = [0.08, 0.14, 0.17, 0.2, 0.3]
        proyected_tax = self.calculateProyectedTax(stretches, stretches_rates)

        # -- STEP 4: Calculate withholdings -- #
        withholdings = [] # "retenciones"
        for i in range(1, 12+1):
            if i >= self.month_entry:
                monthly_withholding = self.calculateWithholding(self.month_entry, proyected_tax, self.previous_withholdings, self.divisions)
                withholdings.append(monthly_withholding)
            else:
                withholdings.append(0)
        
        self.withholdings = withholdings
    
    def calculateExtraWithholdings(self, month):
        # -- STEP 5: Additional withholding -- #
        stretches_nums = [0, 5, 20, 35, 45]
        stretches_limits = self.getStrecthesLimits(stretches_nums)
        stretches = self.divideIntoStrecthes(self.RNA, stretches_limits)
        stretches_plus = self.divideIntoStrecthes(self.RNA+self.extra[month-1], stretches_limits)
        stretches_rates = [0.08, 0.14, 0.17, 0.2, 0.3]
        proyected_tax = self.calculateProyectedTax(stretches, stretches_rates)
        proyected_tax_plus = self.calculateProyectedTax(stretches_plus, stretches_rates)
        extra_tax = proyected_tax_plus - proyected_tax
        self.withholdings[month-1] += extra_tax