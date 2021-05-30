from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# se importa la clase(s) del 
# archivo genera_tablas
from genera_tabla import Establecimiento, Parroquia, Canton

from sqlalchemy import or_

# se importa información del archivo configuracion
from configuracion import cadena_base_datos
# se genera enlace al gestor de base de
# datos
# para el ejemplo se usa la base de datos
# sqlite
engine = create_engine(cadena_base_datos)

# Este objeto de sesión es nuestro manejador de base de datos
Session = sessionmaker(bind=engine)
# Se crea un objeto session de tipo Session, mismo que va apermitir 
# guardar, eliminar, actualizar, generar consultas en la base de datosrespecto a las entidades creadas.
session = Session()

# Para proceder a realizar la siguiente consulta se hace un select de la tabla a analizar con session.query(),
# un join de las tablas a las cuales se deseea acceder y un filtrado que el Establecimiento en la jornada sea "Nocturna"
estab_nocturna = session.query(Parroquia).join(Establecimiento).filter(Establecimiento.jornada == "Nocturna").all()
 
print("Las parroquias que tienen establecimientos únicamente en la jornada Nocturna")
for i in estab_nocturna:
    print("%s" % (i))
print("--------------------------------------")

# Para proceder a realizar la siguiente consulta se hace un select de la tabla a analizar con session.query(),
# un join de las tablas a las cuales se deseea acceder y un filtrado con un or_ de que el numero de estudiantes pueder : 
# 448, 450, 451, 454, 458, 459
establecimiento_canton = session.query(Canton).join(Parroquia, Establecimiento).filter(or_(Establecimiento.numero_estudiantes == 448, \
    Establecimiento.numero_estudiantes == 450, Establecimiento.numero_estudiantes == 451, Establecimiento.numero_estudiantes == 454, \
        Establecimiento.numero_estudiantes == 458, Establecimiento.numero_estudiantes == 459)).all()
 
print("Los cantones que tiene establecimientos como número de estudiantes tales como: 448, 450, 451, 454, 458, 459")
for i in establecimiento_canton:
    print("%s" % (i))
print("--------------------------------------")
