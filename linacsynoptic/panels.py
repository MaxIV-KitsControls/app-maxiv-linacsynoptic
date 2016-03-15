from subprocess import Popen

from PyTango import Database, DevState
from taurus.qt.qtgui.panel import TaurusDevicePanel

# various widgets for specific devices
from magnetpanel import MagnetPanel
from maxwidgets.panel import MotorPresets
from tgconf_beamviewer import panels

from popup import CommandsWidgetPopup


class ValvePopup(CommandsWidgetPopup):
    "Quick open/close for vacuum valves"
    commands = ("Open", DevState.OPEN), ("Close", DevState.CLOSE)

class ScreenPopup(CommandsWidgetPopup):
    "Quick movements for camera screens"
    commands = ("MoveIn", DevState.INSERT), ("MoveOut", DevState.EXTRACT)


CLASS_PANELS = {
    "Magnet": MagnetPanel,
    "IORegister": MotorPresets,
    "VacuumValve": ValvePopup,
    "CameraScreen": ScreenPopup
}


def get_panel(device):
    "Return an appropriate panel for the given device"
    db = Database()
    classname = db.get_class_for_device(device)
    if classname in CLASS_PANELS:
        return CLASS_PANELS[classname]
    if classname == "BeamViewerDeviceServer":
        # beam viewer gets its own process
        camera_process(device)
        return
    return TaurusDevicePanel


def camera_process(cam): 
    """Start a camera gui panel in its own process"""
    # This is a (hopefully) temporary workaround to the Taurus polling problem
    # that tends to slow down the camera UI when there are many listeners.
    print "opening camera %s in subprocess", cam
    Popen(["python", "%s/limabeam.py" % panels.__path__[0], cam])


if __name__ == "__main__":
    import sys
    from taurus.qt.qtgui.application import TaurusApplication
    qapp = TaurusApplication([])
    device = sys.argv[1]
    widget = get_panel(device)()
    widget.setModel(device)
    widget.show()
    qapp.exec_()
