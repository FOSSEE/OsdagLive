'''
Created on 16-Jun-2015

@author: deepa
'''
import sys
from PyQt4 import QtGui,QtCore
from ui_osdagpage import Ui_MainWindow

class OsdagMainWindow(QtGui.QMainWindow):
    

    
    
    
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.ui.myListWidget.currentItemChanged.connect(self.changePage)
        self.ui.myListWidget.setCurrentRow(0)
        
    def changePage(self, current, previous):
        if not current:
            current = previous

        self.ui.myStackedWidget.setCurrentIndex(self.ui.myListWidget.row(current))

    
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = OsdagMainWindow()
    window.show()
    sys.exit(app.exec_())