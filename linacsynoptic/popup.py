from taurus.qt.qtgui.container import TaurusWidget
from taurus.external.qt import Qt, QtGui, QtCore
from taurus.qt.qtgui.button import TaurusCommandButton
from taurus.qt.qtgui.display import TaurusLabel
import taurus


class CommandsWidget(TaurusWidget):
    """
    Simple widget that shows a number of Command buttons.
    """
    def __init__(self, parent = None, commands=None):
        TaurusWidget.__init__(self, parent)
        self.commands = commands
        self.buttons = {}
        self.setupUi()

    def setupUi(self):
        w = TaurusWidget()
        self.setLayout(Qt.QHBoxLayout())
        self.layout().addWidget(w)

        self.modelLabel = QtGui.QLabel(w)
        self.layout().addWidget(self.modelLabel)

        self.stateLabel = TaurusLabel(w)
        self.stateLabel.setBgRole("State")
        self.stateLabel.setFgRole("State")
        self.layout().addWidget(self.stateLabel)

        for command, _ in self.commands:
            button = TaurusCommandButton(w, command=command)
            self.layout().addWidget(button)
            self.buttons[command] = button

        #self.initButton.hide() # Only used in popup

    def setModel(self,model):
        TaurusWidget.setModel(self, model)
        self.setWindowTitle(str(model))
        self.modelLabel.setText(str(model))
        self.stateLabel.setModel(str(model))
        for button in self.buttons.values():
            button.setModel(str(model))


class CommandsWidgetPopup(CommandsWidget):
    """
    Popup variant of CommandsWidget.
    It moves to mouse on start and it closes on unfocus or after successful command.
    On show it hides irrelevant buttons.
    It also closes automatically after 10 seconds.
    """
    def __init__(self, parent = None):
        CommandsWidget.__init__(self, parent, self.commands)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.installEventFilter(self)
        for button in self.buttons.values():
            button.clicked.connect(self.close)

    def eventFilter(self, object, event):
        """
        Event filter to close if no focus
        """
        if event.type()== QtCore.QEvent.WindowDeactivate:
            self.close()
        return TaurusWidget.eventFilter(self, object, event)

    def show(self):
        TaurusWidget.show(self)
        self.showhidebuttons()
        self.move_to_mouse()
        QtCore.QTimer.singleShot(10000, lambda: self.close())

    def showhidebuttons(self):
        dev = taurus.Device(self.model)
        for command, state in self.commands:
            button = self.buttons[command]
            print command, dev.State, button
            if dev.State() == state:
                button.hide()
            else:
                button.show()
        self.adjustSize()

    def move_to_mouse(self):
        """
        Moves the window to the mouse cursor
        """
        try:
            pos = QtGui.QCursor.pos()
            self.move(pos.x()-4*(self.width()/5), pos.y()-(self.height()/2))
        except:
            pass


def main():
    from taurus.qt.qtgui.application import TaurusApplication
    from PyTango import DevState
    import sys

    app = TaurusApplication(sys.argv)
    args = app.get_command_line_args()

    class OnOffPopup(CommandsWidgetPopup):
        commands = ("On", DevState.ON), ("Off", DevState.OFF)

    w = OnOffPopup()
    w.setModel(args[0])
    app.setCursorFlashTime(0)

    w.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

