import tkinter as tk
import re
import math

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
    def __init__(self, canvas, x, y ,levelCrossings,levelCrossing_key,color='blue'):
        self.pressed = False
        self.levelCrossings = levelCrossings
        self.levelCrossing_key = levelCrossing_key

        # Create lines and store their ids
        self.ids = [
            canvas.create_line(x+30, y-60, x+30, y+60, fill=color,width=3),
            canvas.create_line(x+30, y-60, x+45, y-75, fill=color,width=3),
            canvas.create_line(x+30, y+60, x+45, y+75, fill=color,width=3),
            canvas.create_line(x-30, y-60, x-30, y+60, fill=color,width=3),
            canvas.create_line(x-30, y-60, x-45, y-75, fill=color,width=3),
            canvas.create_line(x-30, y+60, x-45, y+75, fill=color,width=3)
        ]

        # Bind the click event to all lines
        for id in self.ids:
            canvas.tag_bind(id, "<Button-1>", self.on_net_element_click)

    def on_net_element_click(self, event):
        self.pressed = not self.pressed
        new_color = 'red' if self.pressed else 'blue'
        for levelCrossing in self.levelCrossings.values():
            for id in levelCrossing.ids:
                event.widget.itemconfig(id, fill=new_color)
        if self.pressed:
            print(f'LevelCrossing {self.levelCrossing_key} is closed')
        else:
            print(f'LevelCrossing {self.levelCrossing_key} is open')

class Border:
    def __init__(self, canvas, x, y, direction ,color='black'):
        sign = 1 if direction == '>' else -1
        self.id = None
        canvas.create_line(x+sign*5, y, x+sign*10, y, fill=color,width=3)
        canvas.create_line(x+sign*15, y, x+sign*20, y, fill=color,width=3)

class Signals:
    def __init__(self, canvas, x, y ,name,way,net_coordinate = None,other_signals=None , color='grey' ):
        #self.id = None
        font_size = 8
        self.pressed = False

        self.canvas = canvas
        self.color = color
        self.other_signals = tuple(other_signals.keys()) if other_signals else ()
        self.routes = other_signals if other_signals else {}
        # next_signals = tuple(signal_routes[name].keys())

        direction = name[-2]
        side = name[-1]
        self.name = name[:-2]

        if net_coordinate != None:
            slope = 'up' if (net_coordinate[1][1] - net_coordinate[0][1]) / (net_coordinate[1][0] - net_coordinate[0][0]) > 0 else 'down'
            print(f'{name} {x} {y} {net_coordinate} {way} {slope}')

        x0 = -1
        y0 = 1
        r = 15

        if net_coordinate == None:
            if direction == 'l' and side == 'n':
                #color = 'red'
                x0 = -1
                y0 = 1
            if direction == 'l' and side == 'r':
                #color = 'green'
                x0 = -1
                y0 = 1
            if direction == 'r' and side == 'n':
                #color = 'blue'
                x0 = -1
                y0 = 1
            if direction == 'r' and side == 'r':
                #color = 'black'
                x0 = 1
                y0 = -1

            x0 = x0 if way == '>' else -x0
            y0 = y0 if way == '>' else -y0

            self.id = canvas.create_text(x,y-(y0*55),text=name[:-2],fill=color,font=font_size)
            canvas.create_line(x, (y-y0*30), (x-x0*25), (y-y0*30), fill=color,width=3)
            canvas.create_line(x, (y-y0*30)+10, x, (y-y0*30)-10, fill=color,width=3)
            canvas.create_oval((x-x0*40)-r,(y-y0*30)-r,(x-x0*40)+r,(y-y0*30)+r,outline=color,width=3)
        else:
            x0 = 0
            y0 = 0
            if slope == 'up' and way == '>':
                #color = 'orange'
                self.id =  canvas.create_text(x+70, y+25, text=name, fill=color, font=font_size)
                canvas.create_line(x+30, y+9, x+49, y-14, fill=color,width=3)
                canvas.create_line(x+60, y-5, x+38, y-22, fill=color,width=3)
                canvas.create_oval((x+20)-r, (y+20)-r, (x+20)+r, (y+20)+r, outline=color, width=3)
            if slope == 'up' and way == '<':
                color = 'grey'
            if slope == 'down' and way == '>':
                #color = 'pink'
                self.id =  canvas.create_text(x+100, y-25, text=name, fill=color, font=font_size)
                canvas.create_line(x+82, y+8, x+55, y-16, fill=color,width=3)
                canvas.create_line(x+45, y-5, x+65, y-25, fill=color,width=3)
                canvas.create_oval((x+90)-r, (y+20)-r, (x+90)+r, (y+20)+r, outline=color, width=3)
            if slope == 'down' and way == '<':
                #color = 'cyan'
                self.id = canvas.create_text(x-100, y+45, text=name, fill=color, font=font_size)
                canvas.create_line(x-55, y+35, x-79, y+10, fill=color,width=3)
                canvas.create_line(x-65, y+35+10, x-45, y+35-10, fill=color,width=3)
                canvas.create_oval((x-90)-r, y-r, (x-90)+r, y+r, outline=color, width=3)

        canvas.tag_bind(self.id, "<Button-1>", self.on_signal_click)

    def on_signal_click(self, event):
        self.pressed = not self.pressed

        for signal_name in signals:
            signal = signals[signal_name]

            match self.color:
                case 'grey':
                    if signal_name == self.name:
                        print(f'Signal {self.name} is selected')
                        color = 'green'
                        self.canvas.itemconfig(self.id, fill=color)

                    if signal_name in self.other_signals:
                        signal.color = 'red'
                        signal.canvas.itemconfig(signal.id, fill=signal.color)
                    else:
                        if signal_name != self.name:
                            signal.color = 'grey70'
                            signal.canvas.itemconfig(signal.id, fill=signal.color)
                            signal.canvas.tag_unbind(signal.id, "<Button-1>")
                case 'green':
                    if signal_name == self.name:
                        print(f'Signal {self.name} is released')
                        color = 'grey'
                        self.canvas.itemconfig(self.id, fill=color)
                    if signal_name in self.other_signals:
                        signal.color = 'grey'
                        signal.canvas.itemconfig(signal.id, fill=signal.color)
                    else:
                        if signal_name != self.name:
                            signal.color = 'grey'
                            signal.canvas.itemconfig(signal.id, fill=signal.color)
                            signal.canvas.tag_bind(signal.id, "<Button-1>", signal.on_signal_click)
                case 'red':
                    if signal_name == self.name:
                        #print(f'Route {self.name} {self.routes} is launched')
                        color = 'grey'
                        self.canvas.itemconfig(self.id, fill=color)
                    else:
                        color = 'grey'
                        if signal.color == 'green':
                            print(f'Route {signal.routes[self.name]} launched')
                        signal.color = 'grey'
                        signal.canvas.itemconfig(signal.id, fill=signal.color)
                        signal.canvas.tag_bind(signal.id, "<Button-1>", signal.on_signal_click)
                case _:
                    color = 'grey'
                    self.canvas.itemconfig(self.id, fill=color)

        self.color = color
            
class Switch:
    def __init__(self, canvas, x, y ,switches, switch_key, color='black'):
        r = 15
        self.pressed = False
        self.switches = switches
        self.switch_key = switch_key

        self.ids = [
        canvas.create_oval(x-r, y-r, x+r, y+r, outline=color, width=3, fill = 'white'),
        canvas.create_line(x-r, y, x+r, y, fill=color, width=3)
        ]
        self.canvas = canvas
        self.previous_items = set(self.canvas.find_all())
        self.check_for_changes()
        # Bind the click event to all lines
        for id in self.ids:
            canvas.tag_bind(id, "<Button-1>", self.switch_position)

    def switch_position(self, event):
        self.pressed = not self.pressed
        new_color = 'red' if self.pressed else 'black'
        for switch in self.switches.values():
            #for id in switch.ids:
            #    event.widget.itemconfig(id, fill=new_color)
            event.widget.itemconfig(switch.ids[1], fill=new_color)
        if self.pressed:
            #print(f'Switch {self.levelCrossing_key} is closed')
            print(f'Switch on')
        else:
            #print(f'LevelCrossing {self.levelCrossing_key} is open')
            print(f'Switch off')
        self.raise_to_top()

    def check_for_changes(self):
        current_items = set(self.canvas.find_all())
        if current_items != self.previous_items:
            self.raise_to_top()
        self.previous_items = current_items
        self.canvas.after(100, self.check_for_changes)  # Check for changes every 100 milliseconds

    def raise_to_top(self):
        for id in self.ids:
            self.canvas.tag_raise(id)

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
            direction = SignalIS.SignalConstruction[0].PositionAtTrack[0]
            side = SignalIS.SpotLocation[0].ApplicationDirection[0]
            
            if 'Signal' not in network[node]:
                network[node] |= {'Signal':{}}
            if signal not in network[node]['Signal']:
                network[node]['Signal'] |= {f'{signal}{direction}{side}':()}
                                                                        
    positions = {}
    if visualization.Visualization[0].SpotElementProjection != None:
        for i in visualization.Visualization[0].SpotElementProjection:
            name = i.Name[0].Name
            ref = i.RefersToElement
            if ref.startswith('bus') or name.startswith('Buf') or ref.startswith('oe') or ref.startswith('line') or ref.startswith('tde') or ref.startswith('lcr') or ref.startswith('plf') or ref.startswith('tvd') or ref.startswith('swi') or name.startswith('S'): 
                x_pos = int(float(i.Coordinate[0].X)) if float(i.Coordinate[0].X).is_integer() else float(i.Coordinate[0].X)
                y_pos = -int(float(i.Coordinate[0].Y))  if float(i.Coordinate[0].Y).is_integer() else -float(i.Coordinate[0].Y)
                positions[name] = (x_pos,y_pos)
                #print(f'-{ref} {name} {positions[name]}')

    for x in positions:
        #print(f'{x} {positions[x]}')
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
            if 'Signal' in network[node]:
                way = network[node]['Way']

                if x+'ln' in network[node]['Signal'] or x+'lr' in network[node]['Signal'] or x+'rn' in network[node]['Signal'] or x+'rr' in network[node]['Signal']:
                    min_distance = float('inf')
                    min_line = None

                    for line_name, line in network[node].items():
                        if line_name.startswith('line'):
                            (x1, y1), (x2, y2) = line
                            (x0, y0) = positions[x]
                            dx, dy = x2 - x1, y2 - y1
                            t = ((x0 - x1) * dx + (y0 - y1) * dy) / (dx * dx + dy * dy)
                            if t < 0:
                                t = 0
                            elif t > 1:
                                t = 1
                            projected = x1 + t * dx, y1 + t * dy
                            dist = math.hypot(x0 - projected[0], y0 - projected[1])
                            if dist < min_distance:
                                min_distance = dist
                                min_line = line_name
 
                    #print(f'//{x} {node} {min_line}')

                    if min_line != None:
                        if network[node][min_line][0][1] == network[node][min_line][1][1]:
                            position = (positions[x][0],network[node][min_line][0][1])
                        else:
                            position = ((network[node][min_line][0][0] + network[node][min_line][1][0]) / 2, (network[node][min_line][0][1] + network[node][min_line][1][1]) / 2) #positions[x]

                        #print(f'*{x} {positions[x]} {node} {min_line} {way} {position}')

                    if x+'ln' in network[node]['Signal']:
                        network[node]['Signal'] |= {f'{x}ln':position}
                    if x+'lr' in network[node]['Signal']:
                        network[node]['Signal'] |= {f'{x}lr':position}
                    if x+'rn' in network[node]['Signal']:
                        network[node]['Signal'] |= {f'{x}rn':position}
                    if x+'rr' in network[node]['Signal']:
                        network[node]['Signal'] |= {f'{x}rr':position}
                    
    return network

def create_canvas(window, width, height):
    return tk.Canvas(window, width=width, height=height)

signals = {}
signal_routes = {}

def draw_lines(canvas, network, width, height, netElement):
    def convert_coordinates(x, y):
        return x + width // 2, height // 2 - y

    net_elements = {}
    levelCrossings = {}
    switches = {}
    for key, value in network[netElement].items():
        if key.startswith('line'):
            x1y1, x2y2 = value
            net_element = NetElement(canvas, *convert_coordinates(*x1y1), *convert_coordinates(*x2y2), net_elements, netElement)
            net_elements[key] = net_element
        if key.startswith('BufferStop'):
            for i in value:
                x,y = value[i]
                line_xs = [coord[0] for key, value in network[netElement].items() if key.startswith('line') for coord in value]
                #print(f'---{i} {line_xs} | {int(x)}')
                direction = '>' if all(int(x) >= line_x for line_x in line_xs) else '<'

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
                levelCrossing = LevelCrossing(canvas, *convert_coordinates(x, y), levelCrossings,i)
                levelCrossings[key] = levelCrossing       
        if key.startswith('Signal'):
            for i in value:
                x,y = value[i]
                name = i[:-2]
                #print(f'---{i} {x} {y}')
                way = network[netElement]['Way']

                min_distance = float('inf')
                min_line = None
                for line_name, line in network[netElement].items():
                    if line_name.startswith('line'):
                        (x1, y1), (x2, y2) = line
                        (x0, y0) = (x,y)
                        dx, dy = x2 - x1, y2 - y1
                        t = ((x0 - x1) * dx + (y0 - y1) * dy) / (dx * dx + dy * dy)
                        if t < 0:
                            t = 0
                        elif t > 1:
                            t = 1
                        projected = x1 + t * dx, y1 + t * dy
                        dist = math.hypot(x0 - projected[0], y0 - projected[1])
                        if dist < min_distance:
                            min_distance = dist
                            min_line = line_name

                net_coordinate = None
                if min_line != None:
                    if network[netElement][min_line][0][1] != network[netElement][min_line][1][1]:
                        net_coordinate = network[netElement][min_line]

                next_signals = None
                if name in signal_routes:
                    next_signals = signal_routes[name]
                    #print(next_signals)
                signal = Signals(canvas, *convert_coordinates(x, y),i,way,net_coordinate, other_signals = next_signals)
                signals[name] = signal
        if key.startswith('Switch'):
            for i in value:
                x,y = value[i]
                switch = Switch(canvas, *convert_coordinates(x, y),switches,i)
                switches[key] = switch

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

def AGG(RML,routes,test = False):
    print("#"*20+" Starting Automatic GUI Generator "+"#"*20)
    print("Reading railML object")
    netElements = get_netElements(RML)

    for netElement in netElements:
        print(f'{netElement} {netElements[netElement]}')

    for route in routes:
        #print(f'R{route} {routes[route]}')

        start = 'S'+str(routes[route]['Start'][1:])
        end = 'S'+str(routes[route]['End'][1:])

        if start not in signal_routes:
            signal_routes[start] = {}

        signal_routes[start] |= {end:f'R{route}'}

    #for signal in signal_routes:
    #    print(f'{signal} {signal_routes[signal]}')

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