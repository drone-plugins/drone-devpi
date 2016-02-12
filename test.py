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
        t_vargs = input_dict['vargs']
        run_devpi.select_server(
            t_vargs['server'], clientdir=clientdir)
        run_devpi.login(
            t_vargs['username'], t_vargs['password'],
            clientdir=self.default_clientdir)
        try:
            run_devpi.create_index(
                t_vargs['index'], clientdir=clientdir)
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


class ValidationTestCase(unittest.TestCase):

    def setUp(self):
        self.basic_input = {
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

    def test_vargs_server_validation(self):
        """
        Tests validation for vargs server keyword.
        """
        vargs = self.basic_input.copy()['vargs']
        # Start the party with something weird.
        vargs['server'] = 'blah'
        self.assertRaises(SystemExit, run_devpi.check_vargs, vargs)
        # Why not?
        vargs['server'] = None
        self.assertRaises(SystemExit, run_devpi.check_vargs, vargs)
        vargs['server'] = ''
        self.assertRaises(SystemExit, run_devpi.check_vargs, vargs)
        # Protocol isn't included.
        vargs['server'] = 'somehost.com/'
        self.assertRaises(SystemExit, run_devpi.check_vargs, vargs)
        # Relative paths aren't useful.
        vargs['server'] = '/somewhere'
        self.assertRaises(SystemExit, run_devpi.check_vargs, vargs)
        # As if the user didn't pass it at all.
        del vargs['server']
        self.assertRaises(SystemExit, run_devpi.check_vargs, vargs)
        # These should all be valid.
        vargs['server'] = 'http://test.com/'
        self.assertIsNone(run_devpi.check_vargs(vargs))
        vargs['server'] = 'http://test.com/devpi/'
        self.assertIsNone(run_devpi.check_vargs(vargs))
        vargs['server'] = 'http://test.com:3141/'
        self.assertIsNone(run_devpi.check_vargs(vargs))


if __name__ == '__main__':
    unittest.main()
