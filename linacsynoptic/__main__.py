import os

from taurus.external.qt import Qt

from svgsynoptic.taurussynopticwidget import TaurusSynopticWidget


def main():
    qapp = Qt.QApplication([])
    sw = TaurusSynopticWidget()

    # We need to give the absolute path to the HTML file
    # because our webview is setup to load assets from the
    # svgsynoptic library's path.
    path = os.path.dirname(__file__)
    sw.setModel(os.path.join(path, "resources/index.html"))

    sw.show()
    qapp.exec_()


if __name__ == "__main__":
    main()
