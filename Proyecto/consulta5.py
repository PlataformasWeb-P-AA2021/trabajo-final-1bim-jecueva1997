from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.base import state_str

# se importa la clase(s) del 
# archivo genera_tablas
from genera_tabla import Establecimiento, Parroquia

from sqlalchemy import and_
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
# un join de las tablas a las cuales se deseea acceder y un filtrado en donde el Establecimiento en su numero de 
# docentes sea mayor a 20 y ademas que el Establecimeinto en su atributo tipo educación contenga la cadena "Permanente", ademas ordenar 
# por los nombre de las Parroquias
n_docentes = session.query(Establecimiento).join(Parroquia).filter(and_(Establecimiento.numero_docentes > 20, 
     Establecimiento.tipo_educacion.like("%Permanente%"))).order_by(Parroquia.nombre_parroquia).all()
 
print("Los establecimientos ordenados por nombre de parroquia que tengan más de 20 profesores y la cadena 'Permanente' en tipo de educación")
for i in n_docentes:
    print("%s" % (i))
print("--------------------------------------")

# Para proceder a realizar la siguiente consulta se hace un select de la tabla a analizar con session.query(),
# un join de las tablas a las cuales se deseea acceder y un filtrado en el Establecimiento que en su 
# codigo de distrito contenga la cadena "11D02" 
canton_docentes = session.query(Establecimiento).filter(Establecimiento.codigo_distrito == "11D02").order_by(Establecimiento.sostenimiento).all()
 
print("Todos los establecimientos ordenados por sostenimiento y tengan código de distrito '11D02'")
for i in canton_docentes:
    print("%s" % (i))
print("--------------------------------------")
