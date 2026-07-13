import os
from tkinter import Tk, Button, Label, Entry, filedialog, messagebox
from PIL import Image

def crop_image(input_path, output_folder, num_horizontal, num_vertical):
    img = Image.open(input_path)
    img_width, img_height = img.size
    piece_width = img_width // num_horizontal
    piece_height = img_height // num_vertical
    img_basename = os.path.splitext(os.path.basename(input_path))[0]
    
    target_folder = os.path.join(output_folder, img_basename)
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
        
    for i in range(num_horizontal):
        for j in range(num_vertical):
            left = i * piece_width
            upper = j * piece_height
            right = (i + 1) * piece_width
            lower = (j + 1) * piece_height
            
            cropped_img = img.crop((left, upper, right, lower))
            cropped_img_filename = os.path.join(target_folder, f"crop_{i}_{j}.png")
            cropped_img.save(cropped_img_filename)

def select_images():
    file_paths = filedialog.askopenfilenames(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    if file_paths:
        image_paths_entry.delete(0, 'end')
        image_paths_entry.insert(0, ";".join(file_paths))

def on_crop_click():
    try:
        input_paths = image_paths_entry.get().split(";")
        if not image_paths_entry.get():
            messagebox.showerror("Error", "Por favor, selecciona al menos una imagen.")
            return
            
        num_horizontal = int(horizontal_entry.get())
        num_vertical = int(vertical_entry.get())
        output_folder = "output_pieces"
        
        if num_horizontal > 0 and num_vertical > 0:
            for input_path in input_paths:
                if input_path.strip():
                    crop_image(input_path, output_folder, num_horizontal, num_vertical)
            messagebox.showinfo("Éxito", "¡Imágenes recortadas correctamente!")
        else:
            messagebox.showerror("Error", "Los números deben ser mayores a 0.")
    except ValueError:
        messagebox.showerror("Error", "Por favor, introduce números válidos.")
    except Exception as e:
        messagebox.showerror("Error Inesperado", f"Ocurrió un error: {str(e)}")

root = Tk()
root.title("Image Cropper")

Label(root, text="Select Images:").grid(row=0, column=0, padx=10, pady=10)
image_paths_entry = Entry(root, width=40)
image_paths_entry.grid(row=0, column=1, padx=10, pady=10)
Button(root, text="Browse", command=select_images).grid(row=0, column=2, padx=10, pady=10)

Label(root, text="Horizontal Pieces:").grid(row=1, column=0, padx=10, pady=10)
horizontal_entry = Entry(root, width=10)
horizontal_entry.grid(row=1, column=1, padx=10, pady=10)

Label(root, text="Vertical Pieces:").grid(row=2, column=0, padx=10, pady=10)
vertical_entry = Entry(root, width=10)
vertical_entry.grid(row=2, column=1, padx=10, pady=10)

Button(root, text="Crop", command=on_crop_click).grid(row=3, columnspan=3, pady=20)

root.mainloop()
