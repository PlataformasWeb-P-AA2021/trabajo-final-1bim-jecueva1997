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