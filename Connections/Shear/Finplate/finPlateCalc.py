'''
Created on 07-Aug-2014

@author: subhrajit
'''
    
import math
from model import *
from PyQt4.Qt import QString
import logging
flag  = 1
logger = None

def module_setup():
    
    global logger
    logger = logging.getLogger("osdag.finPlateCalc")

module_setup()

def finConn(uiObj):
    global flag
    global logger
    '''(Dictionary) --> Dictionary
    '''
    
    beam_sec = uiObj['Member']['beamSection']
    column_sec = uiObj['Member']['columSection']
    connectivity = uiObj['Member']['connectivity']
    f_u = uiObj['Member']['fu(MPa)']
    f_y = uiObj['Member']['fy(MPa)']
    
    F = uiObj['Load']['shearForce(kN)']
    	
    bolt_dia = uiObj['Bolt']['diameter(mm)']
    bolt_type  = uiObj["Bolt"]["type"]
    bolt_grade = uiObj['Bolt']['grade']
    
    plate_thk = uiObj['Plate']['thickness(mm)']
    plate_width = uiObj['Plate']['width(mm)']
    plate_len = uiObj['Plate']['height(mm)']
    
    weld_thk = uiObj["Weld"]['size(mm)']
    FOS_u = 1.25
    FOS_n = 1.1
    k_b = 0.5
    dictbeamdata  = get_beamdata(beam_sec)
    print dictbeamdata
    t_wb = float(dictbeamdata[QString("tw")])
    d_web_b = float(dictbeamdata[QString("D")])
    mu_f = 0.55
    
    #------- tw of beamt_wb = 8.9      # Thickness of web of the connected member ISMB 400
    #-----D of beam d_web_b = 380   #column Clear depth of web of the connected member ISMB 400
    no_row_b = 3
    no_col_b = 1
#------------------------------------------------------------------------------ 
    #---------------------------------------------------------- # Fin plate data
    #------------------------------------------------------------ plate_thk = 10
    #--------------------------------------------------------- plate_width = 100
    #----------------------------------------------------------- plate_len = 300
#------------------------------------------------------------------------------ 
    #------------------------------------------------------------------- F = 140
    # your calculations
    '''
    Design of bolts
    '''
    logger.info("Starting Design Calculations ")
    # Shearing capacity of bolt
    V_dsb = (0.78*math.pi*bolt_dia**2/4 * math.floor(float(bolt_grade))*100)/(math.sqrt(3)*1000*FOS_u) 
    V_dsb = round(V_dsb,3)
    
    
    # Bearing capacity of bolt
    V_dpb = 2.5*k_b*bolt_dia*t_wb*f_u/(FOS_u*1000)
    V_dpb = round(V_dpb,3)
    if V_dsb > V_dpb:
       V_db = V_dpb
    else:
       V_db = V_dsb
      
    #number of bolts
    no_b = math.ceil(F/V_db)
    if no_b <= 2:
        no_b = 3 
           
    # Hole diameter
    if bolt_dia == 12 or bolt_dia == 14:
        dia_h = bolt_dia + 1
    elif bolt_dia == 16 or bolt_dia == 18 or bolt_dia == 20 or bolt_dia == 22 or bolt_dia == 24:
        dia_h = bolt_dia + 2
    else:
        dia_h = bolt_dia + 3    
    
    # End and edge distance
    d_edge = 2 * dia_h
    d_end = 2 * dia_h
    if d_edge < 50 or d_end < 50:
        d_edge = 50
        d_end = 50
    else:
        d_edge = math.ceil(d_edge)
        d_end = math.ceil(d_end)
    
    # Web side plate length and width input
    if plate_len == 0:
        plate_len = d_web_b - 60
    elif plate_len > d_web_b - 60:
        logger.error("The length of the plate is more than the available depth of %2.2f mm " % (plate_len))
        print('Re-enter Length')
    plate_width_min = 2*d_end
    if plate_width == 0:
        plate_width_min = 2*d_end
    if plate_width < plate_width_min:
        logger.error(" Plate width is less than the minimum width required of %2.2f mm " % (plate_width_min))
        #print('Re-enter Width')
    #.......................................................................
        
    plate_len_b = plate_len - 2*d_edge # Length available for bolt group
    pitch_min = 1.5*bolt_dia
    pitch = plate_len_b/(no_b-1)
    pitch = round(pitch,3)
    if no_col_b == 1:
       gauge = 0
    else:
       gauge = 50 
    
    # Deciding on arrangement of bolts    
    no_b_oneline = (plate_len_b//pitch_min) + 1
    
    
        
    if pitch < pitch_min:
        logger.warning("Pitch distance is less than the minimum required")
        #print('Pitch distance is insufficient') 
    
   
        
    
    #.......................................................................
    '''
    Web side plate design
    '''
    
    #if plate_len > d_web_b:
        #print('Reselect the length of plate less than depth of the connected web')
    
    thk_min = round((5*F*1000)/(f_y*plate_len),3)
    
    if thk_min > plate_thk:
        logger.error("The selected thickness of finplate is less than the minimun required")
        flag = 0
        #print('Thickness of fin plate is insufficient')
        
    #d_clear = 20
    x = int(no_b//2)
    M_ext = 0
    for i in range(1,x+1):
        if no_b%2 == 1: 
            M_ext += 2*(i*(pitch**2)/pitch)*V_dsb
        elif no_b%2 == 0:
            M_ext = i*((pitch/2)**2)/(pitch/2)*V_dsb    
    M_ext = round(M_ext/1000,3)
    #print(M_ext) 
        
    M_cap = 1.2*(f_y/FOS_n)*(plate_thk*plate_len**2)/(6*1000)
    M_cap = round(M_cap/(1000),3)
    #print(M_cap) 
    
    if M_cap < M_ext:
        
        logger.error("The flexural moment capacity of the finplate is less than the external moment")
        flag = 0
        #print('The plate design is OK') 
    #flag = False
    
    '''
    Weld Design
    '''
    # Resultant shear on weld
    l_eff_w = plate_len - 2*weld_thk
    #print(l_eff_w)
    H_sh = (M_ext*6000)/(2*(l_eff_w**2))
    #print(H_sh)
    V_sh = F/float(2*l_eff_w) 
    #print(V_sh)
    R_sh = math.sqrt(H_sh**2 + V_sh**2)
    R_sh = round(R_sh,3)
    #print(R_sh)
    
    t_w_ductility = 0.6 * plate_thk / 0.7
    #print(t_w_ductility)
    
    if weld_thk < t_w_ductility:
        thk_weld = int(t_w_ductility)
    else:
        thk_weld = weld_thk
        
    #print(weld_thk)
    
    # Weld strength
    f_wd = f_u/float(math.sqrt(3)*FOS_u)    
    #print(f_wd)
    R_nw = f_wd*0.7*weld_thk/1000
    R_nw = round(R_nw,3)
    # End of calculation
    
    outputObj = {}
    outputObj['Bolt'] ={}
    outputObj['Bolt']['shearcapacity'] = V_dsb
    outputObj['Bolt']['bearingcapacity'] = V_dpb
    outputObj['Bolt']['boltcapacity'] = V_db
    outputObj['Bolt']['numofbolts'] = no_b
    outputObj['Bolt']['boltgrpcapacity'] = 0.0
    outputObj['Bolt']['numofrow'] = no_row_b
    outputObj['Bolt']['numofcol'] = no_col_b
    outputObj['Bolt']['pitch'] = pitch
   
    outputObj['Bolt']['enddist'] = d_end
    
    outputObj['Bolt']['edge'] = d_edge
    outputObj['Bolt']['gauge'] = gauge
    
    outputObj['Weld'] = {}
    outputObj['Weld']['thickness'] = thk_weld
    outputObj['Weld']['resultantshear'] = R_sh
    outputObj['Weld']['weldstrength'] = R_nw
    
    outputObj['Plate'] = {}
    outputObj['Plate']['height'] = 0
    outputObj['Plate']['width'] = 0
    outputObj['Plate']['externalmoment'] = M_ext
    outputObj['Plate']['momentcapacity'] = M_cap

    if flag != 0:
        logger.info("Design is safe")
    else:
        logger.error("Design is not safe")
    return outputObj

