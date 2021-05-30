from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.base import state_str

# se importa la clase(s) del 
# archivo genera_tablas
from genera_tabla import Provincia

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

# Leyendo un Archivo CSV Con csv.reader
with open('../data/Listado-Instituciones-Educativas.csv', 'r', encoding="utf8") as File:
    reader = csv.reader(File, delimiter='|', quotechar=',',
                        quoting=csv.QUOTE_MINIMAL)
    # Auxiliar para guardar los nombres para despues con un if comparar si se esta repitiendo los nombres
    aux=[]
    # for para recorrer el csv y con el método interitertools.islice se le esta diciendo que cuando vaya a leer el archivo 
    # la posiscion 1 no la tome en cuenta
    for row in itertools.islice(reader, 1, None):
        # if en donde se compara el nombre ya ingresado guardado en la variable aux con el nuevo nombre a ingresar 
        # en donde 'not in' identifican con un 'True' o 'False' si se estan repitiendo los nombres  
        if row[3] not in aux:
            # Con el .append se procede a guardar si el nombre evaluado es único
            aux.append(row[3])
            # Asigación de los datos en los atributos y posiciones correctas
            e = Provincia(nombre_provincia=row[3], codigo_division_provincia=row[2])
            # Se guarda dicho objeto como registro en la base de datos.
            session.add(e)

# Se confirma las transacciones
session.commit()