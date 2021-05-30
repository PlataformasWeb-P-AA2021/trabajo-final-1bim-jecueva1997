from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.base import state_str

# se importa la clase(s) del 
# archivo genera_tablas
from genera_tabla import Establecimiento, Parroquia

# importación de librerías a utilizar como el csv para poder abrir el archivo a ingresar
import csv
# Es un módulo de la librería estándar de Python que incorpora funciones que devuelven objetos iterables
import itertools

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

# Se lee archivo CSV con csv.reader para luego convertirla en una lista para poder manejar el archivo por posiciones
with open('../data/Listado-Instituciones-Educativas.csv', 'r', encoding="utf8") as File:
    reader = list(csv.reader(File, delimiter='|', quotechar=',',
                        quoting=csv.QUOTE_MINIMAL))
    # Se realiza una consulta de la tabla Parroquia para guardar los datos en una variable
    data_parroquia = session.query(Parroquia).all() 
    # for para recorrer el csv y con el método interitertools.islice se le esta diciendo que cuando vaya a leer el archivo 
    # la posiscion 1 no la tome en cuenta 
    for row in itertools.islice(reader, 1, None):
        # for para recorrer los datos de la tabla Parroquia para poder sacar el id de la tabla parroquia y 
        # poder ponerlo en la tabla Establecimeinto en el atributo de la clave foránea establecida 
        for parroquia in data_parroquia:
            # if para comparar si existen datos en la posición del nombre del Cantón para proceder a sacar el 
            # id de esa tabla y asignarlo a una variable
            if row[7] == parroquia.nombre_parroquia:
                id_parroquia = parroquia.id
        # Asigación de los datos en los atributos y posiciones correctas
        e = Establecimiento(codigo_AMIE=row[0],nombre_establecimiento=row[1], codigo_distrito=row[8], \
            sostenimiento=row[9], tipo_educacion=row[10],  modalidad=row[11], jornada=row[12], acceso=row[13], \
                numero_estudiantes=row[14], numero_docentes=row[15], parroquia_id=id_parroquia)
        # Se guarda dicho objeto como registro en la base de datos.
        session.add(e)
    
# Se confirma las transacciones
session.commit()



