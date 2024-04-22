import tkinter as tk

class Line:
    def __init__(self, canvas, x1, y1, x2, y2, lines, line_key, color='black'):
        self.id = canvas.create_line(x1, y1, x2, y2, fill=color,width=3)
        self.pressed = False
        self.lines = lines
        self.line_key = line_key  # This is the 'i' in your loop
        canvas.tag_bind(self.id, "<Button-1>", self.on_line_click)

    def on_line_click(self, event):
        self.pressed = not self.pressed
        new_color = 'red' if self.pressed else 'black'
        for line in self.lines.values():
            event.widget.itemconfig(line.id, fill=new_color)
        if self.pressed:  # If the line is colored red
            print(f'netElement {self.line_key} is occupied')  # Print the line index
        else:
            print(f'netElement {self.line_key} is released')

def get_lines(RML):
    lines = {}
    coords = {}
    NetElements = RML.Infrastructure.Topology.NetElements

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
            if i not in lines:
                lines[i] = {}
            lines[i] |= {f'line{j+1}' : (coords[i][j], coords[i][j + 1])}
        
    
    return lines

def create_canvas(window, width, height):
    return tk.Canvas(window, width=width, height=height)

def draw_lines(canvas, lines_coords, width, height, netElement):
    def convert_coordinates(x, y):
        return x + width // 2, height // 2 - y

    lines = {}
    for key, (x1y1, x2y2) in lines_coords.items():
        line = Line(canvas, *convert_coordinates(*x1y1), *convert_coordinates(*x2y2), lines, netElement)
        lines[key] = line
    return lines

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
    lines = get_lines(RML)

    for line in lines:
        print(f'{line} {lines[line]}')

    print("Generating GUI layout")

    
    window = tk.Tk()
    width, height = 1200, 800
    canvas = create_canvas(window, width, height)
    canvas.pack()
    for i in lines:
        lines_plot = draw_lines(canvas, lines[i], width, height,i)
        bind_events(canvas, lines_plot)

    # Get the bounding box of all items on the canvas
    bbox = canvas.bbox("all")

    # Calculate the center of the bounding box
    center_x = (bbox[2] + bbox[0]) // 2
    center_y = (bbox[3] + bbox[1]) // 2

    # Calculate the distance to move to center the bounding box
    dx = canvas.winfo_width() // 2 - center_x
    dy = canvas.winfo_height() // 2 - center_y

    # Move all items on the canvas to center the bounding box
    canvas.move("all", dx, dy)

    window.mainloop()
