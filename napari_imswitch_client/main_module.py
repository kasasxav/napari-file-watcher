import os
from qtpy.QtWidgets import QWidget
from PyQt5 import Qsci
from qtpy import QtGui, QtWidgets
from napari_imswitch_client.guitools.BetterPushButton import BetterPushButton
from napari_imswitch_client.guitools.dialogtools import askForFolderPath, askForFilePath
from napari_imswitch_client.FileWatcher import FileWatcher
from PIL import Image
import numpy as np


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

    def browse(self):
        path = askForFolderPath(self, defaultFolder=self.path)
        if path:
            self.path = path
            self.folderEdit.setText(self.path)

    def add(self):
        text = self.scintilla.text()
        file = open(self.path + '\\' + self.nameEdit.text() + '.py', 'w')
        file.write(text)
        file.close()

    def open(self):
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

        self.execution = False
        self.toExecute = []
        self.current = []
        self.watcher = []

    def updateFileList(self):
        res = []
        for file in os.listdir(self.path):
            if file.endswith('tiff'):
                res.append(file)

        self.listWidget.clear()
        self.listWidget.addItems(res)

    def browse(self):
        path = askForFolderPath(self, defaultFolder=self.path)
        if path:
            self.path = path
            self.folderEdit.setText(self.path)
            self.updateFileList()

    def toggleWatch(self, checked):
        if checked:
            self.watcher = FileWatcher(self.path, 'tiff', 1)
            files = self.watcher.filesInDirectory()
            self.toExecute = files
            self.watcher.sigNewFiles.connect(self.newFiles)
            self.watcher.start()
            self.runNextFile()
        else:
            self.watcher.stop()
            self.watcher.quit()
            self.toExecute = []

    def newFiles(self, files):
        self.updateFileList()
        self.toExecute.extend(files)
        self.runNextFile()

    def runNextFile(self):
        if len(self.toExecute) and not self.execution:
            self.current = self.path + '\\' + self.toExecute.pop()
            im = np.array(Image.open(self.current))
            self._viewer.add_image(im)
            self.execution = False
            #os.remove(self.current)
            self.updateFileList()
            self.runNextFile()

