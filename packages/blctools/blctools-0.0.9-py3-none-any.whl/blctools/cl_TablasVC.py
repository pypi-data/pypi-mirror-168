from . import dirs
from . import fechas

import pymysql
import numpy as np
import pandas as pd
import datetime as dt

__all__ = ['TablasVC',]

class TablasVC():
    
    def __init__(
        self,
        cargar_incidencias=False,
        parques = [],
        clientes = [],
        ):

        self.dfs = {}
        self._idsApiCammesa = {}
        self._ucs = []
        self._nemos = []
        self._parques = parques
        self._clientes = clientes
        
        self.incidencias_todas_auditoria = None
        self.incidencias_todas = None
        self.central = None
        self.origen = None
        self.empresas = None
        self.centralesempresas = None
        self.razones = None
        self.estado = None
        self.tipoequipo = None
        self.tipogenerador = None
        self.conjuntogeneradores = None
        
        self._idApiC_a_nemo = {}
        self._nemo_a_uc = {}
        self._nemo_a_idApiC = {}
        self._nemo_a_owner = {}
        self._uc_a_nemo = {}
        self._uc_a_owner = {}
        self._uc_a_idApiC = {}
        
        self._empresas_bop = None
        self._empresas_gen = None
        self._empresas_grid = None
        
        self._iec61400 = None
        self._iec61400_metodos = ['IEC','WTG','BOP','GRID']
        self.__procesar_norma_iec_61400()
        
        self.incidencias_todas = None
        self.incidencias_todas_auditoria = None
        
        self.conexion = None
        self.host = '10.230.1.152'
        self.database = 'crom'
        self.user = 'driobo'
        self.password = 'd13g0'
        
        self.consultar_datos_basicos()
        if cargar_incidencias:
            self.consultar_incidencias()

    @property
    def parques(self):
        return self._parques
    
    @parques.setter
    def parques(self,val):
        self.__check_cliente_parque(val,tipo='parques')
        if val != []:
            self.clientes = []
    
        self._parques = val

    @property
    def clientes(self):
        return self._clientes
    
    @clientes.setter
    def clientes(self,val):
        self.__check_cliente_parque(val,tipo='clientes')
        if val != []:
            self.parques = []
        
        self._clientes = val
    
    @property
    def idsApiCammesa(self):
        
        if self._idsApiCammesa == {}:
            try:
                df = self.central
            except:
                self.consultar_datos_basicos()
                
            if self.conexion.open:
                self.consultar_idsApiCammesa()
            
        return self._idsApiCammesa
    
    @idsApiCammesa.setter
    def idsApiCammesa(self,val):
        if not isinstance(val,dict):
            raise TypeError('Las IDs de la Api de CAMMESA deben ingresarse como un diccionario {Unidadcomercial : ID}')
        else:
            self._idsApiCammesa = val
        
    @property
    def ucs(self):
        if self._ucs == []:
            if not self.__check_conexion():
                self.consultar_datos_basicos()
            else:
                self.consultar_ucs(solo_CROM=False)
            
        return self._ucs
    
    @ucs.setter
    def ucs(self,val):
        if not isinstance(val,(list,set,tuple)):
            raise TypeError('Las unidades comerciales deben listarse en una lista, tupla o set')
        else:
            if isinstance(val,list):
                self._ucs = val
            else:
                self._ucs = list(val)
                
    @property
    def nemos(self):
        if self._nemos == []:
            if not self.__check_conexion():
                self.consultar_datos_basicos()
            else: 
                self.consultar_nemoCammesa()
            
        return self._nemos
    
    @nemos.setter
    def nemos(self,val):
        if not isinstance(val,(list,set,tuple)):
            raise TypeError('Los Mnemotécnicos de CAMMESA deben listarse en una lista, tupla o set')
        else:
            if isinstance(val,list):
                self._nemos = val
            else:
                self._nemos = list(val)

    @property
    def dir_salida(self):
        return self._dir_salida

    @dir_salida.setter
    def dir_salida(self,val):
        '''Toma una ruta a una carpeta en formato string o como objeto pathlib.Path'''
        self._dir_salida = dirs.check_dir(val)    

    def __check_cliente_parque(self,val,tipo='parques'):
        
        if isinstance(val,(list,set,tuple)):
            str_filter =lambda x: isinstance(x,str)
            results = map(str_filter,val)
            if all(results):
                #Acá se podría agregar un chequeo de que los clientes/parques estén en la lista del CROM, en caso de estar conectado.
                return True
            else:
                raise TypeError(f'Todos los valores dentro de la lista "{tipo}" deben ser del tipo string.')
        else:
            raise TypeError(f'Se esperaba una lista, set o tuple para la variable "{tipo}".')

    def __check_conexion(self):
        
        if self.conexion is None:
            return False
        else:
            return self.conexion.open
        
    def __conectar(self):
        try:
            self.conexion = pymysql.connect(host=self.host,database=self.database,user=self.user,password=self.password)
        except:
            print('No se pudo conectar a la base de datos del CROM.\n Chequee su conexión a internet y a la VPN')

    def __consultar(self,tablas):
        if not isinstance(tablas,(list,tuple,set)):
            raise Exception('El listado de tablas debe ser del tipo lista, tupla o set')
        
        elif len(tablas) == 0:
            raise Exception('Debe ingresar al menos una tabla en la lista de tablas')
        
        elif self.conexion is None or not self.conexion.open:
            self.__conectar()
            print(f'Conexión exitosa')

        if self.__check_conexion():
            SQL_a_DF = lambda x: pd.read_sql(f'SELECT * FROM {x}',self.conexion)
            for tabla in tablas:
                self.dfs[tabla] = SQL_a_DF(tabla)
                self.__asignar_datos(tabla)
        else:
            print('No se pudo conectar al CROM para recuperar las incidencias.')

    def __asignar_datos(self,tabla):
        if tabla == 'central':
            self.central = self.dfs['central']
            self.central['idApiCammesa'] = self.central['idApiCammesa'].astype('Int64')
            
        elif tabla == 'origen':
            self.origen = self.dfs['origen']
            
        elif tabla == 'empresas':
            self.empresas = self.dfs['empresas']\
                                .rename(columns={'nombre':'Empresa'})\
                                .applymap(lambda x : np.nan if x == 0 else x)
            
            flt_bop = ~self.empresas['mantenimientoBOP'].isna()
            flt_gen = ~self.empresas['generador'].isna() 
            flt_opL = ~self.empresas['operacionLocal'].isna()
            flt_mantL = ~self.empresas['mantenimientoparque'].isna() 
            flt_traspo = ~self.empresas['transportista'].isna()
            flt_distro = ~self.empresas['distribuidora'].isna()
            flt_adm = ~self.empresas['administracion'].isna()
            
            self._empresas_bop = self.empresas.loc[flt_bop,'Empresa'].to_list()
            self._empresas_gen = self.empresas.loc[flt_gen | flt_opL | flt_mantL,'Empresa'].to_list()
            self._empresas_grid = self.empresas.loc[flt_traspo | flt_distro | flt_adm,'Empresa'].to_list()
            
            self._empresas_gen = {x:'GENERATOR' for x in self._empresas_gen}
            self._empresas_bop = {x:'BOP_CONTRACTOR' for x in self._empresas_bop}
            self._empresas_grid = {x:'GRID_OPERATOR' for x in self._empresas_grid}

        elif tabla == 'centralesempresas':
            self.centralesempresas = self.dfs['centralesempresas']
            mapeo = self._crear_dict(self.empresas,'id','Empresa')
        
            for col in self.centralesempresas.columns[1:]:
                self.centralesempresas[col] = self.centralesempresas[col].map(mapeo)
            
        elif tabla == 'razones':
            self.razones = self.dfs['razones']
            
        elif tabla == 'estado':
            self.estado = self.dfs['estado']
            
        elif tabla == 'tipoequipo':
            self.tipoequipo = self.dfs['tipoequipo']\
                                .rename(columns={'nombre':'equipo','potencia':'PotEquipo'})
                                
            flt_tiene_fabricante =  ~self.tipoequipo.fabricante.isna()
            pot_inst_ct = self.tipoequipo[flt_tiene_fabricante].groupby('id_central',as_index=False)['PotEquipo'].sum()
            pot_inst_ct['idtipoEquipo'] = 0
            pot_inst_ct['idTipoGenerador'] = 0
            pot_inst_ct['equipo'] = 'PLANT'
            self.tipoequipo = pd.concat([self.tipoequipo,pot_inst_ct],ignore_index=True)
            
            
            mapeo_ucs = self._crear_dict(self.central,'idcentral','unidadComercial')
            mapeo_nemos = self._crear_dict(self.central,'idcentral','nemoCammesa')
            self.tipoequipo['UC'] = self.tipoequipo['id_central'].map(mapeo_ucs)
            self.tipoequipo['Nemo'] = self.tipoequipo['id_central'].map(mapeo_nemos)
            self.tipoequipo['equipo'] = self.tipoequipo['equipo'].str.upper()
            
        elif tabla == 'tipogenerador':
            self.tipogenerador = self.dfs['tipogenerador']
            
            data = {
                'id':[0],
                'nombre':['Planta Completa'],
                'agrupamiento':[np.nan]
                }
            df_tmp = pd.DataFrame(data)

            self.tipogenerador = pd.concat([self.tipogenerador,df_tmp],ignore_index=True)
            
        elif tabla == 'conjuntogeneradores':
                        
            self.conjuntogeneradores = pd.merge(left=self.dfs['conjuntogeneradores'],right=self.tipoequipo,left_on='idGenerador',right_on='idtipoEquipo',suffixes=('_or',''))\
                .drop(columns=['idGenerador','idtipoEquipo','cantidad'])\
                .rename(columns={
                    'idTipoGenerador_or':'Agrupamiento',
                    'idTipoGenerador':'GenType'
                }
            )
                                
            mapeo_ucs = self._crear_dict(self.central,'idcentral','unidadComercial')
            mapeo_nemos = self._crear_dict(self.central,'idcentral','nemoCammesa')
            mapeo_equipos = self._crear_dict(self.tipoequipo,'idtipoEquipo','equipo')
            mapeo_tipogenerador = self._crear_dict(self.tipogenerador,'id','nombre')
            
            self.conjuntogeneradores['UC'] = self.conjuntogeneradores['id_central'].map(mapeo_ucs)
            self.conjuntogeneradores['Nemo'] = self.conjuntogeneradores['id_central'].map(mapeo_nemos)
            self.conjuntogeneradores['GenType'] = self.conjuntogeneradores['GenType'].map(mapeo_tipogenerador)
            self.conjuntogeneradores['Agrupamiento'] = self.conjuntogeneradores['Agrupamiento'].map(mapeo_equipos)
            
            self.conjuntogeneradores.drop(columns=['id_central'],inplace=True)
            
            self.conjuntogeneradores['Agrupamiento'] = self.conjuntogeneradores['Agrupamiento'].str.upper()
            self.conjuntogeneradores['equipo'] = self.conjuntogeneradores['equipo'].str.upper()
            
        elif tabla == 'incidencias':
            self.incidencias_todas = self.dfs['incidencias']
            self.__procesar_incidencias()
            
        else:
            pass
        
    def _crear_dict(self,df,llave,valor):
        
        llaves = df[llave].to_list()
        valores = df[valor].to_list()
        
        return dict(zip(llaves,valores))
    
    def __procesar_norma_iec_61400(self):
    
        try:
            self._iec61400 = pd.read_excel(dirs.get_dc_cfg() + '\\IEC61400.xlsx')
        except:
            self._iec61400 =  pd.read_excel(__file__ + '\\IEC61400.xlsx')
        
        #self._iec61400.set_index(['Origin','Reason','SolverAgent'])
        
        cols = [f'Priority_{x}' for x in self._iec61400_metodos]
        maximo = self._iec61400.loc[:,cols].values.max()
        numeros = [x for x in range(maximo,0,-1)]
        cat = pd.CategoricalDtype(numeros,ordered=True)
        self._iec61400.loc[:,cols] = self._iec61400.loc[:,cols].astype(cat)
        
    def consultar_ucs(self,solo_CROM=True):
        if solo_CROM:
            flt = self.central['opcCROM'].isna()
            self.ucs = self.central.loc[~flt,'unidadComercial'].to_list()
        else:
            self.ucs = self.central.loc[:,'unidadComercial'].to_list()

    def consultar_idsApiCammesa(self):
        flt = self.central['idApiCammesa'] >0
        self.idsApiCammesa =  self.central\
                                    .loc[flt,['unidadComercial','idApiCammesa']]\
                                    .set_index('unidadComercial')\
                                    .to_dict('dict')['idApiCammesa']  

    def consultar_nemoCammesa(self):
        flt = self.central['nemoCammesa'].str.len() > 0
        self.nemos = self.central\
                            .loc[flt,'nemoCammesa']\
                            .to_list()

    def consultar_datos_basicos(self):  
        tablas = [
            'central',
            'origen',
            'empresas',
            'centralesempresas',
            'razones',
            'estado',
            'tipoequipo',
            'tipogenerador',
            'conjuntogeneradores'
        ]
        
        print('Consultando datos básicos de las centrales')
        self.__consultar(tablas)
        # Acá habría que chequear si es un objeto conexión
        # O si es = None o = False
        # PAra que no arroje error al intentar acceder al método .open 
        if self.conexion.open:
            self.consultar_nemoCammesa()
            self.consultar_idsApiCammesa()
            self.consultar_ucs()
        
        self.conexion.close()

    def consultar_incidencias(self):
        print('Consultando incidencias históricas')
        self.__consultar(['incidencias',])
        try:
            self.conexion.close()
        except:
            print('Error al cerrar la conexión.')
    
    def __check_nemo(self,nemo_parque):
        
        if not isinstance(nemo_parque,str):
            raise TypeError('El Nemotécnico debe ser del tipo String')
        elif not nemo_parque:
            raise ValueError('El nemo del parque no puede estar vacío')
        elif not nemo_parque.upper() in self.nemos:
            raise ValueError(f'El nemotécnico {nemo_parque} no se encuentre entre:\n{self.nemos}')
        else:
            return nemo_parque.upper()

    def __check_uc(self,uc):
        
        if not isinstance(uc,str):
            raise TypeError('El Nemotécnico debe ser del tipo String')
        elif not uc:
            raise ValueError('El nemo del parque no puede estar vacío')
        elif not uc.upper() in self.ucs:
            raise ValueError(f'El nemotécnico {uc} no se encuentre entre:\n{self.ucs}')
        else:
            return uc.upper()


    def __check_params_nemo_uc(self,nemo_parque='',uc=''):
        if nemo_parque != '' and uc != '':
            raise ValueError('No se puede seleccionar un Nemotécnico y una Unidad Comercial a la vez')
        
        elif nemo_parque == '' and uc == '':
            raise ValueError('Debe ingresar un valor para nemo_parque parque o para uc')
        elif nemo_parque !='' and uc== '':
            nemo_parque = self.__check_nemo(nemo_parque)
            return ('Nemo',nemo_parque)
        else:
            uc = self.__check_uc(uc)
            return ('UC',nemo_parque)

    def __obtener_equipos_parque(self,filtro,valor):
        #El valor del filtro (sea un nemo o una UC), 
        # debe ser previamente chequeado por las funciones __check_uc o __check_nemo respectivamente
        
        if not isinstance(filtro,str):
            raise TypeError('El parámetro filtro debe ser del tipo string')
        elif not filtro.lower() in ['nemo','uc']:
            raise ValueError('El parámetro filtro debe ser "nemo" o "uc"')
        else:
            if filtro.lower() == 'nemo':
                filtro = 'Nemo'
            else:
                filtro = 'UC'
                
            agrupamientos = self.conjuntogeneradores\
                                .query(f'{filtro} == "{valor}"')\
                                .loc[:,'Agrupamiento']\
                                .sort_values()\
                                .unique()
                                
            generadores = self.conjuntogeneradores\
                                .query(f'{filtro} == "{valor}"')\
                                .loc[:,'equipo']\
                                .sort_values()\
                                .unique()
            
            return ['PLANT',] + list(agrupamientos) + list(generadores)

    def __obtener_equipos_parque_no_agr(self,filtro,valor):
        #El valor del filtro (sea un nemo o una UC), 
        # debe ser previamente chequeado por las funciones __check_uc o __check_nemo respectivamente
        
        if not isinstance(filtro,str):
            raise TypeError('El parámetro filtro debe ser del tipo string')
        elif not filtro.lower() in ['nemo','uc']:
            raise ValueError('El parámetro filtro debe ser "nemo" o "uc"')
        else:
            if filtro.lower() == 'nemo':
                filtro = 'Nemo'
            else:
                filtro = 'UC'
            
            generadores = self.conjuntogeneradores\
                                .query(f'{filtro} == "{valor}"')\
                                .loc[:,'equipo']\
                                .sort_values()\
                                .unique()
            
            return list(generadores)
            
    def __obtener_equipos_agrupamiento(self,filtro,valor):
        #El valor del filtro (sea un nemo o una UC), 
        # debe ser previamente chequeado por las funciones __check_uc o __check_nemo respectivamente
        
        if not isinstance(filtro,str):
            raise TypeError('El parámetro filtro debe ser del tipo string')
        elif not filtro.lower() in ['nemo','uc']:
            raise ValueError('El parámetro filtro debe ser "nemo" o "uc"')
        else:
            if filtro.lower() == 'nemo':
                filtro = 'Nemo'
            else:
                filtro = 'UC'
                
            df = self.conjuntogeneradores.query(f'{filtro} == "{valor}"') 
            agrupamientos =  df['Agrupamiento'].unique()
            lista_equipos = lambda x : df.query(f'Agrupamiento == "{x}"')['equipo'].to_list()
            
            return {agrupamiento:lista_equipos(agrupamiento) for agrupamiento in agrupamientos}


    def __obtener_agrupamientos_parque(self,filtro,valor):
        
        if not isinstance(filtro,str):
            raise TypeError('El parámetro filtro debe ser del tipo string')
        elif not filtro.lower() in ['nemo','uc']:
            raise ValueError('El parámetro filtro debe ser "nemo" o "uc"')
        else:
            if filtro.lower() == 'nemo':
                filtro = 'Nemo'
            else:
                filtro = 'UC'
                
            df = self.conjuntogeneradores.query(f'{filtro} == "{valor}"') 
            agrupamientos =  list(df['Agrupamiento'].unique())
            
            return agrupamientos
        
    def consultar_equipos_parque(self,nemo_parque='',uc='',potencia=False):
        # NO FUNCIONÓ CON PEGARCIG
        filtro,valor = self.__check_params_nemo_uc(nemo_parque,uc)

        if potencia:
            df = self.tipoequipo.query(f'{filtro} == "{valor}"')
            return self._crear_dict(df,'equipo','PotEquipo')
        else:
            return self.__obtener_equipos_parque(filtro=filtro,valor=valor)
        
    def consultar_equipos_por_agrupamiento(self,nemo_parque='',uc=''):
        # NO FUNCIONÓ CON PEGARCIG
        filtro,valor = self.__check_params_nemo_uc(nemo_parque,uc)
        return self.__obtener_equipos_agrupamiento(filtro=filtro,valor=valor)
        
    def consultar_agrupamientos_parque(self,nemo_parque='',uc=''):
        filtro,valor = self.__check_params_nemo_uc(nemo_parque,uc)
        return self.__obtener_agrupamientos_parque(filtro=filtro,valor=valor)

    def consultar_equipos_parque_no_agrupamientos(self,nemo_parque='',uc=''):
        filtro,valor = self.__check_params_nemo_uc(nemo_parque,uc)
        return self.__obtener_equipos_parque_no_agr(filtro=filtro,valor=valor)


    def __procesar_incidencias(self):
        
        df_tipoequipo = self.tipoequipo\
                            .loc[:,['idtipoEquipo','id_central','equipo','idTipoGenerador','PotEquipo']]
                            
        df_incidencias = pd\
                            .merge(
                                left=self.incidencias_todas,
                                right=df_tipoequipo,
                                left_on=['id_tipoEquipo','id_central'],
                                right_on=['idtipoEquipo','id_central'],
                                how='left')\
                            .drop(columns=['id_tipoEquipo','idtipoEquipo'])
                            
        mapeo_owner = self._crear_dict(self.centralesempresas,'idCentral','generador')
        mapeo_origen = self._crear_dict(self.origen,'idorigen','origen')
        mapeo_origen2 = {'Interno':'INT','Externo':'EXT','--':'NA'}
        mapeo_empresas = self._crear_dict(self.empresas,'id','Empresa')
        mapeo_razones = self._crear_dict(self.razones,'idrazones','razones')
        mapeo_ucs = self._crear_dict(self.central,'idcentral','unidadComercial')
        mapeo_nemos = self._crear_dict(self.central,'idcentral','nemoCammesa')
        mapeo_estado = self._crear_dict(self.estado,'idestado','estado')
        mapeo_tipogenerador = self._crear_dict(self.tipogenerador,'id','nombre')
        mapeo_solveragent = self._empresas_bop | self._empresas_gen | self._empresas_grid
        
        mapeo_razones2= {
            'MAPRO':'MAPRO',
            'MAPRO (no computa)':'MAPRO S_A',
            'Mantenimiento no programado':'MANOPRO',
            'Falla':'FAILURE',
            'Limitación':'LIMITATION',
            'Reactivo Nocturno':'QNIGHT',
            'Suspensdido':'SUSPENDED',
            'Fuerza mayor':'FORCE MAJEURE'
            }
        
        df_incidencias['UC'] = df_incidencias['id_central'].map(mapeo_ucs)
        df_incidencias['Nemo'] = df_incidencias['id_central'].map(mapeo_nemos)
        df_incidencias['idTipoGenerador'] = df_incidencias['idTipoGenerador'].map(mapeo_tipogenerador)
        df_incidencias['id_trabajo'] = df_incidencias['id_trabajo'].map(mapeo_empresas)
        df_incidencias['id_central'] = df_incidencias['id_central'].map(mapeo_owner)
        df_incidencias['id_razones'] = df_incidencias['id_razones'].map(mapeo_razones).map(mapeo_razones2)
        df_incidencias['id_origen'] = df_incidencias['id_origen'].map(mapeo_origen).map(mapeo_origen2)
        df_incidencias['id_estado'] = df_incidencias['id_estado'].map(mapeo_estado)
        df_incidencias['SolverAgent'] = np.nan
        df_incidencias['numero_pt11'] = df_incidencias['numero_pt11'].replace(to_replace=-1,value=0)
    
        #Renombrar columnas
        cols_renombrar = {
            'idincidencia':'ID',
            'idPrimario':'ID_prim',
            'idLimitacion':'ID_lim',
            
            'id_estado':'Status',
            'UC':'UC',
            'Nemo':'Nemo',
            'id_central':'Owner',
            'cantEquipos':'QtyTot',
            
            'evStFecha':'Start',
            'evStUser':'StartUsr',
            'evStPotCor':'PowerCut',

            'cuNoFecha':'NoticeDate',
            
            'evEndFecha':'End',
            'evEndUser':'EndUsr',
            'evEndPot':'PowerRet',
            
            'id_pt11':'PT11',
            'numero_pt11':'ID_PT11',
            
            'equipo':'Equipo',
            'PotEquipo':'PotEquipo',
            'idTipoGenerador':'GenType',
            'afCantEquipos':'Qty',
            'afQuantity':'QtyProp',
            
            'afTime':'Hours',
            'energyLoss':'ENS',
            'id_trabajo':'SolvedBy',
            'SolverAgent':'SolverAgent',
            'id_razones':'Reason',
            'id_origen':'Origin',
            'codFalla':'Code',

            'pot_posible':'Pteo',
            'setpoint_pot':'SP_P',

            'descripcion':'BLC_Description',
            'comentario':'BLC_Comments',
            
            'descripcionFalla':'Owner_Description',
            'equipoAfectado':'Owner_AffectedEquipment',
            'accionesTomadas':'Owner_ActionsTaken',
            'resultados':'Owner_Results',
            'proximosPasos':'Owner_NextSteps',
            'comentariosCliente':'Owner_Comments',
        }

        cols_produccion = list(cols_renombrar.values())
        cols_auditoria = [ 
            'sinCuNo',
            'abiertoFecha',
            'cerrIncFecha',
            'cerrComFecha',
            'visadoFecha',
            'descartadoFecha',
            'justificacionDescarte',

            'lastModifUser',
            'lastModifFecha',
            'lastModifUserWeb',
            'lastModifFechaWeb',
            'comentarioEdicion',

            'resaltar',
        ]

        df_incidencias.rename(columns=cols_renombrar,inplace=True)
        
        #Rellenar huecos, que se dan naturalmente
        descartadas = ~df_incidencias['descartadoFecha'].isna()
        falta_SolvedBy = df_incidencias['SolvedBy'].isna()
        falta_EndUsr = df_incidencias['EndUsr'].isna()
        
        #Para aquellas incidencias descartadas, se coloca como usuario que cerró, el usuario que descartó.
        df_incidencias.loc[descartadas & falta_EndUsr,'EndUsr'] = df_incidencias.loc[descartadas & falta_EndUsr,'lastModifUser']
        
        #Las no descartadas deberían ser incidencias abiertas, por cómo funciona el sistema
        df_incidencias.loc[~descartadas & falta_EndUsr,'EndUsr'] = 'corte_automático'
        df_incidencias.loc[~descartadas & falta_EndUsr,'End'] = dt.datetime.now().replace(second=0,microsecond=0)
        
        #Hay un único caso en el que falta el campo SolvedBy, de una incidencia muy vieja.
        #Se deja esto aquí para no hardcodear soluciones.
        df_incidencias.loc[falta_SolvedBy,'SolvedBy'] = df_incidencias.loc[falta_SolvedBy,'Owner']

        #Recalcular el SolverAgent, ya que se llenaron los huecos
        df_incidencias['SolverAgent'] = df_incidencias['SolvedBy'].map(mapeo_solveragent)
        falta_SolverAgent = df_incidencias['SolverAgent'].isna()
        
        df_incidencias.loc[falta_SolverAgent,'SolverAgent'] = 'INVALIDO'
        
        for col in ['Equipo','GenType','Reason']:
            df_incidencias[col] = df_incidencias[col].fillna('DESCONOCIDO')
        
        #Cambiar tipos de datos para ahorrar memoria
        cols_ui16 = ['PT11','ID_PT11','QtyTot','Qty']
        cols_ui32 = ['ID','ID_prim','ID_lim',]
        cols_cat = [
            'Status',
            'UC',
            'Nemo',
            'Owner',
            'StartUsr',
            'EndUsr',
            'Equipo',
            'GenType',
            'SolvedBy',
            'SolverAgent',
            'Reason',
            'Origin',
            'Code'
            ]

        for col in cols_ui16:
            print(f'Convirtiendo {col} a UI16')
            df_incidencias[col] = df_incidencias[col].astype('UInt16')
            
        for col in cols_ui32:
            print(f'Convirtiendo {col} a UI32')
            df_incidencias[col] = df_incidencias[col].astype('UInt32')

        for col in cols_cat:
            try:
                df_incidencias.loc[:,col] = df_incidencias.loc[:,col].str.upper()
                valores = df_incidencias[col].unique()
                categoria = pd.CategoricalDtype(valores,ordered=False)
                df_incidencias.loc[:,col] = df_incidencias[col].astype(categoria)
            except:
                print(f'Procesando Incidencias CROM: Imposible convertir {col} a categoría...')

        
        flt_no_descartada = df_incidencias['Status'] != 'Descartada'
        
        self.incidencias_todas_auditoria = df_incidencias.loc[:,cols_produccion+cols_auditoria]
        self.incidencias_todas = df_incidencias.loc[flt_no_descartada,cols_produccion]
        

        self.incidencias_todas = self.incidencias_todas.merge(right=self._iec61400,on=['Origin','Reason','SolverAgent'],how='left')