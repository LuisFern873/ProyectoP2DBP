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

    #------------ADMINISTRADORES-----------------#
    def test_register_admin_failed(self):
        pass

    def test_register_admin_success(self):
        pass

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
        pass

    def test_update_tareas_failed(self):
        pass

    def test_update_tarea_success(self):
        pass

### note to self: gonna update every case one by one
