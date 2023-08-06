import json
import os
import shutil
from sys import executable
import unittest

import semantic_version
from pyutils.executor import Executor
from pyutils.autoupgrade import AutoUpgrade


class TestAutoupgrade(unittest.TestCase):
    def test_autoupgrade(self):
        # TODO:there should create an isolated env for testing.
        if os.path.exists('pyutils_basstal.egg-info'):
            shutil.rmtree('pyutils_basstal.egg-info')
        executor = Executor(True)
        result = executor.execute_straight(executable, ["-m", "pip", "uninstall", "pyutils_basstal", "--yes"])
        self.assertEqual(result.code, 0)
        result = executor.execute_straight(executable, ["-m", "pip", "install", "pyutils_basstal==0.1.1"])
        self.assertEqual(result.code, 0)
        autoupgrade = AutoUpgrade("pyutils_basstal", verbose=True)
        # TODO: there may timeout.
        upgrade_needed = autoupgrade.upgrade_if_needed(False, True)
        self.assertTrue(upgrade_needed)
        # NOTE: py is specified as python3 executable
        result = executor.execute_straight(executable, ['-m', "pip", "list", "-u", "--format=json"])
        result = json.loads(result.out_str)
        highest_version = autoupgrade.get_highest_version()
        self.assertTrue(len([pkg for pkg in result if pkg["name"] == "pyutils-basstal" and semantic_version.Version(pkg["version"]) == highest_version]) > 0)
