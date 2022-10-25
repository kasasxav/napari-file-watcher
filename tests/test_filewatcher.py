from napari_imswitch_client.main_module import WatcherWidget
import napari
import shutil
import os

def test_browse(widget=None):
    if not widget:
        widget = WatcherWidget(napari.Viewer(show=False))
    os.mkdir('example_data/run')
    path = 'example_data/run'
    widget.browse(path=path)
    os.rmdir('example_data/run')


def test_new_files(qtbot, widget=None):
    if not widget:
        widget = WatcherWidget(napari.Viewer(show=False))
    test_browse(widget)
    widget.toggleWatch(True)
    os.mkdir('example_data/run')
    with qtbot.waitSignal(widget.watcher.sigNewFiles):
        shutil.copy('example_data/neuron_tile_8.zarr', 'example_data/run/neuron_tile_8.zarr')
    widget.showMetadata('neuron_tile_8.zarr')
    os.rmdir('example_data/run')

