import gc
import numpy as np
import pandas as pd
import datetime as dt
from pathlib import Path

from . import eo
from . import dirs
from . import fechas
from .cl_TablasVC import *


__all__ = ['DatosCROM']

class DatosCROM(TablasVC):
    
    def __init__(
        self,
        fecha_i = None,
        fecha_f = None,
        parques = [],
        clientes = [],
        dir_salida = None,
        cargar_incidencias=False,
        cargar_datos_segundales=False,
        cargar_instancia=None
        ):
        
        initialize = True
        
        # Esto todavía no está resuelto.
        #la idea es que, con necesidades del testing, se puedan cargar objetos y guardar su estado
        # luego, crear nuevos objetos, pero retomar desde un estado anterior, guardado en un archivo.
        # Bastante complicado, ya que no es lo mismo "la instancia de un objeto" que "los datos que contiene"
        # Decidir qué hacer
        
        # if not cargar_instancia is None:
        #     if isinstance(cargar_instancia,Path):
        #         archivo = cargar_instancia.resolve()
        #     elif isinstance(cargar_instancia,str):
        #         archivo = Path(cargar_instancia).resolve()
        #     else:
        #         raise TypeError('Cargar instancia debe ser un objeto pathlib.Path o una ruta a un archivo .pickle en formato string')
            
        #     if cargar_instancia.suffix != '.pickle':
        #         raise ValueError('La ruta al archivo de instancia debe ser en formato .pickle')
        #     else:
        #         try:
        #             #self.load(str(archivo))
        #             #initialize = False
        #             pass
        #         except:
        #             pass

        if initialize:
            self.init_sequence(
                fecha_i = fecha_i,
                fecha_f = fecha_f,
                parques = parques,
                clientes = clientes,
                dir_salida = dir_salida,
                cargar_incidencias=cargar_incidencias,
                cargar_datos_segundales=cargar_datos_segundales,
                )
        
    def init_sequence(
        self,
        fecha_i,
        fecha_f,
        parques,
        clientes,
        dir_salida,
        cargar_incidencias,
        cargar_datos_segundales,
        ):
            super().__init__(
                cargar_incidencias=cargar_incidencias,
                parques = parques,
                clientes = clientes,
                )
            
            self._dir_salida = dirs.raiz if dir_salida == None else dir_salida 
            
            self._parques_excluidos = ['CFCALDEG',]
            self._parques = [parque for parque in parques if not parque in self._parques_excluidos]

            self._archivos_necesarios = None
            self._archivos_encontrados = None
            self._archivos_faltantes = None
            self._archivos_disponibles = None
            
            self._fecha_i = fechas.ayer() if fecha_i is None else fecha_i
            self._fecha_f = fechas.ayer() if fecha_f is None else fecha_f
            
            self.fecha_i = self._fecha_i
            self.fecha_f = self._fecha_f
            
            self._incidencias = None
            self._incidencias_explotadas = None
            self._incidencias_explotadas_ancho = None
            self._incidencias_desagrupadas = None
            
            self._rpt_consolidado_seg = None
            self._rpt_consolidado_udf = None
            
            self.rpt_iec61400 = None

            self._datos_s = None
            if cargar_incidencias:
                self._actualizar_incidencias()
            
            if cargar_datos_segundales:
                self.cargar_segundales()

    @property
    def fecha_i(self):
        return self._fecha_i
    
    @fecha_i.setter
    def fecha_i(self,val):
        '''Ingresar una fecha para usar como fecha inicial del rango a analizar/pricesar
        Puede ser un objeto datetime.datetime o texto (string)'''
        fi, ff = fechas.validar_fechas(val,self._fecha_f)
        self._fecha_i = fi
        self._fecha_f = ff
        self._actualizar_archivos()
        
    @property
    def fecha_f(self):
        return self._fecha_f
    
    @fecha_f.setter
    def fecha_f(self,val):
        '''Ingresar una fecha para usar como fecha final del rango a analizar/pricesar
        Puede ser un objeto datetime.datetime o texto (string)'''
        fi, ff = fechas.validar_fechas(self._fecha_i,val)
        self._fecha_i = fi
        self._fecha_f = ff
        self._actualizar_archivos()

    @property
    def incidencias(self):
        self._actualizar_incidencias()
        return self._incidencias
    
    @incidencias.setter
    def incidencias(self,val):
        raise AttributeError('La propiedad "incidencias" es de sólo lectura.')

    @property
    def incidencias_explotadas(self):
        return self._incidencias_explotadas
    
    @incidencias_explotadas.setter
    def incidencias_explotadas(self,val):
        raise AttributeError('La propiedad "incidencias_explotadas" es de sólo lectura.')
        
    @property
    def datos_seg(self):
        return self._datos_s
    
    @datos_seg.setter
    def datos_seg(self,val):
        self._datos_s = val
    
    @property
    def archivos_necesarios(self):
        '''Lista de Strings representando nombres de archivos con extensión
        No incluyen la ruta absoluta hacia su ubicación teórica'''
        return self._archivos_necesarios

    @property
    def archivos_encontrados(self):
        '''Lista de objetos pathlib.Path con los archivos reales encontrados'''
        return self._archivos_encontrados

    @property
    def archivos_faltantes(self):
        '''Archivos necesarios pero no encontrados
        Lista de Strings representando nombres de archivos con extensión
        No incluyen la ruta absoluta hacia su ubicación teórica'''
        return self._archivos_faltantes

    @property
    def archivos_disponibles(self):
        '''Combinación de archivos necesarios y encontrados
        Lista de Strings representando nombres de archivos con extensión
        No incluyen la ruta absoluta hacia su ubicación teórica'''
        return self._archivos_disponibles
        
    @archivos_necesarios.setter
    def archivos_necesarios(self,val):
        self._archivos_necesarios = val
    
    @archivos_encontrados.setter
    def archivos_encontrados(self,val):
        self._archivos_encontrados = val
    
    @archivos_faltantes.setter
    def archivos_faltantes(self,val):
        self._archivos_faltantes = val
    
    @archivos_disponibles.setter
    def archivos_disponibles(self,val):
        self._archivos_disponibles = val

    @property
    def dir_salida(self):
        return self._dir_salida

    @dir_salida.setter
    def dir_salida(self,val):
        '''Toma una ruta a una carpeta en formato string o como objeto pathlib.Path'''
        self._dir_salida = dirs.check_dir(val)
    
    def _actualizar_incidencias(self):
        
        if self.incidencias_todas is None:
            self._incidencias = None
        elif not isinstance(self.incidencias_todas,pd.DataFrame):
            raise TypeError('El atributo "incidencias_todas" debe ser del tipo pandas.DataFrame o None')
        else:
            if self.incidencias_todas.empty:
                self._incidencias = None
            else:
                
                flt_activa_a = (self.fecha_i <= self.incidencias_todas['End']) 
                flt_activa_b = (self.fecha_f >= self.incidencias_todas['Start'])
                flt_no_descartada = self.incidencias_todas['Status'].str.upper() != 'DESCARTADA'
                
                flt_activa = flt_activa_a & flt_activa_b & flt_no_descartada           
                flt_hay_plantas = False
                
                if self.parques == [] and self.clientes == []:
                    flt_hay_plantas = False
                    
                elif self.parques != []:
                    flt_plantas_a = self.incidencias_todas['UC'].isin(self.parques) 
                    flt_plantas_b = self.incidencias_todas['Nemo'].isin(self.parques) 
                    flt_plantas = flt_plantas_a | flt_plantas_b
                    flt_hay_plantas = True
                else:
                    flt_plantas = self.incidencias_todas['Owner'].isin(self.clientes) 
                    flt_hay_plantas = True
                
                if flt_hay_plantas:
                    self._incidencias = self.incidencias_todas.loc[flt_activa & flt_plantas,:]
                else:
                    self._incidencias = self.incidencias_todas.loc[flt_activa,:]

    def _actualizar_archivos(self):
        
        self.archivos_encontrados = self._obtener_archivos_encontrados()
        self.archivos_necesarios = self._obtener_archivos_necesarios()
        
        nombres_encontrados = [archivo.stem for archivo in self.archivos_encontrados]
        existe = lambda x: x.stem in nombres_encontrados
        no_existe = lambda x: not x.exists()

        self.archivos_faltantes = list(filter(no_existe,self.archivos_necesarios))
        self.archivos_disponibles = list(filter(existe,self.archivos_necesarios))
        
    def _obtener_archivos_encontrados(self):

        archivos_totales = self.__buscar_archivos_10s_ct_rango()
        parques_vacio = self.parques == [] or self.parques == None or len(self.parques)==0
        
        pertenece_a_parques_seleccionados = lambda archivo: any(parque in archivo.name for parque in self.parques)
        
        if parques_vacio:
            return archivos_totales
        else:
            return list(filter(pertenece_a_parques_seleccionados,archivos_totales))


    def _obtener_archivos_necesarios(self):
        
        iterable = fechas.iterar_entre_timestamps_diario(self.fecha_i,self.fecha_f)
        get_carpeta = lambda x : Path(dirs.get_dc_10s_fecha(x))
        
        carpetas = [get_carpeta(fi) for fi,_ in iterable]
        
        parques_vacio = self.parques == [] or self.parques == None or len(self.parques)==0
        parques = self.nemos if parques_vacio else self.parques

        if parques != []:
            archivos_necesarios = []
            for carpeta in carpetas:
                for parque in parques:
                    if parque in self._parques_excluidos:
                        continue

                    fecha_archivo = carpeta.stem.replace('-','.')
                    
                    archivo = f'{carpeta}\\{fecha_archivo} {parque}'
                    archivo_pickle = Path(archivo + '.pickle')
                    archivo_xlsx = Path(archivo + '.xlsx')
                    
                    if archivo_pickle.exists():
                        archivos_necesarios.append(archivo_pickle)
                    else:
                        archivos_necesarios.append(archivo_xlsx)
                        
            return archivos_necesarios
        else:
            return []


    def __buscar_archivos_10s_ct_rango(self):
        
        iterable = fechas.iterar_entre_timestamps_diario(self.fecha_i,self.fecha_f)
        
        lista_de_listas = [self.__buscar_archivos10s_diarios(fi) for fi,_ in iterable]
        lista_unificada = [archivo for lista_archivos in lista_de_listas for archivo in lista_archivos]
        return lista_unificada

    def __buscar_archivos10s_diarios(self,fecha):
        '''Para un día determinado, busca los archivos .xlsx de la central elegida.
        Importante: la fecha debe proveerse como objeto datetime'''
        
        dir_tmp = Path(dirs.get_dc_10s_fecha(fecha))
        if dir_tmp.exists():
        
            iterable = dir_tmp.iterdir()
            
            archivos_xlsx = dirs.filtra_archivos(iterable,'.xlsx')
            archivos_pickle = dirs.filtra_archivos(iterable,'.pickle')
            
            nombres_archivos_pickle = (archivo.stem for archivo in archivos_pickle)
            
            archivos_xlsx_no_procesados = [archivo for archivo in archivos_xlsx if not (archivo.stem in nombres_archivos_pickle)]
            
            return archivos_pickle + archivos_xlsx_no_procesados
        else:
            return []


    def __renombrar_lvl0(self,texto,prefijo_generador='WTG'):
        texto = texto.replace('Datos del parque','PLANT')
        
        if 'Unnamed: 0_level_0' in texto:
            texto = ''
        
        if 'Datos del equipo' in texto:
            generador = texto.split(' ')[-1].zfill(2)
            texto = ''.join([prefijo_generador,generador])

        return texto

    def __renombrar_lvl1(self,texto):
        v = texto
        v = v.replace('Wind Dir','wind_dir')
        v = v.replace('Wind Speed','wind')
        v = v.replace('P Disponible','P_Pos')
        v = v.replace('FB Consigna P Equipo','SP_P')
        v = v.replace('Q Equipo','Q')
        v = v.replace('P Equipo','P')
        v = v.replace('Estado','op_state')
        v = v.replace('Consigna P','SP_P')
        v = v.replace('Consigna Q','SP_Q')
        v = v.replace('Consigna V','SP_V')
        v = v.replace('FB ','FB_')
        
        return v

    def __obtener_id_central(self,nemo_central):
        mapeo_nemo_idcentral = self._crear_dict(self.central,'nemoCammesa','idcentral')
        return mapeo_nemo_idcentral[nemo_central]
        

    def __obtener_prefijo_equipos(self,nemo_central):
        
        id_central = self.__obtener_id_central(nemo_central)
        
        equipos = self.tipoequipo\
                    .query(f'id_central == {id_central} & fabricante.notnull()')\
                    .loc[:,'equipo']\
                    .to_list()
                    
        #Con esto alcanza para eólicos
        remover_numeros = lambda s: ''.join([c for c in s if not c.isdigit()])
        
        #Pensar cómo resolver para solares que tienen nombres tipo
        #INV1_25
        prefijo = set(map(remover_numeros,equipos))
        if len(prefijo) != 1:
            raise ValueError(f'Se han encontrado más de un prefijo de equipos para el parque {nemo_central}.\n A saber: {prefijo}')
        else:
            return prefijo


    def __renombrar_cols(self,cols,nemo_central):
        nuevas_cols = []
        for col in cols:
            
            # en la llamada a la función __renombrar_lvl0 debería estar la inteligencia previa
            # para detectar si las turbinas de dicho parque comienzan con WTG, o con "T", o con "V" u otro prefijo.
            # Adicionalmente, la cantidad de 0s delante de cada equipo, debería ser dinámica
            # de acuerdo a la cantidad de generadores en dicho parque. 
            
            prefijo = self.__obtener_prefijo_equipos(nemo_central)
            lvl0 = self.__renombrar_lvl0(col[0])
            lvl1 = self.__renombrar_lvl1(col[1])
            nuevas_cols.append((lvl0,lvl1))
        
        nuevas_cols[0] = ('t_stamp','t_stamp')
        return nuevas_cols

    def __preprocesar_un_xlsx(self,archivo):
        
        nemo_central = archivo.stem.split(' ')[-1]
        
        if archivo.exists():
            df = pd.read_excel(archivo,skiprows=1,header=[0,1])
            
            nuevas_columnas = self.__renombrar_cols(df.columns,nemo_central)
        
            df.columns = pd.MultiIndex.from_tuples(nuevas_columnas,names=['Equipo','Variable'])
            df.insert(1,('Park','Name'),nemo_central)
            
            nuevo_archivo = str(archivo.parent) + '\\' + archivo.stem + '.pickle'
            df.to_pickle(nuevo_archivo)
            del df
            gc.collect()
        else:
            # Esto debería haber quedado solucionado con la lógica de archivos disponibles vs necesarios.
            # ¿Qué pasó?
            print(f'El archivo "{archivo.name}" no existe.')
        
    def __preprocesar_disponibles(self):
        
        ahora = dt.datetime.now()
        
        a_pre_procesar = [archivo for archivo in self.archivos_disponibles if archivo.name.lower().endswith('.xlsx')]
        
        if a_pre_procesar:
            cantidad = len(a_pre_procesar)
            ritmo = cantidad/60
            print(f'Se pre-procesarán {cantidad} archivos Excel. Paciencia...')
            print(f'Tiempo estimado: {round(ritmo*20)} a {round(ritmo*50)} minutos.')
            
            for archivo in a_pre_procesar:
                print(f'Pre-procesando: {archivo.name}')
                self.__preprocesar_un_xlsx(archivo)
            self._actualizar_archivos()
            
            duracion = (dt.datetime.now() - ahora).total_seconds() 
            ritmo = duracion / len(a_pre_procesar)
            
            print(f'Pre-procesamiento finalizado. Duración: {round(duracion)}seg a razón de {round(ritmo)} seg/archivo.')
            
    def cargar_segundales(self,fecha_i=None,fecha_f=None):
        if not fecha_i is None:
            self.fecha_i = fecha_i
        
        if not fecha_f is None:
            self.fecha_f = fecha_f
        
        
        self.__preprocesar_disponibles()
        
        if len(self.archivos_disponibles) >0:
            print(f'Cargando {len(self.archivos_disponibles)} archivos en la memoria...')
            
            lista_dfs = []
            for archivo in self._archivos_disponibles:
                print(f'Cargando {archivo.name}...')
                lista_dfs.append(pd.read_pickle(archivo)) 
            
            self.datos_seg = pd.concat(lista_dfs,ignore_index=True)
            
            self.datos_seg[('t_stamp','t_stamp')] = pd.to_datetime(
                                                    self.datos_seg[('t_stamp','t_stamp')],
                                                    format='%Y-%m-%d %H:%M:%S'
                                                )
            
            columnas_para_indice = [('Park','Name'),('t_stamp','t_stamp')]
            nuevo_indice = pd.MultiIndex.from_frame(
                        self.datos_seg[columnas_para_indice],
                        names=['Park','t_stamp']
                        )
            self.datos_seg.index = nuevo_indice
            self.datos_seg = self.datos_seg\
                                .sort_index()\
                                .drop(columns=columnas_para_indice)
            
            del lista_dfs
            gc.collect()
            print('Listo!')
        else:
            raise Exception(f'No hay archivos con datos 10 segundales disponibles para cargar de los parques {self.parques}')
    
    def __check_periodo(self,periodo,intervalos):
        
        if isinstance(periodo,str):
            periodo = periodo.lower()
            if periodo not in intervalos.keys():
                raise ValueError(f'El período indicado no es un objeto datetime.timedelta ni está entre {list(intervalos.keys())}')
            else:
                return intervalos[periodo]

        elif not isinstance(periodo,dt.timedelta):
            raise TypeError('El parámetro "período" debe ser del tipo string o datetime.timedelta.')
        else:
            return periodo
             
    def explotar_incidencias(self,periodo='1dia'):
        
        intervalos = {
            '10seg':dt.timedelta(seconds=10),
            '1min':dt.timedelta(minutes=1),
            '10min':dt.timedelta(minutes=10),
            '15min':dt.timedelta(minutes=15),
            '1hora':dt.timedelta(hours=1),
            '1dia':dt.timedelta(days=1)
            }
        
        intervalo = self.__check_periodo(periodo,intervalos)
        
        cols_seleccion = [
            'ID',
            'Status',
            'UC',
            'Nemo',
            'Owner',
            'Start',
            'End',
            'Equipo',
            'PotEquipo',
            'GenType',
            'Hours',
            'ENS',
            'SolvedBy',
            'SolverAgent',
            'Reason',
            'Origin',
            'Code',
            'Pteo',
            'SP_P',
            'IEC_Label',
            'Priority_IEC',
            'Priority_WTG',
            'Priority_BOP',
            'Priority_GRID'
            ]
        
        iterable = self.incidencias.loc[:,cols_seleccion].iterrows()
        funcion = lambda x: self.__explotar_incidencia(x,intervalo)
        
        lista_dfs = [funcion(incidencia) for _ , incidencia in iterable]
        
        self._incidencias_explotadas = pd.concat(lista_dfs,ignore_index=True)

    def __explotar_incidencia(self,incidencia,intervalo):
        
        fecha_ini_real = incidencia['Start']
        fecha_fin_real = incidencia['End']
        fecha_ini_iter = fecha_ini_real.replace(hour=0,minute=0,second=0,microsecond=0)
        fecha_fin_iter = fecha_fin_real.replace(hour=23,minute=59,second=59,microsecond=0)

        iterable = fechas.iterar_entre_timestamps(fecha_ini_iter,fecha_fin_iter,intervalo)

        data = {
            'Start':[],
            'End':[],
            'Activa':[],
        }

        for fecha_i, fecha_f in iterable:
            activa = (fecha_ini_real < fecha_f) and (fecha_fin_real >= fecha_i)
            
            data['Start'].append(fecha_i)
            data['End'].append(fecha_f)
            data['Activa'].append(activa)

        if len(data['Activa']) == 1:
            data = incidencia.to_dict()
            return pd.DataFrame(data,index=[0])

        #Continuamos con incidencias de duración mayor a un registro
        df = pd.DataFrame(data)
        df = df[df['Activa']].copy(deep=True).reset_index(drop=True)
        try:
            df.iloc[0,0] = fecha_ini_real #Columna 'Start', primera fila
            df.iloc[-1,1] = fecha_fin_real #Columna 'End', última fila
            
            #Colocando el tiempo y la energía perdidos
            df['Hours'] = (df['End'] - df['Start']).dt.total_seconds()/3600
            df['ENS'] = incidencia['ENS'] * (df['Hours'] / incidencia['Hours'])
            
            #eliminar columna auxiliar
            df.drop(columns='Activa',inplace=True)
            
            for col in incidencia.index:
                if col not in df.columns:
                    df[col] = incidencia[col]
            
            return df.loc[:,incidencia.index]
            
        except:
            print(f'Error al procesar la incidencia {incidencia["ID"]}')




    def _crear_df_ancho_vacio(self,indice,variables,parque,equipo):
        cols = indice + variables
        listas_vacias = [[np.nan,] for x in cols]
        data = dict(zip(cols,listas_vacias))
        data['Park'] = parque
        df_vacio = pd.DataFrame(data)

        df_vacio.index = pd.MultiIndex.from_frame(
                                            df_vacio[indice],
                                            names=indice
                                            )

        df_vacio.drop(columns=indice,inplace=True)

        viejas_cols = df_vacio.columns.to_list()
        df_vacio.columns = pd.MultiIndex.from_product(
                    iterables=[[equipo,],viejas_cols],
                    names=['Equipo','Variables'])
        
        return df_vacio
        
    def _crear_df_ancho_vacio_agrup(self,parque,agrup):
        indice = ['Park','t_stamp']
        variables_por_incidencia = [
            'ID', 'Status', 
            'Equipo', 'PotEquipo', 'Hours', 'ENS', 
            'SolverAgent', 'Reason', 'Origin', 
            'IEC_Label', 'Priority_IEC', 'Priority_WTG', 'Priority_BOP', 'Priority_GRID'
            ]
        variables_por_agrupamiento = ['PotDisp','ENS_unitaria','Eteo']

        variables = variables_por_incidencia + variables_por_agrupamiento
        return self._crear_df_ancho_vacio(indice=indice,variables=variables,parque=parque,equipo=agrup)

    def _crear_df_ancho_vacio_equipo(self,parque,equipo):
        indice = ['Park','t_stamp']
        variables_por_incidencia = [
            'ID', 'Status', 
            'Equipo', 'PotEquipo', 'Hours', 'ENS', 
            'SolverAgent', 'Reason', 'Origin', 
            'IEC_Label', 'Priority_IEC', 'Priority_WTG', 'Priority_BOP', 'Priority_GRID'
            ]
        variables_por_equipo = ['DispTBA','ReasonTBA','DispPBA','ReasonEBA','ENS_unitaria','Eteo']

        variables = variables_por_incidencia + variables_por_equipo
        return self._crear_df_ancho_vacio(indice=indice,variables=variables,parque=parque,equipo=equipo)
    
    def _crear_df_ancho_vacio_parque(self,parque):
        
        agrupamientos = self.consultar_agrupamientos_parque(nemo_parque=parque)
        equipos_por_parque_no_agr = self.consultar_equipos_parque_no_agrupamientos(nemo_parque=parque)

        lista_dfs = []
        for equipo in self.consultar_equipos_parque(nemo_parque=parque):
            
            es_planta = equipo == 'PLANT'
            es_agrup = equipo in agrupamientos
            es_generador = equipo in equipos_por_parque_no_agr

            if es_planta or es_agrup:
                df_tmp = self._crear_df_ancho_vacio_agrup(parque,equipo)
                lista_dfs.append(df_tmp)
            elif es_generador:
                df_tmp = self._crear_df_ancho_vacio_equipo(parque,equipo)
                lista_dfs.append(df_tmp)
            else:
                print(f"No se pudo clasificar el equipo {equipo} para crear un df ancho vacío")

        return pd.concat(lista_dfs,axis=1)


    def _crear_df_ancho_vacio_parques(self):
        parques_con_datos_seg = self.datos_seg.index.levels[0]
        lista_dfs = [self._crear_df_ancho_vacio_parque(parque) for parque in parques_con_datos_seg]
        return pd.concat(lista_dfs,axis=0)

    def _incidencias_explotadas_formato_largo_a_ancho(self):
        #Incorporarle a esta función poder hacerlo para datos 10 seg o 10 min
        if self._incidencias_explotadas is None:
            self.explotar_incidencias('10seg')

        identificadores = ['Nemo','Start']
        cols_nuevo_indice = ['Park','t_stamp']
        renombrar_cols = dict(zip(identificadores,cols_nuevo_indice))

        variables_por_incidencia = [
            'ID', 'Status', 
            'Equipo', 'PotEquipo', 'Hours', 'ENS', 
            'SolverAgent', 'Reason', 'Origin', 
            'IEC_Label', 'Priority_IEC', 'Priority_WTG', 'Priority_BOP', 'Priority_GRID'
            ]

        get_equipos = lambda x: self.consultar_equipos_parque(nemo_parque=x)
        parques_con_datos = self.datos_seg.index.levels[0]
        equipos_por_parque = {parque:list(get_equipos(parque)) for parque in parques_con_datos}

        df_incr = None
        for parque,equipos in equipos_por_parque.items():
            flt_parque = self._incidencias_explotadas['Nemo'] == parque
            df_vacio_parque = self._crear_df_ancho_vacio_parque(parque=parque)
            
            for equipo in equipos:
                flt_equipo = self._incidencias_explotadas['Equipo'] == equipo
                flt_total = flt_parque & flt_equipo
                print(f'Hay {flt_total.sum()} registros explotados para {parque}, {equipo}')
                
                df_tmp = self._incidencias_explotadas\
                            .loc[flt_total,identificadores + variables_por_incidencia]\
                            .rename(columns=renombrar_cols)\
                            .copy(deep=True)
                            
                cols_contraste = df_vacio_parque.loc[(parque,slice(None)),(equipo,slice(None))].columns.get_level_values(1)
                cols_faltantes = [col for col in cols_contraste if not col in df_tmp.columns]
                for col in cols_faltantes:
                    df_tmp[col] = df_tmp[col] = np.nan
                
                nuevas_columnas = [('Park','Name'),('t_stamp','t_stamp')] + [(equipo,variable) for variable in df_tmp.columns[2:]]
                df_tmp.columns = pd.MultiIndex.from_tuples(nuevas_columnas,names=['Equipo','Variable'])
                
                if df_tmp.empty:
                    df_tmp.loc[0,('Park','Name')] = parque
            
                if df_incr is None:
                    df_incr = df_tmp.copy(deep=True)
                else:
                    df_incr = df_incr.merge(df_tmp,on=[('Park','Name'),('t_stamp','t_stamp')],how='outer')

        df_incr.index = pd.MultiIndex.from_frame(
                    df_incr[[('Park','Name'),('t_stamp','t_stamp')]],
                    names=cols_nuevo_indice
                    )

        cols_drop = [('Park','Name'),('t_stamp','t_stamp')] + df_incr.loc[:,(slice(None),'Equipo')].columns.to_list()

        df_incr.drop(columns=cols_drop,inplace=True)

        #Liberar memoria
        del df_tmp
        gc.collect()

        self._incidencias_explotadas_ancho = df_incr

    def reporte_consolidado_seg(self):

        if self._incidencias_explotadas_ancho is None:
            self._incidencias_explotadas_formato_largo_a_ancho()
        
        print("Combinando mediciones e incidencias explotadas")
        self._rpt_consolidado_seg = self.datos_seg\
                                        .join(self._incidencias_explotadas_ancho,how='left')\
                                        .sort_index(axis=0)
        
        get_equipos = lambda x: self.consultar_equipos_parque(nemo_parque=x)              
        parques_con_datos = self.datos_seg.index.levels[0]
        equipos_por_parque = {parque:list(get_equipos(parque)) for parque in parques_con_datos}
        
        
        viento_bins = np.arange(0,28,0.5)
        viento_labels = viento_bins[0:-1]
        
        for parque, equipos in equipos_por_parque.items():
            
            #Colocar la potencia nominal de cada generador/agrupamiento/planta
            potencias = self.consultar_equipos_parque(nemo_parque=parque,potencia=True)
            for equipo,potencia in potencias.items():
                self._rpt_consolidado_seg.loc[:,(equipo,'PotEquipo')] = potencia
                
            #==========================================
            #
            # Primera iteración "de abajo hacia arriba"
            #
            #==========================================
            
            #Eliminar np.nans para facilitar operaciones
            seleccion = (slice(None),['Hours','ENS',])
            self._rpt_consolidado_seg.loc[:,seleccion] = self._rpt_consolidado_seg.loc[:,seleccion].fillna(0)

            seleccion = (slice(None),['Priority_BOP','Priority_IEC','Priority_WTG','Priority_GRID'])
            self._rpt_consolidado_seg.loc[:,seleccion] = self._rpt_consolidado_seg.loc[:,seleccion].fillna(1)
            
            #Cambio de unidades
            seleccion = ('PLANT',['P','SP_P','Q'])
            self._rpt_consolidado_seg.loc[:,seleccion] = (self._rpt_consolidado_seg.loc[:,seleccion] *1000)
            
            seleccion = (slice(None),['P','SP_P','Q'])
            self._rpt_consolidado_seg.loc[:,seleccion] = (self._rpt_consolidado_seg.loc[:,seleccion] /1000).fillna(0)

            #Previo a llenar los valores NA, hay que calcular el promedio unitario
            seleccion = (slice(None),'P_Pos')
            self._rpt_consolidado_seg.loc[:,seleccion] = (self._rpt_consolidado_seg.loc[:,seleccion] /1000)
            
            
            indisponibilidad_TBA = ['MAPRO','MANOPRO','MAPRO S_A','FAILURE']

            equipos_por_parque_no_agr = self.consultar_equipos_parque_no_agrupamientos(nemo_parque=parque)
            for equipo in equipos_por_parque_no_agr:
                print(f'Iteración 1: Calculando variables indirectas: {parque}, {equipo}')
                #Calcular la Eteo como Ener generada + Ener No Suministrada
                self._rpt_consolidado_seg.loc[:,(equipo,'Eact')] = self._rpt_consolidado_seg.loc[:,(equipo,'P')].apply(lambda x: x * (1/360) if x > 0 else 0)
                self._rpt_consolidado_seg.loc[:,(equipo,'Eteo')] = self._rpt_consolidado_seg.loc[:,(equipo,'Eact')] + self._rpt_consolidado_seg.loc[:,(equipo,'ENS')]
                self._rpt_consolidado_seg.loc[:,(equipo,'Epos')] = self._rpt_consolidado_seg.loc[:,(equipo,'P_Pos')].apply(lambda x: x * (1/360) if x > 0 else 0)

                #Colocar disponibilidad verdadero/falso para todas las incidencias que no sean limitaciones ni control de reactivo
                self._rpt_consolidado_seg.loc[:,(equipo,'Limitacion')] = self._rpt_consolidado_seg.loc[:,(equipo,'Reason')] == 'LIMITATION'
                self._rpt_consolidado_seg.loc[:,(equipo,'DispTBA')] = self._rpt_consolidado_seg.loc[:,(equipo,'Reason')].apply(lambda x: False if x in indisponibilidad_TBA else True)
                self._rpt_consolidado_seg.loc[:,(equipo,'PotDisp')] = self._rpt_consolidado_seg.loc[:,(equipo,'DispTBA')] * self._rpt_consolidado_seg.loc[:,(equipo,'PotEquipo')]
                
                #Colocar disponibilidad 0 a 1 en base a P, ENS y Eteo
                self._rpt_consolidado_seg.loc[:,(equipo,'DispPBA')] = (self._rpt_consolidado_seg.loc[:,(equipo,'Eact')] / self._rpt_consolidado_seg.loc[:,(equipo,'Eteo')]).fillna(1)
                self._rpt_consolidado_seg.loc[:,(equipo,'PI')] = self._rpt_consolidado_seg.loc[:,(equipo,'Eact')] / self._rpt_consolidado_seg.loc[:,(equipo,'Epos')]
                
                #Convertir dirección de vientos a rosa de los vientos
                self._rpt_consolidado_seg.loc[:,(equipo,'wind_dir')] = self._rpt_consolidado_seg.loc[:,(equipo,'wind_dir')].apply(eo.convertir_a_rosa_de_los_vientos)
                
                #Convertir la velocidad de viento a bins de 0.5
                self._rpt_consolidado_seg.loc[:,(equipo,'wind_bins')] = pd.cut(
                                                                            self._rpt_consolidado_seg.loc[:,(equipo,'wind')],
                                                                            bins=viento_bins,
                                                                            labels=viento_labels,
                                                                            ordered=True
                                                                            )
                #Definir valores unitarios
                self._rpt_consolidado_seg.loc[:,(equipo,'P_Pos_unitaria')] = self._rpt_consolidado_seg.loc[:,(equipo,'P_Pos')] / self._rpt_consolidado_seg.loc[:,(equipo,'PotEquipo')]
                self._rpt_consolidado_seg.loc[:,(equipo,'Eact_unitaria')] = self._rpt_consolidado_seg.loc[:,(equipo,'Eact')] / self._rpt_consolidado_seg.loc[:,(equipo,'PotEquipo')]
                self._rpt_consolidado_seg.loc[:,(equipo,'Eteo_unitaria')] = self._rpt_consolidado_seg.loc[:,(equipo,'Eteo')] / self._rpt_consolidado_seg.loc[:,(equipo,'PotEquipo')]
                self._rpt_consolidado_seg.loc[:,(equipo,'ENS_unitaria')] = self._rpt_consolidado_seg.loc[:,(equipo,'ENS')] / self._rpt_consolidado_seg.loc[:,(equipo,'PotEquipo')]


                
            #Calcular valores por agrupamientos (Normalmente circuitos que engloban más de un generador)
            agrupamientos = self.consultar_equipos_por_agrupamiento(nemo_parque=parque)
            for equipo,equipos_asociados in agrupamientos.items():
                print(f'Iteración 1: Calculando variables indirectas: {parque}, {equipo}. Equipos asociados: {equipos_asociados}')
                self._rpt_consolidado_seg.loc[:,(equipo,'P')] = self._rpt_consolidado_seg.loc[:,(equipos_asociados,'P')].sum(axis=1)
                self._rpt_consolidado_seg.loc[:,(equipo,'Eact')] = self._rpt_consolidado_seg.loc[:,(equipo,'P')].apply(lambda x: x * (1/360) if x > 0 else 0)
                self._rpt_consolidado_seg.loc[:,(equipo,'Eteo')] = self._rpt_consolidado_seg.loc[:,(equipo,'Eact')] + self._rpt_consolidado_seg.loc[:,(equipo,'ENS')]
                self._rpt_consolidado_seg.loc[:,(equipo,'Eteo_asoc')] = self._rpt_consolidado_seg.loc[:,(equipos_asociados,'ENS')].sum(axis=1)
                
                self._rpt_consolidado_seg.loc[:,(equipo,'P_Pos_unitaria')] = self._rpt_consolidado_seg.loc[:,(equipos_asociados,'P_Pos')].mean(axis=1)
                self._rpt_consolidado_seg.loc[:,(equipo,'Eact_unitaria')] = self._rpt_consolidado_seg.loc[:,(equipo,'ENS')] / self._rpt_consolidado_seg.loc[:,(equipo,'PotEquipo')]
                self._rpt_consolidado_seg.loc[:,(equipo,'Eteo_unitaria')] = self._rpt_consolidado_seg.loc[:,(equipo,'ENS')] / self._rpt_consolidado_seg.loc[:,(equipo,'PotEquipo')]
                self._rpt_consolidado_seg.loc[:,(equipo,'ENS_unitaria')] = self._rpt_consolidado_seg.loc[:,(equipo,'ENS')] / self._rpt_consolidado_seg.loc[:,(equipo,'PotEquipo')]

                self._rpt_consolidado_seg.loc[:,(equipo,'Limitacion')] = self._rpt_consolidado_seg.loc[:,(equipo,'Reason')] == 'LIMITATION'
                self._rpt_consolidado_seg.loc[:,(equipo,'DispTBA')] = self._rpt_consolidado_seg.loc[:,(equipo,'Reason')].apply(lambda x: False if x in indisponibilidad_TBA else True)
                self._rpt_consolidado_seg.loc[:,(equipo,'PotDisp')] = self._rpt_consolidado_seg.loc[:,(equipo,'DispTBA')] * potencias[equipo]
                self._rpt_consolidado_seg.loc[:,(equipo,'PotDisp_asoc')] = self._rpt_consolidado_seg.loc[:,(equipos_asociados,'PotDisp')].sum(axis=1)
                self._rpt_consolidado_seg.loc[:,(equipo,'DispTBA_asoc')] = self._rpt_consolidado_seg.loc[:,(equipo,'PotDisp_asoc')] / self._rpt_consolidado_seg.loc[:,(equipo,'PotEquipo')]
                
                self._rpt_consolidado_seg.loc[:,(equipo,'PI')] = (self._rpt_consolidado_seg.loc[:,(equipos_asociados,'Eact')].sum(axis=1) / self._rpt_consolidado_seg.loc[:,(equipos_asociados,'Epos')].sum(axis=1)).fillna(1)
                self._rpt_consolidado_seg.loc[:,(equipo,'ENS_unitaria_disp')] = (self._rpt_consolidado_seg.loc[:,(equipo,'ENS')] / self._rpt_consolidado_seg.loc[:,(equipo,'DispTBA_asoc')]).fillna(0)

            #Variables calculadas para el parque completo
            print(f'Iteración 1: Calculando variables indirectas: {parque}, PLANT')
            self._rpt_consolidado_seg.loc[:,('PLANT','wind')] = self._rpt_consolidado_seg.loc[:,(slice(None),'wind')].mean(axis=1)
            self._rpt_consolidado_seg.loc[:,('PLANT','wind_bins')] = pd.cut(
                                                                        self._rpt_consolidado_seg.loc[:,('PLANT','wind')],
                                                                        bins=viento_bins,
                                                                        labels=viento_labels,
                                                                        ordered=True
                                                                        )
            self._rpt_consolidado_seg.loc[:,('PLANT','Eact')] = self._rpt_consolidado_seg.loc[:,('PLANT','P')].apply(lambda x: x * (1/360) if x > 0 else 0)
            self._rpt_consolidado_seg.loc[:,('PLANT','PotDisp_asoc')] = self._rpt_consolidado_seg.loc[:,(equipos_por_parque_no_agr,'PotDisp')].sum(axis=1)
            self._rpt_consolidado_seg.loc[:,('PLANT','DispTBA_asoc')] = self._rpt_consolidado_seg.loc[:,('PLANT','PotDisp_asoc')] / self._rpt_consolidado_seg.loc[:,('PLANT','PotEquipo')]
            self._rpt_consolidado_seg.loc[:,('PLANT','P_Pos_unitaria')] = self._rpt_consolidado_seg.loc[:,(slice(None),'P_Pos_unitaria')].mean(axis=1)
            self._rpt_consolidado_seg.loc[:,('PLANT','P_Pos')] = self._rpt_consolidado_seg.loc[:,('PLANT','P_Pos_unitaria')] * self._rpt_consolidado_seg.loc[:,('PLANT','PotEquipo')]
            self._rpt_consolidado_seg.loc[:,('PLANT','Eteo')] = self._rpt_consolidado_seg.loc[:,('PLANT','Eact')] + self._rpt_consolidado_seg.loc[:,('PLANT','ENS')]
            self._rpt_consolidado_seg.loc[:,('PLANT','Eteo_unitaria')] = self._rpt_consolidado_seg.loc[:,('PLANT','Eteo')] / self._rpt_consolidado_seg.loc[:,('PLANT','PotEquipo')]
            self._rpt_consolidado_seg.loc[:,('PLANT','ENS_unitaria')] = self._rpt_consolidado_seg.loc[:,('PLANT','ENS')] / self._rpt_consolidado_seg.loc[:,('PLANT','PotEquipo')]
            self._rpt_consolidado_seg.loc[:,('PLANT','PotDisp')] = self._rpt_consolidado_seg.loc[:,(equipos_por_parque_no_agr,'PotDisp')].sum(axis=1)
            self._rpt_consolidado_seg.loc[:,('PLANT','Limitacion')] = self._rpt_consolidado_seg.loc[:,('PLANT','Reason')] == 'LIMITATION'
            self._rpt_consolidado_seg.loc[:,('PLANT','DispTBA')] = self._rpt_consolidado_seg.loc[:,('PLANT','Reason')].apply(lambda x: False if x in indisponibilidad_TBA else True)
            self._rpt_consolidado_seg.loc[:,('PLANT','FullPerf')] = (~self._rpt_consolidado_seg.loc[:,('PLANT','Limitacion')]) & (self._rpt_consolidado_seg.loc[:,('PLANT','DispTBA')])
            self._rpt_consolidado_seg.loc[:,('PLANT','ENS_unitaria_disp')] = (self._rpt_consolidado_seg.loc[:,('PLANT','ENS')] / self._rpt_consolidado_seg.loc[:,('PLANT','DispTBA_asoc')]).fillna(0)
            self._rpt_consolidado_seg.loc[:,('PLANT','PI')] = (self._rpt_consolidado_seg.loc[:,(equipos_por_parque_no_agr,'Eact')].sum(axis=1) / self._rpt_consolidado_seg.loc[:,(equipos_por_parque_no_agr,'Epos')].sum(axis=1)).fillna(1)
            #==========================================
            #
            # Segunda iteración "roll down" de incidencias
            #
            #==========================================
            print(f'Iteración 2: Calculando variables indirectas: Rolldown de Energía perdida y estado de Full Performance')
            flt_parque_fullperf = self._rpt_consolidado_seg.loc[:,('PLANT','FullPerf')] 

            #Calcular estado de full performance de los agrupamientos 
            for equipo in agrupamientos.keys():
                print(f'Iteración 2: Calculando estado Full Performance: {parque}, {equipo}')
                flt_agrupamiento_limitado = self._rpt_consolidado_seg.loc[:,(equipo,'Limitacion')]
                flt_agrupamiento_disponible = self._rpt_consolidado_seg.loc[:,(equipo,'DispTBA')]
                self._rpt_consolidado_seg.loc[:,(equipo,'FullPerf')] = ~flt_agrupamiento_limitado & flt_agrupamiento_disponible & flt_parque_fullperf
                
                #Falta llenar los huecos acá (Eteo, P_Pos,ws)
                
            #Calcular estado de full performance de los generadores individuales 
            df = self.conjuntogeneradores.query(f'Nemo == "{parque}"')
            agrups_por_equipo = self._crear_dict(df,'equipo','Agrupamiento')
            for equipo in equipos_por_parque_no_agr:
                print(f'Iteración 2: Calculando variables indirectas: {parque}, {equipo}')
                agrupamiento = agrups_por_equipo[equipo]
                
                flt_equipo_limitado = self._rpt_consolidado_seg.loc[:,(equipo,'Limitacion')]
                flt_equipo_disponible = self._rpt_consolidado_seg.loc[:,(equipo,'DispTBA')]
                flt_agrupamiento_fullperf = self._rpt_consolidado_seg.loc[:,(agrupamiento,'FullPerf')]


                ens_unit_parque = self._rpt_consolidado_seg.loc[:,('PLANT','ENS_unitaria_disp')]
                ens_unit_agrup = self._rpt_consolidado_seg.loc[:,(agrupamiento,'ENS_unitaria_disp')]
                ens_unit_equipo = ens_unit_parque + ens_unit_agrup
                
                self._rpt_consolidado_seg.loc[:,(equipo,'FullPerf')] = ~flt_equipo_limitado & flt_equipo_disponible & flt_agrupamiento_fullperf
                self._rpt_consolidado_seg.loc[:,(equipo,'ENS_rolldown')] = ens_unit_equipo* self._rpt_consolidado_seg.loc[:,(equipo,'PotDisp')]
                self._rpt_consolidado_seg.loc[:,(equipo,'Eteo_rolldown')] = self._rpt_consolidado_seg.loc[:,(equipo,'ENS_rolldown')] + self._rpt_consolidado_seg.loc[:,(equipo,'Eact')]
                self._rpt_consolidado_seg.loc[:,(equipo,'DispPBA_rolldown')] = (self._rpt_consolidado_seg.loc[:,(equipo,'Eact')] / self._rpt_consolidado_seg.loc[:,(equipo,'Eteo_rolldown')]).fillna(1)
                
                #Falta llenar los huecos acá (Eteo, P_Pos,ws)

        self._rpt_consolidado_seg = self._rpt_consolidado_seg.sort_index(axis=1).copy(deep=True)


    def __rolldown_incidencias(self,metodo='WTG'):
        metodos_posibles = ['WTG','BOP','GRID','IEC']

        cols_por_incidencia = [
            'Priority_WTG',
            'Priority_BOP',
            'Priority_GRID',
            'Priority_IEC',
            'Reason',
            'SolverAgent',
            ]
        
        
        if not isinstance(metodo,str):
            raise TypeError('La variable método debe ser del tipo String')
        else:
            metodo = metodo.upper()
            if not metodo in metodos_posibles:
                raise ValueError(f'Error, la variable "método" es {metodo} y debe ser alguna de las siguientes opciones: {metodos_posibles}')
            else:
                col_prioridad = f'Priority_{metodo}'


        parques_con_datos = self.datos_seg.index.levels[0]
        
        for parque in parques_con_datos:
            print(f'Roll Down de incidencias: {parque}')
            
            parque_selec = (parque,slice(None))
            plant_selec = ('PLANT',cols_por_incidencia)
            plant_prioridad = ('PLANT',col_prioridad)
            
            flt_tiene_inci_plant = self._rpt_consolidado_seg.loc[parque_selec,plant_prioridad] > 1

            agrupamientos = self.consultar_equipos_por_agrupamiento(nemo_parque=parque) 
            for agrup,equipos_asociados in agrupamientos.items():
                agrup_selec = (agrup,cols_por_incidencia)
                agrup_prioridad = (agrup,col_prioridad)
                flt_tiene_inci_agrup = self._rpt_consolidado_seg.loc[parque_selec,agrup_prioridad] > 1
                
                for equipo in equipos_asociados:
                    print(f'Roll Down de incidencias: {parque} {equipo}. Buscando Incidencias...')
                    equipo_selec = (equipo,cols_por_incidencia)
                    equipo_prioridad = (equipo,col_prioridad)
                    flt_tiene_inci_equipo = self._rpt_consolidado_seg.loc[parque_selec,equipo_prioridad] > 1
                    
                    flt = flt_tiene_inci_plant | flt_tiene_inci_agrup | flt_tiene_inci_equipo
                    
                    j = None
                    for i in self._rpt_consolidado_seg.loc[flt,:].index:
                        if j != i[1].date():
                            j = i[1].date()
                            print(f'Roll Down de incidencias: {parque} {equipo} {j}. Procesando')
                            
                        if self._rpt_consolidado_seg.loc[[i],[plant_prioridad]].iat[0,0] > self._rpt_consolidado_seg.loc[[i],[agrup_prioridad]].iat[0,0]:
                            self._rpt_consolidado_seg.loc[i,agrup_selec] = self._rpt_consolidado_seg.loc[i,plant_selec]

                            if self._rpt_consolidado_seg.loc[[i],[equipo_prioridad]].iat[0,0] > self._rpt_consolidado_seg.loc[[i],[agrup_prioridad]].iat[0,0]:
                                self._rpt_consolidado_seg.loc[i,equipo_selec] = self._rpt_consolidado_seg.loc[i,agrup_selec]
        print('Listo!')                


    def reporte_iec61400(self,metodo='WTG',granularidades=['1D','1M'],ruta=None,nombre=None):
        
        self.__rolldown_incidencias(metodo=metodo)
        
        indisponibilidad_TBA = ['MAPRO','MANOPRO','MAPRO S_A','FAILURE']
        parques_con_datos = self.datos_seg.index.levels[0]
        
        df = self._rpt_consolidado_seg.copy(deep=True)
        
        #Eliminar columnas innecesarias, ya que se hizo un rolldown
        agrupamientos = {'PLANT',}
        for parque in parques_con_datos:
            agrupspamientos_tmp = self.consultar_equipos_por_agrupamiento(nemo_parque=parque)
            agrupamientos = agrupamientos | set(agrupspamientos_tmp.keys())
            
        agrupamientos = list(agrupamientos)

        cols_drop = df.loc[:,(agrupamientos,slice(None))].columns
        df.drop(columns=cols_drop,inplace=True)
        
        cols_keep = df.loc[:,(slice(None),['DispTBA','PotDisp','PotEquipo','Reason','Eact','Eteo','Epos','PI','DispPBA','Eteo_rolldown','DispPBA_rolldown'])].columns
        cols_drop = [col for col in df.columns if not col in cols_keep]
        df.drop(columns=cols_drop,inplace=True)
        
        #Iniciar proceso de recálculo de TBA y PBA (último aún no disponible)
        print('Recalculando Valores de TBA y PBA')
        for parque in parques_con_datos:
            print(f'Parque: {parque}')
            equipos_por_parque_no_agr = self.consultar_equipos_parque_no_agrupamientos(nemo_parque=parque)
            
            for equipo in equipos_por_parque_no_agr:
                print(f'Equipo: {equipo}')
                df.loc[:,(equipo,'DispTBA')] = df.loc[:,(equipo,'Reason')].apply(lambda x: False if x in indisponibilidad_TBA else True)
                df.loc[:,(equipo,'PotDisp')] = df.loc[:,(equipo,'DispTBA')] * df.loc[:,(equipo,'PotEquipo')]
        print('Listo!')
        
        #Hechos todos los ajustes, se procede a reducir el dataframe
        seleccion = (slice(None),['Eact','DispTBA','DispPBA_rolldown','PI','Eteo','Eteo_rolldown','Epos','PotDisp'])
        
        df = df.loc[:,seleccion].copy(deep=True)
                
        self.rpt_iec61400 = df
        
        for parque in parques_con_datos:
            
            if not nombre:
                #Exportar curvas por parque
                fecha_str = dt.datetime.now().strftime("%Y-%m-%d %H.%M.%S")
                fecha_i_str = self.fecha_i.strftime("%Y-%m-%d")
                fecha_f_str = self.fecha_f.strftime("%Y-%m-%d")
                nombre_rpt = f'IEC61400 {parque} {fecha_i_str} a {fecha_f_str} {fecha_str}.xlsx'
                
            if not ruta:
                ruta = str(Path.cwd())
                
            ruta_archivo = ruta + '\\' + nombre_rpt
            
            with pd.ExcelWriter(ruta_archivo) as writer:
                for g in granularidades:
                    print(f'Exportando datos de {parque}, con granularidad {g}')
                    df = self.__consolidar_rpt_iec61400(g)
                    df.to_excel(writer,sheet_name=g,index=False)

    def __consolidar_rpt_iec61400(self,granularidad):
        
        df = self.rpt_iec61400
        
        cols_prom = df.loc[:,(slice(None),['DispTBA'])].sort_index(axis=1).columns
        cols_suma = df.loc[:,(slice(None),['Eact','Epos','Eteo_rolldown'])].sort_index(axis=1).columns

        df = df.reset_index().set_index('t_stamp')

        # Calcular valores promedios y valores sumados, por granularidad deseada y por turbina.
        df_prom = df.reset_index().set_index('t_stamp').loc[:,cols_prom].resample(granularidad).mean()
        df_suma = df.reset_index().set_index('t_stamp').loc[:,cols_suma].resample(granularidad).sum()

        for equipo in df_suma.columns.get_level_values(0):
            df_suma.loc[:,(equipo,'DispPBA')] = df_suma.loc[:,(equipo,'Eact')] / df_suma.loc[:,(equipo,'Eteo_rolldown')]
            df_suma.loc[:,(equipo,'PI')] = df_suma.loc[:,(equipo,'Eact')] / df_suma.loc[:,(equipo,'Epos')]

        df_resampled = pd.concat([df_prom,df_suma],axis=1).sort_index(axis=1)

        #Reformatear las tablas, llenar huecos y exportar.
        df_resampled = df_resampled\
                            .melt(ignore_index=False)\
                            .reset_index()\
                            .pivot(index=['t_stamp','Equipo'],columns='Variable',values='value')\
                            .reset_index()

        df_resampled.loc[:,['DispPBA','DispTBA','PI']] = df_resampled.loc[:,['DispPBA','DispTBA','PI']].fillna(1)
        
        return df_resampled
        
    def __generar_matriz_curvas_de_potencia(self,df,variable,funcion=np.mean):
        df_tmp = df.pivot_table(values=variable,index='wind_bins',columns='Equipo',aggfunc=funcion)\
                    .reset_index()\
                    .rename_axis(None,axis=1)
        return df_tmp
    
    
    def reporte_curvas_de_potencia(self,ruta=None,nombre=None):

        get_equipos = lambda x: self.consultar_equipos_parque(nemo_parque=x)              
        parques_con_datos = self.datos_seg.index.levels[0]
        equipos_por_parque = {parque:list(get_equipos(parque)) for parque in parques_con_datos}
        
        for parque in equipos_por_parque.keys():
            equipos = self.consultar_equipos_parque_no_agrupamientos(nemo_parque=parque)
    
            filtro = self._rpt_consolidado_seg.loc[:,(equipos,'FullPerf')].reset_index(drop=True)
            filtro.columns = filtro.columns.get_level_values(0)
    
            potencia = self._rpt_consolidado_seg\
                            .loc[:,(equipos,'P')]\
                            .reset_index(drop=True)[filtro]\
                            .melt(value_name='P')\
                            .drop(columns='Variable')
                            
            viento_bin = self._rpt_consolidado_seg\
                            .loc[:,(equipos,'wind_bins')]\
                            .reset_index(drop=True)[filtro]\
                            .melt(value_name='wind_bins')\
                            .drop(columns=['Equipo','Variable'])
                            
            viento_vel = self._rpt_consolidado_seg\
                            .loc[:,(equipos,'wind')]\
                            .reset_index(drop=True)[filtro]\
                            .melt(value_name='wind')\
                            .drop(columns=['Equipo','Variable'])
    
            df_resumido = pd.concat([potencia,viento_bin,viento_vel],axis=1)

            #Crear curvas por parque
            df_curvas_p = self.__generar_matriz_curvas_de_potencia(df_resumido,variable='P',funcion=np.mean)
            df_curvas_cuenta = self.__generar_matriz_curvas_de_potencia(df_resumido,variable='P',funcion='count')
            df_curvas_ws = self.__generar_matriz_curvas_de_potencia(df_resumido,variable='wind',funcion=np.mean)

            #Exportar curvas por parque
            if not nombre:
                fecha_str = dt.datetime.now().strftime("%Y-%m-%d %H.%M.%S")
                fecha_i_str = self.fecha_i.strftime("%Y-%m-%d")
                fecha_f_str = self.fecha_f.strftime("%Y-%m-%d")
                nombre_rpt = f'PC {parque} {fecha_i_str} a {fecha_f_str} {fecha_str}.xlsx'
            
            if not ruta:
                ruta = str(Path.cwd())
            
            archivo = Path(ruta + '\\' + nombre_rpt)
            with pd.ExcelWriter(str(archivo)) as writer:
                df_curvas_p.to_excel(writer,sheet_name='CP_Pot_Prom',index=False)
                df_curvas_cuenta.to_excel(writer,sheet_name='CP_Frecuencia',index=False)
                df_curvas_ws.to_excel(writer,sheet_name='CP_WS_promedio',index=False)