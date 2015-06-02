'''
Created on 10-Nov-2014

@author: deepa
'''

#from OCC.Display.SimpleGui import init_display

from exampleSimpleGUI import init_display
from OCC._Quantity import Quantity_NOC_BLACK
from ISection import ISection
import numpy
from OCC.Graphic3d import Graphic3d_NOT_2D_ALUMINUM
from weld import Weld
from plate import Plate
from bolt import Bolt
from OCC.Quantity import Quantity_NOC_SADDLEBROWN, Quantity_NOC_CYAN1
from nut import Nut
from OCC.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.AIS import AIS_Shape
from OCC.TopAbs import TopAbs_EDGE
from OCC.TopExp import TopExp_Explorer
from OCC.TopoDS import topods, TopoDS_Shape
from utilities import osdagDisplayShape


display, start_display, add_menu, add_function_to_menu = init_display(backend_str="pyqt4")

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
plateThickness = 10
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
bolt1 = Bolt(R = 10.0,T = bolt_T, H = 35.0, r = 4.0 )
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

#nutbody = Nut(R = 10.0,T = 10.0,  H = 6.1, innerR1 = 6.0, outerR2 = 8.3)
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

def colorTheEdges(box, aDisplay):
    #ais_shape = AIS.AIS_Shape(box).GetHandle()
    Ex = TopExp_Explorer(box,TopAbs_EDGE)
    
    while Ex.More():
        aEdge = topods.Edge(Ex.Current())
        ais_shape = AIS_Shape(aEdge).GetHandle()
        ctx = aDisplay.Context
        ctx.SetColor(ais_shape,Quantity_NOC_BLACK,True)
        ctx.SetWidth(ais_shape,3.2)
        ctx.Display(ais_shape)
        Ex.Next()
        ctx.Display(ais_shape)
        
# Call for createModel
iSectionModel1 = iSection1.createModel()
iSectionModel2 = iSection2.createModel()
weldModel = weld.createModel()
plateModel = plate.createModel()
boltModels = []
colorbolts = []
for bolt in bolt_list:
    
    boltModels.append(bolt.createModel())
    for colorbolt in boltModels:
        colorTheEdges(colorbolt,aDisplay)
        colorbolts.append(colorbolt)
    
#color = Quantity_NOC_SADDLEBROWN,
nutModels = []
for nut in nut_list:
    nutModels.append(nut.createModel())
    
# def colorTheEdges(box, aDisplay):
#     #ais_shape = AIS.AIS_Shape(box).GetHandle()
#     Ex = TopExp_Explorer(box,TopAbs_EDGE)
#     
#     while Ex.More():
#         aEdge = topods.Edge(Ex.Current())
#         ais_shape = AIS_Shape(aEdge).GetHandle()
#         ctx = aDisplay.Context
#         ctx.SetColor(ais_shape,Quantity_NOC_BLACK,True)
#         ctx.SetWidth(ais_shape,3.2)
#         ctx.Display(ais_shape)
#         Ex.Next()
        
#
# Get Context
#
ais_context = display.GetContext().GetObject()
#
# Get Prs3d_drawer from previous context
#
drawer_handle = ais_context.DefaultDrawer()
drawer = drawer_handle.GetObject()

drawer.SetIsoOnPlane(True)
# 
la = drawer.LineAspect().GetObject()
la.SetWidth(4)
# le = drawer.SetLineAspect().GetObject()
hla = drawer.HiddenLineAspect().GetObject()
hla.SetWidth(2)
hla.SetColor(Quantity_NOC_CYAN1)
# le.SetLineAspect(Aspect_TOL_DASH,Quantity_NOC_YELLOW,4 )
# increase line width in the current viewer
# This is only viewed in the HLR mode (hit 'e' key for instance)
line_aspect = drawer.SeenLineAspect().GetObject()

drawer.EnableDrawHiddenLine()
line_aspect.SetWidth(4)
#drawer.SetLineAspect('Aspect_TOL_DASH')


#
drawer.SetWireAspect(line_aspect.GetHandle())

# Displys CAD Models.
# Complete CAD Model
isection = BRepAlgoAPI_Fuse(iSectionModel1,iSectionModel2).Shape()
weld_isection = BRepAlgoAPI_Fuse(isection,weldModel).Shape()
plate_weld = BRepAlgoAPI_Fuse(weld_isection,plateModel).Shape()

plate_weld_bolt = plate_weld
for bolt in boltModels:
    plate_weld_bolt = BRepAlgoAPI_Fuse(plate_weld_bolt, bolt).Shape()
    
#bolt_plate = BRepAlgoAPI_Fuse(plate_weld,boltModels).Shape()
final_model = plate_weld_bolt
for nt in nutModels:
    final_model = BRepAlgoAPI_Fuse(final_model,nt).Shape()


# colorTheEdges(final_model)      
#display.DisplayShape(final_model, update = True)
colorTheEdges(iSectionModel1, display)    
display.DisplayShape(iSectionModel1, update=True)
# 
# colorTheEdges(iSectionModel2)   
#display.DisplayShape(iSectionModel2,material = Graphic3d_NOT_2D_ALUMINUM, update=True)
# 
# colorTheEdges(weldModel)  
#display.DisplayShape(weldModel,color = 'red', update=True)
# 
# colorTheEdges(plateModel)   
#display.DisplayShape(plateModel,color = 'blue', update=True)
#
#colorTheEdges(boltModels)   
#display.DisplayShape(colorbolts,color = Quantity_NOC_SADDLEBROWN, update=True)
# 
# #colorTheEdges(nutModels)   
#display.DisplayShape(nutModels,color = Quantity_NOC_SADDLEBROWN, update = True)
#display.SetModeHLR()
display.FitAll()

#display.View_Front()
#display.View_Top()
#display.View_Right()
#display.View_Iso()
#display.FitAll()
start_display()

