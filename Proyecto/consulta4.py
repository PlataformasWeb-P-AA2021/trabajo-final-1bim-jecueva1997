from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# se importa la clase(s) del 
# archivo genera_tablas
from genera_tabla import Establecimiento

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
# un join de las tablas a las cuales se deseea acceder y un filtrado en donde el Establecimiento en su numero de docentes sea mayor a 100
# y esta se ordene por el Establecimiento por su número de estudiantes
n_docentes = session.query(Establecimiento).filter(Establecimiento.numero_docentes > 100).order_by(Establecimiento.numero_estudiantes).all()
 
print("Los establecimientos ordenados por número de estudiantes; que tengan más de 100 profesores")
for i in n_docentes:
    print("%s" % (i))
print("--------------------------------------")

# Para proceder a realizar la siguiente consulta se hace un select de la tabla a analizar con session.query(),
# un join de las tablas a las cuales se deseea acceder y un filtrado en donde el Establecimiento en su numero de docentes sea mayor a 100
# y esta se ordene por el Establecimiento por su número de docentes
estab_docentes = session.query(Establecimiento).filter(Establecimiento.numero_docentes > 100).order_by(Establecimiento.numero_docentes).all()
 
print("Los establecimientos ordenados por número de profesores; que tengan más de 100 profesores.")
for i in estab_docentes:
    print("%s" % (i))
print("--------------------------------------")
