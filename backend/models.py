from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

database_path = 'postgresql://ucyhwjueiddyap:d4b568b45f2d21b0d5439543ea3fe7d3560f75ec2799e780897de62bb3752379@ec2-3-224-164-189.compute-1.amazonaws.com:5432/d3kru7fbguascq'

# Host: ec2-3-224-164-189.compute-1.amazonaws.com
# Database: d3kru7fbguascq
# User: ucyhwjueiddyap
# Port: 5432
# Password: d4b568b45f2d21b0d5439543ea3fe7d3560f75ec2799e780897de62bb3752379

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
    empleados = db.relationship('Empleado', backref = 'administrador')

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

    def __repr__(self):
        return "Administrador: {}".format(self.dni_admin)

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def update(self):
        try:
            db.session.commit()
        except:
            db.sesion.rollback()
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

class Empleado(db.Model):
    dni_empleado = db.Column(db.String(8), primary_key = True)
    nombres = db.Column(db.String(50), nullable = False)
    apellidos = db.Column(db.String(50), nullable = False)
    genero = db.Column(db.String(1), nullable = False)

    fecha_anadido = db.Column(db.DateTime(), default = datetime.now)
    fecha_modificado = db.Column(db.DateTime(), nullable = True)

    tareas = db.relationship('Tarea', backref = 'empleado')
    admin = db.Column(db.String(8), db.ForeignKey('administrador.dni_admin'))

    def format(self):
        return {
            'dni_empleado': self.dni_admin,
            'nombres': self.nombres,
            'apellidos': self.apellidos,
            'genero': self.genero,
            'fecha_anadido': self.fecha_anadido,
            'fecha_modificado': self.fecha_modificado
        }

    def __repr__(self):
        return "Empleado: {}".format(self.dni_empleado)

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def update(self):
        try:
            db.session.commit()
        except:
            db.sesion.rollback()
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

    def __repr__(self):
        return "Tarea: {}".format(self.id_tarea)

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def update(self):
        try:
            db.session.commit()
        except:
            db.sesion.rollback()
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


