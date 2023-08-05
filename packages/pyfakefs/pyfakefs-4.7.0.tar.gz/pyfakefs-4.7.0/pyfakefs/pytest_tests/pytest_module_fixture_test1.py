# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os

import pytest

from pyfakefs import fake_filesystem
from pyfakefs.tests.test_utils import TestCase, RealFsTestMixin


class RealFsTestCase(TestCase, RealFsTestMixin):
    """Can be used as base class for tests also running in the real
    file system."""

    def __init__(self, methodName='runTest'):
        TestCase.__init__(self, methodName)
        RealFsTestMixin.__init__(self)

    def create_basepath(self):
        old_base_path = self.base_path
        self.base_path = self.filesystem.path_separator + 'basepath'
        if self.filesystem.is_windows_fs:
            self.base_path = 'C:' + self.base_path
        if old_base_path != self.base_path:
            if old_base_path is not None:
                self.filesystem.reset()
            if not self.filesystem.exists(self.base_path):
                self.filesystem.create_dir(self.base_path)
            if old_base_path is not None:
                self.setUpFileSystem()

    def setUp(self):
        RealFsTestMixin.setUp(self)
        if not self.use_real_fs():
            self.filesystem = fake_filesystem.FakeFilesystem(
                path_separator=self.path_separator())
            self.create_basepath()


    def tearDown(self):
        RealFsTestMixin.tearDown(self)


class TestModuleScopedFsWithTmpdir:
    @pytest.fixture(autouse=True)
    def test_internal(self, tmpdir):
        yield

    def test_fail(self, fs_module):
        # Regression test for #684
        assert True


class TestUnitTest(RealFsTestCase):
    def test_something(self):
        self.check_posix_only()
