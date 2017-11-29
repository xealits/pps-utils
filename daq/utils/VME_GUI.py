# from PySide import QtCore, QtGui, QtDeclarative
from PySide.QtDeclarative import QDeclarativeView
from PySide.QtCore import QUrl, Signal, QAbstractListModel, Qt #, QThread
from PySide import QtGui
import sys
from threading import Thread, Event
import Pyro4


class Comms(QAbstractListModel):
    """docstring for Comms"""
    NAME = Qt.UserRole + 1
    NUMBER = NAME + 1
    SIGNAL = NUMBER + 1
    # COLUMNS = ('name', 'number')

    def __init__(self, strings = [], parent=None):
        QAbstractListModel.__init__(self, parent)
        # super(Comms, self).__init__()
        self.__strings = strings
        self.setRoleNames({Comms.NAME: 'name', Comms.NUMBER: 'number', Comms.SIGNAL: 'sig'})

    def data(self, index, role):
        # print( index )
        # print( role )
        # if index.isValid():# and role == Comms.COLUMNS.index('thing'):
        # return '5' #self.__strings[index.row()][Comms.COLUMNS.index(role)]
        # if role == Qt.ToolTipRole:
            # return "hovering: " + self.__strings[index.row()][0]

        if role == Comms.NAME:
            return self.__strings[index.row()][0] # Comms.NAME
        elif role == Comms.NUMBER:
            return self.__strings[index.row()][1] # Comms.NUMBER
        elif role == Comms.SIGNAL:
            return self.__strings[index.row()][2]
        else:
            return None
        # return None

    def rowCount(self, parent):
        return len(self.__strings)
        

class Graph(QDeclarativeView):
    """docstring for Graph"""

    # sig = Signal()

    def __init__(self, oper_uri, qml_file_path):
        self.oper_uri = oper_uri
        self.oper = Pyro4.Proxy(oper_uri)
        self.oper._pyroGetMetadata() # refresh the connection
        # TODO: when and how might it fail?

        # self.sig = Signal()

        self.app = QtGui.QApplication(sys.argv)
        QDeclarativeView.__init__(self)

        # self.sig.connect(self.test_sig_from_qml)

        inter = [("asbjd", 12321),
            ("quyriqw", 356),
            ("kherjfn", 667),
            ("kherjfn", 667),
            ("kherjfn", 124),
            ("asdasqw", 612),
            ("asdasqw", 111),
            ("asdasqw", 402),
            ("iuewqqq", 112),
            ("iuewqqq", 100),
            ("iuewqqq", 112),
            ("iuewqqq", 444)]
        # [s.connect(self.test_sig_from_qml) for _, _, s in inter]
        comm_model = Comms(inter)

        # define the context, with the model, before pulling QML with the components
        self.root_context = self.rootContext()
        self.root_context.setContextProperty('PyModel', comm_model)

        self.setWindowTitle("DAQ Window")
        self.setSource(QUrl.fromLocalFile(qml_file_path))
        # adapt to the given window size:
        self.setResizeMode(QDeclarativeView.SizeRootObjectToView)

        self.root = self.rootObject()
        # self.root.setProperty('PyModel', comm_model)
        # connecting signals:

        self.root.command_issue.connect(self.test_sig_from_qml)

        # when ready, thread out the demon to the graph object:
        daemon = Pyro4.Daemon()
        self.uri = daemon.register(self)
        print(self.uri)

        thread = Thread(target=daemon.requestLoop, args=())
        thread.daemon = True                      # Daemonize thread
        thread.start()                            # Start the execution

    def test_sig_from_qml(self, *args):
        print("test, signal from QML", args)

    def run(self):
        # self.stopped.clear()
        self.show()
        return self.app.exec_() # TODO: how to stop exec_?


if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[1] == "standalone":
        # the 1 argument == standalone
        # the 2 argument is the path to the VME calls library
        print("Starting as standalone with libpath at %s" % sys.argv[2])

        import VME_operator
        v = VME_operator.PreVMEOperator(sys.argv[2])

        dem_oper = Pyro4.Daemon()
        uri_oper = dem_oper.register(v)
        print(uri_oper)

        # spawn a thread with the VME oper within Pyro4 daemon
        # TODO: get the PID of the process (to access niceness)
        thread_oper = Thread(target=dem_oper.requestLoop, args=())
        thread_oper.daemon = True                      # Daemonize thread
        thread_oper.start()                            # Start the execution
    else:
        # TODO: start the GUI and ask for URI in there
        print("Starting as a coprocess, the VME operator process should be running.")
        # get the URI of the running process with VME oper
        # TODO: set according to Python2/3 version:
        # uri_oper = input("Enter the URI of the VME operator process:").strip()
        uri_oper = raw_input("Enter the URI of the VME operator process:").strip()
    # here the VME oper should run in a Pyro4 daemon process/thread on the system
    # and uri_oper should link to the daemon

    # create the graph object
    # it spawns a thread with the Pyro4 daemon sharing access to the object
    print("Creating the GUI object..")
    g = Graph(uri_oper, 'view.qml')

    # pass g.uri back to the oper
    print("Finishing connection setup to the VME operator..")
    g.oper.add_listener(g.uri)

    print("Everything should be ready. Rolling the graphics!")
    # run graph in the main thread
    sys.exit(g.run())

