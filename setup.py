from setuptools import setup

setup(name='napari-file-watcher',
      version='0.1',
      description='Monitors a folder and displays images as napari layers',
      url='https://github.com/kasasxav/napari-file-watcher',
      author='Xavier Casas Moreno',
      author_email='xavier.casas@outlook.com',
      license='GPL-3.0',
      packages=['napari_file_watcher'],
      install_requires=['napari', 'ome-zarr', 'zarr', 'h5py', 'PyQt5', 'qtpy', 'QScintilla'])