import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, Label
from PIL import Image, ImageTk
from datetime import datetime
import webbrowser

class ImageConverterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Image to WebP Converter')
        self.geometry('500x400')

        # Header Logo
        self.logo_image = Image.open(self.resource_path("logokamrul-px-100x-50.png"))  # Load logo image
        self.logo_image = self.logo_image.resize((100, 50), Image.LANCZOS)  # Resize if needed
        self.logo = ImageTk.PhotoImage(self.logo_image)

        self.logo_label = tk.Label(self, image=self.logo)
        self.logo_label.pack(pady=10)

        # List to store file paths
        self.selected_files = []

        # Button to select images
        self.select_button = tk.Button(self, text="Select Images", command=self.select_images, width=30, height=2)
        self.select_button.pack(pady=20)

        # Label to show number of selected images
        self.label = tk.Label(self, text="No images selected", width=60, height=2, relief="solid")
        self.label.pack(pady=10)

        # Button to convert selected images
        self.convert_button = tk.Button(self, text="Convert to WebP", command=self.convert_images, width=30, height=2, state=tk.DISABLED)
        self.convert_button.pack(pady=20)

        # Footer
        self.footer = tk.Frame(self)
        self.footer.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

        self.developer_label = tk.Label(self.footer, text="Developer: KAMRUL MOLLAH | ", anchor="e")
        self.developer_label.pack(side=tk.LEFT)

        self.website_link = tk.Label(self.footer, text="Website", fg="blue", cursor="hand2")
        self.website_link.pack(side=tk.LEFT)
        self.website_link.bind("<Button-1>", lambda e: webbrowser.open_new("https://kamrulmollah.com"))

        self.github_link = tk.Label(self.footer, text=" | GitHub", fg="blue", cursor="hand2")
        self.github_link.pack(side=tk.LEFT)
        self.github_link.bind("<Button-1>", lambda e: webbrowser.open_new("https://github.com/KAMRUL-MOLLAH/"))

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temporary folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def select_images(self):
        # Allow multiple file selection for JPEG and PNG files
        file_types = [("Image files", "*.jpg;*.jpeg;*.png")]
        files = filedialog.askopenfilenames(filetypes=file_types)

        if files:
            self.selected_files = list(files)  # Convert the tuple to a list
            self.label.config(text=f"{len(files)} image(s) selected")
            self.convert_button.config(state=tk.NORMAL)  # Enable the convert button
        else:
            self.label.config(text="No images selected")
            self.convert_button.config(state=tk.DISABLED)  # Disable the convert button if no images selected

    def convert_images(self):
        if not self.selected_files:
            messagebox.showwarning("No Images", "Please select images to convert.")
            return

        # Get the directory of the first selected image
        directory = os.path.dirname(self.selected_files[0])

        # Create a new folder with the current date
        today = datetime.now().strftime('%Y-%m-%d')  # Get current date as a string
        output_folder = os.path.join(directory, f"webp_converted_{today}")

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)  # Create the new folder if it doesn't exist

        for file_path in self.selected_files:
            try:
                img = Image.open(file_path)  # Open the image
                file_name = os.path.basename(file_path)  # Get the file name
                webp_file_name = os.path.splitext(file_name)[0] + '.webp'  # Create WebP file name
                webp_path = os.path.join(output_folder, webp_file_name)  # Set output WebP file path

                img.save(webp_path, 'webp')  # Save the image as WebP
            except Exception as e:
                messagebox.showerror("Error", f"Failed to convert {file_path}: {str(e)}")
                continue

        messagebox.showinfo("Success", f"All images converted and saved to: {output_folder}")
        self.selected_files.clear()  # Clear the file list after conversion
        self.label.config(text="No images selected")
        self.convert_button.config(state=tk.DISABLED)  # Disable the convert button after conversion

# Run the app
if __name__ == '__main__':
    app = ImageConverterApp()
    app.mainloop()
