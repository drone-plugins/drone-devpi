import os
import sys
import json
import time
import unittest

import run_devpi

BASE_PATH = os.path.dirname(os.path.abspath(__name__))
# We use testpkg as a sample Python module to publish.
TEST_PACKAGE_PATH = os.path.join(BASE_PATH, 'testpkg')


class DevpiTestCase(unittest.TestCase):
    basic_input = {
        "workspace": {
            "path": TEST_PACKAGE_PATH,
        },
        "vargs": {
            "server": "http://localhost:3141/",
            "index": "root/devpitest",
            "username": "root",
            "password": "",
        }
    }
    # We'll override the default clientdir while creating our index below.
    default_clientdir = '/tmp/devpi-testclientdir'

    @classmethod
    def setUpClass(cls):
        # We'll only do this once so we're not hammering the server if we
        # grow this test suite.
        cls._wait_for_devpi_to_start(cls.basic_input, cls.default_clientdir)

    def setUp(self):
        self.old_argv_val = sys.argv

    def tearDown(self):
        sys.argv = self.old_argv_val

    @classmethod
    def _wait_for_devpi_to_start(cls, input_dict, clientdir):
        """
        devpi is a bit... pokey while starting. We'll just harass it until
        it responds before doing the rest of the tests.
        """
        retries_left = 30
        while retries_left > 0:
            try:
                run_devpi.select_server(
                    input_dict['vargs']['server'], clientdir=clientdir)
            except SystemExit:
                retries_left -= 1
                time.sleep(1)
                continue
            return

    def _ensure_test_index_exists(self, input_dict, clientdir):
        """
        Since Drone fires up a new devpi server for each test run, we'll
        need to create an index before we can upload.
        """
        t_varargs = input_dict['vargs']
        run_devpi.select_server(
            t_varargs['server'], clientdir=clientdir)
        run_devpi.login(
            t_varargs['username'], t_varargs['password'],
            clientdir=self.default_clientdir)
        try:
            run_devpi.create_index(
                t_varargs['index'], clientdir=clientdir)
        except SystemExit:
            pass

    def test_upload(self):
        """
        Tests a simple package upload to an existing DevPi server.
        """
        self._ensure_test_index_exists(
            self.basic_input, self.default_clientdir)
        sys.argv = ['--', json.dumps(self.basic_input)]
        run_devpi.main()


if __name__ == '__main__':
    unittest.main()
