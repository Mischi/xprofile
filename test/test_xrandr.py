# -*- coding: utf-8 -*-
from mock import patch
from xprofile import xrandr


with open('test/multi_screen.txt', 'rb') as file:
    XRANDR_MULTI_SCREEN = file.read()


@patch('xprofile.xrandr.Popen')
def test_call_xrandr_failure(Popen):
    Popen.return_value.communicate.return_value = (None, 'An unknown error occurred.')
    Popen.return_value.wait.return_value = 1
    try:
        edid = xrandr._call_xrandr(['--verbose'])
    except RuntimeError as err:
        assert str(err) == 'xrandr error: An unknown error occurred.'
    else:
        assert False, 'Failed to raise RuntimeError'

    assert Popen.called
    assert Popen.call_args[0][0] == ['/usr/bin/xrandr', '--verbose']


@patch('xprofile.xrandr.Popen')
def test_parse_xrandr_output(Popen):
    Popen.return_value.communicate.return_value = (XRANDR_MULTI_SCREEN, None)
    Popen.return_value.wait.return_value = 0

    displays = xrandr._parse_xrandr_output()

    assert Popen.called
    assert Popen.call_args[0][0] == ['/usr/bin/xrandr']
    assert len(displays) == 3

    assert displays[0]['name'] == 'VGA1'
    assert displays[0]['connected'] == True
    assert displays[0]['status'] == 'connected'
    assert displays[0]['geometry']['dimension'] == '1280x1024'
    assert displays[0]['geometry']['offset'] == '0x0'
    assert displays[0]['active'] == True
    assert displays[0]['rotation'] == None
    assert displays[0]['primary'] == False

    assert displays[1]['name'] == 'DVI1'
    assert displays[1]['connected'] == True
    assert displays[1]['status'] == 'connected'
    assert displays[1]['geometry']['dimension'] == '1280x1024'
    assert displays[1]['geometry']['offset'] == '1280x0'
    assert displays[1]['active'] == True
    assert displays[1]['rotation'] == None
    assert displays[1]['primary'] == False

    assert displays[2]['name'] == 'TV1'
    assert displays[2]['connected'] == False
    assert displays[2]['status'] == 'unknown connection'
    assert displays[2]['geometry'] == None

@patch('xprofile.xrandr.Popen')
def test_get_current_xrandr_config(Popen):
    Popen.return_value.communicate.return_value = (XRANDR_MULTI_SCREEN, None)
    Popen.return_value.wait.return_value = 0

    config = xrandr._get_current_xrandr_config()

    assert config == [
        '--output', 'VGA1', '--mode', '1280x1024', '--pos', '0x0',
        '--output', 'DVI1', '--mode', '1280x1024', '--pos', '1280x0'
    ]