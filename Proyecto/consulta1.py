from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# se importa la clase(s) del 
# archivo genera_tablas
from genera_tabla import Establecimiento, Parroquia, Canton, Provincia


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
# un join de las tablas a las cuales se deseea acceder y un filtrado por el nombre de la provincia que sea = "Loja"
establecimiento_prov = session.query(Establecimiento).join(Parroquia, Canton, Provincia).filter(Provincia.nombre_provincia == "LOJA").all()
 
print("Todos los establecimientos de la provincia de Loja")
for i in establecimiento_prov:
    print("%s" % (i))
print("--------------------------------------")

# Para proceder a realizar la siguiente consulta se hace un select de la tabla a analizar con session.query(),
# un join de las tablas a las cuales se deseea acceder y un filtrado por el nombre del cantón que sea = "Loja"
establecimiento_canton = session.query(Establecimiento).join(Parroquia, Canton).filter(Canton.nombre_canton == "LOJA").all()
 
print("Todos los establecimientos del cantón de Loja")
for i in establecimiento_canton:
    print("%s" % (i))
print("--------------------------------------")


