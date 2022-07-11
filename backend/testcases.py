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

        self.admin_failure =  {
                'dni_admin': None,
                'nombres': None,
                'apellidos': None,
                'correo': None,
                'password': None,
                'cpassword': None
            }

        self.admin_successful =  {
                'dni_admin': '63578380',
                'nombres': 'Admin',
                'apellidos': 'Istrador',
                'correo': 'adminmail@gmail.com',
                'password': '1234',
                'cpassword': '1234' 
            }        

        self.empleado_failure =  {
            'dni_empleado': None,
            'nombres': None,
            'apellidos': None,
            'genero': None
        }

        self.empleado_successful =  {
            'dni_empleado': '77776543',
            'nombres': 'Emple',
            'apellidos': 'Ado',
            'genero': 'f'
        }

        self.empleado_update =  {
            'dni_empleado': '01010101',
            'nombres': 'update',
            'apellidos': 'empleado',
            'genero': 'm'
        }       

    #------------ADMINISTRADORES-----------------#
    def test_register_admin_failed(self):
        res = self.client().post('/register/register_admin', json = self.admin_failure)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    def test_register_admin_success(self):
        res = self.client().post('/register/register_admin', json = self.admin_successful)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_login_admin_failed(self):
        res = self.client().post('/login/log_admin', json = self.admin_failure)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    def test_login_admin_success(self):
        res = self.client().post('/login/log_admin', json = self.admin_successful)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['logged'])


    #---------------EMPLEADOS--------------------#
    def test_create_empleado_failed(self):
        res = self.client().post('/empleados/new_empleado', json = self.empleado_failure)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable') 

    def test_create_empleado_success(self):
        res = self.client().post('/empleados/new_empleado', json = self.empleado_successful)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['empleado'])  

    def test_get_empleados_failed(self):
        res = self.client().get('/empleados?dni_empleado=0000000000000')
        data = json.loads(res.data)

        self.assertNotEqual(res.status_code, 500)
        self.assertNotEqual(data['success'], False)
        self.assertNotEqual(data['empleados'], 'Internal Server Error')

    def test_get_empleados_success(self):
        res = self.client().get('/empleados')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['empleados'])

    def test_update_empleado_failed(self):
        res = self.client().patch('/empleados/update_empleado/00001111')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_update_empleado_success(self):
        res0 = self.client().post('/empleados/new_empleado', json = self.empleado_update)
        data0 = json.loads(res0.data)
        updated_dni = data0['empleado']

        res = self.client().patch('/empleados/update_empleado/' + str(updated_dni), json={'nombres': 'new nombre'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['empleado_updated'])

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
        pass

    def test_update_tareas_failed(self):
        pass

    def test_update_tarea_success(self):
        pass

### note to self: gonna update every case one by one
