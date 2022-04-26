import PySimpleGUI as sg
import os
import numpy as np
import pandas as pd
from dbfread import DBF
import re
import itertools
from pandas import Series, DataFrame

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
# from junciones import *
# parámetros y valores fijos
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

# funciones


def llenarData(concepto, a, b):
    if concepto != "Neteo":
        # print('dentro ',pares["Comprobante"][a])
        data2.append({
            "Fecha": pares["Fecha"][a], "Tipo": pares["Tipo"][a], "Comprobante": pares["Comprobante"][a], "Concepto": concepto,
            "Mayor1": pares["Mayor"][a], "Mayor2": pares["Mayor"][b], "codMov": pares["codMov"][b],
            "Movimiento": pares["Movimiento"][b], "MontoUSD": round(pares["MN"][a]/6.86, 2),
            "Detalle": pares["GlosaDetalle"][b], "Glosa": pares["Glosa"][a]
        })
    else:
        data2.append({
            "Fecha": pares["Fecha"][a], "Tipo": pares["Tipo"][a], "Comprobante": pares["Comprobante"][a], "Concepto": concepto,
            "Mayor1": pares["Mayor"][a], "Mayor2": pares["Mayor"][b], "codMov": pares["codMov"][b],
            "Movimiento": pares["Movimiento"][b], "MontoUSD": 0,
            "Detalle": ("±", round(pares["MN"][a]/6.86, 2)), "Glosa": pares["Glosa"][a]
        })


def dv(concepto, suma):
    # print("largo cuando dentra al debehaber: ",len(aux2))
    if len(aux2) == 1:
        data2.append({''
                      "Fecha": aux2["fecha"][0], "Tipo": aux2["tipo"][0], "Comprobante": aux2["comprobante"][0], "Concepto": concepto,
                      "Mayor1": aux2["mayor"][0], "Mayor2": "999", "codMov": "999",
                      "Movimiento": "--", "MontoUSD": round(suma, 2),
                      "Detalle": aux2["glosaRenglon"][0], "Glosa": aux2["glosa"][0]
                      })
    else:
        data2.append({''
                      "Fecha": aux2["fecha"][0], "Tipo": aux2["tipo"][0], "Comprobante": aux2["comprobante"][0], "Concepto": concepto,
                      "Mayor1": aux2["mayor"][0], "Mayor2": aux2["mayor"][1], "codMov": aux2["codMov"][1],
                      "Movimiento": aux2["nomMov"][1], "MontoUSD": round(suma, 2),
                      "Detalle": aux2["glosaRenglon"][0], "Glosa": aux2["glosa"][0]
                      })


def debemenoshaber(hasta):
    sumaDebe = 0
    sumaHaber = 0
    for i in hasta:
        if aux2["mayor"][i] in cuentas and aux2["dh"][i] == 'D':
            sumaDebe = sumaDebe+aux2["mn"][i]/6.86
        elif aux2["mayor"][i] in cuentas and aux2["dh"][i] == 'H':
            sumaHaber = sumaHaber+aux2["mn"][i]/6.86
    suma = sumaDebe-sumaHaber
    if suma > 0:
        dv("Ingreso", suma)
    else:
        dv("Egreso", -suma)


def leer(nombrearchivo):
    extension = os.path.splitext(nombrearchivo)[1]
    # print(nombrearchivo)
    if extension == '.dbf':
        # print(extension)
        #print("estamos en dbf con  ", nombrearchivo)
        table = DBF(nombrearchivo, encoding='latin', load=True)
        return pd.DataFrame(iter(table))
    else:
        # print(extension)
        return pd.read_excel(nombrearchivo)
# funciones


# tema
sg.theme('LightGrey1')
# el diseño

layout = [[sg.T("")],
          [sg.Text("GEF: "),
           sg.Input(key="-GEF2-", change_submits=True,  pad=((30, 10), 5), size=(80, 1)), sg.FileBrowse(key="-GEF-")],
          [sg.Text("GOM: "),
           sg.Input(key="-GOM2-", change_submits=True, pad=((26, 10), 5), size=(80, 1)), sg.FileBrowse(key="-GOM-")],
          [sg.Text("GOI: "),
           sg.Input(key="-GOI2-", change_submits=True, pad=((34, 10), 5), size=(80, 1)), sg.FileBrowse(key="-GOI-")],
          [sg.Text("GTES: "),
           sg.Input(key="-GTES2-", change_submits=True, pad=((22, 10), 5), size=(80, 1)), sg.FileBrowse(key="-GTES-")],
          [sg.Button("Procesar", pad=((350, 0), 30), font='Arial 12', button_color=('firebrick3'))]]

# Creamos la ventana
window = sg.Window('Balenza Cambiaria', layout, size=(750, 250))
# escuchamos los eventos
print("Estamos estiendo, no vasde tocar nada")
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == "Exit":
        break
    elif event == "Procesar":

        nombreGEF = os.path.abspath(values["-GEF2-"])
        nombreGOM = os.path.abspath(values["-GOM-"])
        nombreGOI = os.path.abspath(values["-GOI2-"])
        nombreGTES = os.path.abspath(values["-GTES2-"])

        bdgef = leer(nombreGEF)
        bdgom = leer(nombreGOM)
        bdgoi = leer(nombreGOI)
        bdgtes = leer(nombreGTES)

        ''' bdgef = pd.read_excel(nombreGEF)
        bdgom = pd.read_excel(nombreGOM)
        bdgoi = pd.read_excel(nombreGOI)
        bdgtes = pd.read_excel(nombreGTES) '''

        bdBruto = pd.concat([bdgtes, bdgoi, bdgom, bdgef], ignore_index=True)
        bdBruto.columns = map(str.lower, bdBruto.columns)
        if os.path.splitext(nombreGEF)[1] == '.dbf':
            bdReducida = bdBruto.loc[:, ('fecha_dia', 'nro_centro', 'cve_tipo_c', 'glosa_reng', 'cve_debe_h', 'monto_mo',
                                     'cod_moneda', 'cod_movimi', 'nom_movimi',
                                         'monto_mn', 'glosa_comp', 'nro_compro', 'cod_mayor')]
        else:

            bdReducida = bdBruto.loc[:, ('fecha_dia', 'nro_centro', 'cve_tipo_comprob', 'glosa_reng', 'cve_debe_haber', 'monto_mo',
                                     'cod_moneda', 'cod_movimiento', 'nom_movimiento',
                                         'monto_mn', 'glosa_comprob', 'nro_comprob', 'cod_mayor')]
        index_names = bdReducida[bdReducida['nro_centro'] != 1].index
        bdReducida.drop(index_names, inplace=True)

        if os.path.splitext(nombreGEF)[1] == '.dbf':
            dict = {'fecha_dia': 'fecha', 'cve_tipo_c': 'tipo', 'glosa_reng': 'glosaRenglon', 'cve_debe_h': 'dh', 'monto_mo': 'mo',
                    'cod_moneda': 'moneda', 'cod_movimi': 'codMov', 'nom_movimi': 'nomMov',
                    'monto_mn': 'mn', 'glosa_comp': 'glosa', 'nro_compro': 'comprobante', 'cod_mayor': 'mayor'}
        else:

            dict = {'fecha_dia': 'fecha', 'cve_tipo_comprob': 'tipo', 'glosa_reng': 'glosaRenglon', 'cve_debe_haber': 'dh', 'monto_mo': 'mo',
                    'cod_moneda': 'moneda', 'cod_movimiento': 'codMov', 'nom_movimiento': 'nomMov',
                    'monto_mn': 'mn', 'glosa_comprob': 'glosa', 'nro_comprob': 'comprobante', 'cod_mayor': 'mayor'}
        bdReducida.rename(columns=dict, inplace=True)
        #print("El  reducido ", bdReducida)
        bdReducida['mayor'] = bdReducida['mayor'].astype(float)
        bdFiltro1 = bdReducida[bdReducida['mayor'].isin(cuentas)]
        # print("las cuentas ", bdReducida['comprobante'])
        # print("El  reducido mayor isincuentas ",
        #      bdReducida['mayor'].astype(float))
        #print("El  bdFiltro1 ", bdFiltro1)

        bdFiltro1["comprobante"].unique()
        bd = bdReducida[bdReducida["comprobante"].isin(
            bdFiltro1["comprobante"])].sort_values(by=["comprobante", "dh"], ascending=True)
        bd = bd.reset_index(drop=True)
        bd = bd.drop_duplicates()
        bd = bd.reset_index(drop=True)
        #print("El  bd ", bd)
        #######
        ###############################################################################################
        ################################ la cosa ######################################################
        aux1 = bd["comprobante"].unique()  # creamos un dataframe vacio
        consolidado = pd.DataFrame()  # creamos un dataframe vació

        for q in range(len(aux1)):
            # Vamos comprobante por comprobante
            aux2 = bd[bd["comprobante"] == aux1[q]]
            aux2 = aux2.reset_index(drop=True)  # reseteamos el index
            data1 = []
            columnas1 = ["Fecha", "Tipo", "Comprobante", "Concepto", "Mayor",
                         "codMov", "Movimiento", "MN", "Glosa", "GlosaDetalle"]
            data2 = []
            columnas2 = ["Fecha", "Tipo", "Comprobante", "Concepto", "Mayor1", "Mayor2", "codMov",
                         "Movimiento", "MontoUSD", "Detalle", "Glosa"]  # luego pones mas campos importantes

            # los ajustes por arbitraje y revalorizacion ######
            if aux2["tipo"][0] == 'V' or aux2["tipo"][0] == 'D':
                # aplicamos función para sumar y luego la función para llenar  los comprobantes DV
                debemenoshaber(aux2.index)
                unRegistro = pd.DataFrame(data2, columns=columnas2)
                consolidado = consolidado.append(unRegistro, ignore_index=True)
            else:  # estos son los casos normales digamos ##############################################################
                # aqui sacamos los repetidos en la MN
                # si hay duplicado en MN  entonces...
                if aux2.duplicated(subset=['mn']).any() == True:
                    # mantenemos los que no se repiten
                    aux3 = aux2.duplicated(subset=['mn'], keep=False)
                    # el array de indices
                    aux4 = aux3.index[aux3 == True].tolist()
                    if len(aux4) == 2:
                        for x in range(len(aux4)):
                            data1.append({
                                "Fecha": aux2["fecha"][aux4[x]], "Tipo": aux2["tipo"][aux4[x]], "Comprobante": aux2["comprobante"][aux4[x]], "Concepto": aux2["dh"][aux4[x]],
                                "Mayor": aux2["mayor"][aux4[x]], "codMov": aux2["codMov"][aux4[x]], "Movimiento": aux2["nomMov"][aux4[x]],
                                "MN": aux2["mn"][aux4[x]], "Glosa": aux2["glosa"][aux4[x]], "GlosaDetalle": aux2["glosaRenglon"][aux4[x]],
                            })
                            pares = pd.DataFrame(data1, columns=columnas1)
                        # print(pares)
                        if pares["Mayor"][0] in cuentas and pares["Mayor"][1] in cuentas:
                            # print("Posible Neteo")
                            # aqui ver para que el monto sea cero y que en el detalle salga el monto
                            llenarData("Neteo", 0, 1)
                            unRegistro = pd.DataFrame(data2, columns=columnas2)
                        else:
                            if pares["Mayor"][0] in cuentas and pares["Mayor"][1] not in cuentas and pares["Concepto"][0] == "D":
                                # print('caso 1')
                                llenarData("Ingreso", 0, 1)
                            if pares["Mayor"][0] in cuentas and pares["Mayor"][1] not in cuentas and pares["Concepto"][0] == "H":
                                # print('caso 2')
                                llenarData("Egreso", 0, 1)
                            if pares["Mayor"][1] in cuentas and pares["Mayor"][0] not in cuentas and pares["Concepto"][1] == "D":
                                # print('caso 3')
                                llenarData("Ingreso", 1, 0)
                            if pares["Mayor"][1] in cuentas and pares["Mayor"][0] not in cuentas and pares["Concepto"][1] == "H":
                                # print('caso 4')
                                llenarData("Egreso", 1, 0)
                    else:
                        debemenoshaber(range(len(aux2)))
                else:   # Aqui anotamos todos los que no son repetidos
                    aux2 = aux2.sort_values(by='mayor')  # , key=cuentas)
                    aux2 = aux2.reset_index(drop=True)
                    # print(aux2)
                    for x in range(len(aux2)):
                        data1.append({
                            "Fecha": aux2["fecha"][x], "Tipo": aux2["tipo"][x], "Comprobante": aux2["comprobante"][x], "Concepto": aux2["dh"][x],
                            "Mayor": aux2["mayor"][x], "codMov": aux2["codMov"][x], "Movimiento": aux2["nomMov"][x],
                            "MN": aux2["mn"][x], "Glosa": aux2["glosa"][x], "GlosaDetalle": aux2["glosaRenglon"][x],
                        })
                        pares = pd.DataFrame(data1, columns=columnas1)
                    # print(pares)
                    # los sueltitos (se supone que los otros movimientos estan en otras areas, ej. gadm)
                    if len(aux2) == 1:
                        # print("entramos con 1")
                        if pares["Concepto"][0] == "D":
                            # print('caso 5')
                            llenarData("Ingreso", 0, 0)
                        else:
                            # print('caso 6')
                            llenarData("Egreso", 0, 0)
                    else:             # Aqui es cuando no hay duplicados y no son pares ni sueltitos
                        # print("mas de 2")
                        debemenoshaber(range(len(aux2)))
                unRegistro = pd.DataFrame(data2, columns=columnas2)
                consolidado = consolidado.append(unRegistro, ignore_index=True)

        consolidado
        consolidado.to_excel("borrareste.xlsx")
        consolidado['Mayor2'] = pd.to_numeric(consolidado['Mayor2'])
        consolidado['codMov'] = pd.to_numeric(consolidado['codMov'])
        ################### la cosa ###################################

        # las apropiaciones
        movimientosAux = movimientos.drop(columns=['nomMovimiento'])
        clasificadorAux = clasificador.drop(columns=['x'])
        conCodigos = pd.merge(consolidado, movimientosAux, on=[
            'Concepto', 'Mayor2', 'codMov'], how='left').fillna(valorDefecto)
        # las apropiaciones
        # eso
        for i in range(len(conCodigos)):
            objeto = conCodigos.loc[i, "Glosa"] + \
                str(conCodigos.loc[i, "Detalle"])
            # print(i, "=",objeto)
            buscareis = re.findall(r'(%s)' % apachurrado,
                                   objeto, flags=re.IGNORECASE+re.MULTILINE)
            # print ("antes ", buscareis)
            unasola = list(itertools.chain.from_iterable(buscareis))
            # print("una sola ",unasola)
            unasola = list(dict.fromkeys(unasola))
            unasola = [i for i in unasola if i]
            # print("sin duplicados ",unasola)
            # este =', '.join(map(str,unasola))

            if conCodigos.loc[i, "Tipo"] in ["D", "V"]:
                if conCodigos.loc[i, "Concepto"] == "Ingreso":
                    conCodigos.loc[i,
                                   "codigoBC"] = "AJUSTE POR ARBITRAJE DE SALDOS (BCI32)"
                else:
                    conCodigos.loc[i,
                                   "codigoBC"] = "AJUSTE POR ARBITRAJE DE SALDOS (BCE29)"

            if conCodigos.loc[i, "Mayor2"] == 498:
                if conCodigos.loc[i, "Concepto"] == "Ingreso":
                    conCodigos.loc[i,
                                   "codigoBC"] = "ABONOS TRANSITORIOS (BCI31)"

            if conCodigos.loc[i, "codigoPropio"] == valorDefecto:
                # print ("este ", este)
                # print(conCodigos.loc[i,"codigoPropio"])
                conCodigos.loc[i, "codigoPropio"] = ', '.join(
                    map(str, unasola))

        conCodigos

        conClasificador = pd.merge(conCodigos, clasificadorAux, on=[
            'codigoBC'], how='left').fillna(valorDefecto)

        # dt.datetime.today().strftime("%m/%d/%Y")
        nombreSalida = "Bruto_"+conCodigos["Fecha"].min().strftime("%d%b") + "-"+conCodigos["Fecha"].max(
        ).strftime("%d%b")+"("+pd.Timestamp.now().strftime("%d%b%H%M")+")"
        # get current directory
        path = os.getcwd()
        #print("Current Directory", path)
        # parent directory
        parent = os.path.dirname(path)
        #print("Parent directory", parent)
        ######conCodigos.to_excel(parent+"/"+nombreSalida+".xlsx", index=False)
        conClasificador.to_excel(parent+"/"+nombreSalida+".xlsx", index=False)
        print("Ya hemos generado el excel oe")
        # eso
