#Formation Master V1.0
#Cuda Wong

from tkinter import *

class Circle:
    def __init__(self, canvas, x, y, radius, color):
        self.canvas = canvas
        self.item = canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=color)
        self.radius = radius
        # Bind methods to canvas events for dragging
        self.canvas.tag_bind(self.item, '<ButtonPress-1>', self.on_button_press)  # Bind mouse button press event
        self.canvas.tag_bind(self.item, '<B1-Motion>', self.on_move)  # Bind mouse motion event
        self.canvas.tag_bind(self.item, '<ButtonRelease-1>', self.on_button_release)  # Bind mouse button release event
        self.drag_data = {'x': 0, 'y': 0, 'item': None}  # Initialize data for tracking drag interactions

    # Methods for handling drag events
    def on_button_press(self, event):
        self.drag_data['item'] = self.item  # Record initial position and item being dragged
        self.drag_data['x'] = event.x
        self.drag_data['y'] = event.y

    def on_move(self, event):
        delta_x = event.x - self.drag_data['x']  # Calculate the change in position
        delta_y = event.y - self.drag_data['y']
        self.canvas.move(self.drag_data['item'], delta_x, delta_y)  # Move the circle accordingly
        self.drag_data['x'] = event.x
        self.drag_data['y'] = event.y

    def on_button_release(self):
        self.drag_data['item'] = None  # Reset the item being dragged

class FormationMaster:
    def __init__(self, window):
        self.window = window
        self.window.title("Formation Master")
        self.canvas = self.create_canvas()
        self.dancers = []
        self.dancer_info_frame = self.create_dancer_info_frame()

    def create_canvas(self):
        canvas = Canvas(self.window, width=800, height=600, bd=2, relief='solid', bg='white')
        canvas.pack(side=LEFT)
        return canvas

    def create_dancer_info_frame(self):
        dancer_info_frame = Frame(self.window, bg='white', relief='solid', bd=2)
        dancer_info_frame.pack(side=RIGHT, padx=10, pady=10)
        return dancer_info_frame

    def add_dancers(self):
        x = 200
        y = 200
        radius = 30
        color = 'blue'
        circle = Circle(self.canvas, x, y, radius, color)
        self.dancers.append(circle)
        self.add_dancer_info(len(self.dancers), color)

    def delete_dancers(self):
        if self.dancers:
            dancer = self.dancers.pop()
            self.canvas.delete(dancer.item)
            self.remove_dancer_info(len(self.dancers) + 1)

    def add_dancer_info(self, dancer_id, color):
        dancer_frame = Frame(self.dancer_info_frame, bg='white')
        dancer_frame.pack(fill=X, padx=5, pady=5)
        
        dancer_label = Label(dancer_frame, text=f"Dancer {dancer_id}", bg=color)
        dancer_label.pack(side=LEFT)
        
        name_entry = Entry(dancer_frame, width=10)
        name_entry.pack(side=LEFT)

    def remove_dancer_info(self, dancer_id):
        for widget in self.dancer_info_frame.winfo_children():
            widget.destroy()

        for i in range(1, dancer_id):
            color = 'blue'  
            self.add_dancer_info(i, color)

    def mainloop(self):
        add_dancers_button = Button(self.window, text="Add Dancer", command=self.add_dancers)
        add_dancers_button.pack(side=TOP, padx=10, pady=10)
        delete_dancer_button = Button(self.window, text="Delete Dancer", command=self.delete_dancers)
        delete_dancer_button.pack(side=TOP, padx=10, pady=10)

if __name__ == "__main__":
    root = Tk()
    app = FormationMaster(root)
    app.mainloop()
