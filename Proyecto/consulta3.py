from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# se importa la clase(s) del 
# archivo genera_tablas
from genera_tabla import Establecimiento, Parroquia, Canton


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
# un join de las tablas a las cuales se deseea acceder y un filtrado que el Establecimiento el numero de docentes sea = 0
canton_docentes = session.query(Canton).join(Parroquia, Establecimiento).filter(Establecimiento.numero_docentes == 0).all()
 
print("Los cantones que tiene establecimientos con 0 número de profesores")
for i in canton_docentes:
    print("%s" % (i))
print("--------------------------------------")

# Para proceder a realizar la siguiente consulta se hace un select de la tabla a analizar con session.query(),
# un join de las tablas a las cuales se deseea acceder y un filtrado en donde el nombre de la parroquia sea 'CATACOCHA', 
# y el Establecimiento en su numero de estuiantes sea >= 21
n_estudiantes = session.query(Establecimiento).join(Parroquia).filter(Parroquia.nombre_parroquia == "CATACOCHA", Establecimiento.numero_estudiantes >= 21 ).all()
 
print("Los establecimientos que pertenecen a la parroquia Catacocha con estudiantes mayores o iguales a 21")
for i in n_estudiantes:
    print("%s" % (i))
print("--------------------------------------")