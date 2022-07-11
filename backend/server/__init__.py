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
        error_422 = False

        try:
            body = request.get_json()

            dni_admin = body.get('dni_admin')
            nombres = body.get('nombres')
            apellidos = body.get('apellidos')
            correo = body.get('correo')
            password = body.get('password')
            confirm_password = body.get('cpassword')

            if dni_admin is None or nombres is None or apellidos is None or correo is None or password is None or confirm_password is None:
                error_422 = True
                abort(422)

            hashed = generate_password_hash(password)

            if check_password_hash(hashed, confirm_password):
                admin = Administrador(
                    dni_admin = dni_admin,
                    nombres = nombres,
                    apellidos = apellidos,
                    correo = correo,
                    password = hashed)

                new_admin_dni = admin.insert()

                return jsonify({
                    'success': True,
                    'created': new_admin_dni
                })

            else:
                return jsonify({
                    'success': False,
                    'message': 'Unconfirmed password'
                })

        except Exception as exp:
            print(exp)
            if error_422:
                abort(422)
            else:
                abort(500)


    @app.route('/login/log_admin', methods = ['POST'])
    def log_admin():
        error_422 = False

        try:
            body = request.get_json()

            dni_admin = body.get('dni_admin')
            password = body.get('password')

            if dni_admin is None or password is None:
                error_422 = True
                abort(422)
            
            admin = Administrador.query.filter_by(dni_admin = dni_admin).first()

            if check_password_hash(admin.password, password):
                return jsonify({
                    'success': True,
                    'logged': dni_admin,
                    'token': jwt.encode({'dni_admin': dni_admin}, app.config['SECRET_KEY'])
                })

            else:
                return jsonify({
                    'success': False,
                    'message': 'Incorrect dni/password combination'
                })

        except Exception as exp:
            print(exp)
            if error_422:
                abort(422)
            else:
                abort(500)

    @app.route('/empleados', methods=["GET"])
    def empleados():
        empleados = Empleado.query.all()

        if len(empleados) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'empleados': [empleado.format() for empleado in empleados],
        })

    @app.route('/empleados/new_empleado', methods=["POST"])
    def new_empleado():
        error_422 = False
        try:
            body = request.get_json()
                       
            dni_empleado = body.get('dni_empleado')
            nombres = body.get('nombres')
            apellidos = body.get('apellidos') 
            genero = body.get('genero')

            if dni_empleado is None or nombres is None or apellidos is None or genero is None:
                error_422 = True
                abort(422)

            empleado = Empleado(
                dni_empleado = dni_empleado,
                nombres = nombres,
                apellidos = apellidos,
                genero = genero
            )

            new_empleado_dni = empleado.insert()

            return jsonify({
                'success': True,
                'empleado': new_empleado_dni
            })

        except Exception as exp:
            print(exp)
            if error_422:
                abort(422)
            else:   
                abort(500)

    @app.route('/empleados/delete_empleado/<dni_empleado>', methods=['DELETE'])
    def delete_empleado(dni_empleado):
        error_404 = False

        try:
            empleado = Empleado.query.filter_by(dni_empleado = dni_empleado).one_or_none()
 
            if empleado is None:
                error_404 = True
                abort(404)
            
            empleado.delete()

            tareas = Tarea.query.filter_by(asignado = dni_empleado)

            tareas.delete()

            return jsonify({
                'success': True,
                'empleado_deleted': dni_empleado
            })

        except Exception as exp:
            print(exp)
            if error_404:
                abort(404)
            else:
                abort(500)

    @app.route('/empleados/update_empleado/<dni_empleado>', methods=['PATCH'])
    def update_empleado(dni_empleado):
        error_404 = False

        try:
            empleado = Empleado.query.filter_by(dni_empleado = dni_empleado).one_or_none()

            if empleado is None:
                error_404 = True
                abort(404)
            
            body = request.get_json()
            if 'dni_empleado' in body:
                empleado.dni_empleado = body.get('dni_empleado')

            if 'nombres' in body:
                empleado.nombres = body.get('nombres')
            
            if 'apellidos' in body:
                empleado.apellidos = body.get('apellidos')     

            empleado.update()

            return jsonify({
                'success': True,
                'empleado_updated': dni_empleado
            })

        except Exception as exp:
            print(exp)
            if error_404:
                abort(404)
            else:
                abort(500)

    @app.route('/tareas', methods = ['GET'])
    def tareas():
        tareas = Tarea.query.all()
        return jsonify({
            'success': True,
            'tareas': [tarea.format() for tarea in tareas]
        })

    @app.route('/empleados/asignar_tarea/<dni_empleado>', methods = ['POST'])
    def asignar_tarea(dni_empleado):
        error_422 = False
        error_404 = False

        # Empleado asignado para la tarea
        empleado = Empleado.query.filter_by(dni_empleado = dni_empleado).first()

        if empleado is None:
            error_404 = True
            abort(404)

        # Recuperando datos de la tarea
        body = request.get_json()

        id_tarea = body.get('id_tarea')
        titulo = body.get('titulo')
        descripcion = body.get('descripcion', None)

        if titulo is None:
            error_422 = True
            abort(422)
        
        # Creando la tarea
        tarea = Tarea(
            id_tarea = id_tarea,
            titulo = titulo,
            descripcion = descripcion,
            completo = False,
            empleado = empleado
        ) 

        tarea.insert()

        return jsonify({
            'success': True,
            'assigned': id_tarea
        })

    @app.route('/tareas/update_tarea/<id_tarea>', methods = ['PATCH'])
    def update_tarea(id_tarea):
        error_404 = False

        try:
            # Buscamos la tarea
            tarea = Tarea.query.filter_by(id_tarea = id_tarea).one_or_none()
            
            if tarea is None:
                abort(404)
            
            # Marcamos como completa a la tarea
            tarea.completo = True
            tarea.update()

            return jsonify({
                'success': True,
                'tarea_updated': id_tarea
            })
        
        except Exception as exp:
            print(exp)
            if error_404:
                abort(404)
            else:
                abort(500)

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
    
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'code': 422,
            'message': 'Unprocessable'
        }), 422

    return app  