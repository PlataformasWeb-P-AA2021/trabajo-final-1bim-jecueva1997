# Trabajo Final Primer Bimestre

## Uso de SqlAlchemy

Consideraciones a tomar para una correcta ejecución

* Se debe ingresar a la carpeta Proyecto en donde se encuentran todos los archivos a ejecutar

* Orden en el que se debe jecutar los archivos se pueda generar y cargar los datos en SqlAlchemy.
	* genera_tabla.py
	* ingresa_provincias.py
	* ingresa_cantones.py
	* ingresa_parroquias.py
    * ingresa_establecimientos.py
    * Nota: Se debe ejecutar los archivosen la forma propuesta ya que como estan relacionados y si se llega al alterar el orden
            no se cargaran los datos del CSV.

* Orden y acalaración de las consultas:
	* consulta1.py
	* consulta2.py
	* consulta3.py
	* consulta4.py
	* consulta5.py
    * Nota: Se debe tomar en cuenta de las relaciones establecidas entre tablas en donde el orden sería el siguiente:
            Establecimiento -> Parroquia -> Canton -> Provincia

## Inicio del proyecto

Para poder usar el presente proyecto, tomar en consideración lo siguiente:

### Prerrequisitos

* Instalar [Python](https://www.python.org/) 
* Instalar [SQLAlchemy](https://www.sqlalchemy.org/) 
``` python
  	pip install SQLAlchemy
```

La carpeta Proyecto tiene los siguiente archivos:

```
* configuracion.py
```python
# este módulo será usado para posibles configuraciones
#
# cadena conector a la base de datos
#

cadena_base_datos = 'sqlite:///demobase.db' 

```
* genera_tabla.py
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.sql.expression import false
from sqlalchemy.sql.schema import CheckConstraint
from sqlalchemy.sql.sqltypes import INTEGER

# se importa información del archivo configuracion
from configuracion import cadena_base_datos

# se genera en enlace al gestor de base de
# datos
# para el ejemplo se usa la base de datos
# sqlite
engine = create_engine(cadena_base_datos)

# se crea una clase llamada Base para definir las clases en lenguaje Python.
Base = declarative_base()
# Creación de la tabla Provincia con su relación de la tabla Canton y también 
# estableciendo que el nombre sea un campo único
class Provincia(Base):
    __tablename__ = 'provincia'
    id = Column(Integer, primary_key=True)
    nombre_provincia = Column(String(50), unique=True, nullable=False)
    codigo_division_provincia = Column(String(50), nullable=False)
    cantones = relationship("Canton", back_populates="provincia")

    def __repr__(self):
        return "Provincia: nombre_provincia=%s - codigo_division_provincia=%s"% (
                          self.nombre_provincia, 
                          self.codigo_division_provincia) 

    
# Creación de la tabla Cantón con su relación de la tabla Provincia y Parroquia, 
# se establece la clave foránea de de la tabla Provincia y que el nombre del Cantón sea único
class Canton(Base):
    __tablename__ = 'canton'
    id = Column(Integer, primary_key=True)
    nombre_canton = Column(String(50), unique=True, nullable=False)
    codigo_division_canton = Column(String(50), nullable=False)
    provincia_id = Column(Integer, ForeignKey('provincia.id'))
    provincia = relationship("Provincia", back_populates="cantones")
    parroquias = relationship("Parroquia",back_populates="canton")
    def __repr__(self):
        return "Canton: provincia_id=%s\n nombre_canton=%s codigo_division_canton=%s"% (
                          self.provincia_id ,
                          self.nombre_canton,
                          self.codigo_division_canton) 

# Creación de la tabla Provincia con su relación de la tabla Parroquia y Establecimiento, 
# se establece la clave foránea de la tabla Cantón  y también que el nombre de la Parroquia sea único
class Parroquia (Base):
    __tablename__ = 'parroquia'
    canton_id = Column(INTEGER, ForeignKey('canton.id'))
    id = Column(Integer, primary_key=True)
    nombre_parroquia = Column(String(50), unique=True, nullable=False)
    codigo_division_parroquia = Column(String(50), nullable=False)
    canton = relationship("Canton", back_populates="parroquias")
    establecimientos = relationship("Establecimiento", back_populates="parroquia")

    def __repr__(self):
        return "Parroquia: canton_id=%s\n nombre_parroquia=%s  codigo_division_parroquia=%s"% (
                          self.canton_id ,
                          self.nombre_parroquia, 
                          self.codigo_division_parroquia) 

# Creación de la tabla Establecimiento con su relación de la tabla Parroquia así 
# también estableciendo la clave foránea de la tabla Parroquia
class Establecimiento(Base):
    __tablename__ = 'establecimiento'
    parroquia_id = Column(Integer, ForeignKey('parroquia.id'))
    establecimiento_id = Column(Integer, primary_key=True)
    codigo_AMIE = Column(String, nullable=False)
    nombre_establecimiento = Column(String(50), nullable=False)
    codigo_distrito = Column(String(50), nullable=False)
    sostenimiento = Column(String(50), nullable=False)
    tipo_educacion = Column(String(50), nullable=False)
    modalidad = Column(String(50), nullable=False)
    jornada = Column(String(50))
    acceso = Column(String(50))
    numero_estudiantes = Column(Integer, nullable=False)
    numero_docentes = Column(Integer, nullable=False)
    parroquia = relationship("Parroquia", back_populates="establecimientos")
    
    def __repr__(self):
        return "Establecimiento: parroquia_id=%s\n codigo_AMIE=%s\n nombre_establecimiento=%s\n \
            codigo_distrito=%s\n sostenimiento=%s\n tipo_educacion=%s\n modalidad=%s\n jornada=%s\n \
                acceso=%s\n numero_estudiantes=%s\n numero_docentes=%s\n"% (
                          self.parroquia_id,
                          self.codigo_AMIE, 
                          self.nombre_establecimiento,
                          self.codigo_distrito,
                          self.sostenimiento,
                          self.tipo_educacion,
                          self.modalidad,
                          self.jornada,
                          self.acceso,
                          self.numero_estudiantes,
                          self.numero_docentes)

# Se indica a SQLAlchemy que cree las tablas 
Base.metadata.create_all(engine)


```
* ingresa_provincias.py
```python
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

```
* ingresa_cantones.py
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.base import state_str

# se importa la clase(s) del 
# archivo genera_tablas
from genera_tabla import Canton, Provincia

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
    # Se realiza una consulta de la tabla Provincia para guardar los datos en una variable
    data_provincia = session.query(Provincia).all() 
    # Auxiliar para guardar los nombres para despues con un if comparar si se esta repitiendo los nombres
    aux = []
    # for para recorrer el csv y con el método interitertools.islice se le esta diciendo que cuando vaya a leer el archivo 
    # la posiscion 1 no la tome en cuenta
    for row in itertools.islice(reader, 1, None):
        # if en donde se compara el nombre ya ingresado guardado en la variable aux con el nuevo nombre a ingresar 
        # en donde 'not in' identifican con un 'True' o 'False' si se estan repitiendo los nombres
        if row[5] not in aux:
            # Con el .append se procede a guardar si el nombre evaluado es único
            aux.append(row[5])
            # for para recorrer los datos de la tabla Provincia para poder sacar el id de la tabla provincia y 
            # poder ponerlo en la tabla Cantón en el atributo de la clave foránea establecida 
            for provincia in data_provincia:
                # if para comparar si existen datos en la posición del nombre de la provincia para proceder a sacar el 
                # id de esa tabla y asignarlo a una variable 
                if row[3] == provincia.nombre_provincia:
                    id_provincia = provincia.id
                    # Asigación de los datos en los atributos y posiciones correctas
                    e = Canton(nombre_canton=row[5], codigo_division_canton=row[4], provincia_id=id_provincia)
                    # Se guarda dicho objeto como registro en la base de datos.
                    session.add(e)

# Se confirma las transacciones
session.commit()

```
* ingresa_parroquias.py
```python
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
            # for para recorrer los datos de la tabla Cantón para poder sacar el id de la tabla Cantón y 
            # poder ponerlo en la tabla Parroquia en el atributo de la clave foránea establecida 
            for canton in data_canton:
                # if para comparar si existen datos en la posición del nombre del Cantón para proceder a sacar el 
                # id de esa tabla y asignarlo a una variable 
                if row[5] == canton.nombre_canton:
                    id_canton = canton.id 
                    # Asigación de los datos en los atributos y posiciones correctas
                    e = Parroquia(nombre_parroquia=row[7], codigo_division_parroquia=row[6], canton_id=id_canton)
                    # Se guarda dicho objeto como registro en la base de datos.
                    session.add(e)

# Se confirma las transacciones  
session.commit()

```
* ingresa_establecimientos.py
```python
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

```
* consulta1.py
```python
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


```
* consulta2.py
```python
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


```
* consulta3.py
```python
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


```
* consulta4.py
```python
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

```
* consulta5.py
```python
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
