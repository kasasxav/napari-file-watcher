from qtpy.QtWidgets import QWidget
from PyQt5 import Qsci
from qtpy import QtGui, QtWidgets
from napari_imswitch_client.guitools.BetterPushButton import BetterPushButton
from napari_imswitch_client.ScriptExecutor import ScriptExecutor
from PyQt5.QtWidgets import QLineEdit


class ImScriptingWidget(QWidget):
    def __init__(self, viewer: 'napari.viewer.Viewer'):
        super().__init__()
        self._viewer = viewer
        self._running = False
        self._scriptExecutor = ScriptExecutor()

        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        topContainer = QtWidgets.QHBoxLayout()
        topContainer.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(topContainer, 0)

        topContainer.addSpacerItem(
            QtWidgets.QSpacerItem(
                40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
            )
        )
        self.hostEdit = QLineEdit('127.0.0.1')
        topContainer.addWidget(self.hostEdit, 0)
        self.portEdit = QLineEdit('54333')
        topContainer.addWidget(self.portEdit, 0)
        self.connectButton = BetterPushButton('Connect')
        topContainer.addWidget(self.connectButton, 0)
        self.connectButton.clicked.connect(self._startServer)

        self.scintilla = Scintilla()

        self.runAllButton = BetterPushButton('Run all')
        self.runAllButton.clicked.connect(
            lambda: self._runCurrentCode(self.scintilla.text())
        )
        topContainer.addWidget(self.runAllButton, 1)

        self.runSelectionButton = BetterPushButton('Run selection')
        self.runSelectionButton.clicked.connect(
            lambda: self._runCurrentCode(self.scintilla.selectedText())
        )
        topContainer.addWidget(self.runSelectionButton, 1)

        layout.addWidget(self.scintilla, 3)

    def _startServer(self):
        host = self.hostEdit.text()
        port = self.portEdit.text()
        self._scriptExecutor.setServer(host, port)

    def _runCurrentCode(self, code):
        output = self._scriptExecutor.execute(code)
        if output is not None:
            self._viewer.add_image(output)


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