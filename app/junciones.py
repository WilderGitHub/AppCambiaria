#funciones
def llenarData(concepto,a,b):
    if concepto !="Neteo":    
        print('dentro ',pares["Comprobante"][a])
        data2.append({
                "Tipo":pares["Tipo"][a],"Comprobante":pares["Comprobante"][a],"Concepto":concepto,
                "Mayor1":pares["Mayor"][a],"Mayor2":pares["Mayor"][b],"codMov":pares["codMov"][b],
                "Movimiento":pares["Movimiento"][b],"MontoUSD":round(pares["MN"][a]/6.86,2),
                "Detalle":pares["GlosaDetalle"][b],"Glosa":pares["Glosa"][a]
                })
    else:
        data2.append({
                "Tipo":pares["Tipo"][a],"Comprobante":pares["Comprobante"][a],"Concepto":concepto,
                "Mayor1":pares["Mayor"][a],"Mayor2":pares["Mayor"][b],"codMov":pares["codMov"][b],
                "Movimiento":pares["Movimiento"][b],"MontoUSD":0, 
                "Detalle":("±", round(pares["MN"][a]/6.86,2)),"Glosa":pares["Glosa"][a]
                })

def dv(concepto,suma):
    print("largo cuando dentra al debehaber: ",len(aux2))
    if len(aux2)==1:
        data2.append({''
                    "Tipo":aux2["tipo"][0],"Comprobante":aux2["comprobante"][0],"Concepto":concepto,
                    "Mayor1":aux2["mayor"][0],"Mayor2":"--","codMov":"--",
                    "Movimiento":"--","MontoUSD":round(suma,2),
                    "Detalle":aux2["glosaRenglon"][0],"Glosa":aux2["glosa"][0]
                    })
    else:
        data2.append({''
                    "Tipo":aux2["tipo"][0],"Comprobante":aux2["comprobante"][0],"Concepto":concepto,
                    "Mayor1":aux2["mayor"][0],"Mayor2":aux2["mayor"][1],"codMov":aux2["codMov"][1],
                    "Movimiento":aux2["nomMov"][1],"MontoUSD":round(suma,2),
                    "Detalle":aux2["glosaRenglon"][0],"Glosa":aux2["glosa"][0]
                    })

def debemenoshaber(hasta):
    sumaDebe=0
    sumaHaber=0
    for i in hasta:
        if aux2["mayor"][i] in cuentas and aux2["dh"][i]=='D':
            sumaDebe=sumaDebe+aux2["mn"][i]/6.86
        elif aux2["mayor"][i] in cuentas and aux2["dh"][i]=='H':
            sumaHaber=sumaHaber+aux2["mn"][i]/6.86
    suma=sumaDebe-sumaHaber
    if suma>0:
        dv("Ingreso",suma)
    else:
        dv("Egreso",-suma)
#funciones