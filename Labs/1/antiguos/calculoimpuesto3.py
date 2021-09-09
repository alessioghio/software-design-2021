
# Variables de entrada ==========================
# Mes de Entrada 
# Bono extraordinario - Otros
# Remuneración en trabajo actual 
# Remumneración en trabajo previo
# Número de meses en empresa de trabajo previo


# Variables de Entrada - Test 
remun_mensual = 7500
mes_inicial = 1
pago_adi_mes = 0
gratificaciones = 7500*2
meses_grat = [7, 12]
bonificacion_extraordinaria = 15000*9/100 # Ley 29351
compensacion = 0 # No afecto
gratificacion_extraordinaria = 5100
otros = 6715
gastos_deducibles = 300

# Valores diferentes
# remun_anual = remun_mensual * 14
# gratis = 0
# gratis = gratificaciones



# PASO 1: Proyecte los ingresos gravados que percibirá en todo el año 
meses_faltantes = 12 - mes_inicial + 1 # incluido el mes al que corresponda la retención
ing_grav = remun_mensual*meses_faltantes
remun_bruta = ing_grav + gratificaciones 
remun_bruta += bonificacion_extraordinaria + compensacion + gratificacion_extraordinaria



# Paso 2: Deducción de 7 UIT 
UIT = 4300
if remun_mensual > 2100: 
    remun_neta = remun_bruta - UIT*7
else 
    print("No está sujeto a retenciones de quinta categoría")

# Paso 3: Cálculo del Impuesto Anual Proyectada
# Dentro del if remun_mensual
remun_anual = remun_mensual * 14
if remun_anual <= 5*UIT:
    tasa = 0.08
elif 5 < remun_anual <= 20:
    tasa = 0.14
elif 20 < remun_anual <= 35:
    tasa = 0.17
elif 35 < remun_anual <= 45:
    tasa = 0.2
else:
    tasa = 0.3
anual_proy = remun_neta * tasa    

def calcularReduccion(mes_inicial, retenciones):
    reduccion = 0
    if mes_inicial >= 3:
        total_meses = mes_inicial - 1
        for i in range(total_meses):
            reduccion += retenciones[i]
    return reduccion

def calcularRetencion(mes_inicial, anual_proy, retenciones, divisiones):
    # ret = (impuesto - red) / div
    reduccion = calcularReduccion(mes_inicial, retenciones)
    division = divisiones[mes_inicial]
    retencion_mensual = (anual_proy - reduccion) / division
    return retencion_mensual

if remun_mensual > 2100:
    remun_neta = remun_bruta - UIT*7
    if remun_anual <= 5*UIT:
        tasa = 0.08
    elif 5*UIT < remun_anual <= 20*UIT:
        tasa = 0.14
    elif 20*UIT < remun_anual <= 35*UIT:
        tasa = 0.17
    elif 35*UIT < remun_anual <= 45*UIT:
        tasa = 0.2
    else:
        tasa = 0.3
    anual_proy = remun_neta * tasa # impuesto anual proyectado

    retenciones = []
    for i in range(mes_inicial, 12+1):
        ret_mensual = calcularRetencion(i, anual_proy, retenciones, divisiones)
        retenciones[i-1] = ret_mensual
    
    # print retenciones
    for mes, ret in enumerate(retenciones):
        print(f"Retencion del mes {mes}: {ret}")
        print("") # new line

else:
    print("No está sujeto a retenciones de quinta categoría") # o si ingreso anual menor a 7 UIT





