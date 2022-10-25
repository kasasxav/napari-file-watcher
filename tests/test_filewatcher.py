from napari_imswitch_client.main_module import WatcherWidget
import napari
import shutil


def test_browse(widget=None):
    if not widget:
        widget = WatcherWidget(napari.Viewer(show=False))
    path = 'tests/run'
    widget.browse(path=path)


def test_new_files(qtbot, widget=None):
    if not widget:
        widget = WatcherWidget(napari.Viewer(show=False))
    test_browse(widget)
    widget.toggleWatch(True)
    with qtbot.waitSignal(widget.watcher.sigNewFiles):
        shutil.copy('example_data/neuron_tile_8.zarr', 'tests/run/neuron_tile_8.zarr')
    widget.showMetadata('neuron_tile_8.zarr')

