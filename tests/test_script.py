from napari_imswitch_client.main_module import ImScriptingWidget
import napari
import filecmp
import os


def test_open(widget=None):
    if not widget:
        widget = ImScriptingWidget(napari.Viewer(show=False))
    path = 'example_data/timelapse.py'
    widget.open(path=path)


def test_browse(widget=None):
    if not widget:
        widget = ImScriptingWidget(napari.Viewer(show=False))
    os.mkdir('example_data/run')
    path = 'example_data/run'
    widget.browse(path=path)
    os.rmdir('example_data/run')


def test_add():
    widget = ImScriptingWidget(napari.Viewer(show=False))
    test_open(widget)
    test_browse(widget)
    widget.add()
    os.mkdir('example_data/run')
    assert(filecmp.cmpfiles('example_data/', 'example_data/run/', ['timelapse.py', 'experiment.py']))
    os.remove('example_data/run/experiment.py')
    os.rmdir('example_data/run')