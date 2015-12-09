'''
Created on 24-Aug-2015

@author: deepa
'''
import svgwrite
from PyQt4.QtCore import QString
import numpy as np
from numpy import math


class FinCommonData(object):
    
    def __init__(self, inputObj,ouputObj,dictBeamdata,dictColumndata):
        '''
        Provide all the data related to Finplate connection
        
        :param inputObj:
        :type inputObj:dictionary(Input parameter dictionary)
        :param outputObj:
        :type ouputObj :dictionary (output parameter dictionary)
        :param dictBeamdata :
        :type dictBeamdata:  dictionary (Beam sectional properties) 
        :param dictColumndata :
        :type dictBeamdata: dictionary (Column sectional properties dictionary)

        '''
        self.beam_T = float(dictBeamdata[QString("T")])
        self.col_T = float(dictColumndata[QString("T")])
        self.D_beam = int (dictBeamdata[QString("D")])
        self.D_col = int (dictColumndata[QString("D")])
        self.col_B = int(dictColumndata[QString("B")])
        self.beam_B = int(dictBeamdata[QString("B")])
        self.col_tw = float(dictColumndata[QString("tw")])
        self.beam_tw = float(dictBeamdata[QString("tw")])
        self.col_Designation = dictColumndata[QString("Designation")]
        self.beam_Designation = dictBeamdata[QString("Designation")]
        self.beam_R1 = float(dictBeamdata[QString("R1")])
        self.col_R1 = float(dictColumndata[QString("R1")])
        self.plate_ht= ouputObj['Plate']['height'] 
        self.plate_thick = inputObj['Plate']["Thickness (mm)"]

        self.plate_width = ouputObj['Plate']['width']
        self.weld_len = ouputObj['Plate']['height']
        self.weld_thick =  ouputObj['Weld']['thickness']
        self.bolt_dia  = inputObj["Bolt"]["Diameter (mm)"]
        self.connectivity =  inputObj['Member']['Connectivity']
        self.pitch = ouputObj['Bolt']["pitch"]
        self.gauge = ouputObj['Bolt']["gauge"]
        self.end_dist = ouputObj['Bolt']["enddist"]
        self.edge_dist = ouputObj['Bolt']["edge"]
        self.no_of_rows = ouputObj['Bolt']["numofrow"] 
        self.no_of_col = ouputObj['Bolt']["numofcol"]
        self.col_L = 800
        self.beam_L = 350
        self.gap = 20 # Clear distance between Column and Beam as per subramanyam's book ,range 15-20 mm
        
    def addSMarker(self, dwg):
        '''
        Draws start arrow to given line  -------->
        
        :param dwg :
        :type dwg : svgwrite (obj) ( Container for all svg elements)
        '''
        smarker = dwg.marker(insert=(-8,0), size=(10,10), orient="auto")
        smarker.add(dwg.polyline([(-2.5,0), (0,3), (-8,0), (0,-3)], fill='black'))
        dwg.defs.add(smarker)
        return smarker
    
    
    def addEMarker(self, dwg):
        '''
        This routine returns end arrow  <---------
        
        :param dwg :
        :type dwg : svgwrite  ( Container for all svg elements)
        
        '''
        emarker = dwg.marker(insert=(8,0), size=(10,10), orient="auto")
        emarker.add(dwg.polyline([(2.5,0), (0,3), (8,0), (0,-3)], fill='black'))
        dwg.defs.add(emarker)
        return emarker
    
    
    def drawFaintLine(self,ptOne,ptTwo,dwg):
        '''
        Draw faint line to show dimensions.
        
        :param dwg :
        :type dwg : svgwrite (obj)
        :param: ptOne :
        :type NumPy Array
        :param ptTwo :
        :type NumPy Array
        
        '''
        dwg.add(dwg.line(ptOne,ptTwo).stroke('#D8D8D8',width = 2.5,linecap = 'square',opacity = 0.7))
        
    
    def draw_dimension_outerArrow(self, dwg, pt1, pt2, text, params):    
        '''
        :param dwg :
        :type dwg : svgwrite (obj)
        :param: pt1 :
        :type NumPy Array
        :param pt2 :
        :type NumPy Array
        :param text :
        :type text : String
        :param params["offset"] :
        :type params["offset"] : offset of the dimension line
        :param params["textoffset"]:
        :type params["textoffset"]: float (offset of text from dimension line)
        :param params["lineori"]: 
        :type params ["lineori"]: String (right/left) 
        :param params["endlinedim"]:
        :type params'["endlindim"] : float (dimension line at the end of the outer arrow)       
        '''
        smarker = dwg.marker(insert=(-8,0), size=(10,10), orient="auto")
        smarker.add(dwg.polyline([(-2.5,0), (0,3), (-8,0), (0,-3)], fill='black'))
        emarker = dwg.marker(insert=(8,0), size=(10,10), orient="auto")
        emarker.add(dwg.polyline([(2.5,0), (0,3), (8,0), (0,-3)], fill='black'))
          
        dwg.defs.add(emarker)
        dwg.defs.add(smarker)

        lineVec = pt2 - pt1 # [a, b]
        normalVec = np.array([-lineVec[1], lineVec[0]]) # [-b, a]
        normalUnitVec = self.normalize(normalVec)
        if(params["lineori"] == "left"):
            normalUnitVec = -normalUnitVec
            
        # Q1 = pt1 + params["offset"] * normalUnitVec
        # Q2 = pt2 + params["offset"] * normalUnitVec
        Q1 = pt1 + params["offset"] * normalUnitVec
        Q2 = pt2 + params["offset"] * normalUnitVec
        line = dwg.add(dwg.line(Q1, Q2).stroke('black', width = 2.5, linecap = 'square'))
        line['marker-start'] = smarker.get_funciri()
        line['marker-end'] = emarker.get_funciri()

        Q12mid = 0.5 * (Q1 + Q2)
        txtPt = Q12mid + params["textoffset"] * normalUnitVec
        dwg.add(dwg.text(text, insert=(txtPt), fill='black',font_family = "sans-serif",font_size = 28))
        
        L1 = Q1 + params["endlinedim"] * normalUnitVec
        L2 = Q1 + params["endlinedim"]* (-normalUnitVec)
        dwg.add(dwg.line(L1,L2).stroke('black',width = 2.5,linecap = 'square',opacity = 1.0))
        L3 = Q2 + params["endlinedim"] * normalUnitVec
        L4 = Q2 + params["endlinedim"]* (-normalUnitVec)
        dwg.add(dwg.line(L3,L4).stroke('black',width = 2.5,linecap = 'square',opacity = 1.0))
        
    def normalize(self, vec):
        a = vec[0]
        b = vec[1]
        mag = math.sqrt(a * a + b * b)
        return vec / mag
    
        
    def draw_dimension_innerArrow(self, dwg, ptA, ptB, text, params):
        '''
        :param dwg :
        :type dwg : svgwrite (obj)
        :param: ptA :
        :type NumPy Array
        :param ptB :
        :type NumPy Array
        :param text :
        :type text : String
        :param params["textoffset"]:
        :type params["textoffset"]: float (offset of text from dimension line)
        :param params["endlinedim"]:
        :type params'["endlindim"] : float (dimension line at the end of the outer arrow)   
        :param params["arrowlen"]:
        :type params["arrowlen"]: float (Size of the arrow)
        '''
        
        smarker = dwg.marker(insert=(-8,0), size=(10,10), orient="auto")
        smarker.add(dwg.polyline([(-2.5,0), (0,3), (-8,0), (0,-3)], fill='black'))
        emarker = dwg.marker(insert=(8,0), size=(10,10), orient="auto")
        emarker.add(dwg.polyline([(2.5,0), (0,3), (8,0), (0,-3)], fill='black'))
          
        dwg.defs.add(emarker)
        dwg.defs.add(smarker)
        
        u = ptB - ptA # [a, b]
        uUnit = self.normalize(u)
        
        vUnit = np.array([-uUnit[1], uUnit[0]]) # [-b, a]
        
        A1 = ptA + params["endlinedim"] * vUnit
        A2 = ptA - params["endlinedim"]* (-vUnit)
        dwg.add(dwg.line(A1,A2).stroke('black',width = 2.5,linecap = 'square'))
        B1 = ptB + params["endlinedim"] * vUnit
        B2 = ptB - params["endlinedim"]* (-vUnit)
        dwg.add(dwg.line(B1,B2).stroke('black',width = 2.5,linecap = 'square'))
        A3 = ptA - params["arrowlen"]* uUnit
        B3 = ptB + params["arrowlen"]* uUnit
        
        line = dwg.add(dwg.line(A3, ptA).stroke('black', width = 2.5, linecap = 'square'))
        line['marker-end'] = emarker.get_funciri()
        line = dwg.add(dwg.line(B3, ptB).stroke('black', width = 2.5, linecap = 'square'))
        
        line['marker-end'] = emarker.get_funciri()
        txtPt = B3 + params["textoffset"] * uUnit
        dwg.add(dwg.text(text, insert=(txtPt), fill='black',font_family = "sans-serif",font_size = 28))
        
    def drawArrow(self,line,s_arrow,e_arrow):
        line['marker-start'] = s_arrow.get_funciri()
        line['marker-end'] = e_arrow.get_funciri()

    def drawStartArrow(self,line,s_arrow):
        line['marker-start'] = s_arrow.get_funciri()

    def drawEndArrow(self,line,e_arrow):
        line['marker-end'] = e_arrow.get_funciri()
        
        
    def drawOrientedArrow(self, dwg, pt, theta, orientation, offset, textUp,textDown):
        '''
        Drawing an arrow on given direction 
        
        :param dwg :
        :type dwg : svgwrite (obj)
        :param: ptA :
        :type NumPy Array
        :param theta: 
        :type theta : Int
        :param orientation :
        :type orientation : String
        :param offset :
        :type offset : float
        :param textUp :
        :type textUp : String
        :param textDown :
        :type textup : String
        
        '''
        #Right Up.
        theta = math.radians(theta)
        charWidth = 18
        xVec = np.array([1, 0])
        yVec = np.array([0, 1])
        
        p1 = pt
        lengthA = offset / math.sin(theta)
        
        arrowVec = None
        if(orientation == "NE"):
            arrowVec = np.array([-math.cos(theta), math.sin(theta)])
        elif(orientation == "NW"):
            arrowVec = np.array([math.cos(theta), math.sin(theta)])
        elif(orientation == "SE"):
            arrowVec = np.array([-math.cos(theta), -math.sin(theta)])
        elif(orientation == "SW"):
            arrowVec = np.array([math.cos(theta), -math.sin(theta)])
            
        p2 = p1 - lengthA * arrowVec
        
        text = textDown if len(textDown) > len(textUp) else textUp
        lengthB = len(text) * charWidth
        
        labelVec = None
        if(orientation == "NE"):
            labelVec = -xVec
        elif(orientation == "NW"):
            labelVec = xVec
        elif(orientation == "SE"):
            labelVec = -xVec
        elif(orientation == "SW"):
            labelVec = xVec

        
        p3 = p2 + lengthB * (-labelVec)
            
        txtOffset = 18
        offsetVec = - yVec

        txtPtUp = None
        if(orientation == "NE"):
            txtPtUp = p2 + 0.1 * lengthB * (-labelVec) + txtOffset * offsetVec
            txtPtDwn = p2 - 0.1 * lengthB * (labelVec) -  txtOffset * offsetVec
        elif(orientation == "NW"):
            txtPtUp = p3 + 0.1 * lengthB * labelVec + txtOffset * offsetVec
            txtPtDwn = p3 - 0.1 * lengthB * labelVec - txtOffset * offsetVec
        elif(orientation == "SE"):
            txtPtUp = p2 + 0.1 * lengthB * (-labelVec) + txtOffset * offsetVec
            txtPtDwn = p2 - 0.1 * lengthB * (labelVec) - txtOffset * offsetVec
        elif(orientation == "SW"):
            txtPtUp = p3 + 0.1 * lengthB * labelVec + txtOffset * offsetVec
            txtPtDwn = p3 - 0.1 * lengthB * labelVec - txtOffset * offsetVec
        
        line = dwg.add(dwg.polyline(points=[p1, p2, p3], fill= 'none', stroke='black', stroke_width = 2.5))
        smarker = self.addSMarker(dwg)
        line['marker-start'] = smarker.get_funciri()
        
        dwg.add(dwg.text(textUp, insert=(txtPtUp), fill='black',font_family = "sans-serif",font_size = 28))
        dwg.add(dwg.text(textDown, insert=(txtPtDwn), fill='black',font_family = "sans-serif",font_size = 28))
    
    def saveToSvg(self):
        ''' It returns the svg drawing depending upon connectivity
        CFBW = Column Flange Beam Web
        CWBW = Column Web Beam Web
        BWBW = Beam Web Beam Web
        '''
        fin2DFront = Fin2DCreatorFront(self)
        fin2DTop = Fin2DCreatorTop(self)
        fin2DSide = Fin2DCreatorSide(self)
        
        if self.connectivity == 'Column flange-Beam web':
            fin2DFront.callCFBWfront()
            fin2DSide.callCFBWSide()
            fin2DTop.callCFBWTop()
            
            
        elif self.connectivity == 'Column web-Beam web':
            fin2DFront.callCWBWfront()
            fin2DSide.callCWBWSide()
            fin2DTop.callCWBWTop()
            
        else:
            self.callBWBWSide()

class Fin2DCreatorFront(object):
    
    def __init__(self,finCommonObj):
        
        self.dataObj = finCommonObj
        
        self.A2 =(self.dataObj.col_B,(self.dataObj.col_L-self.dataObj.D_beam)/2)
        self.B = (self.dataObj.col_B,0)
        self.A = (0,0)
        self.D = (0,self.dataObj.col_L)
        self.C = (self.dataObj.col_B,self.dataObj.col_L)
        self.B2 = (self.dataObj.col_B,(self.dataObj.D_beam + self.dataObj.col_L)/2)
        
        ptEx = (self.dataObj.col_B-self.dataObj.col_tw)/2
        ptEy = 0.0
        self.E = (ptEx,ptEy)
        
        ptHx = (self.dataObj.col_B-self.dataObj.col_tw)/2
        ptHy = self.dataObj.col_L
        self.H = (ptHx,ptHy)
        
        ptFx = (self.dataObj.col_B + self.dataObj.col_tw)/2
        ptFy = 0
        self.F = (ptFx,ptFy)
        
        ptGx = (self.dataObj.col_B + self.dataObj.col_tw)/2
        ptGy = self.dataObj.col_L
        self.G = np.array([ptGx,ptGy])
        
        #Draw rectangle for finPlate PRSU
        ptPx = (self.dataObj.col_B + self.dataObj.col_tw)/2
        ptPy = ((self.dataObj.col_L - self.dataObj.D_beam)/2) + (self.dataObj.beam_T + self.dataObj.beam_R1 + 3)
        self.P = (ptPx,ptPy) 
        self.ptP = np.array([ptPx,ptPy])
        
        self.U = self.ptP + (self.dataObj.plate_ht) * np.array([0,1])
        
        ptRx = (self.dataObj.col_B + self.dataObj.col_tw)/2 + self.dataObj.plate_width
        ptRy = ((self.dataObj.col_L - self.dataObj.D_beam)/2) + (self.dataObj.beam_T + self.dataObj.beam_R1 + 3)
        self.R = (ptRx,ptRy)
        
        ptSx = ptRx
        ptSy = ptPy + self.dataObj.plate_ht
        self.S = (ptSx,ptSy)
        
        ptC1x = ((self.dataObj.col_B + self.dataObj.col_tw)/2 + self.dataObj.gap)
        ptC1y = ((self.dataObj.col_L - self.dataObj.D_beam)/2) + (self.dataObj.beam_T + self.dataObj.beam_R1 + 3)
        self.C1 =np.array([ptC1x,ptC1y])
        
        ptA1x = ((self.dataObj.col_B + self.dataObj.col_tw)/2 + self.dataObj.gap)
        ptA1y = ((self.dataObj.col_L - self.dataObj.D_beam)/2)
        self.A1 = np.array([ptA1x,ptA1y])
        
        ptA3x = ((self.dataObj.col_B + self.dataObj.col_tw)/2 + self.dataObj.gap) + self.dataObj.beam_L
        ptA3y = ((self.dataObj.col_L - self.dataObj.D_beam)/2)
        self.A3 = (ptA3x,ptA3y)
        
        ptB3x = ((self.dataObj.col_B + self.dataObj.col_tw)/2 + self.dataObj.gap) + self.dataObj.beam_L
        ptB3y = ((self.dataObj.col_L + self.dataObj.D_beam)/2 ) 
        self.B3 = (ptB3x,ptB3y)
        
        ptB1x = ((self.dataObj.col_B + self.dataObj.col_tw)/2 + self.dataObj.gap)
        ptB1y = ((self.dataObj.col_L + self.dataObj.D_beam)/2 ) 
        self.B1 = np.array([ptB1x,ptB1y])
        self.ptB1 = np.array([ptB1x,ptB1y])
        
        ptC2x= ((self.dataObj.col_B + self.dataObj.col_tw)/2 + 20)
        ptC2y = ptC1y + self.dataObj.plate_ht
        self.C2 = (ptC2x,ptC2y)
        
        ptA5x = ((self.dataObj.col_B + self.dataObj.col_tw)/2 + 20)
        ptA5y = ((self.dataObj.col_L - self.dataObj.D_beam)/2) + self.dataObj.beam_T
        self.A5 = ptA5x,ptA5y
        
        ptA4x = ((self.dataObj.col_B + self.dataObj.col_tw)/2 + 20) + self.dataObj.beam_L
        ptA4y = ((self.dataObj.col_L - self.dataObj.D_beam)/2) + self.dataObj.beam_T
        self.A4 = (ptA4x,ptA4y)
        
        ptB4x = ((self.dataObj.col_B + self.dataObj.col_tw)/2 + 20) + self.dataObj.beam_L
        ptB4y = ((self.dataObj.col_L + self.dataObj.D_beam)/2 )  - self.dataObj.beam_T  
        self.B4 = (ptB4x,ptB4y)
        
        ptBx5 = ((self.dataObj.col_B + self.dataObj.col_tw)/2) + 20
        ptBy5 = ((self.dataObj.col_L + self.dataObj.D_beam)/2 )  - self.dataObj.beam_T
        self.B5 = (ptBx5,ptBy5)
        
        ptP1x = ((self.dataObj.col_B + self.dataObj.col_tw)/2 + self.dataObj.edge_dist)
        ptP1y = ((self.dataObj.col_L - self.dataObj.D_beam)/2 +(self.dataObj.col_tw + self.dataObj.beam_R1 + 3)+ self.dataObj.end_dist)
        self.P1 = (ptP1x,ptP1y)
        

        #### Column flange points for column flange beam web connectivity #####
        
        fromPlate_pt = self.dataObj.D_col + self.dataObj.gap # 20 mm clear distance between colume and beam
        ptFAx = 0
        ptFAy = 0
        self.FA = (ptFAx,ptFAy)
         
        ptFEx = self.dataObj.col_T
        ptFEy = 0.0
        self.FE =(ptFEx,ptFEy)
         
        ptFFx = self.dataObj.D_col - self.dataObj.col_T
        ptFFy = 0.0
        self.FF =(ptFFx,ptFFy)
         
        ptFBx = self.dataObj.D_col 
        ptFBy = 0.0
        self.FB =(ptFBx,ptFBy)
         
        ptFCx = self.dataObj.D_col
        ptFCy = self.dataObj.col_L
        self.FC = np.array([ptFBx,ptFCy])
         
        ptFGx = self.dataObj.D_col - self.dataObj.col_T
        ptFGy = self.dataObj.col_L
        self.FG =(ptFGx,ptFGy)
         
        ptFHx = self.dataObj.col_T
        ptFHy = self.dataObj.col_L
        self.FH =(ptFHx,ptFHy)
         
        ptFDx = 0.0
        ptFDy = self.dataObj.col_L
        self.FD =(ptFDx,ptFDy)
        
        ptFPx = self.dataObj.D_col
        ptFPy = ((self.dataObj.col_L - self.dataObj.D_beam)/2) + (self.dataObj.beam_T + self.dataObj.beam_R1 + 3)
        self.FP = (ptFPx,ptFPy)
        self.ptFP = np.array([ptFPx,ptFPy])
        
        ptFUx = self.dataObj.D_col
        ptFUy = ((self.dataObj.col_L - self.dataObj.D_beam)/2) + (self.dataObj.beam_T + self.dataObj.beam_R1 + 3) + self.dataObj.plate_ht
        self.FU = (ptFUx,ptFUy)
        
        
        #FC1
        ptFC1x = fromPlate_pt 
        ptFC1y = ((self.dataObj.col_L - self.dataObj.D_beam)/2) + (self.dataObj.beam_T + self.dataObj.beam_R1 + 3)
        self.FC1 = np.array([ptFC1x, ptFC1y])
        
        #FC2
        ptFC2x = fromPlate_pt
        ptFC2y = ((self.dataObj.col_L - self.dataObj.D_beam)/2) +( self.dataObj.beam_T + self.dataObj.beam_R1 + 3) + self.dataObj.plate_ht
        self.FC2 = (ptFC2x, ptFC2y)
        
        #FA1
        ptFA1x = fromPlate_pt
        ptFA1y = (self.dataObj.col_L - self.dataObj.D_beam)/2
        self.FA1 = np.array([ptFA1x, ptFA1y])
        
        #FA4
        ptFA4x = fromPlate_pt
        ptFA4y = (self.dataObj.col_L - self.dataObj.D_beam)/2  + self.dataObj.beam_T
        self.FA4 = ptFA4x, ptFA4y
        
        #FA2
        ptFA2x = ptFC1x + self.dataObj.beam_L
        ptFA2y = ptFA1y
        self.FA2 = np.array([ptFA2x, ptFA2y])
        
        #FA3
        ptFA3x = fromPlate_pt  + self.dataObj.beam_L
        ptFA3y = (((self.dataObj.col_L - self.dataObj.D_beam)/2 ) + self.dataObj.beam_T) 
        self.FA3 = ptFA3x, ptFA3y
        
        #FB3
        ptFB3x = fromPlate_pt + self.dataObj.beam_L
        ptFB3y = ((self.dataObj.col_L - self.dataObj.D_beam)/2 + self.dataObj.D_beam) - self.dataObj.beam_T
        self.FB3 = (ptFB3x, ptFB3y)
        
        
        #FB2
        ptFB2x = fromPlate_pt + self.dataObj.beam_L
        ptFB2y = (self.dataObj.col_L -self.dataObj.D_beam)/2 +  self.dataObj.D_beam 
        self.FB2 = ptFB2x, ptFB2y
        
        #FB1
        ptFB1x = self.dataObj.D_col + self.dataObj.gap
        ptFB1y = (self.dataObj.col_L - self.dataObj.D_beam)/2 + self.dataObj.D_beam 
        self.FB1 = np.array([ptFB1x, ptFB1y])
        
        
        #FB4
        ptFB4x = fromPlate_pt
        ptFB4y = ((self.dataObj.col_L - self.dataObj.D_beam)/2 + self.dataObj.D_beam) - self.dataObj.beam_T
        self.FB4 = ptFB4x, ptFB4y
        
    def callBWBWfront(self):
        pass
    
    
    def callCFBWfront(self):
        
        dwg = svgwrite.Drawing('finfront.svg', profile='full')
        smarker = dwg.marker(insert=(-2.5,0), size=(10,10), orient="auto")
        smarker.add(dwg.polyline([(-2.5,0), (0,3), (-10,0), (0,-3)], fill='black'))
        
        emarker = dwg.marker(insert=(2.5,0), size=(10,10), orient="auto")
        emarker.add(dwg.polyline([(2.5,0), (0,3), (10,0), (0,-3)], fill='black'))
        dwg.add(dwg.polyline(points = [(self.FA),(self.FB),(self.FC),(self.FD),(self.FA)],stroke = 'blue',fill = 'none',stroke_width = 2.5))
        dwg.add(dwg.line((self.FE),(self.FH)).stroke('blue',width = 2.5,linecap = 'square'))
        dwg.add(dwg.line((self.FF),(self.FG)).stroke('blue',width = 2.5,linecap = 'square'))
        dwg.add(dwg.polyline(points=[(self.FC1),(self.FA1),(self.FA2),(self.FB2),(self.FB1),(self.FC2)],stroke = 'blue',fill= 'none',stroke_width =2.5))
        dwg.add(dwg.line((self.FC1),(self.FC2)).stroke('red',width = 2.5,linecap = 'square').dasharray(dasharray = ([5,5])))
        dwg.add(dwg.line((self.FA4),(self.FA3)).stroke('blue',width = 2.5,linecap = 'square'))
        dwg.add(dwg.line((self.FB4),(self.FB3)).stroke('blue',width = 2.5,linecap = 'square'))
        
        # Weld hatching to represent WELD.
        pattern = dwg.defs.add(dwg.pattern(id ="diagonalHatch",size=(4, 4), patternUnits="userSpaceOnUse",patternTransform="rotate(45 2 2)"))
        pattern.add(dwg.path(d = "M -1,2 l 6,0", stroke='#000000',stroke_width = 0.7))
        dwg.add(dwg.rect(insert=(self.FP), size=(self.dataObj.weld_thick, self.dataObj.plate_ht),fill= "url(#diagonalHatch)", stroke='white', stroke_width=2.0))
        
        dwg.add(dwg.rect(insert=(self.FP), size=(self.dataObj.plate_width, self.dataObj.plate_ht),fill = 'none', stroke='blue', stroke_width=2.5))
        dwg.add(dwg.rect(insert=(self.FP), size=(self.dataObj.plate_width, self.dataObj.plate_ht),fill = 'none', stroke='blue', stroke_width=2.5))
        
        
        nr = self.dataObj.no_of_rows
        nc = self.dataObj.no_of_col
        bolt_r = self.dataObj.bolt_dia/2
        ptList = []
        
        for i in range(1,(nr+1)):
            colList = []
            for j in range (1,(nc+1)):
                pt = self.ptFP + self.dataObj.edge_dist * np.array([1,0]) + self.dataObj.end_dist * np.array ([0,1]) + \
                    (i-1) * self.dataObj.pitch * np.array([0,1]) + (j-1) * self.dataObj.gauge * np.array([1,0])
                dwg.add(dwg.circle(center=(pt), r = bolt_r, stroke='blue',fill = 'none',stroke_width=1.5))
                ptC = pt - (bolt_r + 4) * np.array([1,0])
                PtD = pt + (bolt_r + 4) * np.array([1,0])
                dwg.add(dwg.line((ptC),(PtD)).stroke('red',width = 2.0,linecap = 'square'))
                ptE = self.ptFP + self.dataObj.edge_dist * np.array([1,0]) +(j-1) * self.dataObj.gauge * np.array([1,0])
                ptF = ptE + self.dataObj.plate_ht * np.array([0,1])
                dwg.add(dwg.line((ptE),(ptF)).stroke('blue',width = 1.5,linecap = 'square').dasharray(dasharray = ([20, 5, 1, 5])))   
                colList.append(pt)
            ptList.append(colList)
        
        pitchPts =[]
        for row in ptList:
            if len(row) > 0:
                pitchPts.append(row[0])
        params = {"offset": self.dataObj.D_col + self.dataObj.edge_dist + 50, "textoffset": 235, "lineori": "right", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg, np.array(pitchPts[0]), np.array(pitchPts[len( pitchPts)-1]), str(len(pitchPts)-1)+ u' \u0040'+ str(int(self.dataObj.pitch)) + " mm c/c", params)     
        
        # Distance between Beam Flange and Plate
        
        params = {"offset": self.dataObj.D_col + self.dataObj.gap + 50, "textoffset": 125, "lineori": "right", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg, self.FA1, self.FC1,  str(int(self.dataObj.beam_T + self.dataObj.beam_R1 + 3)) + " mm", params) 
            # Draw Faint Line To Represent Distance Between Beam Flange and Plate.
        ptOne = self.FA1
        ptBx = -30
        ptBy = ((self.dataObj.col_L - self.dataObj.D_beam)/2) 
        ptTwo = (ptBx,ptBy)
        self.dataObj.drawFaintLine(ptOne, ptTwo, dwg)
        
        # End Distance from the starting point of plate Information
        edgPtx = (self.dataObj.D_col) + self.dataObj.edge_dist
        edgPty = ((self.dataObj.col_L - self.dataObj.D_beam)/2) + (self.dataObj.beam_T + self.dataObj.beam_R1 + 3)
        edgPt = (edgPtx,edgPty)
        params = {"offset": self.dataObj.D_col + self.dataObj.edge_dist + 50, "textoffset": 125, "lineori": "left", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg, np.array(pitchPts[0]), np.array([edgPtx,edgPty]),  str(int(self.dataObj.end_dist)) + " mm", params)   
        
        # End Distance from plate end point.
        edgPt1x = edgPtx
        edgPt1y = edgPty + self.dataObj.plate_ht
        edgPt1 = (edgPt1x,edgPt1y)
        params = {"offset": self.dataObj.D_col + self.dataObj.edge_dist + 50, "textoffset": 125, "lineori": "right", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg, np.array(pitchPts[len( pitchPts)-1]), np.array([edgPt1x,edgPt1y]),  str(int(self.dataObj.end_dist)) + " mm", params)   
        
        # Edge Distance information
        pt1A = self.ptFP + self.dataObj.edge_dist * np.array([1,0])  + \
               (self.dataObj.no_of_col-1)*  self.dataObj.gauge * np.array([1,0]) + self.dataObj.end_dist * np.array ([0,1])
        pt1B = self.ptFP + self.dataObj.edge_dist * np.array([1,0])  + \
               (self.dataObj.no_of_col-1)*  self.dataObj.gauge * np.array([1,0]) + self.dataObj.edge_dist *  np.array([1,0]) + self.dataObj.end_dist * np.array ([0,1])
        offset = self.dataObj.end_dist + self.dataObj.beam_T + self.dataObj.beam_R1 +3
        params = {"offset": self.dataObj.D_col + self.dataObj.edge_dist , "textoffset": 20, "lineori": "left", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg, pt1A, pt1B, str(int(self.dataObj.edge_dist)) + " mm" , params)   
        
        # Faint line for Edge distance dimension
        ptB1 = self.ptFP + self.dataObj.edge_dist * np.array([1,0])  + \
               (self.dataObj.no_of_col-1)*  self.dataObj.gauge * np.array([1,0]) + self.dataObj.edge_dist *  np.array([1,0])
        ptB2 = ptB1 + ((self.dataObj.end_dist + self.dataObj.beam_T + self.dataObj.beam_R1 +3) + 115)* np.array([0,-1])    
        self.dataObj.drawFaintLine(ptB1,ptB2,dwg)
        
        # Gauge Distance
        
        if self.dataObj.no_of_col > 1:
            A = self.ptFP + self.dataObj.edge_dist * np.array([1,0]) + self.dataObj.end_dist * np.array([0,1])
            B = self.ptFP + self.dataObj.edge_dist * np.array([1,0])  + \
               (self.dataObj.no_of_col-1)*  self.dataObj.gauge * np.array([1,0]) + self.dataObj.end_dist * np.array ([0,1])
            offset = (self.dataObj.beam_T + self.dataObj.beam_R1 + 3) + 130
            params = {"offset": offset, "textoffset": 20, "lineori": "left", "endlinedim":10}
            self.dataObj.draw_dimension_outerArrow(dwg, A, B, str(int(self.dataObj.gauge)) + " mm" , params)  
            FA = self.FP + self.dataObj.edge_dist * np.array([1,0])
            FB = self.FP + self.dataObj.edge_dist * np.array([1,0]) + ((self.dataObj.beam_T + self.dataObj.beam_R1 + 3) + 70) * np.array([0,-1])
            self.dataObj.drawFaintLine(FA, FB, dwg) 
        
        # Gap Distance
        gapPt = self.dataObj.col_L - ((self.dataObj.col_L - self.dataObj.D_beam)/2 + (self.dataObj.beam_T + self.dataObj.beam_R1 + 3)) 
        ptG1 = self.ptFP + (gapPt + 30) * np.array([0,1])
        ptG2 = self.FC1 + (gapPt + 30) * np.array([0,1])
        offset = self.dataObj.col_L  # 60% of the column length
        params = {"offset": offset, "textoffset": 20, "lineori": "left", "endlinedim":10,"arrowlen":50}
        self.dataObj.draw_dimension_innerArrow(dwg, ptG1, ptG2, str(self.dataObj.gap) + " mm", params)
       
        # Draw Faint line for Gap Distance
        ptC1 = self.FC
        ptC2 = ptC1 + 40 * np.array([0,1])
        self.dataObj.drawFaintLine(ptC1,ptC2,dwg)
        
        ptD1 = self.FB1
        ptD2 = ptD1 + 240 * np.array([0,1])
        self.dataObj.drawFaintLine(ptD1,ptD2,dwg)
        
        ###### Draws faint line to show dimensions #########
        # Faint lines for gauge and edge distances
        ptA1 = self.ptFP + self.dataObj.edge_dist * np.array([1,0])  + \
               (self.dataObj.no_of_col-1)*  self.dataObj.gauge * np.array([1,0]) 
        ptA2 = ptA1 + ((self.dataObj.end_dist + self.dataObj.beam_T + self.dataObj.beam_R1 +3) + 115)* np.array([0,-1])    
        self.dataObj.drawFaintLine(ptA1, ptA2, dwg)
        
        ptA = self.FP
        ptBx = -30
        ptBy = ((self.dataObj.col_L - self.dataObj.D_beam)/2) + (self.dataObj.beam_T + self.dataObj.beam_R1 + 3)
        ptB = (ptBx,ptBy)
        self.dataObj.drawFaintLine(ptA, ptB, dwg)
        
        pt1 = np.array(pitchPts[0]) - 20 * np.array([1,0])
        ptBx = -30
        ptBy = ((self.dataObj.col_L - self.dataObj.D_beam)/2) + (self.dataObj.beam_T + self.dataObj.beam_R1 + 3) + self.dataObj.end_dist
        pt2 = (ptBx,ptBy)
        self.dataObj.drawFaintLine(pt1, pt2, dwg)
        
        ptOne = np.array(pitchPts[len( pitchPts)-1])
        ptBx = -30
        ptBy = ((self.dataObj.col_L - self.dataObj.D_beam)/2) + (self.dataObj.beam_T + self.dataObj.beam_R1 + 3) + (self.dataObj.plate_ht -self.dataObj.end_dist)
        ptTwo = (ptBx,ptBy)
        self.dataObj.drawFaintLine(ptOne, ptTwo, dwg)
        
        ptOne = self.FU
        ptBx = -30
        ptBy = ((self.dataObj.col_L - self.dataObj.D_beam)/2) + (self.dataObj.beam_T + self.dataObj.beam_R1 + 3) + self.dataObj.plate_ht 
        ptTwo = (ptBx,ptBy)
        self.dataObj.drawFaintLine(ptOne, ptTwo, dwg)
        
        
        # Beam Information
        beam_pt = self.FA2 + self.dataObj.D_beam/2 * np.array([0,1])
        theta = 1
        offset = 0.0 
        textUp = "Beam " + self.dataObj.beam_Designation
        textDown = ""
        self.dataObj.drawOrientedArrow(dwg, beam_pt, theta, "SE", offset, textUp, textDown)
        
        # Column Designation
        ptx = self.dataObj.D_col /2
        pty = 0
        pt = np.array([ptx,pty])
        theta = 30
        offset = self.dataObj.col_L /10
        textUp =  "Column " + self.dataObj.col_Designation
        textDown = ""
        self.dataObj.drawOrientedArrow(dwg, pt, theta, "NW", offset, textUp,textDown)
        
        # Weld Information
        weldPtx = (self.dataObj.D_col)
        weldPty = ((self.dataObj.col_L - self.dataObj.D_beam)/2) + (self.dataObj.beam_T + self.dataObj.beam_R1 + 3)
        weldPt = np.array([weldPtx,weldPty])
        theta = 45
        offset = self.dataObj.col_B 
        textUp = "          z " + str(int(self.dataObj.weld_thick)) + " mm"
        textDown = u"\u25C1"
        self.dataObj.drawOrientedArrow(dwg, weldPt, theta, "NW", offset, textUp, textDown)
        
        # Bolt Information
        bltPtx = self.FP + self.dataObj.edge_dist * np.array([1,0]) + self.dataObj.end_dist * np.array ([0,1]) +(self.dataObj.no_of_col-1) * self.dataObj.gauge * np.array([1,0])
        theta = 45
        offset = (self.dataObj.D_beam * 3)/8
        textUp = str(self.dataObj.no_of_rows) + " nos " + str(int(self.dataObj.bolt_dia)) + u'\u00d8' + " holes"
        textDown = "for M20 bolts (grade 8.8)"
        self.dataObj.drawOrientedArrow(dwg, bltPtx, theta, "NE", offset, textUp,textDown)
        
        # Plate Information
        pltPtx = self.dataObj.D_col  + self.dataObj.plate_width /2
        pltPty = ((self.dataObj.col_L - self.dataObj.D_beam)/2) + (self.dataObj.beam_T + self.dataObj.beam_R1 + 3) + self.dataObj.plate_ht
        pltPt = np.array([pltPtx,pltPty])
        theta = 45
        offset = (self.dataObj.D_beam)/2
        textUp = "PLT. " + str(int(self.dataObj.plate_ht)) +"X" + str(int(self.dataObj.plate_width)) +"X" + str(int(self.dataObj.plate_thick))
        textDown = ""
        self.dataObj.drawOrientedArrow(dwg, pltPt, theta, "SE", offset, textUp, textDown)
        
        dwg.save()
        print"########### Column Flange Beam Web Saved ############"
        
        
        
    def callCWBWfront(self):
        
        dwg = svgwrite.Drawing('finfront.svg', profile='full')
        smarker = dwg.marker(insert=(-2.5,0), size=(10,10), orient="auto")
        smarker.add(dwg.polyline([(-2.5,0), (0,3), (-10,0), (0,-3)], fill='black'))
        
        emarker = dwg.marker(insert=(2.5,0), size=(10,10), orient="auto")
        emarker.add(dwg.polyline([(2.5,0), (0,3), (10,0), (0,-3)], fill='black'))
        
        dwg.add(dwg.polyline(points=[(self.A2),(self.B),(self.A),(self.D),(self.C) ,(self.B2)], stroke='blue', fill='none', stroke_width=2.5))
        dwg.add(dwg.line((self.E),(self.H)).stroke('blue',width = 2.5,linecap = 'square'))
        dwg.add(dwg.line((self.F),(self.G)).stroke('blue',width = 2.5,linecap = 'square'))
        
        # Diagonal Hatching to represent WELD
        pattern = dwg.defs.add(dwg.pattern(id ="diagonalHatch",size=(4, 4), patternUnits="userSpaceOnUse",patternTransform="rotate(45 2 2)"))
        pattern.add(dwg.path(d = "M -1,2 l 6,0", stroke='#000000',stroke_width = 0.7))
        dwg.add(dwg.rect(insert=(self.P), size=(self.dataObj.weld_thick, self.dataObj.plate_ht),fill= "url(#diagonalHatch)", stroke='white', stroke_width=2.0))
        
        dwg.add(dwg.rect(insert=(self.P), size=(self.dataObj.plate_width, self.dataObj.plate_ht),fill = 'none', stroke='blue', stroke_width=2.5))
        
        #C1,A1,A3,B3,B1,C2
        dwg.add(dwg.polyline(points=[(self.C1),(self.A1),(self.A3),(self.B3),(self.B1),(self.C2)],stroke = 'blue',fill= 'none',stroke_width =2.5))
        #C1,C2
        dwg.add(dwg.line((self.C1),(self.C2)).stroke('red',width = 2.5,linecap = 'square').dasharray(dasharray = ([5,5])))
        #A2,B2
        dwg.add(dwg.line((self.A2),(self.B2)).stroke('red',width = 2.5,linecap = 'square').dasharray(dasharray = ([5,5])))
        dwg.add(dwg.line((self.A5),(self.A4)).stroke('blue',width = 2.5,linecap = 'square'))
        dwg.add(dwg.line((self.B5),(self.B4)).stroke('blue',width = 2.5,linecap = 'square'))
        nr = self.dataObj.no_of_rows
        nc = self.dataObj.no_of_col
        bolt_r = self.dataObj.bolt_dia/2
        ptList = []
        
        for i in range(1,(nr+1)):
            colList = []
            for j in range (1,(nc+1)):
                pt = self.ptP + self.dataObj.edge_dist * np.array([1,0]) + self.dataObj.end_dist * np.array ([0,1]) + \
                    (i-1) * self.dataObj.pitch * np.array([0,1]) + (j-1) * self.dataObj.gauge * np.array([1,0])
                dwg.add(dwg.circle(center=(pt), r = bolt_r, stroke='blue',fill = 'none',stroke_width=1.5))
                ptC = pt - (bolt_r + 4) * np.array([1,0])
                PtD = pt + (bolt_r + 4) * np.array([1,0])
                dwg.add(dwg.line((ptC),(PtD)).stroke('red',width = 2.0,linecap = 'square'))
                ptE = self.ptP + self.dataObj.edge_dist * np.array([1,0]) +(j-1) * self.dataObj.gauge * np.array([1,0])
                ptF = ptE + self.dataObj.plate_ht * np.array([0,1])
                dwg.add(dwg.line((ptE),(ptF)).stroke('blue',width = 1.5,linecap = 'square').dasharray(dasharray = ([20, 5, 1, 5])))
                colList.append(pt)
            ptList.append(colList)
            
        pitchPts =[]
        for row in ptList:
            if len(row) > 0:
                pitchPts.append(row[0])
        txtOffset = (self.dataObj.col_B + self.dataObj.col_tw)/2 + self.dataObj.edge_dist + 80
        params = {"offset": (self.dataObj.col_B + self.dataObj.col_tw)/2 + self.dataObj.edge_dist + 80, "textoffset": txtOffset, "lineori": "right", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg, np.array(pitchPts[0]), np.array(pitchPts[len( pitchPts)-1]), str(len(pitchPts)-1)+ u' \u0040'+ str(int(self.dataObj. pitch)) + " mm c/c", params)     
        
        # End Distance from the starting point of plate Information
        edgPtx = (self.dataObj.col_B + self.dataObj.col_tw)/2 + self.dataObj.edge_dist
        edgPty = ((self.dataObj.col_L - self.dataObj.D_beam)/2) + (self.dataObj.beam_T + self.dataObj.beam_R1 + 3)
        edgPt = (edgPtx,edgPty)
        params = {"offset": (self.dataObj.col_B + self.dataObj.col_tw)/2 + self.dataObj.edge_dist + 80, "textoffset": 120, "lineori": "left", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg, np.array(pitchPts[0]), np.array([edgPtx,edgPty]),  str(int(self.dataObj.end_dist)) + " mm", params)     
        
        # Distance between Beam Flange and Plate
        offset = (self.dataObj.col_B + self.dataObj.col_tw)/2 + self.dataObj.gap + 50
        params = {"offset":(self.dataObj.col_B + self.dataObj.col_tw)/2 + self.dataObj.gap + 80, "textoffset": 125, "lineori": "right", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg, self.A1, self.C1,  str(int(self.dataObj.beam_T + self.dataObj.beam_R1 + 3)) + " mm", params) 
        
        # Draw Faint line for dimensions
        ptOne = self.P
        ptTwox = -60 
        ptTwoy = ((self.dataObj.col_L - self.dataObj.D_beam)/2) + (self.dataObj.beam_T + self.dataObj.beam_R1 + 3)  
        ptTwo = (ptTwox,ptTwoy)
        self.dataObj.drawFaintLine(ptOne, ptTwo, dwg)
        
        pt1 = np.array(pitchPts[0])
        ptTwox = -60 
        ptTwoy = ((self.dataObj.col_L - self.dataObj.D_beam)/2) + (self.dataObj.beam_T + self.dataObj.beam_R1 + 3) + self.dataObj.end_dist
        pt2 = (ptTwox,ptTwoy)
        self.dataObj.drawFaintLine(pt1, pt2, dwg)
        
        ptA = np.array(pitchPts[len( pitchPts)-1])
        ptBx = -60
        ptBy = ((self.dataObj.col_L - self.dataObj.D_beam)/2) + (self.dataObj.beam_T + self.dataObj.beam_R1 + 3) + (self.dataObj.plate_ht -self.dataObj.end_dist)
        ptB = (ptBx,ptBy)
        self.dataObj.drawFaintLine(ptA, ptB, dwg)
        
        ptOne = self.U
        ptBx = -60
        ptBy = ((self.dataObj.col_L - self.dataObj.D_beam)/2) + (self.dataObj.beam_T + self.dataObj.beam_R1 + 3) + self.dataObj.plate_ht 
        ptTwo = (ptBx,ptBy)
        self.dataObj.drawFaintLine(ptOne, ptTwo, dwg)
        
        # End Distance from plate end point.
        edgPt1x = edgPtx
        edgPt1y = edgPty + self.dataObj.plate_ht
        edgPt1 = (edgPt1x,edgPt1y)
        params = {"offset": (self.dataObj.col_B + self.dataObj.col_tw)/2 + self.dataObj.edge_dist + 80, "textoffset": 120, "lineori": "right", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg, np.array(pitchPts[len( pitchPts)-1]), np.array([edgPt1x,edgPt1y]), str(int(self.dataObj.end_dist)) + " mm" , params)   
        
        # Gap Distance
            # Draw Faint Lines to representation of Gap distance #
        dist1 = self.dataObj.col_L - ((self.dataObj.col_L - self.dataObj.D_beam)/2 + self.dataObj.D_beam)
        ptA = self.B1
        ptB = self.B1 + (dist1 + 100)* np.array([0,1])
        self.dataObj.drawFaintLine(ptA,ptB,dwg)
        ptC = self.G 
        ptD = ptC + (100)*np.array([0,1])
        self.dataObj.drawFaintLine(ptC,ptD,dwg)
        ptG1 = self.B1 + (dist1 + 50)* np.array([0,1])
        ptG2 = self.B1 + self.dataObj.gap * np.array([-1,0]) + (dist1 + 50)* np.array([0,1])
        offset = 1
        params = {"offset": offset, "textoffset": 120, "lineori": "right", "endlinedim":10,"arrowlen":50}
        self.dataObj.draw_dimension_innerArrow(dwg, ptG1, ptG2, str(self.dataObj.gap) + " mm", params)
       
        # Gauge Distance Information
        gaugePts = ptList[0]   
        for i in range (len( gaugePts)-1):
            offset_dist = -(self.dataObj.end_dist + self.dataObj.beam_T + self.dataObj.beam_R1 + 3 + dist1 + 100)
            params = {"offset": offset_dist, "textoffset": 35, "lineori": "right", "endlinedim":10}
            ptP = np.array(gaugePts[i]) 
            ptQ = np.array(gaugePts[i + 1]) 
            self.dataObj.draw_dimension_outerArrow(dwg, ptP, ptQ, str(int(self.dataObj.gauge)) + " mm", params)
        
        if len(ptList[(len(ptList)-1)]) > 1:
            ptA = self.ptP + self.dataObj.edge_dist * np.array([1,0])
            ptB = ptA + (self.dataObj.end_dist + self.dataObj.beam_T + self.dataObj.beam_R1 + 3 + dist1 + 50)* np.array([0,-1])
            self.dataObj.drawFaintLine(ptA, ptB, dwg)  
            
            ptC = self.ptP + self.dataObj.edge_dist * np.array([1,0]) +self.dataObj.gauge * np.array([1,0])   
            ptD = ptC + (self.dataObj.end_dist + self.dataObj.beam_T + self.dataObj.beam_R1 + 3 + dist1 + 50)* np.array([0,-1])
            #self.dataObj.drawFaintLine(ptC, ptD, dwg)  
        
        # Edge Distance Information
        ptA = self.ptP + self.dataObj.edge_dist * np.array([1,0]) + (self.dataObj.no_of_col-1) * self.dataObj.gauge * np.array([1,0])
        ptB  = ptA + self.dataObj.edge_dist * np.array([1,0])
        offsetDist =  -(self.dataObj.end_dist + self.dataObj.beam_T + self.dataObj.beam_R1 + 3 + dist1 + 120)
        params = {"offset": offsetDist, "textoffset": 35, "lineori": "right", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg,ptA,ptB, str(int(self.dataObj.edge_dist)) + " mm", params)  
            # Draw Faint line for Edge distance
        ptC = self.ptP + self.dataObj.edge_dist * np.array([1,0]) + (self.dataObj.no_of_col-1) * self.dataObj.gauge * np.array([1,0])   
        ptD = ptC + (self.dataObj.end_dist + self.dataObj.beam_T + self.dataObj.beam_R1 + 3 + dist1 + 100)* np.array([0,-1])
        self.dataObj.drawFaintLine(ptC, ptD, dwg) 
        ptE = self.ptP + self.dataObj.edge_dist * np.array([1,0]) + (self.dataObj.no_of_col-1) * self.dataObj.gauge * np.array([1,0]) + self.dataObj.edge_dist * np.array([1,0])  
        ptF = ptE + (self.dataObj.end_dist + self.dataObj.beam_T + self.dataObj.beam_R1 + 3 + dist1 + 100)* np.array([0,-1])
        self.dataObj.drawFaintLine(ptE, ptF, dwg)   
        
        # Plate Width Information
        pltPtx = (self.dataObj.col_B + self.dataObj.col_tw)/2 + self.dataObj.plate_width /2
        pltPty = ((self.dataObj.col_L - self.dataObj.D_beam)/2) + (self.dataObj.beam_T + self.dataObj.beam_R1 + 3) + self.dataObj.plate_ht
        pltPt = np.array([pltPtx,pltPty])
        theta = 45
        offset = (self.dataObj.D_beam)/2
        textUp = "PLT. " + str(int(self.dataObj.plate_ht)) +"X" + str(int(self.dataObj.plate_width)) +"X" + str(int(self.dataObj.plate_thick))
        textDown = ""
        self.dataObj.drawOrientedArrow(dwg, pltPt, theta, "SE", offset, textUp, textDown)
        
        dwg.defs.add(emarker)
        dwg.defs.add(smarker)
        
        # Column Designation
        ptx = self.dataObj.col_B /2
        pty = 0
        pt = np.array([ptx,pty])
        theta = 30
        offset = self.dataObj.col_L /10
        textUp =  "Column " + self.dataObj.col_Designation
        textDown = ""
        self.dataObj.drawOrientedArrow(dwg, pt, theta, "NW", offset, textUp,textDown)
        
        # Bolt Information
        bltPtx = self.ptP + self.dataObj.edge_dist * np.array([1,0]) + self.dataObj.end_dist * np.array ([0,1]) +(self.dataObj.no_of_col-1) * self.dataObj.gauge * np.array([1,0])
        theta = 45
        offset = (self.dataObj.D_beam * 3)/8
        textUp = str(self.dataObj.no_of_rows) + " nos " + str(self.dataObj.bolt_dia) + u'\u00d8' + " holes"
        textDown = "for M20 bolts (grade 8.8)"
        self.dataObj.drawOrientedArrow(dwg, bltPtx, theta, "NE", offset, textUp,textDown)
        
        
        # Beam Information
        beam_pt = self.ptB1 + (self.dataObj.beam_L) * np.array([1,0])+ self.dataObj.D_beam/2 * np.array([0,-1])
        theta = 1
        offset = 0.0
        textUp = "Beam " + self.dataObj.beam_Designation
        textDown = ""
        self.dataObj.drawOrientedArrow(dwg, beam_pt, theta, "SE", offset, textUp, textDown)
        
        # Weld Information
        weldPtx = (self.dataObj.col_B + self.dataObj.col_tw)/2
        weldPty = ((self.dataObj.col_L - self.dataObj.D_beam)/2) + (self.dataObj.beam_T + self.dataObj.beam_R1 + 3)
        weldPt = np.array([weldPtx,weldPty])
        theta = 45
        offset = self.dataObj.col_B 
        textUp = "          z " + str(self.dataObj.weld_thick) + " mm"
        textDown = ""
        
        self.dataObj.drawOrientedArrow(dwg, weldPt, theta, "NW", offset, textUp, textDown)
        
        dwg.save()
        print"########### Column Web Beam Web Saved ############"
    
             
class Fin2DCreatorTop(object):
    
    def __init__(self,finCommonObj):
        
        self.dataObj = finCommonObj
        self.A = np.array([0,0])
        self.B = np.array([0,0]) + (self.dataObj.col_B)* np.array([1,0])
        self.C = self.B + (self.dataObj.col_T)* np.array([0,1])
        self.D = self.A +  (self.dataObj.col_B + self.dataObj.col_tw)/2 * np.array([1,0]) + (self.dataObj.col_T) * np.array([0,1])
        self.E = self.A +  (self.dataObj.col_B + self.dataObj.col_tw)/2 * np.array([1,0]) + (self.dataObj.D_col - self.dataObj.col_T)* np.array([0,1])
        self.F = self.B + (self.dataObj.D_col - self.dataObj.col_T)* np.array([0,1])
        self.G = self.B + (self.dataObj.D_col)* np.array([0,1])
        self.H = self.A + (self.dataObj.D_col)* np.array([0,1])
        self.I = self.A + (self.dataObj.D_col - self.dataObj.col_T)* np.array([0,1])
        self.J = self.E - (self.dataObj.col_tw) * np.array([1,0])
        self.K = self.D - (self.dataObj.col_tw) * np.array([1,0])
        self.L = self.A + (self.dataObj.col_T)* np.array([0,1])
        self.A1 = self.A + ((self.dataObj.col_B + self.dataObj.col_tw)/2 + self.dataObj.gap)* np.array([1,0]) + (self.dataObj.col_T + self.dataObj.beam_R1)  * np.array([0,1])
        self.A4 = self.A1 + self.dataObj.beam_B * np.array([0,1])
        self.A7 = self.A1 + (self.dataObj.beam_B - self.dataObj.beam_tw) /2 * np.array([0,1])
        self.A5 = self.A7 - 20 * np.array([1,0])
        self.A8 = self.A7 + (self.dataObj.beam_L) * np.array([1,0])
        self.P1 = self.A1 + (self.dataObj.beam_B + self.dataObj.beam_tw) /2 * np.array([0,1])
        self.A6 = self.P1 + (self.dataObj.beam_L) * np.array([1,0])
        self.P = self.P1 - 20 * np.array([1,0])
        self.P2 = self.P + (self.dataObj.plate_width) * np.array([1,0])
        self.P4 = self.P1 + (self.dataObj.plate_thick)* np.array([0,1])
        self.P3 = self.P2 + (self.dataObj.plate_thick)* np.array([0,1])
        
        # Weld Triangle
        
        self.ptP = self.P + 2.5 * np.array([1,0]) + 2.5 * np.array([0,-1])
        self.O = self.P + self.dataObj.weld_thick * np.array([1,0])
        self.ptO = self.O  + 2.5 * np.array([1,0]) + 2.5 * np.array([0,-1])
        self.R = self.P + self.dataObj.weld_thick * np.array([0,-1])
        self.ptR = self.R + 2.5 * np.array([1,0]) + 2.5 * np.array([0,-1]) 
        
        self.X = self.P + (self.dataObj.plate_thick)* np.array([0,1])
        self.ptX = self.X + 2.5 * np.array([1,0]) + 2.5 * np.array([0,1]) 
        self.Y = self.X + (self.dataObj.weld_thick) * np.array([0,1])
        self.ptY = self.Y + 2.5 * np.array([1,0]) + 2.5 * np.array([0,1]) 
        self.Z = self.X + (self.dataObj.weld_thick) * np.array([1,0])
        self.ptZ = self.Z + 2.5 * np.array([1,0]) + 2.5 * np.array([0,1]) 
        
        
        #### CFBW connectivity points
        self.FA = np.array([0,0])
        self.FB = self.FA + self.dataObj.col_T * np.array([1,0])
        self.FC = self.FB + (self.dataObj.col_B - self.dataObj.col_tw)/2 * np.array([0,1])
        self.FD = self.FC  + (self.dataObj.D_col - 2*(self.dataObj.col_T))* np.array([1,0])
        self.FE = self.A + (self.dataObj.D_col - self.dataObj.col_T) * np.array([1,0])
        self.FF = self.FA + self.dataObj.D_col * np.array([1,0])
        self.FG = self.FF + self.dataObj.col_B * np.array([0,1])
        self.FH = self.FG + self.dataObj.col_T * np.array([-1,0])
        self.FI = self.FD + self.dataObj.col_tw * np.array([0,1])
        self.FJ = self.FC + self.dataObj.col_tw * np.array([0,1])
        self.FK = self.FB + self.dataObj.col_B * np.array([0,1])
        self.FL = self.FK + self.dataObj.col_T * np.array([-1,0])
        self.FA7 = self.FD + (self.dataObj.col_T + self.dataObj.gap) * np.array([1,0])
        self.FP1 = self.FA7 + self.dataObj.beam_tw * np.array([0,1])
        self.FP = self.FP1 + self.dataObj.gap * np.array([-1,0])
        self.FA1 = self.FA7 + (self.dataObj.beam_B - self.dataObj.beam_tw)/2 *np.array([0,-1])
        self.FA2 = self.FA1 + self.dataObj.beam_L * np.array([1,0])
        self.FA3 = self.FA2 + self.dataObj.beam_B * np.array([0,1])
        self.FA4 = self.FA1 + self.dataObj.beam_B * np.array([0,1])
        self.FX = self.FP + self.dataObj.plate_thick * np.array([0,1])
        self.FP2 = self.FP + self.dataObj.plate_width * np.array([1,0])
        self.FP3 = self.FP2 + self.dataObj.plate_thick * np.array([0,1])
        self.FP4 =  self.FX + self.dataObj.gap * np.array([1,0])
        self.FA8 = self.FA7 + self.dataObj.beam_L * np.array([1,0])
        self.FA6 = self.FP1 + self.dataObj.beam_L * np.array([1,0])
        self.FP5 = self.FA7 + self.dataObj.gap * np.array([-1,0])
        # Weld Triangle
        
        self.ptFP = self.FP + 2.5 * np.array([1,0]) + 2.5 * np.array([0,-1])
        self.FQ = self.FP + self.dataObj.weld_thick * np.array([1,0])
        self.ptFQ = self.FQ  + 2.5 * np.array([1,0]) + 2.5 * np.array([0,-1])
        self.FR = self.FP + self.dataObj.weld_thick * np.array([0,-1])
        self.ptFR = self.FR + 2.5 * np.array([1,0]) + 2.5 * np.array([0,-1]) 
        
        self.FX = self.FP + (self.dataObj.plate_thick)* np.array([0,1])
        self.ptFX = self.FX + 2.5 * np.array([1,0]) + 2.5 * np.array([0,1]) 
        self.FY = self.FX + (self.dataObj.weld_thick) * np.array([0,1])
        self.ptFY = self.FY + 2.5 * np.array([1,0]) + 2.5 * np.array([0,1]) 
        self.FZ = self.FX + (self.dataObj.weld_thick) * np.array([1,0])
        self.ptFZ = self.FZ + 2.5 * np.array([1,0]) + 2.5 * np.array([0,1]) 

    def callCFBWTop(self):
        '''
        '''
        dwg = svgwrite.Drawing('finTop.svg', profile = 'full')
        
        dwg.add(dwg.polyline(points=[(self.FA),(self.FB),(self.FC),(self.FD),(self.FE),(self.FF),(self.FG),(self.FH),(self.FI),(self.FJ),(self.FK),(self.FL),(self.FA)], stroke='blue', fill='none', stroke_width=2.5))
        dwg.add(dwg.rect(insert=(self.FA1), size=(self.dataObj.beam_L, self.dataObj.beam_B),fill = 'none', stroke='blue', stroke_width=2.5))
        dwg.add(dwg.line((self.FP),(self.FP1)).stroke('blue',width = 2.5,linecap = 'square'))
        dwg.add(dwg.line((self.FX),(self.FP4)).stroke('blue',width = 2.5,linecap = 'square'))
        dwg.add(dwg.polyline(points=[(self.FP1),(self.FP2),(self.FP3),(self.FP4)], stroke='red', fill='none', stroke_width=2.5).dasharray(dasharray = ([5,5])))
        dwg.add(dwg.line((self.FA7),(self.FA8)).stroke('red',width = 2.5,linecap = 'square').dasharray(dasharray = ([5,5])))
        dwg.add(dwg.line((self.FP1),(self.FA6)).stroke('red',width = 2.5,linecap = 'square').dasharray(dasharray = ([5,5])))
        dwg.add(dwg.polyline([(self.ptFP), (self.ptFQ), (self.ptFR), (self.ptFP)], fill='black',stroke_width=2.5,stroke='black'))
        dwg.add(dwg.polyline([(self.ptFX), (self.ptFY), (self.ptFZ), (self.ptFX)], fill='black',stroke_width=2.5,stroke='black'))
        
        nc = self.dataObj.no_of_col
        bolt_r = self.dataObj.bolt_dia/2
        ptList = []
        if nc >= 1:
            for col in range (nc):
                pt = self.FP5  + self.dataObj.edge_dist * np.array([1,0]) + (col) * self.dataObj.gauge * np.array([1,0])
                pt1 = pt - bolt_r *  np.array([1,0])
                rect_width = self.dataObj.bolt_dia
                rect_ht = self.dataObj.beam_tw + self.dataObj.plate_thick
                dwg.add(dwg.rect(insert=(pt1), size=(rect_width, rect_ht),fill = 'black', stroke='black', stroke_width=2.5))
                B1 = pt + 10 * np.array([0,-1])
                B2 = pt + (rect_ht + 10) * np.array([0,1])
                dwg.add(dwg.line((B1),(B2)).stroke('black',width = 2.5,linecap = 'square'))
                ptList.append(pt)
                dimOffset = self.dataObj.beam_B/2 + self.dataObj.col_T + self.dataObj.col_R1 + 150
                # Draw Faint line between edge and gauge distance
                ptA = B1 + (dimOffset ) * np.array([0,-1])
                self.dataObj.drawFaintLine(B1,ptA,dwg)
                
                if len(ptList) > 1:
                    params = {"offset": dimOffset, "textoffset": 20, "lineori": "left", "endlinedim":10}
                    self.dataObj.draw_dimension_outerArrow(dwg,np.array(ptList[0]),np.array(ptList[1]),  str(int(self.dataObj.gauge)) + " mm", params)  
                
        # Draw Faint line to represent edge distance
        ptB = self.FP5 + self.dataObj.edge_dist * np.array([1,0]) + (col) * self.dataObj.gauge * np.array([1,0]) + self.dataObj.edge_dist * np.array([1,0])
        ptC = ptB + (self.dataObj.beam_B/2 + self.dataObj.col_T + self.dataObj.col_R1 + 90) * np.array([0,-1])
        self.dataObj.drawFaintLine(ptB,ptC,dwg)
        
        ptx = self.FP5 + self.dataObj.edge_dist * np.array([1,0]) + (col) * self.dataObj.gauge * np.array([1,0])
        ptY = ptx + self.dataObj.edge_dist * np.array([1,0])
        offset = self.dataObj.beam_B/2 + self.dataObj.col_T + self.dataObj.col_R1 + 100
        params = {"offset": offset, "textoffset": 20, "lineori": "left", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg,ptx,ptY,  str(int(self.dataObj.edge_dist)) + " mm", params)  
        
        # Beam Information
        beam_pt = self.FA6
        theta = 1
        offset = 0
        textUp = "Beam " + self.dataObj.beam_Designation
        textDown = ""
        self.dataObj.drawOrientedArrow(dwg, beam_pt, theta, "SE", offset, textUp, textDown)
        
        # Column Information
        col_pt = self.FL
        theta = 45
        offset = (self.dataObj.D_beam * 3)/8
        textUp = "Beam " + self.dataObj.col_Designation
        textDown = ""
        self.dataObj.drawOrientedArrow(dwg, col_pt, theta, "SE", offset, textUp, textDown)
        
        # Plate  Information
        plt_pt = self.FP3 
        theta = 45
        offset =  self.dataObj.beam_B /2 + 50
        textUp = "PLT. " + str(int(self.dataObj.plate_ht))+'x'+ str(int(self.dataObj.plate_width))+ 'x' + str(int(self.dataObj.plate_thick))
        textDown = ""
        self.dataObj.drawOrientedArrow(dwg, plt_pt, theta, "SE", offset, textUp, textDown)
        
        # Weld Information
        weldPt = self.FP
        theta = 40
        offset = self.dataObj.weld_thick + self.dataObj.plate_thick + self.dataObj.beam_B /2 + 80
        textUp = "          z " + str(int(self.dataObj.weld_thick)) + " mm"
        textDown = u"\u25C1"
        self.dataObj.drawOrientedArrow(dwg, weldPt, theta, "NW", offset, textUp, textDown)

        # Gap Informatoin
        ptG1 = self.FG + 50 * np.array([0,1])
        ptG2 = ptG1 + 20 * np.array([1,0])
        offset = 1
        params = {"offset": offset, "textoffset": 10, "lineori": "right", "endlinedim":10,"arrowlen":50}
        self.dataObj.draw_dimension_innerArrow(dwg, ptG1, ptG2, str(self.dataObj.gap) + " mm", params)
            # Draw Faint Lines to representation of Gap distance #
        ptA = self.FG
        ptB = ptG1
        self.dataObj.drawFaintLine(ptA,ptB,dwg)
        ptC = self.FA4
        ptD = ptG2
        self.dataObj.drawFaintLine(ptC,ptD,dwg)
         
        dwg.save()
        print"$$$$$$$$$ Saved Column Flange Beam Web Top $$$$$$$$$$$$"
    
    def callCWBWTop(self):
        '''
        '''
        dwg = svgwrite.Drawing('finTop.svg', profile='full')
        
        dwg.add(dwg.polyline(points=[(self.A),(self.B),(self.C),(self.D),(self.E),(self.F),(self.G),(self.H),(self.I),(self.J),(self.K),(self.L),(self.A)], stroke='blue', fill='none', stroke_width=2.5))
        dwg.add(dwg.rect(insert=(self.A1), size=(self.dataObj.beam_L, self.dataObj.beam_B),fill = 'none', stroke='blue', stroke_width=2.5))
        dwg.add(dwg.line((self.A7),(self.A8)).stroke('red',width = 2.5,linecap = 'square').dasharray(dasharray = ([5,5])))
        dwg.add(dwg.line((self.P1),(self.A6)).stroke('red',width = 2.5,linecap = 'square').dasharray(dasharray = ([5,5])))
        dwg.add(dwg.line((self.P),(self.P1)).stroke('blue',width = 2.5,linecap = 'square'))
        dwg.add(dwg.line((self.X),(self.P4)).stroke('blue',width = 2.5,linecap = 'square'))
        dwg.add(dwg.polyline(points=[(self.P1),(self.P2),(self.P3),(self.P4)], stroke='red', fill='none', stroke_width=2.5).dasharray(dasharray = ([5,5])))
        dwg.add(dwg.polyline([(self.ptP), (self.ptO), (self.ptR), (self.ptP)], fill='black',stroke_width=2.5,stroke='black'))
        dwg.add(dwg.polyline([(self.ptX), (self.ptY), (self.ptZ), (self.ptX)], fill='black',stroke_width=2.5,stroke='black'))
        
        nc = self.dataObj.no_of_col
        bolt_r = self.dataObj.bolt_dia/2
        ptList = []
        if nc >= 1:
            for col in range (nc):
                pt = self.A5  + self.dataObj.edge_dist * np.array([1,0]) + (col) * self.dataObj.gauge * np.array([1,0])
                print self.dataObj.gauge
                pt1 = pt - bolt_r *  np.array([1,0])
                rect_width = self.dataObj.bolt_dia
                rect_ht = self.dataObj.beam_tw + self.dataObj.plate_thick
                dwg.add(dwg.rect(insert=(pt1), size=(rect_width, rect_ht),fill = 'black', stroke='black', stroke_width=2.5))
                B1 = pt + 10 * np.array([0,-1])
                B2 = pt + (rect_ht + 10) * np.array([0,1])
                dwg.add(dwg.line((B1),(B2)).stroke('black',width = 2.5,linecap = 'square'))
                ptList.append(pt)
                if len(ptList) > 1:
                    dimOffset = self.dataObj.beam_B/2 + self.dataObj.col_T + self.dataObj.col_R1 + 50
                    params = {"offset": dimOffset, "textoffset": 20, "lineori": "left", "endlinedim":10}
                    self.dataObj.draw_dimension_outerArrow(dwg,np.array(ptList[0]),np.array(ptList[1]),  str(int(self.dataObj.gauge)) + "mm", params)  
                    
        # Draw Faint line to represent edge distance
        ptB = self.A5 + self.dataObj.edge_dist * np.array([1,0]) + (nc -1) * self.dataObj.gauge * np.array([1,0]) + self.dataObj.edge_dist * np.array([1,0])
        ptC = ptB + (self.dataObj.beam_B/2 + self.dataObj.col_T + self.dataObj.col_R1 + 150) * np.array([0,-1])
        self.dataObj.drawFaintLine(ptB,ptC,dwg)
        ptL = self.A5 + self.dataObj.edge_dist * np.array([1,0]) + (nc-1) * self.dataObj.gauge * np.array([1,0])
        ptM = ptL + (self.dataObj.beam_B/2 + self.dataObj.col_T + self.dataObj.col_R1 + 150) * np.array([0,-1])
        self.dataObj.drawFaintLine(ptL,ptM,dwg)
        
        # Edge Distance
        ptx = self.A5 + self.dataObj.edge_dist * np.array([1,0]) + (nc-1) * self.dataObj.gauge * np.array([1,0])
        ptY = ptx + self.dataObj.edge_dist * np.array([1,0])
        offset = self.dataObj.beam_B/2 + self.dataObj.col_T + self.dataObj.col_R1 + 150
        params = {"offset": offset, "textoffset": 20, "lineori": "left", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg,ptx,ptY,  str(int(self.dataObj.edge_dist)) + " mm", params)  
        
        #  Draws Faint line to represent Gauge Distance
        ptK = self.A5 + self.dataObj.edge_dist * np.array([1,0])
        ptM = ptK + (self.dataObj.beam_B/2 + self.dataObj.col_T + self.dataObj.col_R1 + 50)* np.array([0,-1])
        self.dataObj.drawFaintLine(ptK,ptM,dwg)
        
        # Beam Information
        beam_pt = self.A6
        theta = 1
        offset = 0
        textUp = "Beam " + self.dataObj.beam_Designation
        textDown = ""
        self.dataObj.drawOrientedArrow(dwg, beam_pt, theta, "NE", offset, textUp, textDown)
        
        # column  Information
        col_pt = self.H
        theta = 45
        offset = self.dataObj.beam_B /2 + 100
        textUp = "Column " + self.dataObj.col_Designation
        textDown = " " 
        self.dataObj.drawOrientedArrow(dwg, col_pt, theta, "SE", offset, textUp, textDown)
        
        # Plate  Information
        plt_pt = self.P3 
        theta = 45
        offset =  self.dataObj.beam_B /2 + 50
        textUp = "PLT. " + str(int(self.dataObj.plate_ht))+'x'+ str(int(self.dataObj.plate_width))+ 'x' + str(int(self.dataObj.plate_thick))
        textDown = ""
        self.dataObj.drawOrientedArrow(dwg, plt_pt, theta, "SE", offset, textUp, textDown)
        
        # Weld Information
        weldPt = self.P
        theta = 40
        offset = self.dataObj.weld_thick + self.dataObj.plate_thick + self.dataObj.beam_B /2 + 80
        textUp = "          z " + str(int(self.dataObj.weld_thick)) + " mm"
        textDown = u"\u25C1"
        self.dataObj.drawOrientedArrow(dwg, weldPt, theta, "NW", offset, textUp, textDown)
        
        # Gap Informatoin
        ptG1 = self.E + 50 * np.array([0,1])
        ptG2 = ptG1 + self.dataObj.gap * np.array([1,0]) 
        offset = 100
        params = {"offset": offset, "textoffset": 10, "lineori": "right", "endlinedim":10,"arrowlen":50}
        self.dataObj.draw_dimension_innerArrow(dwg, ptG1, ptG2, str(self.dataObj.gap) + " mm", params)
            # Draw Faint Lines to representation of Gap distance #
        ptA = self.E
        ptB = ptA + (85) * np.array([0,1])
        self.dataObj.drawFaintLine(ptA,ptB,dwg)
        ptC = self.A4
        ptD = ptC + (100) * np.array([0,1])
        self.dataObj.drawFaintLine(ptC,ptD,dwg)
        
        dwg.save()
        print"$$$$$$$$$ Saved Column Web Beam Web Top $$$$$$$$$$$"


            
class Fin2DCreatorSide(object):
    def __init__(self,finCommonObj):
        
        self.dataObj = finCommonObj
        
        # CWBW connectivity points
        self.A = np.array([0,0])
        self.B = self.A + self.dataObj.col_T * np.array([1,0])
        self.C = self.A + (self.dataObj.D_col - self.dataObj.col_T) * np.array([1,0])
        self.D = self.A + self.dataObj.D_col * np.array([1,0])
        self.H = self.C + self.dataObj.col_L * np.array([0,1])
        self.G = self.B + self.dataObj.col_L * np.array([0,1])
        self.A1 = (self.dataObj.col_T + self.dataObj.col_R1) * np.array((1,0)) + ((self.dataObj.col_L - self.dataObj.D_beam)/2) * np.array([0,1])
        self.A2 = self.A1 + self.dataObj.beam_B * np.array([1,0])
        self.A3 = self.A2 + self.dataObj.beam_T * np.array([0,1])
        self.A12 = self.A1 + self.dataObj.beam_T * np.array([0,1])
        self.A11 = self.A12 + (self.dataObj.beam_B - self.dataObj.beam_tw)/2 * np.array([1,0])
        self.A4 = self.A11 + self.dataObj.beam_tw * np.array([1,0])
        self.A5 = self.A4 + (self.dataObj.D_beam - (2* self.dataObj.beam_T)) * np.array([0,1])
        self.A6 = self.A2 + (self.dataObj.D_beam - self.dataObj.beam_T) * np.array([0,1])
        self.A7 = self.A2 + self.dataObj.D_beam * np.array([0,1])
        self.A8 = self.A1 + self.dataObj.D_beam * np.array([0,1])
        self.A9 = self.A1 + (self.dataObj.D_beam - self.dataObj.beam_T) * np.array([0,1])
        self.A10 = self.A11 + (self.dataObj.D_beam - (2* self.dataObj.beam_T)) * np.array([0,1])
        self.P = self.A11 + (self.dataObj.beam_R1 + 3) * np.array([0,1])
        self.Q = self.P + self.dataObj.plate_thick * np.array([-1,0])
        self.X = self.Q + self.dataObj.weld_thick * np.array([-1,0])
        self.R = self.P + self.dataObj.plate_ht * np.array([0,1])
        
        #### CFBW connectivity
        self.FA = np.array([0,0])
        self.FB = self.FA + self.dataObj.col_B * np.array([1,0])
        self.ptMid = self.FA + ((self.dataObj.col_B/2) + (self.dataObj.col_tw/2))* np.array([1,0])
        self.ptMid1 = self.ptMid + ((self.dataObj.col_L - self.dataObj.D_beam)/2) * np.array([0,1])
        self.FC = self.FB + self.dataObj.col_L * np.array([0,1])
        self.FD = self.FA + self.dataObj.col_L * np.array([0,1])
        self.FA1 = self.ptMid1 + (self.dataObj.beam_tw/2)* np.array([-1,0])+ self.dataObj.beam_B/2 * np.array([-1,0])
        self.FA2 = self.FA1 + self.dataObj.beam_B * np.array([1,0])
        self.FA3 = self.FA2 + self.dataObj.beam_T * np.array([0,1])
        self.FA12 = self.FA1 + self.dataObj.beam_T * np.array([0,1])
        self.FA11 = self.FA12 + (self.dataObj.beam_B - self.dataObj.beam_tw)/2 * np.array([1,0])
        self.FA4 = self.FA11 + self.dataObj.beam_tw * np.array([1,0])
        self.FA5 = self.FA4 + (self.dataObj.D_beam - (2* self.dataObj.beam_T)) * np.array([0,1])
        self.FA6 = self.FA2 + (self.dataObj.D_beam - self.dataObj.beam_T) * np.array([0,1])
        self.FA7 = self.FA2 + self.dataObj.D_beam * np.array([0,1])
        self.FA8 = self.FA1 + self.dataObj.D_beam * np.array([0,1])
        self.FA9 = self.FA1 + (self.dataObj.D_beam - self.dataObj.beam_T) * np.array([0,1])
        self.FA10 = self.FA11 + (self.dataObj.D_beam - (2* self.dataObj.beam_T)) * np.array([0,1])
        self.FP = self.FA11 + (self.dataObj.beam_R1 + 3) * np.array([0,1])
        self.FQ = self.FP + self.dataObj.plate_thick * np.array([-1,0])
        self.FX = self.FQ + self.dataObj.weld_thick * np.array([-1,0])
        self.FR = self.FP + self.dataObj.plate_ht * np.array([0,1])
        self.FY = self.FX + self.dataObj.plate_ht * np.array([0,1])
    
    def callCWBWSide(self):
        '''
        '''
        dwg = svgwrite.Drawing('finSide.svg', profile='full')
        dwg.add(dwg.rect(insert=(self.A), size=(self.dataObj.D_col, self.dataObj.col_L),fill = 'none', stroke='blue', stroke_width=2.5))
        dwg.add(dwg.line((self.C),(self.H)).stroke('blue',width = 2.5,linecap = 'square'))
        dwg.add(dwg.line((self.B),(self.G)).stroke('blue',width = 2.5,linecap = 'square'))
        dwg.add(dwg.polyline(points=[(self.A1),(self.A2),(self.A3),(self.A4),(self.A5),(self.A6),(self.A7),(self.A8),(self.A9),(self.A10),(self.A11),(self.A12),(self.A1)], stroke='blue', fill='none', stroke_width=2.5))
        
        # Diagonal Hatching for WELD
        pattern = dwg.defs.add(dwg.pattern(id ="diagonalHatch",size=(6, 6), patternUnits="userSpaceOnUse",patternTransform="rotate(45 2 2)"))
        pattern.add(dwg.path(d = "M -1,2 l 6,0", stroke='#000000',stroke_width = 0.7))
        dwg.add(dwg.rect(insert=(self.X), size=(self.dataObj.weld_thick, self.dataObj.plate_ht),fill = "url(#diagonalHatch)", stroke='white', stroke_width=2.5))
        
        dwg.add(dwg.rect(insert=(self.Q), size=(self.dataObj.plate_thick, self.dataObj.plate_ht),fill = 'none', stroke='blue', stroke_width=2.5))
        
        nr = self.dataObj.no_of_rows
        pitchPts = []
        for row in range(nr):
            pt = self.P + self.dataObj.end_dist * np.array([0,1]) + (row) *self.dataObj.pitch  * np.array([0,1])
            ptOne = pt + 20 * np.array([1,0])
            ptTwo = pt + 30 * np.array([-1,0])
            dwg.add(dwg.circle(center=(pt), r = 1.5, stroke='red',fill = 'none',stroke_width=1.5))
            dwg.add(dwg.line((ptOne),(ptTwo)).stroke('red',width = 1.5,linecap = 'square').dasharray(dasharray = ([10, 5, 1, 5])))   
            bltPt1 = pt + self.dataObj.bolt_dia/2 * np.array([0,-1]) + self.dataObj.plate_thick * np.array([-1,0]) 
            bltPt2 = pt + self.dataObj.bolt_dia/2 * np.array([0,-1]) + self.dataObj.beam_tw * np.array([1,0])
            bltPt3 = pt + self.dataObj.bolt_dia/2 * np.array([0,1]) + self.dataObj.plate_thick * np.array([-1,0])
            bltPt4 = pt +  self.dataObj.bolt_dia/2 * np.array([0,1]) + self.dataObj.beam_tw * np.array([1,0]) 
            dwg.add(dwg.line((bltPt1),(bltPt2)).stroke('black',width = 1.5,linecap = 'square'))   
            dwg.add(dwg.line((bltPt3),(bltPt4)).stroke('black',width = 1.5,linecap = 'square'))   
            pitchPts.append(pt)
        
        # End and Pitch Distance Information
        params = {"offset": self.dataObj.D_col / 2 + 30, "textoffset": 15, "lineori": "left", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg, np.array(pitchPts[0]), np.array(pitchPts[len( pitchPts)-1]),str(len(pitchPts)-1)+u' \u0040'+ str(int(self.dataObj.pitch)) + " mm c/c", params)     
        params = {"offset": self.dataObj.D_col / 2 + 30, "textoffset": 15, "lineori": "left", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg, self.P, np.array(pitchPts[0]), str(int(self.dataObj.end_dist)) + " mm ", params)     
        params = {"offset": self.dataObj.D_col / 2 + 30, "textoffset": 15, "lineori": "left", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg, np.array(pitchPts[len( pitchPts)-1]), self.R, str(int(self.dataObj.end_dist)) + " mm", params)     
        
        # Draw Faint Line
        pt2 = self.P + ((self.dataObj.D_col /2) + 15) * np.array([1,0])
        self.dataObj.drawFaintLine(self.P,pt2,dwg)
        pt1 = np.array(pitchPts[0]) + ((self.dataObj.D_col /2) + 15) * np.array([1,0])
        self.dataObj.drawFaintLine(np.array(pitchPts[0]),pt1,dwg)
        ptA = self.R + ((self.dataObj.D_col /2) + 15) * np.array([1,0])
        self.dataObj.drawFaintLine(self.R,ptA,dwg)
        ptB = np.array(pitchPts[len( pitchPts)-1]) + ((self.dataObj.D_col /2) + 15) * np.array([1,0])
        self.dataObj.drawFaintLine(np.array(pitchPts[len( pitchPts)-1]),ptB,dwg)
        
        # Beam Information
        beam_pt = self.A2
        theta = 45
        offset = self.dataObj.col_T + self.dataObj.col_R1 + 10 
        textUp = "Beam " + self.dataObj.beam_Designation
        textDown = ""
        self.dataObj.drawOrientedArrow(dwg, beam_pt, theta, "NE", offset, textUp, textDown)
        
        # column  Information
        col_pt = self.H
        theta = 45
        offset = 70
        textUp = "Column " + self.dataObj.col_Designation
        textDown = " " 
        self.dataObj.drawOrientedArrow(dwg, col_pt, theta, "SE", offset, textUp, textDown)
        
        # Plate  Information
        beam_pt = self.R + self.dataObj.plate_thick/2 * np.array([-1,0])
        theta = 45
        offset =  self.dataObj.plate_thick + self.dataObj.beam_B /2 + 80
        textUp = "PLT. " + str(int(self.dataObj.plate_ht))+'x'+ str(int(self.dataObj.plate_width))+ 'x' + str(int(self.dataObj.plate_thick))
        textDown = ""
        self.dataObj.drawOrientedArrow(dwg, beam_pt, theta, "SE", offset, textUp, textDown)
        
        # Weld Information
        weldPt = self.X + self.dataObj.weld_thick/2 * np.array([1,0])
        theta = 45
        offset = self.dataObj.weld_thick + self.dataObj.plate_thick + self.dataObj.beam_B /2 + 80
        textUp = "          z " + str(int(self.dataObj.weld_thick)) + " mm"
        textDown = u"\u25C1"
        self.dataObj.drawOrientedArrow(dwg, weldPt, theta, "NE", offset, textUp, textDown)
        
        dwg.save()
        print "********* Column Web Beam Web Side Saved ***********"
    
    def callCFBWSide(self):
        '''
        '''
        dwg = svgwrite.Drawing('finSide.svg', profile='full')
        dwg.add(dwg.rect(insert=(self.FA), size=(self.dataObj.col_B, self.dataObj.col_L),fill = 'none', stroke='blue', stroke_width=2.5))
        dwg.add(dwg.polyline(points=[(self.FA1),(self.FA2),(self.FA3),(self.FA4),(self.FA5),(self.FA6),(self.FA7),(self.FA8),(self.FA9),(self.FA10),(self.FA11),(self.FA12),(self.FA1)], stroke='blue', fill='none', stroke_width=2.5))
        
        # Diagonal Hatching for WELD
        pattern = dwg.defs.add(dwg.pattern(id ="diagonalHatch",size=(6, 6), patternUnits="userSpaceOnUse",patternTransform="rotate(45 2 2)"))
        pattern.add(dwg.path(d = "M -1,2 l 6,0", stroke='#000000',stroke_width = 0.7))
        dwg.add(dwg.rect(insert=(self.FX), size=(self.dataObj.weld_thick, self.dataObj.plate_ht),fill = "url(#diagonalHatch)", stroke='white', stroke_width=2.5))
        
        dwg.add(dwg.rect(insert=(self.FQ), size=(self.dataObj.plate_thick, self.dataObj.plate_ht),fill = 'none', stroke='blue', stroke_width=2.5))#dwg.add(dwg.line((self.ptMid),(self.ptMid1)).stroke('green',width = 2.5,linecap = 'square'))

        nr = self.dataObj.no_of_rows
        pitchPts = []
        for row in range(nr):
            pt = self.FP + self.dataObj.end_dist * np.array([0,1]) + (row) *self.dataObj.pitch  * np.array([0,1])
            ptOne = pt + 20 * np.array([1,0])
            ptTwo = pt + 30 * np.array([-1,0])
            dwg.add(dwg.line((ptOne),(ptTwo)).stroke('red',width = 1.5,linecap = 'square').dasharray(dasharray = ([10, 5, 1, 5])))   
            bltPt1 = pt + self.dataObj.bolt_dia/2 * np.array([0,-1]) + self.dataObj.plate_thick * np.array([-1,0]) 
            bltPt2 = pt + self.dataObj.bolt_dia/2 * np.array([0,-1]) + self.dataObj.beam_tw * np.array([1,0])
            bltPt3 = pt + self.dataObj.bolt_dia/2 * np.array([0,1]) + self.dataObj.plate_thick * np.array([-1,0])
            bltPt4 = pt +  self.dataObj.bolt_dia/2 * np.array([0,1]) + self.dataObj.beam_tw * np.array([1,0]) 
            dwg.add(dwg.line((bltPt1),(bltPt2)).stroke('black',width = 1.5,linecap = 'square'))   
            dwg.add(dwg.line((bltPt3),(bltPt4)).stroke('black',width = 1.5,linecap = 'square'))
            pitchPts.append(pt)
                            
        params = {"offset": self.dataObj.col_B / 2 + 30, "textoffset": 15, "lineori": "left", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg, np.array(pitchPts[0]), np.array(pitchPts[len( pitchPts)-1]),str(len(pitchPts)-1)+u' \u0040'+ str(int(self.dataObj.pitch)) + "mm c/c", params)     
        params = {"offset": self.dataObj.col_B / 2 + 30, "textoffset": 15, "lineori": "left", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg, self.FP, np.array(pitchPts[0]), str(int(self.dataObj.end_dist)) + " mm ", params)     
        params = {"offset": self.dataObj.col_B / 2 + 30, "textoffset": 15, "lineori": "left", "endlinedim":10}
        self.dataObj.draw_dimension_outerArrow(dwg, np.array(pitchPts[len( pitchPts)-1]), self.FR, str(int(self.dataObj.end_dist)) + " mm", params)     
        
        # Draw Faint Line
        pt2 = self.FP  + ((self.dataObj.col_B /2) + 15) * np.array([1,0])
        self.dataObj.drawFaintLine(self.FP,pt2,dwg)
        pt1 = np.array(pitchPts[0]) + ((self.dataObj.col_B /2) + 15) * np.array([1,0])
        self.dataObj.drawFaintLine(np.array(pitchPts[0]),pt1,dwg)
        ptA = self.FR + ((self.dataObj.col_B /2) + 15) * np.array([1,0])
        self.dataObj.drawFaintLine(self.FR,ptA,dwg)
        ptB = np.array(pitchPts[len( pitchPts)-1]) + ((self.dataObj.col_B /2) + 15) * np.array([1,0])
        self.dataObj.drawFaintLine(np.array(pitchPts[len( pitchPts)-1]),ptB,dwg)
        
        # Beam Information
        beam_pt = self.FA2
        theta = 45
        offset = self.dataObj.col_T + self.dataObj.col_R1 + 10 
        textUp = "Beam " + self.dataObj.beam_Designation
        textDown = ""
        self.dataObj.drawOrientedArrow(dwg, beam_pt, theta, "NE", offset, textUp, textDown)
        
        # column  Information
        beam_pt = self.FC
        theta = 45
        offset = 70
        textUp = "Column " + self.dataObj.col_Designation
        textDown = " " 
        self.dataObj.drawOrientedArrow(dwg, beam_pt, theta, "SE", offset, textUp, textDown)
        
        # Plate  Information
        beam_pt = self.FR + self.dataObj.plate_thick/2 * np.array([-1,0])
        theta = 45
        offset =  self.dataObj.plate_thick + self.dataObj.beam_B /2 + 80
        textUp = "PLT. " + str(int(self.dataObj.plate_ht))+'x'+ str(int(self.dataObj.plate_width))+ 'x' + str(int(self.dataObj.plate_thick))
        textDown = ""
        self.dataObj.drawOrientedArrow(dwg, beam_pt, theta, "SE", offset, textUp, textDown)
        
        # Weld Information
        weldPt = self.FX + self.dataObj.weld_thick/2 * np.array([1,0])
        theta = 45
        offset = self.dataObj.weld_thick + self.dataObj.plate_thick + self.dataObj.beam_B /2 + 80
        textUp = "          z " + str(int(self.dataObj.weld_thick)) + " mm"
        textDown = u"\u25C1"
        self.dataObj.drawOrientedArrow(dwg, weldPt, theta, "NE", offset, textUp, textDown)
        dwg.save()
        print "********** Column Flange Beam Web Side Saved  *************"
        
    
        

        