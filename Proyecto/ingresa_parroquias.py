from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.base import state_str

# se importa la clase(s) del 
# archivo genera_tablas
from genera_tabla import Canton, Parroquia

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
    # Se realiza una consulta de la tabla Cantón para guardar los datos en una variable
    data_canton = session.query(Canton).all()
    # Auxiliar para guardar los nombres para despues con un if comparar si se esta repitiendo los nombres
    aux = [] 
    # for para recorrer el csv y con el método interitertools.islice se le esta diciendo que cuando vaya a leer el archivo 
    # la posiscion 1 no la tome en cuenta
    for row in itertools.islice(reader, 1, None):
        # if en donde se compara el nombre ya ingresado guardado en la variable aux con el nuevo nombre a ingresar 
        # en donde 'not in' identifican con un 'True' o 'False' si se estan repitiendo los nombres
        if row[7] not in aux:
            # Con el .append se procede a guardar si el nombre evaluado es único
            aux.append(row[7])
            # Búsqueda del dato a guardar utilizando una consulta
            data_canton = session.query(Canton).filter_by(nombre_canton = row[5]).one() 
            # Asigación de los datos en los atributos y posiciones correctas
            e = Parroquia(nombre_parroquia=row[7], codigo_division_parroquia=row[6], canton=data_canton)
            # Se guarda dicho objeto como registro en la base de datos.
            session.add(e)

# Se confirma las transacciones  
session.commit()