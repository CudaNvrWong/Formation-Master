#Formation Master V2.0
#Cuda Wong

from tkinter import *  # Import the tkinter library for GUI components
from tkinter import colorchooser, messagebox, filedialog  # Import specific components from tkinter
from PIL import Image, ImageGrab, ImageTk, ImageDraw  # Import components from the Python Imaging Library
import wave  # Import the wave module for working with audio WAV files
import matplotlib.pyplot as plt  # Import the matplotlib library for data visualization
import numpy as np  # Import the numpy library for numerical operations
from pydub import AudioSegment  # Import the pydub library for audio file handling
from pydub.playback import play  # Import the play function from pydub for audio playback
import pygame  # Import the pygame library for multimedia applications
from pygame.locals import *  # Import specific components from pygame

# Define a class for creating draggable circles on the canvas
class Circle:
    def __init__(self, canvas, x, y, radius, color):
        # Initialize the circle's attributes
        self.canvas = canvas
        self.item = canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=color)  # Create a circle on the canvas
        self.radius = radius
        self.x = x
        self.y = y
        self.color = color
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

# Define the main application class
class FormationMaster:
    def __init__(self, window):
        # Initialize the FormationMaster instance
        self.window = window
        self.window.title("Formation Master")
        self.window.geometry('1920x1080')

        # Create a canvas for drawing dance formations
        self.canvas = self.create_canvas()
        

        # Create a frame to display dancer information
        self.dancer_info_frame = Frame(window, bg='white', relief='solid', bd=2)
        self.dancer_info_frame.place(x=1258, y=64, width=170, height=645)

        # Initialize dictionaries for storing dancer information and thumbnail images
        self.dancers = []  # List to hold dancer objects
        self.dancer_names = {}  # Dictionary to store dancer names
        self.saved_formations = []  # List to store saved formations
        self.thumbnail_images = {}  # Dictionary to store thumbnail images
        self.clicked_formation = None  # To store the clicked formation filename
        self.current_formation_image = None # To store the clicked formation image

        # Load existing dance formations
        self.load_formations()
        # Create a canvas for displaying audio waveform
        self.waveform_canvas = self.create_waveform_canvas()

        # Create buttons for various actions
        add_dancers_button = Button(window, text="Add Dancer", font="Arial, 22", command=self.add_dancers)
        add_dancers_button.place(x=300, y=15)

        delete_dancer_button = Button(window, text="Delete Dancer", font="Arial, 22", command=self.delete_dancers)
        delete_dancer_button.place(x=500, y=15)

        save_formation_button = Button(window, text="Save Formation", font="Arial, 22", command=self.save_formation)
        save_formation_button.place(x=700, y=15)

        add_music_button = Button(window, text="Add Music", font="Arial, 22", command=self.add_music_file)
        add_music_button.place(x=900, y=15)

        # Initialize buttons for audio control
        self.play_pause_img = ImageTk.PhotoImage(file="play_pause.png")
        self.stop_img = ImageTk.PhotoImage(file="stop.png")

        self.play_pause_button = Button(window, image=self.play_pause_img, command=self.toggle_play_pause)
        self.play_pause_button.place(x=1245, y=725)

        self.stop_button = Button(window, image=self.stop_img, command=self.stop_music)
        self.stop_button.place(x=1245, y=780)

        # Initialize pygame mixer for audio playback
        pygame.mixer.init()
        self.audio_play_obj = None
        self.is_playing = False
        self.current_position = 0

    def create_canvas(self):
        # Create a canvas widget for dancers with specified dimensions and attributes
        canvas = Canvas(self.window, width=1035, height=650, bd=2, relief='solid', bg='white')
        # Place the canvas at the specified coordinates within the window
        canvas.place(x=200, y=60)
        # Return the created canvas
        return canvas

    def create_waveform_canvas(self):
        # Create a waveform canvas widget for audio visualization with specified dimensions and attributes
        waveform_canvas = Canvas(self.window, width=1035, height=100, bd=2, relief='solid', bg='white')
        # Place the waveform canvas at the specified coordinates within the window
        waveform_canvas.place(x=200, y=725)
        # Return the created waveform canvas
        return waveform_canvas

    def add_dancers(self):
        # Specify initial position and attributes for a new dancer
        x = 200
        y = 200
        radius = 50
        # Prompt user to select a color for the dancer and retrieve the chosen color
        color = colorchooser.askcolor(title="Select Color")[1]
        # Generate a unique dancer ID based on the number of existing dancers
        dancer_id = len(self.dancers) + 1
        # Create a Circle instance representing the dancer and add it to the list of dancers
        circle = Circle(self.canvas, x, y, radius, color)
        self.dancers.append(circle)
        # Add information about the dancer to the user interface
        self.add_dancer_info(dancer_id, color)

    def delete_dancers(self):
        # Check if there are dancers to delete
        if self.dancers:
            # Remove the last dancer from the list and delete its canvas item
            dancer = self.dancers.pop()
            self.canvas.delete(dancer.item)
            # Remove information about the dancer from the user interface
            self.remove_dancer_info(dancer)

    def add_dancer_info(self, dancer_id, color):
        # Create an image for the dancer with a colored ellipse
        dancer_image = Image.new("RGBA", (100, 100), (0, 0, 0, 0))
        draw = ImageDraw.Draw(dancer_image)
        draw.ellipse((0, 0, 100, 100), fill=color)
        # Convert the image to a PhotoImage object for displaying in the GUI
        photo_image = ImageTk.PhotoImage(dancer_image)
        # Create a label to display the dancer's image and place it on the UI
        dancer_label = Label(self.dancer_info_frame, image=photo_image, bg='white')
        dancer_label.image = photo_image
        dancer_label.grid(row=dancer_id, column=0)
        # Create an entry field for the dancer's name and place it on the UI
        name_entry = Entry(self.dancer_info_frame, width=5)
        name_entry.grid(row=dancer_id, column=0)
        # Store the dancer's information and image references in a dictionary
        self.dancer_names[dancer_id]["label"].pack(pady=5)
        self.dancer_names[dancer_id]["entry"].pack(pady=5)
        self.dancer_names[dancer_id]["image"] = photo_image

    def remove_dancer_info(self, dancer):
        # Determine the ID of the given dancer
        dancer_id = self.dancers.index(dancer) + 1
        # Retrieve and remove dancer information from the dictionary
        dancer_info = self.dancer_names.pop(dancer_id, None)
        if dancer_info:
            # Remove the label and entry from the UI
            dancer_info["label"].grid_forget()
            dancer_info["entry"].grid_forget()

    def save_formation(self):
        # Get the coordinates and dimensions of the canvas
        x0 = self.canvas.winfo_rootx()
        y0 = self.canvas.winfo_rooty()
        x1 = x0 + self.canvas.winfo_width()
        y1 = y0 + self.canvas.winfo_height()
        # Generate a unique formation filename
        formation_num = len(self.saved_formations) + 1
        formation_filename = f"formation_{formation_num}.png"
        
        # Ask the user for confirmation before saving the formation
        confirmation = messagebox.askquestion(
            "Confirm Save", "Once the formation is saved, it can't be changed.\nDo you want to save the formation?",)
        
        # If the user confirms, attempt to save the formation as an image
        if confirmation == "yes":
            try:
                # Capture a screenshot of the canvas region and save it as an image file
                image = ImageGrab.grab(bbox=(x0, y0, x1, y1))
                image.save(formation_filename)
                # Show an info message about the successful save
                messagebox.showinfo("Formation Master", f"Formation saved as '{formation_filename}'")
                
                # Update the list of saved formations and refresh the UI
                self.saved_formations.append(formation_filename)
                self.load_formations()
                
            # Handle errors that may occur during the save process
            except ImportError:
                messagebox.showerror("Formation Master", "Saving formation requires 'pyscreenshot' module. Please install it.")

    # Define a method for loading saved formations
    def load_formations(self):
        # Remove existing formation buttons from the window
        for widget in self.window.winfo_children():
            if isinstance(widget, Button) and widget['text'].startswith("Formation"):
                widget.destroy()
        
        # Create a frame for displaying formation thumbnails
        formations_frame = Frame(self.window, bg="white", relief="solid", bd=2)
        formations_frame.place(x=20, y=64, width=170, height=645)
        
        # Iterate through saved formations and display their thumbnails
        for i, formation_filename in enumerate(self.saved_formations):
            # Load the thumbnail image for the formation
            thumbnail_img = self.load_thumbnail(formation_filename)
            # Create a button with the thumbnail image
            formation_thumbnail = Button(formations_frame, image=thumbnail_img,
                                        command=lambda filename=formation_filename: self.load_saved_formation(filename))
            formation_thumbnail.pack(pady=5)
            formation_thumbnail.image = thumbnail_img
            

    # Define a method for loading thumbnail images
    def load_thumbnail(self, filename):
        try:
            # Open the image file
            image = Image.open(filename)
            # Resize the image to a thumbnail size
            image.thumbnail((100, 100))
            # Convert the image to a PhotoImage for tkinter
            thumbnail = ImageTk.PhotoImage(image)
            # Store the thumbnail image in the dictionary
            self.thumbnail_images[filename] = thumbnail
            return thumbnail
        except Exception as e:
            # Display an error message if thumbnail loading fails
            messagebox.showerror("Formation Master", f"Error loading thumbnail: {e}")
            return None
        
    
    #Define a method for displaying the clicked formation
    def display_clicked_formation(self):
        # Check if a formation has been clicked
        if self.clicked_formation:
            # Load the thumbnail image for the clicked formation
            thumbnail_image = self.load_thumbnail(self.clicked_formation)
            # Check if thumbnail image was successfully loaded
            if thumbnail_image:
                # Store the thumbnail image for future use
                self.current_thumbnail_image = thumbnail_image
                # Clear the canvas
                self.canvas.delete("all")
                # Display the thumbnail image on the canvas
                self.canvas.create_image(0, 0, anchor=NW, image=self.current_thumbnail_image)

    # Define a method for loading and displaying a saved formation
    def load_saved_formation(self, filename):
        try:
            # Clear the canvas and remove existing dancers
            for dancer in self.dancers:
                self.canvas.delete(dancer.item)
            self.dancers.clear()
            
            # Open the saved formation image
            image = Image.open(filename)
            # Resize the image to fit the canvas
            image.thumbnail((1035, 650))
            # Convert the image to a PhotoImage for tkinter
            self.current_formation_image = ImageTk.PhotoImage(image)
            # Display the formation image on the canvas
            self.canvas.create_image(0, 0, anchor=NW, image=self.current_formation_image)
        except Exception as e:
            # Display an error message if formation loading fails
            messagebox.showerror("Formation Master", f"Error loading formation: {e}")

    # Define a method for adding a music file
    def add_music_file(self):
        # Open a file dialog to select a music file
        music_file = filedialog.askopenfilename(title="Select Music File")
        # Check if a music file was selected
        if music_file:
            # Create a waveform image for the selected music file
            waveform_image = self.create_waveform_image(music_file)
            # Check if waveform image was successfully created
            if waveform_image:
                # Display the waveform image on the waveform canvas
                self.waveform_canvas.create_image(0, 0, anchor=NW, image=waveform_image)
                self.waveform_canvas.image = waveform_image
            # Load the selected music file as an audio segment
            self.audio_segment = AudioSegment.from_file(music_file)

    # Define a method for toggling between play and pause
    def toggle_play_pause(self):
        # Check if music is currently playing
        if self.is_playing:
            # Pause the music if it's playing
            self.pause_music()
        else:
            # Play the music if it's paused
            self.play_music()

    # Define a method for playing the music
    def play_music(self):
        # Check if music is not already playing
        if not self.is_playing:
            # Set the playing flag to True
            self.is_playing = True
            # Check if the audio play object is not initialized
            if self.audio_play_obj is None:
                # Set the audio segment starting position and export it to a temporary WAV file
                self.audio_segment = self.audio_segment[self.current_position:]
                self.audio_segment.export("temp.wav", format="wav")
                # Initialize the audio play object with the temporary WAV file
                self.audio_play_obj = pygame.mixer.Sound("temp.wav")
            # Play the audio
            self.audio_play_obj.play()

    # Define a method for pausing the music
    def pause_music(self):
        # Check if music is currently playing
        if self.is_playing:
            # Pause the pygame mixer
            pygame.mixer.pause()
            # Store the current position in the audio segment
            self.current_position = pygame.mixer.get_pos()
            # Set the playing flag to False
            self.is_playing = False

    # Define a method for stopping the music
    def stop_music(self):
        # Check if music is currently playing
        if self.is_playing:
            # Stop the pygame mixer
            pygame.mixer.stop()
            # Reset the current position to 0
            self.current_position = 0
            # Set the playing flag to False
            self.is_playing = False

    # Define a method for creating a waveform image from a music file
    def create_waveform_image(self, music_file):
        try:
            # Open the WAV file and retrieve its parameters
            wave_file = wave.open(music_file, "rb")
            frames = wave_file.getnframes()
            framerate = wave_file.getframerate()
            wave_data = np.frombuffer(wave_file.readframes(frames), dtype=np.int16)
            wave_file.close()

            # Calculate the duration of the audio in seconds
            duration = frames / framerate

            # Create an array of time values
            time_array = np.linspace(0, duration, len(wave_data))

            # Create a waveform plot using Matplotlib
            plt.figure(figsize=(70, 5))
            plt.plot(time_array, wave_data, color="blue")
            plt.axis("off")
            plt.savefig("waveform.png", bbox_inches="tight", pad_inches=0, transparent=True)

            # Open the saved waveform image
            waveform_image = Image.open("waveform.png")
            # Resize the image to fit the waveform canvas
            waveform_image.thumbnail((1000, 420))
            # Convert the image to a PhotoImage for tkinter
            waveform_photo = ImageTk.PhotoImage(waveform_image)
            return waveform_photo

        except Exception as e:
            # Display an error message if waveform creation fails
            messagebox.showerror("Formation Master", f"Error creating waveform image: {e}")
            return None

# Entry point of the application
if __name__ == "__main__":
    # Create the main Tkinter window
    root = Tk()
    # Initialize the FormationMaster application
    app = FormationMaster(root)
    # Start the main event loop
    root.mainloop()