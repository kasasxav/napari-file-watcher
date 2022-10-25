import os
from qtpy.QtWidgets import QWidget, QTreeWidget, QTreeWidgetItem
from PyQt5 import Qsci
from qtpy import QtGui, QtWidgets
from napari_imswitch_client.guitools.BetterPushButton import BetterPushButton
from napari_imswitch_client.guitools.dialogtools import askForFolderPath, askForFilePath
from napari_imswitch_client.FileWatcher import FileWatcher
from ome_zarr.io import parse_url
from ome_zarr.reader import Reader
import zarr
from datetime import datetime


class ImScriptingWidget(QWidget):
    def __init__(self, viewer: 'napari.viewer.Viewer'):
        super().__init__()
        self._viewer = viewer

        layout = QtWidgets.QGridLayout()
        self.setLayout(layout)

        self.path = os.path.dirname(os.path.realpath(__file__))
        self.folderEdit = QtWidgets.QLineEdit(self.path)
        layout.addWidget(self.folderEdit, 0, 0, 1, 2)
        self.browseButton = BetterPushButton('Browse')
        self.browseButton.clicked.connect(self.browse)
        layout.addWidget(self.browseButton, 0, 2)

        self.nameEdit = QtWidgets.QLineEdit('experiment')
        layout.addWidget(self.nameEdit, 1, 0)

        self.addButton = BetterPushButton('Add')
        self.addButton.clicked.connect(self.add)
        layout.addWidget(self.addButton, 1, 1)
        self.openButton = BetterPushButton('Open')
        self.openButton.clicked.connect(self.open)
        layout.addWidget(self.openButton, 1, 2)

        self.scintilla = Scintilla()
        layout.addWidget(self.scintilla, 2, 0, 1, 3)

    def browse(self, path=None):
        if not path:
            path = askForFolderPath(self, defaultFolder=self.path)
        if path:
            self.path = path
            self.folderEdit.setText(self.path)

    def add(self):
        text = self.scintilla.text()
        file = open(self.path + '\\' + self.nameEdit.text() + '.py', 'w')
        file.write(text)
        file.close()

    def open(self, path=None):
        if not path:
            path = askForFilePath(self, defaultFolder=self.path)
        if path:
            file = open(path, "r")
            text = file.read()
            file.close()
            self.scintilla.setText(text)


class Scintilla(Qsci.QsciScintilla):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setMargins(1)
        self.setMarginWidth(0, '00000000')
        self.setMarginType(0, Qsci.QsciScintilla.NumberMargin)

        self.setTabWidth(4)
        self.setIndentationGuides(True)
        self.setAutoIndent(True)

        self.setScrollWidth(1)
        self.setScrollWidthTracking(True)

        font = QtGui.QFontDatabase.systemFont(QtGui.QFontDatabase.FixedFont)
        font.setPointSize(11)

        lexer = Qsci.QsciLexerPython()
        lexer.setFont(font)
        lexer.setDefaultFont(font)
        self.setLexer(lexer)


class WatcherWidget(QWidget):
    """ Widget that watch for new image files (.tiff) in a specific folder, for running them sequentially."""

    def __init__(self, viewer: 'napari.viewer.Viewer'):
        super().__init__()
        self._viewer = viewer

        self.path = os.path.dirname(os.path.realpath(__file__))
        self.folderEdit = QtWidgets.QLineEdit(self.path)

        self.browseFolderButton = BetterPushButton('Browse')
        self.watchCheck = QtWidgets.QCheckBox('Watch and run')

        self.listWidget = QtWidgets.QListWidget()
        self.updateFileList()

        layout = QtWidgets.QGridLayout()
        self.setLayout(layout)

        layout.addWidget(self.folderEdit, 0, 1)
        layout.addWidget(self.browseFolderButton, 0, 0)
        layout.addWidget(self.listWidget, 1, 0, 1, 2)
        layout.addWidget(self.watchCheck, 2, 0)

        self.watchCheck.toggled.connect(self.toggleWatch)
        self.browseFolderButton.clicked.connect(self.browse)
        self.listWidget.itemClicked.connect(self.showMetadata)
        self.execution = False
        self.toExecute = []
        self.current = []
        self.watcher = []

    def updateFileList(self):
        self.path = self.folderEdit.text()
        res = []
        for file in os.listdir(self.path):
            if file.endswith('zarr'):
                res.append(file)

        self.listWidget.clear()
        self.listWidget.addItems(res)

    def browse(self, path=None):
        if not path:
            path = askForFolderPath(self, defaultFolder=self.path)
        if path:
            self.path = path
            self.folderEdit.setText(self.path)
            self.updateFileList()
            self.watchCheck.setChecked(False)

    def showMetadata(self, item):
        metadata = self.getMetadata(item.text())
        self.window = ViewTree(metadata)
        self.window.show()

    def getMetadata(self, fileName):
        path = self.path + '/' + fileName
        store = parse_url(path, mode="r").store
        root = zarr.group(store=store)
        return root.attrs['ImSwitchData']

    def toggleWatch(self, checked):
        if checked:
            self.watcher = FileWatcher(self.path, 'zarr', 1)
            self.updateFileList()
            files = self.watcher.filesInDirectory()
            self.toExecute = files
            self.watcher.sigNewFiles.connect(self.newFiles)
            self.watcher.start()
            self.runNextFiles()
        else:
            self.watcher.stop()
            self.watcher.quit()
            self.toExecute = []

    def newFiles(self, files):
        self.updateFileList()
        self.toExecute.extend(files)
        self.runNextFiles()

    def runNextFiles(self):
        while len(self.toExecute) and not self.execution:
            self.execution = True
            name = self.toExecute.pop()
            self.current = self.path + '/' + name
            reader = Reader(parse_url(self.current))
            nodes = list(reader())
            image_node = nodes[0]
            dask_data = image_node.data
            self.watcher.addToLog(self.current, str(datetime.now()))
            self._viewer.add_image(dask_data, channel_axis=0, name=name)
            self.updateFileList()
        self.execution = False


class ViewTree(QTreeWidget):
    def __init__(self, value) -> None:
        super().__init__()
        self.fill_item(self.invisibleRootItem(), value)

    @staticmethod
    def fill_item(item: QTreeWidgetItem, value) -> None:
        if value is None:
            return
        elif isinstance(value, dict):
            for key, val in sorted(value.items()):
                ViewTree.new_item(item, str(key), val)
        elif isinstance(value, (list, tuple)):
            for val in value:
                if isinstance(val, (str, int, float)):
                    ViewTree.new_item(item, str(val))
                else:
                    ViewTree.new_item(item, f"[{type(val).__name__}]", val)
        else:
            ViewTree.new_item(item, str(value))

    @staticmethod
    def new_item(parent: QTreeWidgetItem, text:str, val=None) -> None:
        child = QTreeWidgetItem([text])
        ViewTree.fill_item(child, val)
        parent.addChild(child)
        child.setExpanded(False)