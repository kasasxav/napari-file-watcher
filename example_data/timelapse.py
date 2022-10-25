import time
import numpy as np

mainWindow.setCurrentModule('imcontrol')

N = 10
positionerName = "Stage"
x = 100
y = 150
z = 0.5

api.imcontrol.movePositioner(positionerName, "X", x)
api.imcontrol.movePositioner(positionerName, "Y", y)
api.imcontrol.movePositioner(positionerName, "Z", z)

for i in range(N):
    api.imcontrol.startRecording()
    waitForRecordingToEnd = getWaitForSignal(api.imcontrol.signals().recordingEnded)
    waitForRecordingToEnd()
    time.sleep(1)





    