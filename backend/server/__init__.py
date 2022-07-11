from flask import Flask, jsonify, abort, request
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager
from models import setup_db, db, datetime, Administrador, Empleado, Tarea
import json
import jwt

# Environment variables
# $env:FLASK_APP = "server"
# $env:FLASK_ENV = "development"
# http://127.0.0.1:5000/

def create_app(test_config = None):
    app = Flask(__name__)
    login_admin = LoginManager(app)
    login_admin.init_app(app)

    setup_db(app)
    app.config['SECRET_KEY'] = "12345"

    CORS(app)

    @app.after_request
    def after_resquest(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorizations, true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PATCH,DELETE,OPTIONS')
        return response

    @login_admin.user_loader
    def admin_loader(dni):
        return Administrador.query.get(str(dni))

    @app.route('/register/register_admin', methods=["POST"])
    def register_admin():
        error = False
        response = {}

        try:
            dni_admin = request.get_json()['dni']
            nombres = request.get_json()['nombres']
            apellidos = request.get_json()['apellidos']
            correo = request.get_json()['correo']
            password = request.get_json()['password']
            confirm_password = request.get_json()['cpassword']

            hashed = generate_password_hash(password)

            if check_password_hash(hashed, confirm_password):
                admin = Administrador(
                    dni_admin = dni_admin,
                    nombres = nombres,
                    apellidos = apellidos,
                    correo = correo,
                    password = hashed)
                db.session.add(admin)
                db.session.commit()
                response['success'] = True
                response['admin'] = admin.format()
            else:
                response['success'] = False
                response['message'] = 'Confirm correctly validation password'

        except Exception as exp:
            db.session.rollback()
            error = True
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(exp).__name__, exp.args)
            print(message)
            
        finally:
            db.session.close()

        if error:
            abort(500)
        else:
            return jsonify(response)


    @app.route('/login/log_admin', methods = ['POST'])
    def log_admin():
        response = {}
        error = False

        try:
            dni_admin = request.get_json()['dni']
            password = request.get_json()['password']
            admin = Administrador.query.filter_by(dni_admin = dni_admin).first()

            if admin is not None and check_password_hash(admin.password, password):
                response['success'] = True
                response['admin'] = admin.format()
                response['token']  = jwt.encode({
                    'dni_admin': dni_admin
                }, app.config['SECRET_KEY'])
            else:
                response['success'] = False
                response['message'] = 'Incorrect dni/password combination'

        except Exception as exp:
            error = True
            response['success'] = False
            response['message'] = 'Exception is raised'
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(exp).__name__, exp.args)
            print(message)

        if error:
            abort(500)
        else:
            return jsonify(response)

    @app.route('/empleados', methods=["GET"])
    def empleados():
        empleados = Empleado.query.all()
        return jsonify({
            'success': True,
            'empleados': [empleado.format() for empleado in empleados],
        })

    @app.route('/empleados/new_empleado', methods=["POST"])
    def new_empleado():
        error = False
        try:
            body = request.get_json()['body']
            
            print(type(body)) # STRING
            
            data = json.loads(body)

            dni_empleado = data['dni_empleado']
            nombres = data['nombres']
            apellidos = data['apellidos']
            genero = data['genero']
            admin = data['admin']

            empleado = Empleado(
                dni_empleado = dni_empleado,
                nombres = nombres,
                apellidos = apellidos,
                genero = genero,
                admin = admin
            )

            db.session.add(empleado)
            db.session.commit()

        except Exception as exp:
            db.session.rollback()
            error = True
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(exp).__name__, exp.args)
            print(message)
        finally:
            db.session.close()

        if error:
            abort(500)
        else:
            return jsonify({
                'success': True,
                'Empleado': empleado.format()
            })

    @app.route('/empleados/delete_empleado/<dni>', methods=['DELETE'])
    def delete_empleado(dni):
        error = False
        response = {}
        try:
            Tarea.query.filter_by(asignado = dni).delete()
            Empleado.query.filter_by(dni_empleado = dni).delete()
 
            db.session.commit()
            response['success'] = True
            response['admin'] = dni

        except Exception as exp:
            db.session.rollback()
            error = True
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(exp).__name__, exp.args)
            print(message)
        finally:
            db.session.close()

        if error:
            abort(500)
        else:
            return jsonify(response)

    @app.route('/empleados/update_empleado/<dni>', methods=['PATCH'])
    def update_empleado(dni):
        error = False
        response = {}

        try:
            edit_dni_empleado = request.get_json()["edit_dni_empleado"]
            edit_nombres = request.get_json()["edit_nombres"]
            edit_apellidos = request.get_json()["edit_apellidos"]

            empleado = Empleado.query.filter_by(dni_empleado = dni)

            if edit_dni_empleado != "":
                empleado.update({'dni_empleado': edit_dni_empleado})
            else:
                response['mensaje_error'] = 'Ingrese un dni valido'

            if edit_nombres != "":
                empleado.update({'nombres': edit_nombres})
            else:
                response['mensaje_error'] = 'Ingrese un nombre valido'            

            if edit_apellidos != "":
                empleado.update({'apellidos': edit_apellidos})
            else:
                response['mensaje_error'] = 'Ingrese un apellido valido'            

            empleado.update({'fecha_modificado': datetime.now()})

            db.session.commit()

            response['dni_empleado'] = dni

        except Exception as exp:
            db.session.rollback()
            error = True
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(exp).__name__, exp.args)
            print(message)
        finally:
            db.session.close()

        if error:
            abort(500)
        else:
            return jsonify(response)

    @app.route('/tareas', methods = ['GET'])
    def tareas():
        tareas = Tarea.query.all()
        return jsonify({
            'success': True,
            'tareas': [tarea.format() for tarea in tareas]
        })

    @app.route('/empleados/asignar_tarea/<dni>', methods = ['POST'])
    def asignar_tarea(dni):
        # Recuperar datos de la tarea
        titulo = request.get_json()["titulo"]
        descripcion = request.get_json()["descripcion"]

        # Empleado al que le vamos a asignar la tarea
        empleado = Empleado.query.filter_by(dni_empleado = dni).first()

        if empleado is None:
            abort(404)

        # Creamos la tarea
        tarea = Tarea(
            titulo = titulo,
            descripcion = descripcion,
            completo = False,
            empleado = empleado
        )
        # Añadimos la tarea
        db.session.add(tarea)
        db.session.commit()

        # Respuesta
        return jsonify({
            'success': True, 
            'tarea': tarea.format()
        })

    @app.route('/tareas/update_tarea/<id>', methods = ['PATCH'])
    def update_tarea(id):
        # Tarea que va ser completada
        tarea = Tarea.query.filter_by(id_tarea = id)
        if tarea is None:
            abort(404)
        # Tarea marcada como completa
        tarea.update({'completo': True})
        db.session.commit()

        return jsonify({
            'success': True,
            'tarea': tarea.format()
        })

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            'success': False,
            'code': 500,
            'message': 'Internal Server Error'
        }), 500

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'code': 404,
            'message': 'resource not found'
        }), 404

    return app  