from pathlib import Path


__all__ = ['__CarpetaServicios']


mensaje = """No se ha encontrado la carpeta hacia la nube de BLC.\n
Tendrá que indicar la ruta hacia la carpeta de Servicios manualmente.
Para ello por favor ejecutar el comando: blctools.indicar_ruta('ruta completa')
Mientras tanto se trabajará en la ruta del script actual"""


class __CarpetaServicios():
       
    def __init__(self):
        self._ruta = str(Path.cwd())
        self.ruta_encontrada = False
        
        try:
            self.__buscar_dir_segun_carpeta_usuario()
        except:
            try: 
                self.__buscar_dir_segun_archivo_py()
            except:
                self.print_warning
        
    def __buscar_dir_segun_archivo_py(self):
        if r'Documentos Produccion\Servicios' in self.ruta:
            dir_raiz_split = self.ruta.split('\\')
            index_dir_servicios = dir_raiz_split.index('Servicios')
            dir_servicios = '\\'.join(dir_raiz_split[0:index_dir_servicios+1])
            
            self.ruta = dir_servicios
            self.ruta_encontrada = True
        
    def __buscar_dir_segun_carpeta_usuario(self):
        dir_usr = str(Path.home())
        dir_rel = r'OneDrive - BLCGES\Documentos Produccion\Servicios'
        dir_full = dir_usr + '\\' + dir_rel
        path_full = Path(dir_full)
        
        if path_full.is_dir() and path_full.exists():
            self.ruta = dir_full
            self.ruta_encontrada = True

    def print_warning(self):
        if __name__ != '__main__':
            print(mensaje)
            
    @property
    def ruta(self):
        return self._ruta
    
    @ruta.setter
    def ruta(self,val):
        
        if isinstance(val,Path):
            val = str(Path(val))
            
        elif not isinstance(val,str):
            raise TypeError('La ruta ingresada debe ser del tipo String o pathlib.Path')
        
        else:
            obj_path = Path(val)
            
            if not obj_path.is_dir():
                raise ValueError('La ruta especificada aparenta no ser un directorio')
            elif not obj_path.exists():
                raise ValueError('La ruta especificada no existe')
            elif not obj_path.is_absolute():
                raise ValueError('La ruta especificada es relativa, se requiere una ruta completa')
        
            self._ruta = val
