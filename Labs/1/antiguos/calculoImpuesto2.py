remun_mensual = 0
mes_inicial = 1
pago_adi_mes = 0
remun_anual = remun_mensual * 14
gratis = 0
UIT = 4300
#desc = no

meses_faltantes = 12 - mes_inicial + 1 # incluido el mes al que corresponda la retención
ing_grav = remun_mensual*meses_faltantes
remun_bruta = ing_grav + gratis # remuneración bruta anual

divisiones = {
        1: 12,
        2: 12,
        3: 12,
        4: 9,
        5: 8,
        6: 8,
        7: 8,
        8: 5,
        9: 4,
        10: 4,
        11: 4,
        12: 1
    }

monthDict = {
        1: "Enero",
        2: "Febrero",
        3: "Marzo",
        4: "Abril",
        5: "Mayo",
        6: "Junio",
        7: "Julio",
        8: "Agosto",
        9: "Setiembre",
        10: "Octubre",
        11: "Novimebre",
        12: "Diciembre"
    }

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





