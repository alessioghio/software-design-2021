import pandas as pd

a = pd.read_csv('databases_testing/database_supply.csv')
unidades = a['name']

print(unidades[0])