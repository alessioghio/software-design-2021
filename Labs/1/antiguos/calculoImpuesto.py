# inputs:
# Renumeración mensual
# mes que se empieza a trabajar

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

# PASO 1: Proyecte los ingresos gravados que percibirá en todo el año.
meses_faltantes = 12 - mes_inicial + 1 # incluido el mes al que corresponda la retención
ing_grav = remun_mensual*meses_faltantes
remun_bruta = ing_grav + gratificaciones 
remun_bruta += bonificacion_extraordinaria + compensacion + gratificacion_extraordinaria + otros

# PASO 2: Deducción de 7 UIT.
UIT = 4300
if remun_mensual > 2100:
    remun_neta = remun_bruta - UIT*7
else:
    print('No está sujeto a retenciones de quinta categoría')
# o si ingreso anual menor a 7 UIT

# PASO 3: Cálculo del impuesto anual proyectado.
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

# PASO 4: Monto de la retención.
if mes_inicial == 1 or 2 or 3:
    ret_mes = anual_proy / 12
elif mes_inicial == 4:
    ret_mes = anual_proy / 9
elif mes_inicial == 7:
    ret_mes = anual_proy / 8
elif mes_inicial == 8:
    ret_mes = anual_proy / 5
elif mes_inicial == 9 or 10 or 11:
    ret_mes = anual_proy / 4
else:
    ret_mes = anual_proy

# PASO 5: Cálculo adicional SOLO para los meses en que el trabajador ha recibido pagos distintos a las remuneraciones y gratificaciones ordinarias.
ret_adi_mes = pago_adi_mes + remun_bruta + remun_neta * tasa - anual_proy
tot_ret_mes = ret_mes + ret_adi_mes



