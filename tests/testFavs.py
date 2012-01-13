"""Tests for the gh_favs script"""


import sys
import os
import imp
import unittest
import tempfile
import shutil
import socket
from StringIO import StringIO


path = (os.path.abspath(os.path.dirname(os.path.dirname(__file__))) +
        os.sep + 'gh_favs')
gh_favs = imp.load_module('gh_favs', open(path), path,
                          ('', 'r', imp.PY_SOURCE))


try:
    con = socket.create_connection(('github.com', 80), timeout=10)
except (socket.gaierror, socket.timeout), e:
    online = False
else:
    con.close()
    online = True


class TestFavs(unittest.TestCase):

    def setUp(self):
        global path
        self.testfavs = [('a', 'a', 'a'), ('a', 'b', 'b'),
                         ('c', 'c', 'c')]
        self.mefav = [('gh_favs', os.path.dirname(path), 'Boldewyn')]
        self.tmpdir = tempfile.mkdtemp()
        self.stdout = sys.stdout = StringIO()
        self.stderr = sys.stderr = StringIO()

    def tearDown(self):
        shutil.rmtree(self.tmpdir)
        sys.stderr = sys.__stderr__
        self.stderr.close()
        sys.stdout = sys.__stdout__
        self.stdout.close()

    @unittest.skipIf(not online, 'offline')
    def test_exclude_own(self):
        favs1 = gh_favs.fetch_favs('Boldewyn', [], True)
        favs2 = gh_favs.fetch_favs('Boldewyn', [], False)
        self.assertTrue(len(favs2) < len(favs1))

    @unittest.skipIf(not online, 'offline')
    def test_ignore(self):
        favs1 = gh_favs.fetch_favs('Boldewyn', [], True)
        favs2 = gh_favs.fetch_favs('Boldewyn', ['gh_favs'], True)
        self.assertTrue(len(favs2) < len(favs1))

    def test_resolve_prefix(self):
        """resolve conflicts with prefixes"""
        favs = gh_favs.resolve_fav_conflicts(self.testfavs, 'prefix')
        self.assertTrue(('a-a', 'a', 'a') in favs)
        self.assertTrue(('b-a', 'b', 'b') in favs)
        self.assertTrue(('c', 'c', 'c') in favs)

    def test_resolve_subfolders(self):
        """resolve conflicts with global subfolders"""
        favs = gh_favs.resolve_fav_conflicts(self.testfavs,
                'subfolders')
        self.assertTrue(('a/a', 'a', 'a') in favs)
        self.assertTrue(('b/a', 'b', 'b') in favs)
        self.assertTrue(('c/c', 'c', 'c') in favs)

    def test_resolve_none(self):
        """don't resolve conflicts"""
        favs = gh_favs.resolve_fav_conflicts(self.testfavs,
                'subfolders')
        self.assertEqual(self.testfavs, favs)

    def test_clone(self):
        """clone favorites with docs"""
        gh_favs.clone_favs(self.mefav, self.tmpdir)
        self.assertTrue(os.path.isdir(self.tmpdir + os.sep + 'gh_favs'))
        self.assertTrue(os.path.isfile(self.tmpdir + os.sep + 'gh_favs' +
            os.sep + '.git' + os.sep + 'refs' + os.sep + 'heads' +
            os.sep + 'gh-pages'))

    def test_clone_nodocs(self):
        """clone favorites w/o docs"""
        gh_favs.clone_favs(self.mefav, self.tmpdir, with_docs=False)
        self.assertTrue(os.path.isdir(self.tmpdir + os.sep + 'gh_favs'))
        self.assertFalse(os.path.isfile(self.tmpdir + os.sep + 'gh_favs' +
            os.sep + '.git' + os.sep + 'refs' + os.sep + 'heads' +
            os.sep + 'gh-pages'))

    def test_clone_verbosly(self):
        """clone verbosly"""
        gh_favs.clone_favs(self.mefav, self.tmpdir, quiet=False)
        self.assertTrue(os.path.isdir(self.tmpdir + os.sep + 'gh_favs'))

    def test_cli_target(self):
        """fetch CLI arguments with target"""
        args = gh_favs._get_args(['-t', 'a', 'b'])
        self.assertTrue(args == ('a', 'b', None, False, False, False,
                        'subfolders'))

    def test_cli_strategy(self):
        """fetch CLI arguments with strategy"""
        args = gh_favs._get_args(['-s', 'prefix', 'b'])
        self.assertTrue(args == ('.', 'b', None, False, False, False,
                        'prefix'))

    def test_cli_strategy_fail(self):
        try:
            args = gh_favs._get_args(['-s', 'foobar', 'b'])
        except:
            self.assertTrue(self.stderr.len > 0, 'print error message')
        else:
            self.fail('non-existing strategy should fail')

    def test_cli_ignore(self):
        """fetch CLI arguments with ignored ones"""
        args = gh_favs._get_args(['-i', 'a', '--', 'b'])
        self.assertTrue(args == ('.', 'b', ['a'], False, False, False,
                        'subfolders'))

    def test_cli_special(self):
        """fetch CLI arguments with flags set"""
        args = gh_favs._get_args(['-v', '-o', '-n', 'b'])
        self.assertTrue(args == ('.', 'b', None, True, True, True,
                        'subfolders'))

