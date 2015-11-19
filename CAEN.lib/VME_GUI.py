# from PySide import QtCore, QtGui, QtDeclarative
from PySide.QtDeclarative import QDeclarativeView
from PySide.QtCore import QUrl, Signal#, QThread
from PySide import QtGui
import sys
from threading import Thread, Event
import Pyro4


class Graph(QDeclarativeView):
    """docstring for Graph"""

    def __init__(self, oper_uri):
        self.oper_uri = oper_uri
        self.oper = Pyro4.Proxy(oper_uri)

        self.app = QtGui.QApplication(sys.argv)
        QDeclarativeView.__init__(self)
        self.setWindowTitle("DAQ Window")
        self.setSource(QUrl.fromLocalFile('view.qml'))
        # adapt to the given window size:
        self.setResizeMode(QDeclarativeView.SizeRootObjectToView)

        self.root = self.rootObject()
        # connecting signals:

        # when ready, thread out the demon to the graph object:
        daemon = Pyro4.Daemon()
        self.uri = daemon.register(self)
        print(self.uri)

        thread = Thread(target=daemon.requestLoop, args=())
        thread.daemon = True                      # Daemonize thread
        thread.start()                            # Start the execution

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
    g = Graph(uri_oper)

    # pass g.uri back to the oper
    print("Finishing connection setup to the VME operator..")
    g.oper.add_listener(g.uri)

    print("Everything should be ready. Rolling the graphics!")
    # run graph in the main thread
    sys.exit(g.run())
