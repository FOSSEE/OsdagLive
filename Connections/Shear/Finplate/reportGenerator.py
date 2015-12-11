'''
Created on Dec 10, 2015

@author: deepa
'''
def save_html(): # (outObj, uiObj, dictBeamData, dictColData)
    fileName = '/home/deepa/finPlateReport.html'
    f = open(fileName,'w')
    f.write(t('html'))
    f.write(t('head'))
    f.write(t('''link rel="stylesheet" type="text/css" href="mystyle.css"'''))
    f.write(t('/head'))
    f.write(t('body')) 
    f.write(t('img src="Osdag.png" align = "middle" style="width:100px;height:100px;"'))       
    f.write(t('img src="Osdagextd.png" align = "down" style="width:100px;height:35px;"'))     
#     data = [
#             [0, "Project Summary", ""],
#             [1, "Project Title", "XXX"],
#             [1, "Company", "XXX"],
#             [1, "Designer", "XXX"],
#             [0, "finplate", ""],
#             [1, "Connection", ""],
#             [2, "Connection Type", "Shear Connection"],
#             [2, "Connectivity", "Column Flange Beam Web"],
#             [2, "Beam Connection", "Bolted and Welded"],
#             [1, "Load(Factored Load)", ""],
#             [2, "Shear Force(kH)", "140"],
#             [1, "Components", ""],
#             [2, "Column Section", "ISSC200"],
#             [3, "Steel Grade", "410"],
#             [3, "Steel Type", "250"],
#             [2, "Beam Section", "ISMB 400"],
#             [2, "Plate Section", ""],
#             [3, "Thickness", "xx"],
#             [3, "Width", "xx"],
#             [3, "Depth", "xx"],
#             ]

    
    #---------------------
    rstr = t('table')
    rstr += t('''col width=70%''')
    rstr += t('''col width=30%''')
    
    row  = [0,' ', '']
    rstr += t('tr')
    rstr += t('td img src="Osdag.png" alt="Mountain View"align = "middle" style="width:100px;height:100px;') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
    rstr = t('table')
    
    rstr = t('table')
    rstr += t('''col width=70%''')
    rstr += t('''col width=30%''')
    
#     row  = [0,' ', '']
#     rstr += t('tr')
#     rstr += t('td img src="Osdag.png" alt="Mountain View"align = "middle" style="width:100px;height:100px;') + space(row[0]) + row[1] + t('/td')
#     rstr += t('/tr')
    
    row = [0, 'Project Summary', ' ']
    rstr += t('tr')
    rstr += t('td colspan="2" class="header0"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')

    row = [1, "Project Title", "FinPlate Connection"]
    rstr += t('tr')
    rstr += t('td class="header1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header1"') + row[2] + t('/td')
    rstr += t('/tr')

    row = [1, "Company", "Osdag"]
    rstr += t('tr')
    rstr += t('td class="header1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header1"') + row[2] + t('/td')
    rstr += t('/tr')

    row = [1, "Designer", "Hashmi"]
    rstr += t('tr')
    rstr += t('td class="header1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header1"') + row[2] + t('/td')
    rstr += t('/tr')
    
    row = [1, "Job Number", "test_1"]
    rstr += t('tr')
    rstr += t('td class="header1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header1"') + row[2] + t('/td')
    rstr += t('/tr')
    
    row = [1, "Design Code/Method", "IS800:2007/Limit state design"]
    rstr += t('tr')
    rstr += t('td class="header1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header1"') + row[2] + t('/td')
    rstr += t('/tr')
    
    row = [0, "Design Conclusion", "IS800:2007/Limit state design"]
    rstr += t('tr')
    rstr += t('td colspan="2" class="header0"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
     
    row = [1, "Finplate", "Pass"]
    rstr += t('tr')
    rstr += t('td class="header1 "') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header1 safe"') + row[2] + t('/td')
    rstr += t('/tr')
    
    row = [0, "Finplate", " "]
    rstr += t('tr')
    rstr += t('td colspan="2" class="header0"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
    
    row = [0, "Connection Properties", " "]
    rstr += t('tr')
    rstr += t('td colspan="2" class="header1_1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
    
    row = [0, "Connection ", " "]
    rstr += t('tr')
    rstr += t('td colspan="2" class="header1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
    
    row = [1, "Connection Title", " Single Finplate"]
    rstr += t('tr')
    rstr += t('td class="header2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2 "') + row[2] + t('/td')
    rstr += t('/tr')
    
    row = [1, "Connection Type", "Shear Connection"]
    rstr += t('tr')
    rstr += t('td class="header2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2 "') + row[2] + t('/td')
    rstr += t('/tr')
    
    row = [0, "Connection Category ", " "]
    rstr += t('tr')
    rstr += t('td colspan="2" class="header1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
    
    row = [1, "Beam Connection", "Bolted and Welded"]
    rstr += t('tr')
    rstr += t('td class="header2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2 "') + row[2] + t('/td')
    rstr += t('/tr')
    
    row = [1, "Connectivity", "Column Flange Beam Web"]
    rstr += t('tr')
    rstr += t('td class="header2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2 "') + row[2] + t('/td')
    rstr += t('/tr')
    
    row = [0, "Loading (Factored Load) ", " "]
    rstr += t('tr')
    rstr += t('td colspan="2" class="header1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
    
    row = [1, "Shear Force (kN)", "140"]
    rstr += t('tr')
    rstr += t('td class="header2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2 "') + row[2] + t('/td')
    rstr += t('/tr')
    
    row = [0, "Components ", " "]
    rstr += t('tr')
    rstr += t('td colspan="2" class="header1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
    
    row = [1, "Column Section", "ISSC 200"]
    rstr += t('tr')
    rstr += t('td class="header1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2 "') + row[2] + t('/td')
    rstr += t('/tr')
    
    row = [2, "Material", "Fe250"]
    rstr += t('tr')
    rstr += t('td class="header2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2 "') + row[2] + t('/td')
    rstr += t('/tr')
    
    row = [1, "Beam Section", "ISMB 400"]
    rstr += t('tr')
    rstr += t('td class="header1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2 "') + row[2] + t('/td')
    rstr += t('/tr')
    
    row = [2, "Material", "Fe250"]
    rstr += t('tr')
    rstr += t('td class="header2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2 "') + row[2] + t('/td')
    rstr += t('/tr')
    
    row = [2, "Hole", "STD"]
    rstr += t('tr')
    rstr += t('td class="header2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2 "') + row[2] + t('/td')
    rstr += t('/tr')
    
    row = [1, "Plate Section ", "PLT 300X10X100 "]
    rstr += t('tr')
    rstr += t('td class="header1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2 "') + row[2] + t('/td')
    rstr += t('/tr')
    
    row = [2, "Thickness (mm)", "10"]
    rstr += t('tr')
    rstr += t('td class="header2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2 "') + row[2] + t('/td')
    rstr += t('/tr')
    
    row = [2, "Width (mm)", "10"]
    rstr += t('tr')
    rstr += t('td class="header2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2 "') + row[2] + t('/td')
    rstr += t('/tr')
    
    row = [2, "Depth (mm)", "300"]
    rstr += t('tr')
    rstr += t('td class="header2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2 "') + row[2] + t('/td')
    rstr += t('/tr')
    
    row = [2, "Hole", "STD"]
    rstr += t('tr')
    rstr += t('td class="header2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2 "') + row[2] + t('/td')
    rstr += t('/tr')
    
    row = [1, "Weld ", " "]
    rstr += t('tr')
    rstr += t('td colspan="2" class="header1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
    
    row = [2, "Type", "Double Fillet"]
    rstr += t('tr')
    rstr += t('td class="header2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2 "') + row[2] + t('/td')
    rstr += t('/tr')
    
    row = [2, "Size (mm)", "6"]
    rstr += t('tr')
    rstr += t('td class="header2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2 "') + row[2] + t('/td')
    rstr += t('/tr')
    
    row = [1, "Bolts ", " "]
    rstr += t('tr')
    rstr += t('td colspan="2" class="header1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
    
    row = [2, "Type", "HSFG"]
    rstr += t('tr')
    rstr += t('td class="header2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2 "') + row[2] + t('/td')
    rstr += t('/tr')
    
    row = [2, "Grade", "8.8"]
    rstr += t('tr')
    rstr += t('td class="header2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2 "') + row[2] + t('/td')
    rstr += t('/tr')
    
    row = [2, "Diameter (mm)", "20"]
    rstr += t('tr')
    rstr += t('td class="header2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2 "') + row[2] + t('/td')
    rstr += t('/tr')
    
    row = [2, "Bolt Numbers", "3"]
    rstr += t('tr')
    rstr += t('td class="header2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2 "') + row[2] + t('/td')
    rstr += t('/tr')
    
    row = [2, "Columns (Vertical Lines)", "1 "]
    rstr += t('tr')
    rstr += t('td class="header2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2 "') + row[2] + t('/td')
    rstr += t('/tr')
    
    row = [2, "Bolts Per Column", "3"]
    rstr += t('tr')
    rstr += t('td class="header2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2 "') + row[2] + t('/td')
    rstr += t('/tr')
    
    row = [2, "Gauge (mm)", "0"]
    rstr += t('tr')
    rstr += t('td class="header2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2 "') + row[2] + t('/td')
    rstr += t('/tr')
    
    row = [2, "Pitch (mm)", "100"]
    rstr += t('tr')
    rstr += t('td class="header2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2 "') + row[2] + t('/td')
    rstr += t('/tr')
    
    row = [2, "End Distance (mm)", "50"]
    rstr += t('tr')
    rstr += t('td class="header2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2"') + row[2] + t('/td')
    rstr += t('/tr')
    
    row = [2, "Edge Distance (mm)", "50"]
    rstr += t('tr')
    rstr += t('td class="header2"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2 "') + row[2] + t('/td')
    rstr += t('/tr')
    
    row = [0, "Assembly ", " "]
    rstr += t('tr')
    rstr += t('td colspan="2" class="header1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
    
    row = [1, "Column-Beam Clearance (mm)", "20"]
    rstr += t('tr')
    rstr += t('td class="header1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('td class="header2 "') + row[2] + t('/td')
    rstr += t('/tr')
    
    rstr += t('/table')
    
    rstr += t('table')
    row = [0, "3D View", " "]
    rstr += t('tr')
    rstr += t('td colspan="2" class="header1_1"') + space(row[0]) + row[1] + t('/td')
    rstr += t('/tr')
    rstr += t('/table')
    

    f.write(rstr)
    f.write(t('/body'))        
    f.write(t('/html'))    
    f.close()
    

def space(n):
    rstr = "&nbsp;" * 4 * n
    return rstr

def t(n):
    return '<' + n + '>'

def quote(m):
    return '"' + m + '"'

if __name__ == '__main__':
    save_html()
    print "hiiiiii"