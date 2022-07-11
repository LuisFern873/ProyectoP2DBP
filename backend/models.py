from email.policy import default
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

database_path = 'postgresql://{}:{}@{}:{}/{}'.format(
    'ucyhwjueiddyap', # User
    'd4b568b45f2d21b0d5439543ea3fe7d3560f75ec2799e780897de62bb3752379', # Password
    'ec2-3-224-164-189.compute-1.amazonaws.com', # Host
    '5432', # Port
    'd3kru7fbguascq' # Database
)


def setup_db(app, database_path = database_path):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    db.create_all()

class Administrador(db.Model, UserMixin):
    dni_admin = db.Column(db.String(8), primary_key = True)
    nombres = db.Column(db.String(100), nullable = False)
    apellidos = db.Column(db.String(100), nullable = False)
    correo = db.Column(db.String(100), unique = True, nullable = False)
    password = db.Column(db.String(300), nullable = False)
    fecha_anadido = db.Column(db.DateTime(), default = datetime.now)

    def format(self):
        return {
            'dni_admin': self.dni_admin,
            'nombres': self.nombres,
            'apellidos': self.apellidos,
            'correo': self.correo,
            'password': self.password,
            'fecha_anadido': self.fecha_anadido,
        }

    def get_id(self):
        return (self.dni_admin)

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self.dni_admin

        except:
            db.session.rollback()
        finally:
            db.session.close()

    def update(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def __repr__(self):
        return f'Administrador: dni_admin={self.dni_admin}, nombres={self.nombres}, apellidos={self.apellidos}, correo={self.correo}'

class Empleado(db.Model):
    dni_empleado = db.Column(db.String(8), primary_key = True)
    nombres = db.Column(db.String(50), nullable = False)
    apellidos = db.Column(db.String(50), nullable = False)
    genero = db.Column(db.String(1), nullable = False)

    fecha_anadido = db.Column(db.DateTime(), default = datetime.now)
    fecha_modificado = db.Column(db.DateTime(), nullable = True, default=None)

    tareas = db.relationship('Tarea', backref = 'empleado')

    def format(self):
        return {
            'dni_empleado': self.dni_empleado,
            'nombres': self.nombres,
            'apellidos': self.apellidos,
            'genero': self.genero,
            'fecha_anadido': self.fecha_anadido,
            'fecha_modificado': self.fecha_modificado
        }

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self.dni_empleado

        except:
            db.session.rollback()
        finally:
            db.session.close()

    def update(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()  
    
    def __repr__(self):
        return f'Empleado: dni_empleado={self.dni_empleado}, nombres={self.nombres}, apellidos={self.apellidos}, genero={self.genero}, fecha_añadido={self.fecha_anadido}'

class Tarea(db.Model):
    id_tarea = db.Column(db.Integer, primary_key = True)
    titulo = db.Column(db.String(50), nullable = True)
    descripcion = db.Column(db.String(500), nullable = True)
    completo = db.Column(db.Boolean, nullable = False)
    asignado = db.Column(db.String(8), db.ForeignKey('empleado.dni_empleado'))

    def format(self):
        return {
            'id_tarea': self.id_tarea,
            'titulo': self.titulo,
            'descripcion': self.descripcion,
            'completo': self.completo,
            'asignado': self.asignado
        }

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self.id_tarea
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def update(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def __repr__(self):
        return f'Tarea: id_tarea={self.id_tarea}, titulo={self.titulo}, descripcion={self.descripcion}, completado={self.completo}, asignado={self.asignado}'
