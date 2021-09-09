# Inputs
remun = 9500
month_entry = 9
prev_remun = 85000
prev_withholdings = [6000/8, 6000/8, 6000/8, 6000/8, 6000/8, 6000/8, # jan - jun
                    6000/8, 6000/8, 0, 0, 0, 0] # jul- dec
others = 0

# -- PASO 1: Proyecte los ingresos gravados que percibirá en todo el año -- #
remaining_months = 12 - month_entry + 1 # Entry month is included

# Calculate gratifications
jul_grat = 0
if month_entry < 6:
    jul_grat += remun / 6 * (6-month_entry) # First month of work is not considered
    dec_grat = remun
else:
    dec_grat = remun / 6 * (12-month_entry) # First month of work is not considered

# Remuneracion Bruta Anual (RBA)
RBA = remun*remaining_months + jul_grat + dec_grat + prev_remun

# -- Paso 2: Deducción de 7 UIT  -- #
UIT = 4300
if remun > 2100: 
    # Remuneracion Neta Anual (RNA)
    RNA = RBA - UIT*7
else:
    print("No esta sujeto a retenciones de quinta categoria")

# -- Paso 3: Cálculo del Impuesto Anual Proyectada -- #

# Calculate stretches ("tramos") limits
def getStrecthesLimits(stretches_nums):
    stretches_limits = []
    for i in range(1, len(stretches_nums)):
        stretches_limits.append((stretches_nums[i]-stretches_nums[i-1])*UIT)
    return stretches_limits

stretches_nums = [0, 5, 20, 35, 45]
stretches_limits = getStrecthesLimits(stretches_nums)

# Divide RNA into the calculated stretches
def divideIntoStrecthes(RNA, stretches_limits):
    stretches = []
    total_stretch = 0
    for stretch_lim in stretches_limits:
        if RNA < total_stretch + stretch_lim:
            break
        total_stretch += stretch_lim
        stretches.append(stretch_lim)
    stretches.append(RNA-total_stretch)
    return stretches

stretches = divideIntoStrecthes(RNA, stretches_limits)

# Calculate tax rate per stretch
def calculateProyectedTax(stretches, stretches_rates):
    if len(stretches_rates) != 5:
        raise Exception(f"Invalid number of rates. The number of tax rates must be 5")
    proyected_tax = 0
    for i in range(len(stretches)):
        proyected_tax += stretches[i]*stretches_rates[i]
    return proyected_tax

stretches_rates = [0.08, 0.14, 0.17, 0.2, 0.3]
proyected_tax = calculateProyectedTax(stretches, stretches_rates)

# -- PASO 4: Monto de la retención -- #
divisiones = {  1: 12, 2: 12, 3: 12, 4: 9,
                5: 8, 6: 8, 7: 8, 8: 5,
                9: 4, 10: 4, 11: 4, 12: 1
            }

monthDict = {   1: "Enero", 2: "Febrero", 3: "Marzo",
                4: "Abril", 5: "Mayo", 6: "Junio",
                7: "Julio", 8: "Agosto", 9: "Setiembre",
                10: "Octubre", 11: "Novimebre", 12: "Diciembre"
            }

def calculateReduction(entry_month, prev_withholdings):
    reduccion = 0
    if entry_month >= 3:
        total_months = entry_month - 1
        for i in range(total_months):
            reduccion += prev_withholdings[i]
    return reduccion

def calculateWithholding(entry_month, proyected_tax, prev_withholdings, divisions):
    # ret = (impuesto - red) / div
    reduccion = calculateReduction(entry_month, prev_withholdings)
    division = divisions[entry_month]
    retencion_mensual = (proyected_tax - reduccion) / division
    return retencion_mensual

withholdings = [] # "retenciones"
for i in range(1, 12+1):
    if i >= month_entry:
        monthly_withholding = calculateWithholding(i, proyected_tax, prev_withholdings, divisiones)
        withholdings.append(monthly_withholding)
    else:
        withholdings.append(0)

# -- PASO 5: Cálculo adicional -- # 
# SOLO para los meses en que el trabajador ha recibido pagos distintos a las remuneraciones y gratificaciones ordinarias

# Calculate extraordinary bonuses
BONUS_PERCENTAGE = 9/100
jul_extra_bonus = BONUS_PERCENTAGE*jul_grat
dec_extra_bonus = BONUS_PERCENTAGE*dec_grat

extra_RNA = RNA + jul_extra_bonus + dec_extra_bonus + others

extra_stretches = divideIntoStrecthes(extra_RNA, stretches_limits)
extra_proyected_tax = calculateProyectedTax(extra_stretches, stretches_rates)
extra_proyected_tax -= proyected_tax

for i in range(len(withholdings)):
    if i+1 >= month_entry:
        withholdings[i] += extra_proyected_tax

# print retenciones
print("-------------------------------------")
for month, withholding in enumerate(withholdings):
    print(f"Retencion del mes {monthDict[month+1]}: {withholding:.2f}")
print("-------------------------------------")