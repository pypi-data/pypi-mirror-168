import unittest
import os
from monitoring_system_sdk import main

monitoring_system_ip = os.environ.get('MONITORING_SYSTEM_IP')
monitoring_system_port = os.environ.get('MONITORING_SYSTEM_PORT')
monitoring_system_login = os.environ.get('MONITORING_SYSTEM_LOGIN')
monitoring_system_pass = os.environ.get('MONITORING_SYSTEM_PASS')


class TestCase(unittest.TestCase):
    inst = main.MonitoringSystemWorker(host=monitoring_system_ip,
                                       port=monitoring_system_port,
                                       username=monitoring_system_login,
                                       password=monitoring_system_pass)

    def test_auth(self):
        auth_result = self.inst.authorize()
        self.assertIn('access_token', auth_result.json())

    def test_ping_apps(self):
        ping_result = self.inst.ping_all_apps()
        self.assertIsInstance(ping_result.json(), dict)

    def test_get_all_apps(self):
        all_apps = self.inst.get_all_apps().json()
        self.assertIsInstance(all_apps, list)

    def test_open_gate(self):
        self.inst.open_internal_gate(10)

    def test_get_video(self):
        response = self.inst.get_video(1, '2022-09-22 15:00:00',
                                       '2022-09-22 15:01:00')
        return response


if __name__ == '__main__':
    unittest.main()
