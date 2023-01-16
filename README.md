# File watcher plugin for napari (napari-file-watcher)


This plugin contains two widgets: file watcher and script editor.


## Usage: file watcher

The file watcher monitors a folder and displays its images (tiff, ome-zarr or hdf5) as napari layers, watch the following video for a demo:

[![IMAGE ALT TEXT](http://img.youtube.com/vi/lFRVwlHgJ-Y/0.jpg)](https://www.youtube.com/watch?v=lFRVwlHgJ-Y "Demo napari-file-watcher")


## Usage: scripting editor

The script editor is for developing scripts and saving them in the filesystem. 

## Installation

You can install `napari-file-watcher` via [pip]:

    pip install napari-file-watcher

Or if you plan to develop it:

    git clone https://github.com/kasasxav/napari-file-watcher
    cd napari-file-watcher
    pip install -e .

If there is an error message suggesting that git is not installed, run `conda install git`.

## Contributing

Contributions are welcome, tests are run with pytest.

## Issues

Issues can be reported at: https://github.com/kasasxav/napari-file-watcher/issues
