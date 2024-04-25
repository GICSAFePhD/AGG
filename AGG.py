import tkinter as tk
import re

class NetElement:
    def __init__(self, canvas, x1, y1, x2, y2, net_elements, net_element_key, color='black'):
        self.id = canvas.create_line(x1, y1, x2, y2, fill=color,width=3)
        self.pressed = False
        self.net_elements = net_elements
        self.net_element_key = net_element_key
        canvas.tag_bind(self.id, "<Button-1>", self.on_net_element_click)

    def on_net_element_click(self, event):
        self.pressed = not self.pressed
        new_color = 'red' if self.pressed else 'black'
        for net_element in self.net_elements.values():
            event.widget.itemconfig(net_element.id, fill=new_color)
        if self.pressed:
            print(f'NetElement {self.net_element_key} is occupied')
        else:
            print(f'NetElement {self.net_element_key} is released')

class BufferStop:
    def __init__(self, canvas, x, y, direction ,color='black'):
        sign = -1 if direction == '>' else 1
        self.id = canvas.create_line(x, y-25, x+sign*10, y-25,x, y-25, x, y+25,x, y+25, x+sign*10, y+25, fill=color,width=3)
        
class Border:
    def __init__(self, canvas, x, y, direction ,color='black'):
        sign = 1 if direction == '>' else -1
        self.id = None
        canvas.create_line(x+sign*5, y, x+sign*10, y, fill=color,width=3)
        canvas.create_line(x+sign*15, y, x+sign*20, y, fill=color,width=3)

class RailJoint:
    def __init__(self, canvas, x, y, color='black'):
        self.id = None
        canvas.create_line(x+10, y+15, x+10 , y-15, fill=color,width=3)
        canvas.create_line(x-10, y+15, x-10 , y-15, fill=color,width=3)

class Platform:
    def __init__(self, canvas, x, y, alignment ,color='red'):
        self.id = None

        if alignment == 'top':
            canvas.create_line(x-75, y-15, x+75, y-15, fill=color,width=3)
            canvas.create_line(x-75, y-15, x-75, y-45, fill=color,width=3)
            canvas.create_line(x+75, y-15, x+75, y-45, fill=color,width=3)
            canvas.create_line(x-75, y-30, x+75, y-30, fill=color,width=3)
        else:
            canvas.create_line(x-75, y+15, x+75, y+15, fill=color,width=3)
            canvas.create_line(x-75, y+15, x-75, y+45, fill=color,width=3)
            canvas.create_line(x+75, y+15, x+75, y+45, fill=color,width=3)
            canvas.create_line(x-75, y+30, x+75, y+30, fill=color,width=3)

class LevelCrossing:
    def __init__(self, canvas, x, y ,color='blue'):
        self.id = None

        canvas.create_line(x+30, y-60, x+30, y+60, fill=color,width=3)
        canvas.create_line(x+30, y-60, x+45, y-75, fill=color,width=3)
        canvas.create_line(x+30, y+60, x+45, y+75, fill=color,width=3)

        canvas.create_line(x-30, y-60, x-30, y+60, fill=color,width=3)
        canvas.create_line(x-30, y-60, x-45, y-75, fill=color,width=3)
        canvas.create_line(x-30, y+60, x-45, y+75, fill=color,width=3)

class Signals:
    def __init__(self, canvas, x, y ,name,color='grey'):
        self.id = None

        canvas.create_text(x,y-40,text=name,fill=color)
        canvas.create_line(x+10, y-30, x+10, y-10, fill=color,width=3)
        canvas.create_line(x+10, y-10, x-10, y-10, fill=color,width=3)
        canvas.create_line(x-10, y-10, x-10, y-30, fill=color,width=3)
        canvas.create_line(x-10, y-30, x+10, y-30, fill=color,width=3)

def get_netElements(RML):
    network = {}
    coords = {}
    NetElements =       RML.Infrastructure.Topology.NetElements
    NetRelations =		RML.Infrastructure.Topology.NetRelations
    SwitchesIS =        RML.Infrastructure.FunctionalInfrastructure.SwitchesIS
    LevelCrossingsIS =  RML.Infrastructure.FunctionalInfrastructure.LevelCrossingsIS
    Platforms =         RML.Infrastructure.FunctionalInfrastructure.Platforms
    Borders =           RML.Infrastructure.FunctionalInfrastructure.Borders
    BufferStops =       RML.Infrastructure.FunctionalInfrastructure.BufferStops
    RailJoints =        RML.Infrastructure.FunctionalInfrastructure.TrainDetectionElements
    Crossings =         RML.Infrastructure.FunctionalInfrastructure.Crossings
    SignalsIS =         RML.Infrastructure.FunctionalInfrastructure.SignalsIS

    visualization = RML.Infrastructure.InfrastructureVisualizations

    if NetElements != None:
        for i in NetElements.NetElement:
            if i.Id not in coords.keys():
                if i.AssociatedPositioningSystem != None:
                    if i.AssociatedPositioningSystem[0].IntrinsicCoordinate != None:
                        if len(i.AssociatedPositioningSystem[0].IntrinsicCoordinate) > 1 and i.AssociatedPositioningSystem[0].IntrinsicCoordinate[0].GeometricCoordinate != None:
                            for j in range(len(i.AssociatedPositioningSystem[0].IntrinsicCoordinate)):
                                x = int(i.AssociatedPositioningSystem[0].IntrinsicCoordinate[j].GeometricCoordinate[0].X[:-4])
                                y = -int(i.AssociatedPositioningSystem[0].IntrinsicCoordinate[j].GeometricCoordinate[0].Y[:-4])
                                if i.Id not in coords:
                                    coords[i.Id] = {}
                                    coords[i.Id] = ((x,y),) 
                                else:
                                    coords[i.Id] += ((x,y),) 
    
    for i in coords:
        for j in range(len(coords[i]) - 1):
            if i not in network:
                network[i] = {}
            network[i] |= {f'line{j+1}' : (coords[i][j], coords[i][j + 1])}

        if network[i]['line1'][0][0] < network[i][f'line{len(coords[i]) - 1}'][1][0]:
            network[i] |= {f'Way' : '>'} 
        else:
            network[i] |= {f'Way' : '<'}

    if BufferStops != None:
        for BufferStop in BufferStops[0].BufferStop:
            node = BufferStop.SpotLocation[0].NetElementRef
            bufferStop = BufferStop.Name[0].Name

            if 'BufferStop' not in network[node]:
                network[node] |= {'BufferStop':{}}
            if bufferStop not in network[node]['BufferStop']:
                network[node]['BufferStop'] |= {bufferStop:()}

    if Borders != None:
        for Border in Borders[0].Border:
            if Border.IsOpenEnd == 'true':
                node = Border.SpotLocation[0].NetElementRef
                border = Border.Name[0].Name

                if 'Border' not in network[node]:
                    network[node] |= {'Border':{}}
                if border not in network[node]['Border']:
                    network[node]['Border'] |= {border:()}
                
    if RailJoints != None:
        for RailJoint in RailJoints[0].TrainDetectionElement:
            if RailJoint.Name[0].Name[0] == 'J':
                node = RailJoint.SpotLocation[0].NetElementRef
                border = RailJoint.Name[0].Name

                if 'RailJoint' not in network[node]:
                    network[node] |= {'RailJoint':{}}
                if border not in network[node]['RailJoint']:
                    network[node]['RailJoint'] |= {border:()}

    if LevelCrossingsIS != None:  
        for LevelCrossingIS in LevelCrossingsIS[0].LevelCrossingIS:
            node = LevelCrossingIS.SpotLocation[0].NetElementRef
            levelCrossing = LevelCrossingIS.Name[0].Name

            if 'LevelCrossing' not in network[node]:
                network[node] |= {'LevelCrossing':{}}
            if levelCrossing not in network[node]['LevelCrossing']:
                network[node]['LevelCrossing'] |= {levelCrossing:()}

    if Platforms != None:
    	for Platform in Platforms[0].Platform:
            node = Platform.LinearLocation[0].AssociatedNetElement[0].NetElementRef
            platform = Platform.Name[0].Name

            if 'Platform' not in network[node]:
                network[node] |= {'Platform':{}}
            if platform not in network[node]['Platform']:
                special = ''
                if Platform.LinearLocation[0].AssociatedNetElement[0].LinearCoordinateBegin != None and Platform.LinearLocation[0].AssociatedNetElement[0].LinearCoordinateBegin.LateralSide != None:
                    special = Platform.LinearLocation[0].AssociatedNetElement[0].LinearCoordinateBegin.LateralSide[0]
                network[node]['Platform'] |= {f'{platform}{special}':()}

    if SwitchesIS != None: 
        for SwitchIS in SwitchesIS[0].SwitchIS:
            if (SwitchIS.Type == "ordinarySwitch"):

                Net = SwitchIS.LeftBranch[0].NetRelationRef.split('_')[1].split('ne')
                nodeLeft1 = 'ne' + Net[1]        
                nodeLeft2 = 'ne' + Net[2]  
                Net = SwitchIS.RightBranch[0].NetRelationRef.split('_')[1].split('ne')
                nodeRight1 = 'ne' + Net[1]        
                nodeRight2 = 'ne' + Net[2]  
                
                continueCourse = SwitchIS.ContinueCourse
                branchCourse = SwitchIS.BranchCourse

                nodeStart = nodeLeft1 if (nodeLeft1 == nodeRight1 or nodeLeft1 == nodeRight2) else nodeLeft2
                nodeLeft = nodeLeft2 if (nodeStart == nodeLeft1) else nodeLeft1
                nodeRight = nodeRight2 if (nodeStart == nodeRight1) else nodeRight1

                nodeContinue = nodeRight if continueCourse == "Right" else nodeLeft
                nodeBranch = nodeLeft if branchCourse == "Left" else nodeRight

                if 'Switch' not in network[nodeStart]:
                    network[nodeStart] |= {'Switch':{}}
                #if 'Switch_C' not in network[nodeContinue]:
                #    network[nodeContinue] |= {'Switch_C':{}}
                #if 'Switch_B' not in network[nodeBranch]:
                #    network[nodeBranch] |= {'Switch_B':{}}

                network[nodeStart]['Switch'] |= {SwitchIS.Name[0].Name:()}
                #network[nodeContinue]['Switch_C'] |= {SwitchIS.Name[0].Name:()} 
                #network[nodeBranch]['Switch_B'] |= {SwitchIS.Name[0].Name:()}
            
            if (SwitchIS.Type == "doubleSwitchCrossing"):
                node = SwitchIS.SpotLocation[0].NetElementRef

                straightBranch_A = SwitchIS.StraightBranch[0].NetRelationRef#.split('_')[1]
                straightBranch_B = SwitchIS.StraightBranch[1].NetRelationRef#.split('_')[1]
                turningBranch_A = SwitchIS.TurningBranch[0].NetRelationRef#.split('_')[1]
                turningBranch_B = SwitchIS.TurningBranch[1].NetRelationRef#.split('_')[1]

                straightBranch_1 = straightBranch_A if node in straightBranch_A else straightBranch_B
                turningBranch_1 = turningBranch_A if node in turningBranch_A else turningBranch_B
                straightBranch_2 = straightBranch_B if node in straightBranch_A else straightBranch_B
                turningBranch_2 = turningBranch_B if node in turningBranch_A else turningBranch_B

                nodeStart = node
                nodeInt = straightBranch_1.split('_')[1].split('ne')[1:]
                nodeEnd = 'ne'+nodeInt[0] if str(nodeStart[2:]) == nodeInt[1] else 'ne'+nodeInt[1]

                #print(f'S:{nodeStart} {nodeEnd}')
                    
                if 'Switch_X' not in network[nodeStart]:
                    network[nodeStart] |= {'Switch_X':{}}
                if 'Switch_X' not in network[nodeEnd]:
                    network[nodeEnd] |= {'Switch_X':{}}
                if SwitchIS.Name[0].Name not in network[nodeStart]['Switch_X']:
                    network[nodeStart]['Switch_X'] |= {SwitchIS.Name[0].Name:()}
                if SwitchIS.Name[0].Name not in network[nodeEnd]['Switch_X']:
                    network[nodeEnd]['Switch_X'] |= {SwitchIS.Name[0].Name:()}

                nodeStart = node
                nodeInt = turningBranch_1.split('_')[1].split('ne')[1:]
                nodeEnd = 'ne'+nodeInt[0] if str(nodeStart[2:]) == nodeInt[1] else 'ne'+nodeInt[1]

                #print(f'T:{nodeStart} {nodeEnd}')
                    
                if 'Switch_X' not in network[nodeStart]:
                    network[nodeStart] |= {'Switch_X':{}}
                if 'Switch_X' not in network[nodeEnd]:
                    network[nodeEnd] |= {'Switch_X':{}}
                if SwitchIS.Name[0].Name not in network[nodeStart]['Switch_X']:
                    network[nodeStart]['Switch_X'] |= {SwitchIS.Name[0].Name:()}
                if SwitchIS.Name[0].Name not in network[nodeEnd]['Switch_X']:
                    network[nodeEnd]['Switch_X'] |= {SwitchIS.Name[0].Name:()}

                nodeStart = ['ne'+x for x in straightBranch_2.split('_')[1].split('ne')[1:] if x in turningBranch_2.split('_')[1].split('ne')[1:]][0]
                nodeInt = straightBranch_2.split('_')[1].split('ne')[1:]
                nodeEnd = 'ne'+nodeInt[0] if str(nodeStart[2:]) == nodeInt[1] else 'ne'+nodeInt[1]

                #print(f'S:{nodeStart} {nodeEnd}')
                    
                if 'Switch_X' not in network[nodeStart]:
                    network[nodeStart] |= {'Switch_X':{}}
                if 'Switch_X' not in network[nodeEnd]:
                    network[nodeEnd] |= {'Switch_X':{}}
                if SwitchIS.Name[0].Name not in network[nodeStart]['Switch_X']:
                    network[nodeStart]['Switch_X'] |= {SwitchIS.Name[0].Name:()}
                if SwitchIS.Name[0].Name not in network[nodeEnd]['Switch_X']:
                    network[nodeEnd]['Switch_X'] |= {SwitchIS.Name[0].Name:()}

                nodeStart = ['ne'+x for x in straightBranch_2.split('_')[1].split('ne')[1:] if x in turningBranch_2.split('_')[1].split('ne')[1:]][0]
                nodeInt = turningBranch_2.split('_')[1].split('ne')[1:]
                nodeEnd = 'ne'+nodeInt[0] if str(nodeStart[2:]) == nodeInt[1] else 'ne'+nodeInt[1]

                #print(f'T:{nodeStart} {nodeEnd}')
                    
                if 'Switch_X' not in network[nodeStart]:
                    network[nodeStart] |= {'Switch_X':{}}
                if 'Switch_X' not in network[nodeEnd]:
                    network[nodeEnd] |= {'Switch_X':{}}
                if SwitchIS.Name[0].Name not in network[nodeStart]['Switch_X']:
                    network[nodeStart]['Switch_X'] |= {SwitchIS.Name[0].Name:()}
                if SwitchIS.Name[0].Name not in network[nodeEnd]['Switch_X']:
                    network[nodeEnd]['Switch_X'] |= {SwitchIS.Name[0].Name:()}
                            
    if Crossings != None:
        for Crossing in Crossings[0].Crossing:
            crossing = Crossing.Name[0].Name

            Net = Crossing.External[0].Ref.split('_')[1].split('ne')
            node1 = 'ne' + Net[1]        
            node2 = 'ne' + Net[2]  

            Net = Crossing.External[1].Ref.split('_')[1].split('ne')
            node3 = 'ne' + Net[1]        
            node4 = 'ne' + Net[2]  

            if 'Crossing' not in network[node1]:
                network[node1] |= {'Crossing':{}}
            if 'Crossing' not in network[node2]:
                network[node2] |= {'Crossing':{}}
            if 'Crossing' not in network[node3]:
                network[node3] |= {'Crossing':{}}
            if 'Crossing' not in network[node4]:
                network[node4] |= {'Crossing':{}}

            if crossing not in network[node1]['Crossing']:
                network[node1]['Crossing'] |= {crossing:()}
            if crossing not in network[node2]['Crossing']:
                network[node2]['Crossing'] |= {crossing:()}
            if crossing not in network[node3]['Crossing']:
                network[node3]['Crossing'] |= {crossing:()}
            if crossing not in network[node4]['Crossing']:
                network[node4]['Crossing'] |= {crossing:()}
                    
    if SignalsIS != None:
        for SignalIS in SignalsIS.SignalIS:
            node = SignalIS.SpotLocation[0].NetElementRef
            signal = SignalIS.Designator[0].Entry.split(' ')[1]

            if 'Signal' not in network[node]:
                network[node] |= {'Signal':{}}
            if signal not in network[node]['Signal']:
                network[node]['Signal'] |= {signal:()}
                                                                        
    positions = {}
    if visualization.Visualization[0].SpotElementProjection != None:
        for i in visualization.Visualization[0].SpotElementProjection:
            name = i.Name[0].Name
            ref = i.RefersToElement
            if ref.startswith('bus') or name.startswith('Buf') or ref.startswith('oe') or ref.startswith('line') or ref.startswith('tde') or ref.startswith('lcr') or ref.startswith('plf') or ref.startswith('tvd') or ref.startswith('swi') or re.fullmatch(r'S\d{2,3}', name): 
                x_pos = int(float(i.Coordinate[0].X)) if float(i.Coordinate[0].X).is_integer() else float(i.Coordinate[0].X)
                y_pos = -int(float(i.Coordinate[0].Y))  if float(i.Coordinate[0].Y).is_integer() else -float(i.Coordinate[0].Y)

                #print(name,x_pos,y_pos)

                if re.fullmatch(r'X\d{2,3}', ref) or re.fullmatch(r'P\d{2,3}', ref):
                    positions[name] = (x_pos,-y_pos)
                else:
                    positions[name] = (x_pos,y_pos)

    for x in positions:
        print(f'{x} {positions[x]}')
        for node in network:
            if 'BufferStop' in network[node] and x in network[node]['BufferStop']:
                network[node]['BufferStop'] |= {x:positions[x]}
            if 'Border' in network[node] and x in network[node]['Border']:
                network[node]['Border'] |= {x:positions[x]}
            if 'RailJoint' in network[node] and x in network[node]['RailJoint']:
                network[node]['RailJoint'] |= {x:positions[x]}
            if 'LevelCrossing' in network[node] and x in network[node]['LevelCrossing']:
                network[node]['LevelCrossing'] |= {x:positions[x]}
            if 'Platform' in network[node]:
                if x in network[node]['Platform']:
                    network[node]['Platform'] |= {x:positions[x]}
                if x+'l' in network[node]['Platform']:
                    network[node]['Platform'] |= {f'{x}l':positions[x]}
                if x+'r' in network[node]['Platform']:
                    network[node]['Platform'] |= {f'{x}r':positions[x]}
            if 'Switch' in network[node] and x in network[node]['Switch']:
                network[node]['Switch'] |= {x:positions[x]}
            if 'Crossing' in network[node] and x in network[node]['Crossing']:
                network[node]['Crossing'] |= {x:positions[x]}
            if 'Signal' in network[node] and x in network[node]['Signal']:
                network[node]['Signal'] |= {x:positions[x]}

    return network

def create_canvas(window, width, height):
    return tk.Canvas(window, width=width, height=height)

def draw_lines(canvas, network, width, height, netElement):
    def convert_coordinates(x, y):
        return x + width // 2, height // 2 - y

    net_elements = {}
    for key, value in network[netElement].items():
        if key.startswith('line'):
            x1y1, x2y2 = value
            net_element = NetElement(canvas, *convert_coordinates(*x1y1), *convert_coordinates(*x2y2), net_elements, netElement)
            net_elements[key] = net_element
        if key.startswith('BufferStop'):
            for i in value:
                x,y = value[i]
                line_xs = [coord[0] for key, value in network[netElement].items() if key.startswith('line') for coord in value]
                direction = '>' if all(x >= line_x for line_x in line_xs) else '<'
                #print(f'{i} {x} {line_xs} {direction}')

                buffer_stop = BufferStop(canvas, *convert_coordinates(x, y), direction)
                net_elements[key] = buffer_stop
        if key.startswith('Border'):
            for i in value:
                x,y = value[i]
                line_xs = [coord[0] for key, value in network[netElement].items() if key.startswith('line') for coord in value]
                direction = '>' if all(x >= line_x for line_x in line_xs) else '<'
                #print(f'{i} {x} {line_xs} {direction}')

                border = Border(canvas, *convert_coordinates(x, y), direction)
                net_elements[key] = border
        if key.startswith('RailJoint'):
            for i in value:
                x,y = value[i]
                railJoint = RailJoint(canvas, *convert_coordinates(x, y))
                net_elements[key] = railJoint
        if key.startswith('Platform'):
            for i in value:
                x,y = value[i]
                #print(key,value,i)
                direction = network[netElement]['Way']

                if i[-1] == 'r':
                    side = 'right'
                else:
                    side = 'left'

                if direction == '>' and side == 'left':
                    alignment = 'top'
                if direction == '>' and side == 'right':
                    alignment = 'bottom'
                if direction == '<' and side == 'left':
                    alignment = 'bottom'
                if direction == '<' and side == 'right':
                    alignment = 'top'

                platform = Platform(canvas, *convert_coordinates(x, y), alignment)
                net_elements[key] = platform
        if key.startswith('LevelCrossing'):
            for i in value:
                x,y = value[i]
                levelCrossing = LevelCrossing(canvas, *convert_coordinates(x, y))
                net_elements[key] = levelCrossing
        if key.startswith('Signal'):
            for i in value:
                x,y = value[i]
                signal = Signals(canvas, *convert_coordinates(x, y),i)
                net_elements[key] = signal
    return net_elements

def bind_events(canvas, lines):
    def on_button_press(event):
        canvas.scan_mark(event.x, event.y)

    def on_drag(event):
        canvas.scan_dragto(event.x, event.y, gain=1)

    def on_zoom(event):
        factor = 1.0 + event.delta * 0.001
        canvas.scale("all", event.x, event.y, factor, factor)

    canvas.bind("<ButtonPress-1>", on_button_press)
    canvas.bind("<B1-Motion>", on_drag)
    canvas.bind("<MouseWheel>", on_zoom)

def AGG(RML,test = False):
    print("#"*20+" Starting Automatic GUI Generator "+"#"*20)
    print("Reading railML object")
    netElements = get_netElements(RML)

    for netElement in netElements:
        print(f'{netElement} {netElements[netElement]}')

    print("Generating GUI layout")
    
    window = tk.Tk()
    width, height = 1200, 800
    canvas = create_canvas(window, width, height)
    canvas.pack(fill='both', expand=True)

    for netElement in netElements:
        lines_plot = draw_lines(canvas, netElements, width, height,netElement)
        bind_events(canvas, lines_plot)

    # Update the window to make sure all widgets are drawn before we get the bounding box
    window.update_idletasks()
    
    # Get the bounding box of all items on the canvas
    bbox = canvas.bbox("all")

    # Calculate the center of the bounding box
    center_x = (bbox[2] + bbox[0]) // 2
    center_y = (bbox[3] + bbox[1]) // 2

    # Calculate the distance to move to center the bounding box
    dx = width // 2 - center_x
    dy = height // 2 - center_y

    # Move all items on the canvas to center the bounding box
    canvas.move("all", dx, dy)

    # Update the window again to reflect the changes
    window.update_idletasks()

    window.mainloop()