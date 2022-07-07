from datetime import datetime
import unittest

from server import create_app
from models import setup_db
import json

class TestTamboApi(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = 'test_proyecto_dbp'
        self.database_path = 'postgresql://{}@{}/{}'.format('postgres:1234', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.test_admin_successful =  {
                'dni': '63578380',
                'nombres': 'Admin',
                'apellidos': 'Istrador',
                'correo': 'adminmail@gmail.com',
                'password': '1234',
                'cpassword': '1234' 
            }

        self.test_admin_failure =  {
                'dni_admin': '',
                'nombres': '',
                'apellidos': '',
                'correo': '',
                'password': '',
                'cpassword': ''
            }

        self.test_empleado_successful =  {
            'dni_empleado': '77776543',
            'nombres': 'Emple',
            'apellidos': 'Ado',
            'genero': 'F'
        }
        
        self.test_empleado_failure =  {
            'dni_empleado': '',
            'nombres': '',
            'apellidos': '',
            'genero': '',
        }           

        self.test_tarea_succesful = {
            'titulo': 'Comer agua',
            'descripcion': 'Vaya a comer agua o sera despedido',
        }

        self.test_tarea_failure = {
            'titulo': '',
            'descripcion': '',
        }

    #------------ADMINISTRADORES-----------------#
    def test_register_admin_failed(self):
        res = self.client().post('/register/register_admin', json = self.test_admin_failure)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Internal Server Error')


    def test_register_admin_success(self):
        res = self.client().post('/register/register_admin', json = self.test_admin_successful)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['admin'])

    def test_login_admin_failed(self):
        pass

    def test_login_admin_success(self):
        pass

    #---------------EMPLEADOS--------------------#
    def test_create_empleado_failed(self):
        pass

    def test_create_empleado_success(self):
        pass

    def test_get_empleados_failed(self):
        pass

    def test_get_empleados_success(self):
        pass

    def test_update_empleado_failed(self):
        pass

    def test_update_empleado_success(self):
        pass

    def test_delete_empleado_failed(self):
        pass

    def test_delete_empleado_success(self):
        pass

    #------------ASIGNACION-DE-TAREAS----------#

    def test_assign_tarea_failed(self):
        pass

    def test_assign_tarea_success(self):
        pass

    #-------------------TAREAS-------------------#

    def test_get_tareass_failed(self):
        pass

    def test_get_tareas_success(self):
        self.client().post('/tareas', json=self.test_tarea_succesful)

        res = self.client().get('/tareas')
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)

    def test_update_tareas_failed(self):
        pass

    def test_update_tarea_success(self):
        pass



### note to self: gonna update every case one by one
