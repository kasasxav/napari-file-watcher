from napari_imswitch_client.main_module import WatcherWidget
import napari
import shutil
import os
import time


def test_browse(widget=None, path=None):
    if not widget:
        widget = WatcherWidget(napari.Viewer(show=False))
    try:
        os.mkdir('example_data/run')
    except FileExistsError:
        pass
    if not path:
        path = 'example_data/run'
    widget.browse(path=path)


def test_new_files(qtbot, widget=None):
    if not widget:
        widget = WatcherWidget(napari.Viewer(show=False))
    with qtbot.waitSignal(widget.sigNewFiles):
        try:
            test_browse(widget=widget, path='example_data/run')
            shutil.copytree('example_data/neuron_tile_8.zarr', 'example_data/run/neuron_tile_8.zarr')
            widget.toggleWatch(True)
            widget.showMetadata('neuron_tile_8.zarr')
            widget.toggleWatch(False)
            try:
                time.sleep(1)
                shutil.rmtree('example_data/run')
            except FileNotFoundError:
                pass
        except PermissionError:
            test_browse(widget=widget, path='example_data/')
            widget.toggleWatch(True)
            widget.showMetadata('neuron_tile_8.zarr')
            widget.toggleWatch(False)


