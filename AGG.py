import tkinter as tk

def AGG(test = False):
    
    print("#"*20+" Starting Automatic GUI Generator "+"#"*20)
    print("Reading railML object")
    print("Generating GUI layout")

    

    

    # Your lines
    lines = {'line1': ((0, 0), (50, 0)), 'line2': ((50, 0), (100, 50)), 'line3': ((50, 0), (100, 0))}  # replace with your actual lines

    # Create a new tkinter window
    window = tk.Tk()

    # Define the width and height of the canvas
    width, height = 500, 500

    # Create a new canvas
    canvas = tk.Canvas(window, width=width, height=height)
    canvas.pack()

    # Function to convert coordinates to have the origin at the center of the canvas
    def convert_coordinates(x, y):
        return x + width // 2, height // 2 - y

    # Draw the lines and store their state
    line_ids = {key: canvas.create_line(*convert_coordinates(x1, y1), *convert_coordinates(x2, y2), fill='black') for key, ((x1, y1), (x2, y2)) in lines.items()}

    # Function to update the color of the lines based on incoming data
    def update_colors(incoming_data):
        for line_id, color in incoming_data.items():
            canvas.itemconfig(line_ids[line_id], fill=color)

    # Incoming data
    incoming_data = {'line1': 'red', 'line2': 'green', 'line3': 'blue'}  # replace with your actual incoming data

    # Update the color of the lines
    update_colors(incoming_data)

    # Function to handle button press event
    def on_button_press(event):
        canvas.scan_mark(event.x, event.y)

    # Function to handle drag event
    def on_drag(event):
        canvas.scan_dragto(event.x, event.y, gain=1)

    # Function to handle zoom event
    def on_zoom(event):
        factor = 1.0 + event.delta * 0.001
        canvas.scale("all", event.x, event.y, factor, factor)

    # Bind the events to the canvas
    canvas.bind("<ButtonPress-1>", on_button_press)
    canvas.bind("<B1-Motion>", on_drag)
    canvas.bind("<MouseWheel>", on_zoom)

    # Run the tkinter main loop
    window.mainloop()