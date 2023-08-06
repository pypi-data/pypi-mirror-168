"""
SPAM test class based on unitest.TestCase.
Copyright (C) 2020 SPAM Contributors

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option)
any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
more details.

You should have received a copy of the GNU General Public License along with
this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from unittest import TestCase
import os
import shutil
from pathlib import Path

class TestSpam(TestCase):
    """ Overwrites setUp and tearDown of unitest.TestCase
    to create and delete a .dump folder for files created during tests.
    """

    def setUp(self):
        # check if working directory is ".dump"
        wd = os.getcwd()
        if os.path.basename(wd) == ".dump":
            # we're already in ".dump"
            pass
        else:
            # try creating .dump
            d = os.path.join(wd, ".dump")
            if not os.path.isdir(d):
                os.makedirs(d)
            os.chdir(d)

        wd = os.getcwd()

    def tearDown(self):
        # get
        # check if working directory is ".dump"
        wd = os.getcwd()
        if os.path.basename(wd) == ".dump":
            # step back
            d = Path(wd).resolve().parent
            os.chdir(d)

        else:
            # working directory is not ".dump" (that shouldn't happen)
            pass

        wd = os.getcwd()

        # remove ".dump"
        if os.path.isdir(".dump"):
            # print(f"setUp wd: remove .dump dir")
            shutil.rmtree(".dump")
