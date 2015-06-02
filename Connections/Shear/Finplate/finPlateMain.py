'''
Created on 07-May-2015

@author: deepa
'''
from PyQt4.QtCore import QString
from PyQt4.QtGui import QMessageBox
'''
Created on 21-Aug-2014

@author: deepa
'''
import sys
from OCC import VERSION
#from PyQt4 import QtGui,QtCore
from ui_finPlate import Ui_MainWindow
from model import *
#from finPlateCalc import finConn
from finplate_calc1 import finConn
import yaml
import pickle
import logging 
#from exampleSimpleGUI import init_display
from OCC.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC._Quantity import Quantity_NOC_RED,Quantity_NOC_BLUE1,Quantity_NOC_SADDLEBROWN
from ISection import ISection
import numpy
from OCC.Graphic3d import Graphic3d_NOT_2D_ALUMINUM
from weld import  Weld
from plate import Plate
from bolt import Bolt
from nut import Nut 
import os.path
from utilities import osdagDisplayShape
from OCC.Display.pyqt4Display import qtViewer3d
from colWebBeamWebConnectivity import ColWebBeamWeb
from colFlangeBeamWebConnectivity import ColFlangeBeamWeb
from OCC import IGESControl

from filletweld import FilletWeld


class MainController(QtGui.QMainWindow):
    
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.inputDock.setFixedSize(310,710)
        
        self.gradeType ={'Please Select Type':'',
                         'HSFG': [8.8,10.8],
                         'Black Bolt':[3.6,4.6,4.8,5.6,5.8,6.8,9.8,12.9]}
        self.ui.comboType.addItems(self.gradeType.keys())
        self.ui.comboType.currentIndexChanged[str].connect(self.combotype_currentindexchanged)
        self.ui.comboType.setCurrentIndex(0)
        
        self.ui.comboConnLoc.currentIndexChanged[str].connect(self.setimage_connection)
        
        
        self.ui.btn_Reset.clicked.connect(self.resetbtn_clicked)
        
        self.ui.btn_Design.clicked.connect(self.design_btnclicked)
        
        self.ui.btnInput.clicked.connect(lambda: self.dockbtn_clicked(self.ui.inputDock))
        self.ui.btnOutput.clicked.connect(lambda: self.dockbtn_clicked(self.ui.outputDock))
        self.ui.btn_front.clicked.connect(self.call_Frontview)
        self.ui.btn_top.clicked.connect(self.call_Topview)
        self.ui.btn_side.clicked.connect(self.call_Sideview)
        
        self.ui.btn3D.clicked.connect(self.call_3DModel)
        self.ui.chkBxBeam.clicked.connect(self.call_3DBeam)
        self.ui.chkBxCol.clicked.connect(self.call_3DColumn)
        self.ui.chkBxFinplate.clicked.connect(self.call_3DFinplate)
        
        validator = QtGui.QIntValidator()
        self.ui.txtFu.setValidator(validator)
        self.ui.txtFy.setValidator(validator)
        
        dbl_validator = QtGui.QDoubleValidator()
        self.ui.txtPlateLen.setValidator(dbl_validator)
        self.ui.txtPlateLen.setMaxLength(7)
        self.ui.txtPlateWidth.setValidator(dbl_validator)
        self.ui.txtPlateWidth.setMaxLength(7)
        self.ui.txtShear.setValidator(dbl_validator)
        self.ui.txtShear.setMaxLength(7)
        
        minfuVal = 290
        maxfuVal = 590
        self.ui.txtFu.editingFinished.connect(lambda: self.check_range(self.ui.txtFu,self.ui.lbl_fu, minfuVal, maxfuVal))
        
        minfyVal = 165
        maxfyVal = 450
        self.ui.txtFy.editingFinished.connect(lambda: self.check_range(self.ui.txtFy,self.ui.lbl_fy, minfyVal, maxfyVal))
       
        self.ui.combo_Beam.addItems(get_beamcombolist())
        self.ui.comboColSec.addItems(get_columncombolist())
        self.ui.menuView.addAction(self.ui.inputDock.toggleViewAction())
        self.ui.menuView.addAction(self.ui.outputDock.toggleViewAction())
        self.ui.btn_CreateDesign.clicked.connect(self.save_design)
        #self.ui.btn_Saveoutput.clicked.connect(self.save_design)
        self.ui.btn_SaveMessages.clicked.connect(self.save_log)
        #self.ui.btn_Savelog.clicked.connect(self.save_log)
        

        # Saving and Restoring the finPlate window state.
        self.retrieve_prevstate()
        
        # Initialising the qtviewer
        self.display,_ = self.init_display(backend_str="pyqt4")
        
        self.ui.btnSvgSave.clicked.connect(self.save3DtoIGES)
        #self.ui.btnSvgSave.clicked.connect(lambda:self.saveTopng(self.display))
        

    def saveTopng(self,display):
        display.ExportToImage('/home/Pictures/cad.png')
    
    def retrieve_prevstate(self):
        uiObj = self.get_prevstate()
        if(uiObj != None):
            
            self.ui.combo_Beam.setCurrentIndex(self.ui.combo_Beam.findText(uiObj['Member']['beamSection']))
            self.ui.comboColSec.setCurrentIndex(self.ui.comboColSec.findText(uiObj['Member']['columSection']))
            
            self.ui.txtFu.setText(str(uiObj['Member']['fu(MPa)']))
            self.ui.txtFy.setText(str(uiObj['Member']['fy(MPa)']))
           
            self.ui.comboConnLoc.setCurrentIndex(self.ui.comboConnLoc.findText(str(uiObj['Member']['connectivity'])))
            
            self.ui.txtShear.setText(str(uiObj['Load']['shearForce(kN)']))
            
            self.ui.comboDaimeter.setCurrentIndex(self.ui.comboDaimeter.findText(str(uiObj['Bolt']['diameter(mm)'])))
            comboTypeIndex = self.ui.comboType.findText(str(uiObj['Bolt']['type']))
            self.ui.comboType.setCurrentIndex(comboTypeIndex)
            self.combotype_currentindexchanged(str(uiObj['Bolt']['type']))
            
            prevValue = str(uiObj['Bolt']['grade'])
        
            comboGradeIndex = self.ui.comboGrade.findText(prevValue)
          
            self.ui.comboGrade.setCurrentIndex(comboGradeIndex)
        
            #self.ui.comboDaimeter.currentText(str(uiObj['Bolt']['diameter(mm)']))
            #self.ui.comboType.currentText(str(uiObj['Bolt']['diameter(mm)']))
            #self.ui.comboGrade.currentText(str(uiObj['Bolt']['grade']))
            
            self.ui.comboPlateThick_2.setCurrentIndex(self.ui.comboPlateThick_2.findText(str(uiObj['Plate']['thickness(mm)'])))
            #self.ui.comboPlateThick_2.currentText(str(uiObj['Plate']['thickness(mm)']))
            self.ui.txtPlateLen.setText(str(uiObj['Plate']['length(mm)']))
            self.ui.txtPlateWidth.setText(str(uiObj['Plate']['width(mm)']))
            
            self.ui.comboWldSize.setCurrentIndex(self.ui.comboWldSize.findText(str(uiObj['Weld']['size(mm)'])))
            #self.ui.comboWldSize.currentText(str(uiObj['Weld']['size(mm)']))
        #else:
        #    self.btnreset_clicked() 
        
    def setimage_connection(self):
        '''
        Setting image to connctivity.
        '''
        self.ui.lbl_connectivity.show()
        loc = self.ui.comboConnLoc.currentText()
        if loc == "Column flange-Beam web":
            
            pixmap = QtGui.QPixmap(":/newPrefix/images/beam2.jpg")
            pixmap.scaledToHeight(50)
            pixmap.scaledToWidth(60)
            self.ui.lbl_connectivity.setPixmap(pixmap)
            #self.ui.lbl_connectivity.show()
        elif(loc == "Column web-Beam web"):
            picmap = QtGui.QPixmap(":/newPrefix/images/beam.jpg")
            picmap.scaledToHeight(50)
            picmap.scaledToWidth(60)
            self.ui.lbl_connectivity.setPixmap(picmap)
        else:
            self.ui.lbl_connectivity.hide()
            
        
    def getuser_inputs(self):
        '''(nothing) -> Dictionary
        
        Returns the dictionary object with the user input fields for designing fin plate connection
        
        '''
        uiObj = {}
        uiObj["Bolt"] = {}
        uiObj["Bolt"]["diameter(mm)"] = self.ui.comboDaimeter.currentText().toInt()[0]
        uiObj["Bolt"]["grade"] = float(self.ui.comboGrade.currentText())                                                                                                                                                                                                                                                             
        uiObj["Bolt"]["type"] = str(self.ui.comboType.currentText())
        
            
        uiObj["Weld"] = {}
        uiObj["Weld"]['size(mm)'] = self.ui.comboWldSize.currentText().toInt()[0]
        
        uiObj['Member'] = {}
        uiObj['Member']['beamSection'] = str(self.ui.combo_Beam.currentText())
        uiObj['Member']['columSection'] = str(self.ui.comboColSec.currentText())
        uiObj['Member']['connectivity'] = str(self.ui.comboConnLoc.currentText())
        uiObj['Member']['fu(MPa)'] = self.ui.txtFu.text().toInt()[0]
        uiObj['Member']['fy(MPa)'] = self.ui.txtFy.text().toInt()[0]
        
        uiObj['Plate'] = {}
        uiObj['Plate']['thickness(mm)'] = self.ui.comboPlateThick_2.currentText().toInt()[0]
        uiObj['Plate']['height(mm)'] = self.ui.txtPlateLen.text().toInt()[0] # changes the label length to height 
        uiObj['Plate']['width(mm)'] = self.ui.txtPlateWidth.text().toInt()[0]
        
        uiObj['Load'] = {}
        uiObj['Load']['shearForce(kN)'] = self.ui.txtShear.text().toInt()[0]
        
        
        return uiObj    
    
    def save_inputs(self,uiObj):
         
        '''(Dictionary)--> None
         
        '''
        inputFile = QtCore.QFile('saveINPUT.txt')
        if not inputFile.open(QtCore.QFile.WriteOnly | QtCore.QFile.Text):
            QtGui.QMessageBox.warning(self, "Application",
                    "Cannot write file %s:\n%s." % (inputFile, file.errorString()))
        #yaml.dump(uiObj, inputFile,allow_unicode=True, default_flow_style = False)
        pickle.dump(uiObj, inputFile)
        
    
    def get_prevstate(self):
        '''
        '''
        fileName = 'saveINPUT.txt'
         
        if os.path.isfile(fileName):
            fileObject = open(fileName,'r')
            uiObj = pickle.load(fileObject)
            return uiObj
        else:
            return None
    
            
    def outputdict(self):
        
        ''' Returns the output of design in dictionary object.
        '''
        outObj = {}
        outObj['Plate'] ={}
        #outObj['Plate']["Thickness(mm)"] = float(self.ui.txtPlateThick.text())
        outObj['Plate']["External Moment(kNm)"] = float(self.ui.txtExtMomnt.text())
        outObj['Plate']["Moment Capacity(kNm)"] = float(self.ui.txtMomntCapacity.text())
        
        outObj['Weld'] ={}
        #outObj['Weld']["Weld Thickness(mm)"] = float(self.ui.txtWeldThick.text())
        outObj['Weld']["Resultant Shear(kN/mm)"] = float(self.ui.txtResltShr.text())
        outObj['Weld']["Weld Strength(kN/mm)"] = float(self.ui.txtWeldStrng.text())
        
        outObj['Bolt'] = {}
        outObj['Bolt']["Shear Capacity(kN)"] = float(self.ui.txtShrCapacity.text())
        outObj['Bolt']["Bearing Capacity(kN)"] = float(self.ui.txtbearCapacity.text())
        outObj['Bolt']["Capacity Of Bolt(kN)"] = float(self.ui.txtBoltCapacity.text())
        outObj['Bolt']["No Of Bolts"] = float(self.ui.txtNoBolts.text())
        outObj['Bolt']["No.Of Row"] = int(self.ui.txt_row.text())
        outObj['Bolt']["No.Of Column"] = int(self.ui.txt_col.text())
        outObj['Bolt']["Pitch Distance(mm)"] = float(self.ui.txtPitch.text())
        outObj['Bolt']["Guage Distance(mm)"] = float(self.ui.txtGuage.text())
        outObj['Bolt']["End Distance(mm)"]= float(self.ui.txtEndDist.text())
        outObj['Bolt']["Edge Distance(mm)"]= float(self.ui.txtEdgeDist.text())
        
        return outObj
    
    
    def save_design(self):
        self.outdict = self.outputdict()
        self.inputdict = self.getuser_inputs()
        self.save_yaml(self.outdict,self.inputdict)
    
        #self.save(self.outdict,self.inputdict)
        
    def save_log(self):
        
        fileName,pat =QtGui.QFileDialog.getSaveFileNameAndFilter(self,"Save File As","/home/deepa/SaveMessages","Text files (*.txt)")
        return self.save_file(fileName+".txt")
          
    def save_file(self, fileName):
        '''(file open for writing)-> boolean
        '''
        fname = QtCore.QFile(fileName)
        if not fname.open(QtCore.QFile.WriteOnly | QtCore.QFile.Text):
            QtGui.QMessageBox.warning(self, "Application",
                    "Cannot write file %s:\n%s." % (fileName, fname.errorString()))
            return False

        outf = QtCore.QTextStream(fname)
        QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        outf << self.ui.textEdit.toPlainText()
        QtGui.QApplication.restoreOverrideCursor()

        #self.setCurrentFile(fileName);
        QtGui.QMessageBox.about(self,'Information',"File saved")
        return True
    
    
    def save_yaml(self,outObj,uiObj):
        '''(dictiionary,dictionary) -> NoneType
        Saving input and output to file in following format.
        Bolt:
          diameter: 6
          grade: 8.800000190734863
          type: HSFG
        Load:
          shearForce: 100
          
        '''
        newDict = {"INPUT": uiObj, "OUTPUT": outObj} 
        fileName = QtGui.QFileDialog.getSaveFileName(self,"Save File As","/home/deepa/SaveDesign","Text File (*.txt)")
        f = open(fileName,'w')
        yaml.dump(newDict,f,allow_unicode=True, default_flow_style=False)
        return self.save_file(fileName+".txt")

        
    def resetbtn_clicked(self):
        '''(NoneType) -> NoneType
        
        Resets all fields in input as well as output window
    
        '''
        # user Inputs
        self.ui.combo_Beam.setCurrentIndex((0))
        self.ui.comboColSec.setCurrentIndex((0))
        self.ui.comboConnLoc.setCurrentIndex((0))
        self.ui.txtFu.clear()
        self.ui.txtFy.clear()
        
        self.ui.txtShear.clear()
        
        self.ui.comboDaimeter.setCurrentIndex(0)
        self.ui.comboType.setCurrentIndex((0))
        self.ui.comboGrade.setCurrentIndex((0))
        
        self.ui.comboPlateThick_2.setCurrentIndex((0))
        self.ui.txtPlateLen.clear()
        self.ui.txtPlateWidth.clear()
        
        self.ui.comboWldSize.setCurrentIndex((0))
        
        #----Output
        self.ui.txtShrCapacity.clear()
        self.ui.txtbearCapacity.clear()
        self.ui.txtBoltCapacity.clear()
        self.ui.txtNoBolts.clear()
        self.ui.txtboltgrpcapacity.clear()
        self.ui.txt_row.clear()
        self.ui.txt_col.clear()
        self.ui.txtPitch.clear()
        self.ui.txtGuage.clear()
        self.ui.txtEndDist.clear()
        self.ui.txtEdgeDist.clear()
        
        #self.ui.txtPlateThick.clear()
        self.ui.txtplate_ht.clear()
        self.ui.txtplate_width.clear()
        self.ui.txtExtMomnt.clear()
        self.ui.txtMomntCapacity.clear()
        
        #self.ui.txtWeldThick.clear()
        self.ui.txtResltShr.clear()
        self.ui.txtWeldStrng.clear()
        self.ui.textEdit.clear()
        
    def dockbtn_clicked(self,widget):
        
        '''(QWidget) -> NoneType
        
        This method dock and undock widget(QdockWidget)
        '''
        
        flag = widget.isHidden()
        if(flag):
            
            widget.show()
        else:
            widget.hide()
            
    def  combotype_currentindexchanged(self,index):
        
        '''(Number) -> NoneType
        '''
        items = self.gradeType[str(index)]

        self.ui.comboGrade.clear()
        strItems = []
        for val in items:
            strItems.append(str(val))
            
        self.ui.comboGrade.addItems(strItems)
        
        
    def check_range(self, widget,lblwidget, minVal, maxVal):
        
        '''(QlineEdit,QLable,Number,Number)---> NoneType
        Validating F_u(ultimate Strength) and F_y (Yeild Strength) textfields
        '''
        textStr = widget.text()
        val = int(textStr) 
        if( val < minVal or val > maxVal):
            QtGui.QMessageBox.about(self,'Error','Please Enter a value between %s-%s' %(minVal, maxVal))
            widget.clear()
            widget.setFocus()
            palette = QtGui.QPalette()
            palette.setColor(QtGui.QPalette.Foreground,QtCore.Qt.red)
            lblwidget.setPalette(palette)
        else:
            palette = QtGui.QPalette()
            lblwidget.setPalette(palette)
            
    def display_output(self, resultObj):
        
        '''(dictionary) --> NoneType
        
        Setting design result values to the respective textboxes in the output window
        
        '''
        # resultObj['Bolt']
        shear_capacity = resultObj['Bolt']['shearcapacity']
        self.ui.txtShrCapacity.setText(str(shear_capacity))
        
        bearing_capacity = resultObj['Bolt']['bearingcapacity']
        self.ui.txtbearCapacity.setText(str(bearing_capacity))
        
        bolt_capacity = resultObj['Bolt']['boltcapacity']
        self.ui.txtBoltCapacity.setText(str(bolt_capacity))
        
        no_ofbolts = resultObj['Bolt']['numofbolts']
        self.ui.txtNoBolts.setText(str(no_ofbolts))
        #newly added field
        boltGrp_capacity = resultObj['Bolt']['boltgrpcapacity']
        self.ui.txtboltgrpcapacity.setText(str(boltGrp_capacity))
        
        no_ofrows = resultObj['Bolt']['numofrow']
        self.ui.txt_row.setText(str(no_ofrows))
        
        no_ofcol = resultObj['Bolt']['numofcol']
        self.ui.txt_col.setText(str(no_ofcol))
        
        pitch_dist = resultObj['Bolt']['pitch']
        self.ui.txtPitch.setText(str(pitch_dist))
        
        gauge_dist = resultObj['Bolt']['gauge']
        self.ui.txtGuage.setText(str(gauge_dist))
        
        end_dist = resultObj['Bolt']['enddist']
        self.ui.txtEndDist.setText(str(end_dist))
        
        edge_dist = resultObj['Bolt']['edge']
        self.ui.txtEdgeDist.setText(str(edge_dist))
        
        # resultObj['Weld']
        # weld_thickness = resultObj['Weld']['thickness']
        # self.ui.txtWeldThick.setText(str(weld_thickness))
        
        resultant_shear = resultObj['Weld']['resultantshear']
        self.ui.txtResltShr.setText(str(resultant_shear))
        
        weld_strength = resultObj['Weld']['weldstrength']
        self.ui.txtWeldStrng.setText(str(weld_strength))
         
        
        # Newly included fields
        plate_ht = resultObj['Plate']['height'] 
        self.ui.txtplate_ht.setText(str(plate_ht))
        
        plate_width = resultObj['Plate']['width'] 
        self.ui.txtplate_width.setText(str(plate_width))
        
        moment_demand = resultObj['Plate']['externalmoment']
        self.ui.txtExtMomnt.setText(str(moment_demand))
        
        moment_capacity =  resultObj['Plate']['momentcapacity']
        self.ui.txtMomntCapacity.setText(str(moment_capacity))
        
   
    def displaylog_totextedit(self):
        '''
        This method displaying Design messages(log messages)to textedit widget.
        '''
        
        afile = QtCore.QFile('fin.log')
        
        if not afile.open(QtCore.QIODevice.ReadOnly):#ReadOnly
            QtGui.QMessageBox.information(None, 'info', afile.errorString())
        
        stream = QtCore.QTextStream(afile)
        #self.ui.textEdit.setFocus()
        self.ui.textEdit.clear()
        self.ui.textEdit.setHtml(stream.readAll())
        
        afile.close()
        
        
    def get_backend(self):
        """
        loads a backend
        backends are loaded in order of preference
        since python comes with Tk included, but that PySide or PyQt4
        is much preferred
        """
        try:
            from PySide import QtCore, QtGui
            return 'pyside'
        except:
            pass
        try:
            from PyQt4 import QtCore, QtGui
            return 'pyqt4'
        except:
            pass
        # Check wxPython
        try:
            import wx
            return 'wx'
        except:
            raise ImportError("No compliant GUI library found. You must have either PySide, PyQt4 or wxPython installed.")
            sys.exit(1)
        
    # QtViewer
    def init_display(self,backend_str=None, size=(1024, 768)):
        
        global display, start_display, app, _, USED_BACKEND
    
        if not backend_str:
            USED_BACKEND = self.get_backend()
        elif backend_str in [ 'pyside', 'pyqt4']:
            USED_BACKEND = backend_str
        else:
            raise ValueError("You should pass either 'qt' or 'tkinter' to the init_display function.")
            sys.exit(1)
    
        # Qt based simple GUI
        if USED_BACKEND in ['pyqt4', 'pyside']:
            if USED_BACKEND == 'pyqt4':
                from PyQt4 import QtCore, QtGui, QtOpenGL
                from OCC.Display.pyqt4Display import qtViewer3d
            elif USED_BACKEND == 'pyside':
                from PySide import QtCore, QtGui, QtOpenGL
                from OCC.Display.pysideDisplay import qtViewer3d
    
        self.ui.modelTab = qtViewer3d(self)
        self.setWindowTitle("Osdag-%s 3d viewer ('%s' backend)" % (VERSION, USED_BACKEND))
        self.ui.mytabWidget.resize(size[0], size[1])
        self.ui.mytabWidget.addTab(self.ui.modelTab,"")
        
        #self.ui.mytabWidget.setCentralWidget(self.ui.modelTab)
        #self.ui.mytabWidget.centerOnScreen()
        
        self.ui.modelTab.InitDriver()
        display = self.ui.modelTab._display
        #display_2d = self.ui.model2dTab._display
        
        # background gradient
        display.set_bg_gradient_color(23,1,32,23,1,32)
        #display_2d.set_bg_gradient_color(255,255,255,255,255,255)
        # display black trihedron
        display.display_trihedron()
        display.View.SetProj(1, 1, 1)
        def centerOnScreen(self):
                    '''Centers the window on the screen.'''
                    resolution = QtGui.QDesktopWidget().screenGeometry()
                    self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                              (resolution.height() / 2) - (self.frameSize().height() / 2))
        def start_display():
            
            self.ui.modelTab.raise_()  # make the application float to the top
          
        return display, start_display
        
    def display3Dmodel(self,cadlist,component):
        
        self.display,_ = self.init_display(backend_str="pyqt4")
        self.display.set_bg_gradient_color(23,1,32,23,1,32)
        if component == "Column":
            self.display.EraseAll()
            osdagDisplayShape(self.display, cadlist[0], update=True)
        elif component == "Beam":
            display.EraseAll()
            osdagDisplayShape(self.display, cadlist[1],material = Graphic3d_NOT_2D_ALUMINUM, update=True)
        elif component == "Finplate" :
            display.EraseAll()
            osdagDisplayShape(self.display,cadlist[2],color = 'red', update = True)
            osdagDisplayShape(self.display, cadlist[3], color = 'red', update = True)
            osdagDisplayShape(self.display, cadlist[4], color = 'blue', update = True)
            self.display.DisplayShape(cadlist[5],color = Quantity_NOC_SADDLEBROWN, update=True)
            self.display.DisplayShape(cadlist[6],color = Quantity_NOC_SADDLEBROWN, update = True)
        elif  component == "Model":
            
            osdagDisplayShape(self.display, cadlist[0], update=True)
            osdagDisplayShape(self.display, cadlist[1],material = Graphic3d_NOT_2D_ALUMINUM, update=True)
            osdagDisplayShape(self.display,cadlist[2],color = 'red', update = True)
            osdagDisplayShape(self.display,cadlist[3],color = 'red', update = True)
            osdagDisplayShape(self.display, cadlist[4], color = 'blue', update = True)
            self.display.DisplayShape(cadlist[5],color = Quantity_NOC_SADDLEBROWN, update=True)
            self.display.DisplayShape(cadlist[6],color = Quantity_NOC_SADDLEBROWN, update = True)
        else:
            pass
             
        start_display()
        
    
    def create3DColWebBeamWeb(self):
        '''
        creating 3d cad model with column web beam web
        '''
        
        column = ISection(B = 83, T = 14.1, D = 250, t = 11, R1 = 12, R2 = 3.2, alpha = 98, length = 1000)
        beam = ISection(B = 140, T = 16,D = 400,t = 8.9, R1 = 14, R2 = 7, alpha = 98,length = 500)
        Fweld1 = FilletWeld(L= 300,b = 6, h = 6)
        #Fweld1 = Weld(L= 300,W = beam.t, T = 8)
        
        plate = Plate(L= 300,W =100, T = 10)
        boltRadius = 10
        nutRadius = 10

        colwebconn =  ColWebBeamWeb(column,beam,Fweld1,plate,boltRadius,nutRadius)
        return colwebconn.create_3dmodel()
        
    def createColFlangeBeamWeb(self):
        '''
        Creating 3d cad model with column flange beam web connection
        '''
        column = ISection(B = 83, T = 14.1, D = 250, t = 11, R1 = 12, R2 = 3.2, alpha = 98, length = 1000)
        beam = ISection(B = 140, T = 16,D = 400,t = 8.9, R1 = 14, R2 = 7, alpha = 98,length = 500)
        weld = Weld(L= 300,b = 6.0, T = 8)
        plate = Plate(L= weld.L,W =100, T = 10)
        boltRadius = 10
        nutRadius = 10
        
        colflangeconn =  ColFlangeBeamWeb(column,beam,weld,plate,boltRadius,nutRadius)
        return colflangeconn.create_3dmodel()
     
    def call_3DModel(self):
        
        if self.ui.btn3D.isEnabled():
            self.ui.chkBxBeam.setChecked(QtCore.Qt.Unchecked)
            self.ui.chkBxCol.setChecked(QtCore.Qt.Unchecked)
            self.ui.chkBxFinplate.setChecked(QtCore.Qt.Unchecked)
            self.ui.mytabWidget.setCurrentIndex(0)
            
        if self.ui.comboConnLoc.currentText()== "Column web-Beam web":
            memberlist =  self.create3DColWebBeamWeb()
        else:
            self.ui.mytabWidget.setCurrentIndex(0)
            memberlist =  self.createColFlangeBeamWeb()
            
        #memberlist = self.create_3dmodel()
        #self.ui.btn3D.setStyleSheet("background-color: red")
        self.display3Dmodel(memberlist, "Model")
        
    
    def call_3DBeam(self):
        '''
        Creating and displaying 3D Beam
        '''
        memberlist = self.create3DColWebBeamWeb()
        
        if self.ui.chkBxBeam.isChecked():
            self.ui.chkBxCol.setChecked(QtCore.Qt.Unchecked)
            self.ui.chkBxFinplate.setChecked(QtCore.Qt.Unchecked)
            self.ui.mytabWidget.setCurrentIndex(0)
            self.display3Dmodel(memberlist, "Beam")
            #self.ui.chkBxBeam.setChecked(QtCore.Qt.Unchecked)
            
    def call_3DColumn(self):
        memberlist = self.create3DColWebBeamWeb()
        if self.ui.chkBxCol.isChecked():
            self.ui.chkBxBeam.setChecked(QtCore.Qt.Unchecked)
            self.ui.chkBxFinplate.setChecked(QtCore.Qt.Unchecked)
            self.ui.mytabWidget.setCurrentIndex(0)
            self.display3Dmodel(memberlist, "Column")
            #self.ui.chkBxBeam.setChecked(QtCore.Qt.Unchecked
            
    def call_3DFinplate(self):
        memberlist = self.create3DColWebBeamWeb()
        if self.ui.chkBxFinplate.isChecked():
            self.ui.chkBxBeam.setChecked(QtCore.Qt.Unchecked)
            self.ui.chkBxCol.setChecked(QtCore.Qt.Unchecked)
            self.ui.mytabWidget.setCurrentIndex(0)
            self.display3Dmodel(memberlist, "Finplate")
            #self.ui.chkBxBeam.setChecked(QtCore.Qt.Unchecked
    
    def design_btnclicked(self):
        
        
        self.ui.outputDock.setFixedSize(310,710)
        
        # self.memberlist3D =  self.createColFlangeBeamWeb()
        # self.mmemberlist2D
        # Getting User Inputs.
        uiObj = self.getuser_inputs()
        print uiObj
        
        # FinPlate Design Calculations. 
        resultObj = finConn(uiObj)
        
        # Displaying Design Calculations To Output Window
        self.display_output(resultObj)
        
        # Displaying Messages related to FinPlate Design.
        self.displaylog_totextedit()
        
        
    def close_event(self, event):
        '''
        Closing finPlate window.
        '''
        uiInput = self.getuser_inputs()
        self.save_inputs(uiInput)
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore() 


    def create2Dcad(self):
                
    
        # ISection COLUMN
        origin1 = numpy.array([0, 0, 0])
        uDir1 = numpy.array([1.0, 0, 0])
        wDir1 = numpy.array([0.0, 0, 1.0])
        t = 8.9
        weldThick = 8
        iSection1 = ISection(B = 83, T = 14.1, D = 250, t = 11, R1 = 12, R2 = 3.2, alpha = 98, length = 1000)
        iSection1.place(origin1, uDir1, wDir1)
        
        # ISection BEAM
        uDir2 = numpy.array([0, 1.0, 0])
        wDir2 = numpy.array([1.0, 0, 0.0])
        d = t/2.0 + weldThick
        origin2 = numpy.array([0, 0, 500]) + (d+7.55) * wDir2 
        iSection2 = ISection(B = 140, T = 16,D = 400,t = 8.9, R1 = 14, R2 = 7, alpha = 98,length = 400)
        iSection2.place(origin2, uDir2, wDir2)
        
        # WELD
        weld = Weld(L= 300,W =iSection2.t, T = 8)
        #plateThickness = 10
        uDir3 = numpy.array([0, 1.0, 0])
        wDir3 = numpy.array([1.0, 0, 0.0])
        origin3 = (iSection1.secOrigin + 
                   iSection1.t/2.0 * iSection1.uDir + 
                   iSection1.length/2.0 * iSection1.wDir +
                   iSection2.t/2.0 * (-iSection2.uDir)+
                   weld.W/2.0 * (-iSection2.uDir))
        #origin3 = numpy.array([0, 0, 500]) + t/2.0 *wDir3 + plateThickness/2.0 * (-iSection2.uDir)
        weld.place(origin3, uDir3, wDir3)
        
        # PLATE
        plate = Plate(L= weld.L,W =100, T = 10)
        uDir4 = numpy.array([0, 1.0, 0])
        wDir4 = numpy.array([1.0, 0, 0.0])
        origin4 = weld.secOrigin + weld.T * weld.wDir
        plate.place(origin4, uDir4, wDir4)
        
        # BOLT BODY
        bolt_T = 6.0
        origin51 = (plate.secOrigin + (-
                    plate.T/2.0 - bolt_T) * plate.uDir +
                    plate.W/2.0 * plate.wDir)
        
        uDir5 = plate.wDir
        wDir5 = plate.uDir
        ## Bolt1
        bolt1 = Bolt(R = 10.0,T = bolt_T, H = 30.0, r = 4.0 )
        bolt1.place(origin51, uDir5, wDir5)
        
        ## Bolt2
        bolt2 = Bolt(R = 10.0,T = bolt_T, H = 30.0, r = 4.0 )
        origin52 = origin51 + 50 *plate.vDir
        bolt2.place(origin52, uDir5, wDir5)
        
        ## Bolt3
        bolt3 = Bolt(R = 10.0,T = bolt_T, H = 30.0, r = 4.0 )
        origin53 = origin51 - 50*plate.vDir
        bolt3.place(origin53, uDir5, wDir5)
        bolt_list =[bolt1,bolt2,bolt3]
        
        # NUTBODY
        ## Nut1
        nut1 = Nut(R = 10.0,T = 10.0,  H = 6.1, innerR1 = 6.0, outerR2 = 8.3)
        uDir = uDir5
        wDir = wDir5
        nut_Origin1 = origin51 + (bolt1.T/2 * plate.uDir)+(plate.T *plate.uDir)+ (iSection2.T/2 * plate.uDir)
        nut1.place(nut_Origin1, uDir, wDir)
        
        ## Nut2
        nut2 = Nut(R = 10.0,T = 10.0,  H = 6.1, innerR1 = 6.0, outerR2 = 8.3)
        nut_Origin2 = origin52 + (bolt1.T/2 * plate.uDir)+(plate.T *plate.uDir)+ (iSection2.T/2 * plate.uDir)
        nut2.place(nut_Origin2, uDir, wDir)
        
        ## Nut3
        nut3 =Nut(R = 10.0,T = 10.0,  H = 6.1, innerR1 = 6.0, outerR2 = 8.3)
        nut_Origin3 = origin53 + (bolt1.T/2 * plate.uDir)+(plate.T *plate.uDir)+ (iSection2.T/2 * plate.uDir)
        nut3.place(nut_Origin3, uDir5, wDir5)
        nut_list = [nut1,nut2,nut3]
        
        # Call for createModel
        iSectionModel1 = iSection1.createModel()
        iSectionModel2 = iSection2.createModel()
        weldModel = weld.createModel()
        plateModel = plate.createModel()
        boltModels = []
        for bolt in bolt_list:
            
            boltModels.append(bolt.createModel())
        
        #color = Quantity_NOC_SADDLEBROWN,
        nutModels = []
        for nut in nut_list:
            nutModels.append(nut.createModel())
                    
        isection = BRepAlgoAPI_Fuse(iSectionModel1,iSectionModel2).Shape()
        weld_isection = BRepAlgoAPI_Fuse(isection,weldModel).Shape()
        plate_weld = BRepAlgoAPI_Fuse(weld_isection,plateModel).Shape()
        
        plate_weld_bolt = plate_weld
        for bolt in boltModels:
            plate_weld_bolt = BRepAlgoAPI_Fuse(plate_weld_bolt, bolt).Shape()
            
        
        final_model = plate_weld_bolt
        for nt in nutModels:
            final_model = BRepAlgoAPI_Fuse(final_model,nt).Shape()
        return final_model
    
    # Export to IGES
    def save3DtoIGES(self):
        
        shape = self.create2Dcad()
        i  = IGESControl.IGESControl_Controller()
        i.Init()
        iges_writer = IGESControl.IGESControl_Writer()
        iges_writer.AddShape(shape)
        iges_writer.Write('/home/deepa/Pictures/osdag.iges')
    
    def display2DModel(self, final_model, viewName):
        
        #display, start_display, _, _ = self.simpleGUI()        

        self.display.set_bg_gradient_color(255, 255, 255, 255, 255, 255)
        # Get Context
        ais_context = self.display.GetContext().GetObject()

        # Get Prs3d_drawer from previous context
        drawer_handle = ais_context.DefaultDrawer()
        drawer = drawer_handle.GetObject()
        drawer.EnableDrawHiddenLine()
        
        hla = drawer.HiddenLineAspect().GetObject()
        hla.SetWidth(2)
        hla.SetColor(Quantity_NOC_RED)
        
        # increase line width in the current viewer
        # This is only viewed in the HLR mode (hit 'e' key for instance)
        
        line_aspect = drawer.SeenLineAspect().GetObject()
        line_aspect.SetWidth(2.8)
        line_aspect.SetColor(Quantity_NOC_BLUE1)
        self.display.EraseAll()
        self.display.DisplayShape(final_model, update = True)
        
        self.display.SetModeHLR()
        self.display.FitAll()
        
        if (viewName == "Front"):
            self.display.View_Front()
        elif (viewName == "Top"):
            self.display.View_Top()
        elif (viewName == "Right"):
            self.display.View_Right()
        else:
            pass
            
        start_display()

    def call_Frontview(self):
        
        '''Displays front view of 2Dmodel
        '''
        self.ui.mytabWidget.setCurrentIndex(0)
        final_model = self.create2Dcad()
        self.display2DModel(final_model, "Front")
    
    def call_Topview(self):
        
        '''Displays Top view of 2Dmodel
        '''
        self.ui.mytabWidget.setCurrentIndex(0)
        final_model = self.create2Dcad()
        self.display2DModel(final_model, "Top")
        
    def call_Sideview(self):
        
        '''Displays Side view of the 2Dmodel'
        '''
        self.ui.mytabWidget.setCurrentIndex(0)
        final_model = self.create2Dcad()
        self.display2DModel(final_model, "Right")
                        
def set_osdaglogger():
    
    logger = logging.getLogger("osdag")
    logger.setLevel(logging.DEBUG)
 
    # create the logging file handler
    fh = logging.FileHandler("fin.log", mode="a")
    
    #,datefmt='%a, %d %b %Y %H:%M:%S'
    #formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    formatter = logging.Formatter('''
    <div  class="LOG %(levelname)s">
        <span class="DATE">%(asctime)s</span>
        <span class="LEVEL">%(levelname)s</span>
        <span class="MSG">%(message)s</span>
    </div>''')
    formatter.datefmt = '%a, %d %b %Y %H:%M:%S'
    fh.setFormatter(formatter)
 
    # add handler to logger object
    logger.addHandler(fh)
    
    
    

if __name__ == '__main__':
    
    # linking css to log file to display colour logs.
    set_osdaglogger()
    rawLogger = logging.getLogger("raw")
    rawLogger.setLevel(logging.INFO)
    fh = logging.FileHandler("fin.log", mode="w")
    formatter = logging.Formatter('''%(message)s''')
    fh.setFormatter(formatter)
    rawLogger.addHandler(fh)
    rawLogger.info('''<link rel="stylesheet" type="text/css" href="log.css"/>''')
    
    
    
    app = QtGui.QApplication(sys.argv)
    window = MainController()
    window.show()
    sys.exit(app.exec_())





