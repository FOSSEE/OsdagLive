'''
Created on 24-Aug-2015

@author: deepa
'''
import svgwrite
from svgwrite import mm
from PyQt4.QtCore import QString
import numpy as np

class Fin2DCreatorFront(object):
    
    def __init__(self, inputObj,ouputObj,dictBeamdata,dictColumndata):
        
        beam_T = float(dictBeamdata[QString("T")])
        D = int (dictBeamdata[QString("D")])
        col_B = int(dictColumndata[QString("B")])
        col_tw = float(dictColumndata[QString("tw")])
        col_R1 = float(dictColumndata[QString("R1")])
        plate_ht= ouputObj['Plate']['height'] 
        plate_width = ouputObj['Plate']['width']
        weld_len = ouputObj['Plate']['height']
        weld_thick =  ouputObj['Weld']['thickness']
        self.bolt_dia  = inputObj["Bolt"]["Diameter (mm)"]
        self.pitch = ouputObj['Bolt']["pitch"]
        self.gauge = ouputObj['Bolt']["gauge"]
        self.end_dist = ouputObj['Bolt']["enddist"]
        self.edge_dist = ouputObj['Bolt']["edge"]
        self.no_of_rows = ouputObj['Bolt']["numofrow"] 
        self.no_of_col = ouputObj['Bolt']["numofcol"]
        self.col_L = 1000
        self.beam_L = 500
        
        
        self.A2 =(col_B,(self.col_L-D)/2)
        self.B = (col_B,0)
        self.A = (0,0)
        self.D = (0,self.col_L)
        self.C = (col_B,self.col_L)
        self.B2 = (col_B,(D + self.col_L)/2)
        
        ptEx = (col_B-col_tw)/2
        ptEy = 0.0
        self.E = (ptEx,ptEy)
        ptHx = (col_B-col_tw)/2
        ptHy = self.col_L
        self.H = (ptHx,ptHy)
        ptFx = (col_B + col_tw)/2
        ptFy = 0
        self.F = (ptFx,ptFy)
        ptGx = (col_B + col_tw)/2
        ptGy = self.col_L
        self.G = (ptGx,ptGy)
        
        #Draw rectangle for finPlate PRSU
        ptPx = (col_B + col_tw)/2
        ptPy = ((self.col_L - D)/2) + (beam_T + col_R1 + 3)
        self.P = (ptPx,ptPy) 
        self.ptP = np.array([ptPx,ptPy])
        
        self.plate_ht = plate_ht
        self.plate_width = plate_width
        self.weld_thick = weld_thick
        self.weld_len = weld_len
        # Draw Rectangle for weld
        ptCx1 = ((col_B + col_tw)/2 + 20)
        ptCy1 = ((self.col_L - D)/2) + (beam_T + col_R1 + 3)
        self.C1 =(ptCx1,ptCy1)
        
        ptAx1 = ptCx1
        ptAy1 = ((self.col_L - D)/2)
        self.A1 = (ptAx1,ptAy1)
        
        ptAx3 = ptCx1 + self.beam_L
        ptAy3 = ptAy1
        self.A3 = (ptAx3,ptAy3)
        
        ptBx3 = ptAx3
        ptBy3 = ((self.col_L + D)/2 ) 
        self.B3 = (ptBx3,ptBy3)
        
        ptBx1 = ptCx1
        ptBy1 = ptBy3
        self.B1 = (ptBx1,ptBy1)
        
        ptC2x= ptCx1
        ptC2y = ptCy1 + plate_ht
        self.C2 = (ptC2x,ptC2y)
        
        ptAx5 = ptAx1
        ptAy5 = ptAy1 + beam_T
        self.A5 = ptAx5,ptAy5
        
        ptAx4 = ptAx3
        ptAy4 = ptAy3 + beam_T
        self.A4 = (ptAx4,ptAy4)
        
        ptBx4 = ptBx3
        ptBy4 = ptBy3 - beam_T  
        self.B4 = (ptBx4,ptBy4)
        
        ptBx5 = ((col_B + col_tw)/2) + 20
        ptBy5 = ptBy3 - beam_T
        self.B5 = (ptBx5,ptBy5)
        
        ptP1x = ((col_B + col_tw)/2 + self.edge_dist)
        ptP1y = ((self.col_L - D)/2 +(col_tw + col_R1 + 3)+ self.end_dist)
        self.P1 = (ptP1x,ptP1y)
        
        ptP2x = ptP1x
        ptP2y = ptP1y + self.pitch
        self.P2 = (ptP1x,ptP1y)
        
        ptP3x = ptP1x
        ptP3y = ptP2y + self.pitch
        self.P3 = (ptP1x,ptP1y)
        # points for diamension
        
        
    def saveToSvg(self):
            dwg = svgwrite.Drawing('finfront.svg', profile='tiny')
            dwg.add(dwg.polyline(points=[(self.A2),(self.B),(self.A),(self.D),(self.C) ,(self.B2)], stroke='blue', fill='none', stroke_width=2.5))
            dwg.add(dwg.line((self.E),(self.H)).stroke('blue',width = 2.5,linecap = 'square'))
            dwg.add(dwg.line((self.F),(self.G)).stroke('blue',width = 2.5,linecap = 'square'))
            dwg.add(dwg.rect(insert=(self.P), size=(self.plate_width, self.plate_ht),fill = 'none', stroke='blue', stroke_width=2.5))
            dwg.add(dwg.rect(insert=(self.P), size=(self.weld_thick, self.plate_ht),fill = 'none', stroke='blue', stroke_width=2.0))
            #C1,A1,A3,B3,B1,C2
            dwg.add(dwg.polyline(points=[(self.C1),(self.A1),(self.A3),(self.B3),(self.B1),(self.C2)],stroke = 'blue',fill= 'none',stroke_width =2.5))
            #C1,C2
            dwg.add(dwg.line((self.C1),(self.C2)).stroke('red',width = 2.5,linecap = 'square').dasharray(dasharray = ([5,5])))
            #A2,B2
            dwg.add(dwg.line((self.A2),(self.B2)).stroke('red',width = 2.5,linecap = 'square').dasharray(dasharray = ([5,5])))
            dwg.add(dwg.line((self.A5),(self.A4)).stroke('blue',width = 2.5,linecap = 'square'))
            dwg.add(dwg.line((self.B5),(self.B4)).stroke('blue',width = 2.5,linecap = 'square'))
            nr = self.no_of_rows
            nc = self.no_of_col
            bolt_r = self.bolt_dia/2
            for i in range(1,(nr+1)):
                for j in range (1,(nc+1)):
                    pt = self.ptP + self.edge_dist * np.array([1,0]) + self.end_dist * np.array ([0,1]) + \
                        (i-1) * self.pitch * np.array([0,1]) + (j-1) * self.gauge * np.array([1,0])
                    dwg.add(dwg.circle(center=(pt), r = bolt_r, stroke='blue',fill ='black',stroke_width=1.5))
                    ptA = pt - (bolt_r + 4) * np.array([0,1])
                    ptB = pt + (bolt_r + 4) * np.array([0,1])
                    #dwg.add(dwg.line((ptA),(ptB)).stroke('blue',width = 2.0,linecap = 'square'))
                    ptC = pt - (bolt_r + 4) * np.array([1,0])
                    PtD = pt + (bolt_r + 4) * np.array([1,0])
                    dwg.add(dwg.line((ptC),(PtD)).stroke('blue',width = 2.0,linecap = 'square'))
                    ptE = self.ptP + self.edge_dist * np.array([1,0]) +(j-1) * self.gauge * np.array([1,0])
                    ptF = ptE + self.plate_ht * np.array([0,1])
                    dwg.add(dwg.line((ptE),(ptF)).stroke('blue',width = 1.5,linecap = 'square').dasharray(dasharray = ([20, 5, 1, 5])))

            dwg.save()
            print"Saved"
            


    
    
    