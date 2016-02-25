import os

from taurus.qt.qtgui.application import TaurusApplication
from svgsynoptic2.taurussynopticwidget import TaurusSynopticWidget

from panels import get_panel


class LinacSynopticWidget(TaurusSynopticWidget):

    def get_device_panel(self, device):
        return get_panel(device)


def main():

    app = TaurusApplication()
    widget = LinacSynopticWidget()

    # We'd like the synoptic to "select" the relevant item when
    # the user focuses on a panel. Let's connect a handler to
    # the focusChanged signal that does this.
    def onFocus(old, new):
        if new and hasattr(new, "window"):
            for device, panel in widget._panels.items():
                if panel == new.window():
                    widget.select("model", [device])

    app.focusChanged.connect(onFocus)

    # We need to give the absolute path to the HTML file
    # because our webview is setup to load assets from the
    # svgsynoptic library's path, not from the module's path.
    path = os.path.dirname(__file__)
    widget.setModel(os.path.join(path, "resources/index.html"))

    widget.show()
    app.exec_()


if __name__ == "__main__":
    main()
