import io
import tkinter as tk
import customtkinter as ctk
from customtkinter import filedialog
from PIL import Image, ImageTk, ImageFilter

class ImageFilterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Filter App")

        self.canvas_width = 1280
        self.canvas_height = 720

        self.canvas = ctk.CTkCanvas(root, height=self.canvas_height, width=self.canvas_width, background="black")
        self.canvas.pack(pady=10)

        open_button = ctk.CTkButton(root, text="Open Image", command=self.load_image)
        open_button.place(x=400, y=747)

        Reset_button = ctk.CTkButton(root, text="Original", command=self.apply_backup)
        Reset_button.place(x=700, y=747)

        greyscale_button = ctk.CTkButton(root, text="Grey Scale", command=self.apply_greyscale)
        greyscale_button.pack(side=ctk.RIGHT, anchor=ctk.SE, padx=5, pady=50)

        sharpen_button = ctk.CTkButton(root, text="Sharpen", command=self.apply_sharpen)
        sharpen_button.pack(side=ctk.RIGHT, anchor=ctk.SE, padx=5, pady=50)

        ee_button = ctk.CTkButton(root, text="Edge Enhance", command=self.apply_edge_enhance)
        ee_button.pack(side=ctk.RIGHT, anchor=ctk.SE, padx=5, pady=50)

        blur_button = ctk.CTkButton(root, text="Blur", command=self.apply_blur)
        blur_button.pack(side=ctk.RIGHT, anchor=ctk.SE, padx=5, pady=50)

        smooth_button = ctk.CTkButton(root, text="Smooth", command=self.apply_smooth)
        smooth_button.pack(side=ctk.RIGHT, anchor=ctk.SE, padx=5, pady=50)

        ee_button = ctk.CTkButton(root, text="Save Image", command=self.save_image)
        ee_button.pack(side=ctk.LEFT, anchor=ctk.SW, padx=5, pady=50)

    def load_image(self):
        file_path = filedialog.askopenfilename()

        if file_path:
            self.image = Image.open(file_path)
            thumbnail_size = (self.canvas_height, self.canvas_width)
            self.image.thumbnail(thumbnail_size)
            original_size = self.image.size

            double_size = (int(original_size[0] * 1.8), int(original_size[1] * 1.8))
            self.resized_image = self.image.resize(double_size, Image.ADAPTIVE)
            self.canvas_image = ImageTk.PhotoImage(self.resized_image)
            self.backup_image = self.resized_image

            x_position = (self.canvas_width - self.resized_image.width) // 2
            y_position = (self.canvas_height - self.resized_image.height) // 2
            self.image_id = self.canvas.create_image(x_position, y_position, anchor=ctk.NW, image=self.canvas_image)

    def apply_greyscale(self):
        filtered_image = self.resized_image.convert("L")
        self.update_image(filtered_image)

    def apply_sharpen(self):
        filtered_image = self.resized_image.filter(ImageFilter.SHARPEN)
        self.update_image(filtered_image)

    def apply_blur(self):
        filtered_image = self.resized_image.filter(ImageFilter.BLUR)
        self.update_image(filtered_image)

    def apply_edge_enhance(self):
        filtered_image = self.resized_image.filter(ImageFilter.EDGE_ENHANCE)
        self.update_image(filtered_image)

    def apply_smooth(self):
        filtered_image = self.resized_image.filter(ImageFilter.SMOOTH)
        self.update_image(filtered_image)

    def apply_backup(self):
        original_image = self.backup_image
        self.update_image(original_image)

    def update_image(self, new_image):
        self.resized_image = new_image
        self.canvas_image = ImageTk.PhotoImage(self.resized_image)
        self.canvas.itemconfig(self.image_id, image=self.canvas_image)

    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])

        if file_path:
            post_script_data = self.canvas.postscript(colormode="color")
            wanted_image = Image.open(io.BytesIO(post_script_data.encode("utf-8")))
            wanted_image.save(file_path, format="PNG")

if __name__ == "__main__":
    ctk.set_appearance_mode("default")
    root = ctk.CTk()
    app = ImageFilterApp(root)
    root.mainloop()
