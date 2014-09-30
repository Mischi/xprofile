# -*- coding: utf-8 -*-
import tempfile

from mock import patch

from xprofile.xrandr import Xrandr
from xprofile.__main__ import main
from distutils.spawn import find_executable

xrandr_bin = find_executable('xrandr')

@patch('xprofile.xrandr.Popen')
def test_create_new_profile(Popen):
    with open('test/docked.txt', 'rb') as file:
        xrandr_stdout = file.read()

    with tempfile.NamedTemporaryFile() as tmpfile:
        Popen.return_value.communicate.return_value = (xrandr_stdout, None)
        Popen.return_value.wait.return_value = 0

        retval = main(['--config', tmpfile.name, 'create', 'testprofile'])

        assert retval == 0
        assert Popen.called
        assert Popen.call_args[0][0] == [xrandr_bin, '--verbose']


@patch('xprofile.xrandr.Popen')
def test_create_two_new_profiles(Popen):
    with open('test/docked.txt', 'rb') as file1:
        xrandr_stdout1 = file1.read()

    with open('test/laptop.txt', 'rb') as file2:
        xrandr_stdout2 = file2.read()

    with tempfile.NamedTemporaryFile() as tmpfile:
        Popen.return_value.communicate.return_value = (xrandr_stdout1, None)
        Popen.return_value.wait.return_value = 0

        retval = main(['--config', tmpfile.name, 'create', 'testprofile1'])

        assert retval == 0
        assert Popen.called
        assert Popen.call_args[0][0] == [xrandr_bin, '--verbose']


        Popen.return_value.communicate.return_value = (xrandr_stdout2, None)
        Popen.return_value.wait.return_value = 0

        retval = main(['--config', tmpfile.name, 'create', 'testprofile2'])

        assert retval == 0
        assert Popen.called
        assert Popen.call_args[0][0] == [xrandr_bin, '--verbose']


@patch('xprofile.xrandr.Popen')
def test_create_new_profile_dryrun(Popen):
    with open('test/docked.txt', 'rb') as file:
        xrandr_stdout = file.read()

    with tempfile.NamedTemporaryFile() as tmpfile:
        Popen.return_value.communicate.return_value = (xrandr_stdout, None)
        Popen.return_value.wait.return_value = 0

        retval = main(['--config', tmpfile.name, 'create', 'testprofile', '--dry-run'])

        assert retval == 0
        assert Popen.called
        assert Popen.call_args[0][0] == [xrandr_bin, '--verbose']


@patch('xprofile.xrandr.Popen')
def test_create_existing_profile(Popen):
    with open('test/docked.txt', 'rb') as file:
        xrandr_stdout = file.read()

    Popen.return_value.communicate.return_value = (xrandr_stdout, None)
    Popen.return_value.wait.return_value = 0

    retval = main(['--config', 'test/xprofilerc_example', 'create', 'laptop'])

    assert retval == 1
    assert Popen.called
    assert Popen.call_args[0][0] == [xrandr_bin, '--verbose']

def test_list():
    main(['--config', 'test/xprofilerc_example', 'list'])


@patch('xprofile.xrandr.Popen')
def test_current(Popen):
    with open('test/docked.txt', 'rb') as file:
        xrandr_stdout = file.read()

    Popen.return_value.communicate.return_value = (xrandr_stdout, None)
    Popen.return_value.wait.return_value = 0

    retval = main(['--config', 'test/xprofilerc_example', 'current'])

    assert retval == 0
    assert Popen.called


@patch('xprofile.xrandr.Popen')
def test_activate_profile(Popen):
    Popen.return_value.communicate.return_value = (b'', None)
    Popen.return_value.wait.return_value = 0

    retval = main(['--config', 'test/xprofilerc_example', 'activate', 'docked'])

    assert retval == 0
    assert Popen.called
    assert Popen.call_args[0][0] == [
        xrandr_bin,
        '--output', 'LVDS1', '--off',
        '--output', 'DP2', '--mode', '1920x1080', '--pos', '0x500', '--primary',
        '--output', 'HDMI3', '--mode', '1920x1080', '--rotate', 'left', '--pos', '1930x0'
    ]


def test_activate_profile_nonexistent():
    retval = main(['--config', 'test/xprofilerc_example', 'activate', 'nonexistent'])

    assert retval == 1


@patch('xprofile.xrandr.Popen')
def test_activate_profile_auto(Popen):
    with open('test/laptop.txt', 'rb') as file:
        xrandr_stdout = file.read()

    Popen.return_value.communicate.return_value = (xrandr_stdout, None)
    Popen.return_value.wait.return_value = 0

    retval = main(['--config', 'test/xprofilerc_example', 'auto'])

    assert retval == 0
    assert Popen.called
    assert Popen.call_args[0][0] == [xrandr_bin, '--auto']


@patch('xprofile.xrandr.Popen')
def test_activate_profile_auto__dryrun(Popen):
    with open('test/laptop.txt', 'rb') as file:
        xrandr_stdout = file.read()

    Popen.return_value.communicate.return_value = (xrandr_stdout, None)
    Popen.return_value.wait.return_value = 0

    retval = main(['--config', 'test/xprofilerc_example', 'auto', '--dry-run'])

    assert retval == 0
    assert Popen.called
    assert Popen.call_args[0][0] == [xrandr_bin, '--verbose']


@patch('xprofile.xrandr.Popen')
def test_activate_profile_auto_nonexistent(Popen):
    with open('test/docked.txt', 'rb') as file:
        xrandr_stdout = file.read()

    Popen.return_value.communicate.return_value = (xrandr_stdout, None)
    Popen.return_value.wait.return_value = 0

    retval = main(['--config', 'test/xprofilerc_example', 'auto'])

    assert retval == 0
    assert Popen.called
    assert Popen.call_args[0][0] == [xrandr_bin, '--auto']
