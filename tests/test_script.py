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
    path = 'tests/run'
    widget.browse(path=path)


def test_add():
    widget = ImScriptingWidget(napari.Viewer(show=False))
    test_open(widget)
    test_browse(widget)
    widget.add()
    assert(filecmp.cmpfiles('example_data/', 'tests/run/', ['timelapse.py', 'experiment.py']))
    os.remove('tests/run/experiment.py')
