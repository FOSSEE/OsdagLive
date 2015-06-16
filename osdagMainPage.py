'''
Created on 16-Jun-2015

@author: deepa
'''
import sys
from PyQt4 import QtGui,QtCore
from ui_osdagpage import Ui_MainWindow
from Connections.Shear.Finplate.finPlateMain import launchFinPlateController
#from finPlateMain import *

#from finPlateMain import launchFinPlateController


class OsdagMainWindow(QtGui.QMainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.ui.myListWidget.currentItemChanged.connect(self.changePage)
        self.ui.myListWidget.setCurrentRow(0)
        self.ui.shearBtnStart.clicked.connect(self.showFinPlate)
        
    def changePage(self, current, previous):
        if not current:
            current = previous

        self.ui.myStackedWidget.setCurrentIndex(self.ui.myListWidget.row(current))
    
    def showFinPlate(self):
        
        if self.ui.finPlateRdBtn.isChecked():
            launchFinPlateController(self)
            #QtGui.QMessageBox.about(self,"info","finplate clicked")
        elif self.ui.cleatRdBtn.isChecked():
            QtGui.QMessageBox.about(self,"info","cleat clicked")
        elif self.ui.endPlateRdBtn.isChecked():
            QtGui.QMessageBox.about(self,"info","endplateclicked")
        elif self.ui.seatedRdBtn.isChecked():
            QtGui.QMessageBox.about(self,"info","seated clicked")
        else:
            QtGui.QMessageBox.about(self,"info","Please select desire radio button")
            
        
    

    
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = OsdagMainWindow()
    window.show()
    sys.exit(app.exec_())