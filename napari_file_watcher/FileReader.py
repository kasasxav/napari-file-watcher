from ome_zarr.io import parse_url
from ome_zarr.reader import Reader
import zarr
import abc
from PIL import Image
import numpy as np
import h5py


class FileReader(abc.ABC):
    """ Base class for reading data """

    def read(self):
        raise NotImplementedError

    def getMetadata(self):
        raise NotImplementedError


class ZarrReader(FileReader):
    """ Reader for zarr files following OME-ZARR recommendations """

    def read(self, filepath):
        reader = Reader(parse_url(filepath))
        nodes = list(reader())
        for i in range(len(nodes)):
            if i == 0:
                images = nodes[0]
            else:
                images.append(nodes[i])
        return images.data

    def getMetadata(self, filepath):
        store = parse_url(filepath, mode="r").store
        root = zarr.group(store=store)
        return root.attrs[list(root.attrs.keys())[0]]


class TiffReader(FileReader):
    """ Reader for tiff files following OME-ZARR recommendations """

    def read(self, filepath):
        im = Image.open(filepath)
        return np.array(im)

    def getMetadata(self, filepath):
        return None


class HDF5Reader(FileReader):
    """ Reader for hdf5 files following OME-ZARR recommendations """

    def read(self, filepath):
        f = h5py.File(filepath, 'r')
        j = 0
        for i in f.values():
            if j == 0:
                data = i
            else:
                data.append(i)
            j = j + 1
        images = np.array(data)
        f.close()
        return images

    def getMetadata(self, filepath):
        f = h5py.File(filepath, 'r')
        metadata = list(f[list(f.keys())[0]].attrs)
        f.close()
        return metadata
