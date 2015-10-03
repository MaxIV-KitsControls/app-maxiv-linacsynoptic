import os

from taurus.external.qt import Qt

from svgsynoptic.taurussynopticwidget import TaurusSynopticWidget
from panels import get_panel


class LinacSynopticWidget(TaurusSynopticWidget):

    def get_device_panel(self, device):
        return get_panel(device)


def main():
    qapp = Qt.QApplication([])
    widget = LinacSynopticWidget()

    # We need to give the absolute path to the HTML file
    # because our webview is setup to load assets from the
    # svgsynoptic library's path, not from the module's path.
    path = os.path.dirname(__file__)
    widget.setModel(os.path.join(path, "resources/index.html"))

    widget.show()
    qapp.exec_()


if __name__ == "__main__":
    main()
