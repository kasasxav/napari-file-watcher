from napari_imswitch_client.main_module import WatcherWidget
import napari
import shutil
import os


def test_browse(widget=None):
    if not widget:
        widget = WatcherWidget(napari.Viewer(show=False))
    try:
        os.mkdir('example_data/run')
    except FileExistsError:
        pass
    path = 'example_data/run'
    widget.browse(path=path)


def test_new_files(qtbot, widget=None):
    if not widget:
        widget = WatcherWidget(napari.Viewer(show=False))
    test_browse(widget)
    widget.toggleWatch(True)
    with qtbot.waitSignal(widget.watcher.sigNewFiles):
        shutil.copy('example_data/neuron_tile_8.zarr', 'example_data/run/neuron_tile_8.zarr')
    widget.showMetadata('neuron_tile_8.zarr')
    try:
        os.rmdir('example_data/run')
    except FileNotFoundError:
        pass

