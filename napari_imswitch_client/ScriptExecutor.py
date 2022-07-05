import Pyro5.api
from napari_imswitch_client._serialize import register_serializers


class ScriptExecutor:
    """ Handles execution and state of scripts. """

    def __init__(self):
        super().__init__()

    def setServer(self, host, port):
        self._uri = 'PYRO:ImSwitchServer' + '@' + host + ':' + port
        register_serializers()
        self._imswitchServer = Pyro5.api.Proxy(self._uri)

    def execute(self, code):
        self._imswitchServer.runScript(code)
        executing = True
        while executing:
            executing = self._imswitchServer.isExecuting()
        try:
            return self._imswitchServer.getOutput()
        except ValueError:
            pass
