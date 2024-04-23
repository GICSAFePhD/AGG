import tkinter as tk

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
    Crossings =         RML.Infrastructure.FunctionalInfrastructure.Crossings
    SignalsIS =         RML.Infrastructure.FunctionalInfrastructure.SignalsIS

    visualization = RML.Infrastructure.InfrastructureVisualizations

    if NetElements != None:
        for i in NetElements.NetElement:
            #print(i)
            if i.Id not in coords.keys():
                #print([[i.AssociatedPositioningSystem[0].IntrinsicCoordinate[j].GeometricCoordinate[0].X[:-4],i.AssociatedPositioningSystem[0].IntrinsicCoordinate[j].GeometricCoordinate[0].Y[:-4]] for j in range(len(i.AssociatedPositioningSystem[0].IntrinsicCoordinate))])
                if i.AssociatedPositioningSystem != None:
                    if i.AssociatedPositioningSystem[0].IntrinsicCoordinate != None:
                        #print(i.Id,len(i.AssociatedPositioningSystem[0].IntrinsicCoordinate),i.AssociatedPositioningSystem[0].IntrinsicCoordinate)
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

        #network[i] |= {f'otro' : 'xxx'} 

    
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
            node = Border.SpotLocation[0].NetElementRef
            border = Border.Name[0].Name

            if 'Border' not in network[node]:
                network[node] |= {'Border':{}}
            if border not in network[node]['Border']:
                network[node]['Border'] |= {border:()}

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
                network[node]['Platform'] |= {platform:()}

    if SignalsIS != None:
        for SignalIS in SignalsIS.SignalIS:
            node = SignalIS.SpotLocation[0].NetElementRef
            signal = SignalIS.Name[0].Name

            if 'Signal' not in network[node]:
                network[node] |= {'Signal':{}}
            if signal not in network[node]['Signal']:
                network[node]['Signal'] |= {signal:()}
                                                                        
    positions = {}
    if visualization.Visualization[0].SpotElementProjection != None:
        for i in visualization.Visualization[0].SpotElementProjection:
            name = i.Name[0].Name
            if 'Buf' in name or 'Lc' in name or 'Plat' in name or ('S' in name and 'Sw' not in name): 
                x_pos = int(float(i.Coordinate[0].X)) if float(i.Coordinate[0].X).is_integer() else float(i.Coordinate[0].X)
                y_pos = -int(float(i.Coordinate[0].Y))  if float(i.Coordinate[0].Y).is_integer() else -float(i.Coordinate[0].Y)

                #print(i.Name[0].Name,x_pos,y_pos)

                if 'S' in name and 'Sw' not in name:
                    positions[i.RefersToElement] = (x_pos,y_pos)
                else:
                    positions[i.Name[0].Name] = (x_pos,y_pos)

    for x in positions:
        #print(f'{x} {positions[x]}')
        for node in network:
            if 'BufferStop' in network[node] and x in network[node]['BufferStop']:
                network[node]['BufferStop'] = {x:positions[x]}
            if 'Border' in network[node] and x in network[node]['Border']:
                network[node]['Border'] = {x:positions[x]}
            if 'LevelCrossing' in network[node] and x in network[node]['LevelCrossing']:
                network[node]['LevelCrossing'] = {x:positions[x]}
            if 'Platform' in network[node] and x in network[node]['Platform']:
                network[node]['Platform'] = {x:positions[x]}
            
            if 'Signal' in network[node] and x in network[node]['Signal']:
                print(x, network[node]['Signal'])
                network[node]['Signal'][x] = positions[x]

    return network

def create_canvas(window, width, height):
    return tk.Canvas(window, width=width, height=height)

def draw_lines(canvas, lines_coords, width, height, netElement):
    def convert_coordinates(x, y):
        return x + width // 2, height // 2 - y

    net_elements = {}
    for key, value in lines_coords.items():
        # Only process the data indicated with the index 'linex', with x a number
        if key.startswith('line'):
            x1y1, x2y2 = value
            net_element = NetElement(canvas, *convert_coordinates(*x1y1), *convert_coordinates(*x2y2), net_elements, netElement)
            net_elements[key] = net_element
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
        lines_plot = draw_lines(canvas, netElements[netElement], width, height,netElement)
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