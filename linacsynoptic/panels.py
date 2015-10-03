from subprocess import Popen

from PyTango import Database
from taurus.qt.qtgui.panel import TaurusDevicePanel

# various widgets for specific devices
from magnetpanel import MagnetPanel
from maxwidgets.panel import MotorPresets, TaurusFormExpanding
from tgconf_beamviewer import panels

db = Database()

CLASS_PANELS = {
    "Magnet": MagnetPanel,
    "IORegister": MotorPresets,
    "Motor": TaurusFormExpanding
}


def get_panel(device):
    "Return an appropriate panel for the given device"
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
