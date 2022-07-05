from flask import Flask, jsonify, abort, request
from flask_cors import CORS, cross_origin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, login_required, logout_user
from flask_login import LoginManager
from models import setup_db, db, datetime, Administrador, Empleado, Tarea
import json

# Environment variables
# $env:FLASK_APP = "server"
# $env:FLASK_ENV = "development"

def create_app(test_config = None):
    app = Flask(__name__)
    login_admin = LoginManager(app)
    login_admin.init_app(app)

    setup_db(app)
    app.config['SECRET_KEY'] = "12345"

    CORS(app)

    @app.after_request
    def after_resquest(response):
        response.headers.add('Content-Type', 'application/json')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
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
                response['message'] = '¡Confirme correctamente su contraseña!'

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


    @app.route('/login/log_admin', methods=["POST"])
    @cross_origin()
    def log_admin():
        response = {}
        error = False

        try:
            dni_admin = request.get_json()['dni']
            password = request.get_json()['password']
            admin = Administrador.query.filter_by(dni_admin = dni_admin).first()

            if admin is not None and check_password_hash(admin.password, password):
                login_user(admin)
                response['success'] = True
                response['admin'] = admin.format()
            else:
                response['success'] = False
                response['message'] = 'Incorrect dni/password combination'

        except Exception as exp:
            error = True
            response['error'] = True
            response['message'] = 'Exception is raised'
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(exp).__name__, exp.args)
            print(message)

        if error:
            abort(500)
        else:
            return jsonify(response)

    @app.route('/empleados', methods=["GET"])
    # @login_required
    @cross_origin()
    def empleados():
        empleados = Empleado.query.order_by('fecha_anadido').all()
        return jsonify({
            'Empleados': [empleado.format() for empleado in empleados],
            'Current User': 'current_user.nombres'
        })

    @app.route('/administradores', methods=["GET"])
    def administradores():
        administradores = Administrador.query.order_by('fecha_anadido').all()
        return jsonify({
            'Administradores': [admin.format() for admin in administradores],
            'Current User': 'current_user.nombres'
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

            empleado = Empleado(
                dni_empleado = dni_empleado,
                nombres = nombres,
                apellidos = apellidos,
                genero = genero,
                admin = '72450405'
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
            response['mensaje'] = 'success'
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

    @app.route('/empleados/update_empleado/<dni>', methods=['PUT'])
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

    @app.route('/tareas')
    @login_required
    def tareas():
        tareas = Tarea.query.all()
        # render_template("tareas.html", tareas = tareas)
        return jsonify({'Component': 'tareas'})

    @app.route('/empleados/asignar_tarea/<dni>', methods = ['POST','GET'])
    def asignar_tarea(dni):

        response = {}

        # Recuperar datos de la tarea
        titulo = request.get_json()["titulo"]
        descripcion = request.get_json()["descripcion"]

        if titulo == "":
            response['mensaje_error'] = 'Ingrese un titulo valido'
            return response
        elif descripcion == "":
            response['mensaje_error'] = 'Ingrese una descripcion valida'
            return response
        else:
            # Empleado al que le vamos a asignar la tarea
            empleado = Empleado.query.filter_by(dni_empleado = dni).first()

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

            return jsonify({'titulo': titulo, 'descripcion': descripcion})

    @app.route('/tareas/update_tarea/<id>', methods = ['PUT'])
    def update_tarea(id):
        # Tarea que va ser completada
        tarea = Tarea.query.filter_by(id_tarea = id)
        # Tarea marcada como completa
        tarea.update({'completo': True})
        db.session.commit()

        # redirect(url_for('tareas'))

        return jsonify({'Component': 'tareas'})

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return jsonify({'Component': 'logout'})

    return app  