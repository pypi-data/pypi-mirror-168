def convertir_a_rosa_de_los_vientos(val,estricto=True):
    '''Toma un valor int o float y asume que es una dirección de vientos en 360° grados Norte.
    
    val: Valor de la dirección de viento (int o float).
    
    estricto=True (por defecto) devuelve un error al ingresar un tipo de dato no numérico.
    estructo=False devuelve el dato original ante errores'''
    
    if isinstance(val,(int,float)):
        val %= 360

        rosa = ["N","NNE","NE","ENE","E","ESE","SE","SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]

        # Duplica los bins ['N', 'NNE', 'NNE', 'NE', 'NE' .... 'N']
        rosa_aux = ["N"] + [bin for bin in rosa[1:] for _ in (0, 1)] + ["N"]
        # Al desplazar el bin 'N' un lugar hacia la izquierda, obteniendo una N al principio de la lista y otra al final,
        # la categorización de la dirección de viento queda "centrada" en el ángulo medio de cada bin. en español:
            # Dirección de viento entre 348.75 grados y 0 = 'N',
            # Dirección de viento entre 0 grados y 11.25 grados = 'N'

        #Calcular cuantos grados representa cada bin de dirección de viento 
        # Para la lista de 16 posiciones, son 32 medios bins.
        # un bin = 22.5 grados, medio bin = 11.25 grados
        rango_medio_bin = 180/len(rosa)
        indice = int(val//rango_medio_bin)
    
        return rosa_aux[indice]
    
    else:
        
        if estricto:
            raise ValueError('La dirección de viento debe ser un número int o float')
        else:
            return val