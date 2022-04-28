#funciones
import pandas as pd
def traerParametros():
    parametros = "parametros.xlsx"
    movimientos = pd.read_excel(parametros, sheet_name="movimientos")
    clasificador = pd.read_excel(parametros, sheet_name="clasificador")
    cuentas = [7, 10, 11, 12, 16, 17]
    valorDefecto = "Ver glosita"
    # bdBruto= pd.concat([bdgtes,bdgoi,bdgom,bdgef],ignore_index=True)
    palabrasClave = pd.read_excel(parametros, sheet_name="palabras")
    listaPalabrasClave = palabrasClave['PalabrasClave'].values.tolist()
    apachurrado = ''
    for palabrita in listaPalabrasClave:
        apachurrado += '|' + palabrita
    apachurrado = apachurrado[1:]
    return palabrasClave, clasificador
#funciones