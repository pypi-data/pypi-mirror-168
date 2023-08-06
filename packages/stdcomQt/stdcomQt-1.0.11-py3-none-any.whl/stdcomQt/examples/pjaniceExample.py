import sys, re
import argparse


try:
    from PyQt5.QtSvg import QSvgWidget
except ImportError:
    QSvgWidget = None


from stdcomQtPjanice import *

if __name__ == "__main__":
    """
    bumped version
    """

    my_parser = argparse.ArgumentParser( description= "Version " + stdcomQtVersion + " Stec Pjanice Python Version")
    # Add the arguments
    my_parser.add_argument('-p','--project', metavar='project', required=False)

    args = my_parser.parse_args()
    nextProject = args.project
    app = QApplication(sys.argv)

    window = pjanicesimpleGeneric()
    cBridge = window.getcBridge()
    window.setWindowTitle("Stec PJanice Viewer")
    window.show()  # IMPORTANT!!!!! Windows are hidden by default.

    # Start the event loop.
    app.exec_()

    if cBridge != None:
        cBridge.quit()
