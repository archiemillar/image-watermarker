from tkinter import ttk
from tkinter import *
from tkinter import filedialog as fd
from PIL import Image, ImageTk, ImageDraw, ImageFont, ImageColor
import os

COLORS = [
    "Red",
    "Cyan",
    "Blue",
    "DarkBlue",
    "LightBlue",
    "Purple",
    "Yellow",
    "Lime",
    "Magenta",
    "White",
    "Silver",
    "Gray",
    "Black",
    "Orange",
    "Brown",
    "Maroon",
    "Green"
]

FONT_FAMILY = {
    "Arial": 'arial.ttf',
    "Arial Italic": 'ariali.ttf',
    "Arial Bold": 'arialbd.ttf',
    "Arial Bold Italic": 'arialbi.ttf',
}

watermarked_image = None


# Loads image then configures Scales to fit image size
def open_image():
    filename = fd.askopenfilename(filetypes=[("jpeg", ".jpg .jpeg"), ("png", ".png")])
    if filename:
        global img
        img = Image.open(filename)
        x_axis.config(from_=-img.size[0], to=img.size[0])
        y_axis.config(from_=-img.size[1], to=img.size[1])
        update_image()


# Draws watermark and updates displayed image
def update_image(*args):
    # Draws watermark
    txt = Image.new('RGBA', img.size)
    draw = ImageDraw.Draw(txt, 'RGBA')
    # Selects font and size
    font = ImageFont.truetype(FONT_FAMILY[font_choice.get()], int(size_entry.get()))
    if text_entry.get():
        txt = txt.resize(draw.textsize(text_entry.get(), font))
    draw = ImageDraw.Draw(txt, 'RGBA')
    # Changes color
    rgb = ImageColor.getrgb(color_choice.get())
    draw.text(xy=(0, 0), text=text_entry.get(), font=font, fill=(rgb[0], rgb[1], rgb[2], int(opacity.get())))
    # Changes rotation
    current_width = txt.width
    current_height = txt.height
    txt = txt.rotate(int(rotate.get()), expand=True)
    x_offset = int((txt.width - current_width) / 2)
    y_offset = int((txt.height - current_height) / 2)
    # Pastes watermark on original photo. Original copy of photo gets loaded for every change in watermark
    clear = img.copy()
    clear.paste(txt, (int(x_axis.get()) - x_offset, int(y_axis.get()) - y_offset), txt)
    # Display to screen
    if img.size[0] > img.size[1]:
        display_size = (640, 360)
    elif img.size[0] < img.size[1]:
        display_size = (360, 640)
    else:
        display_size = (640, 640)
    updated_photo_image = ImageTk.PhotoImage(image=clear.resize(display_size))
    panel.config(image=updated_photo_image)
    panel.image = updated_photo_image
    # global variable gets updated for saving purposes
    global watermarked_image
    watermarked_image = clear


# Saves watermarked image
def save_image():
    global watermarked_image
    filename = fd.asksaveasfilename(defaultextension=".png", filetypes=[("jpeg", ".jpg"), ("png", ".png")])
    if filename:
        # Convert to RGB if jpeg
        if os.path.splitext(filename)[1] == ".jpg":
            watermarked_image = watermarked_image.convert("RGB")
        watermarked_image.save(filename)


# UI #
root = Tk()
root.title("Image Watermarker")
root.config(padx=30, pady=20)

img = Image.new('L', (360, 640))
photo_image = ImageTk.PhotoImage(image=img)
panel = Label(root, image=photo_image)
panel.image = photo_image
panel.grid(row=0, column=0, rowspan=13)

import_button = Button(root, text="Import Image", command=open_image)
import_button.grid(row=21, column=0)

separator = ttk.Separator(root, orient='vertical')
separator.grid(row=0, column=1, rowspan=30, ipady=320, padx=10)

style_label = Label(root, text="Style", font=("Arial", 11, "bold"))
style_label.grid(row=0, column=3)

text_entry = StringVar()
text_label = Label(root, text="Text:")
text_label.grid(row=1, column=2)
text = Entry(root, textvariable=text_entry, width=40)
text.grid(row=1, column=3)
text_entry.trace("w", update_image)

font_choice = StringVar()
font_label = Label(root, text="Font:")
font_label.grid(row=2, column=2)
font_box = ttk.Combobox(state="readonly", values=list(FONT_FAMILY.keys()), width=37, textvariable=font_choice)
font_box.set("Arial")
font_box.grid(row=2, column=3)
font_choice.trace("w", update_image)

size_entry = StringVar()
size_label = Label(root, text="Size:")
size_label.grid(row=3, column=2)
# size = Scale(root, from_=0, to=1080, length=245, orient=HORIZONTAL, command=update_image)
# size.set(20)
size = Entry(root, textvariable=size_entry, width=40)
size.grid(row=3, column=3)
size_entry.set("20")
size_entry.trace("w", update_image)

color_choice = StringVar()
color_label = Label(root, text="Color:")
color_label.grid(row=4, column=2)
color = ttk.Combobox(root, state="readonly", values=COLORS, width=37, textvariable=color_choice)
color.set("White")
color.grid(row=4, column=3)
color_choice.trace("w", update_image)

opacity_label = Label(root, text="Opacity:")
opacity_label.grid(row=5, column=2)
opacity = Scale(root, from_=0, to=255, length=245, orient=HORIZONTAL, command=update_image)
opacity.set(255)
opacity.grid(row=5, column=3)

orient_label = Label(root, text="Orientation", font=("Arial", 11, "bold"))
orient_label.grid(row=8, column=3)

x_label = Label(root, text="X-Axis:")
x_label.grid(row=9, column=2)
x_axis = Scale(root, from_=-360, to=360, length=245, orient=HORIZONTAL, command=update_image)
x_axis.grid(row=9, column=3)

y_label = Label(root, text="Y-Axis:")
y_label.grid(row=10, column=2)
y_axis = Scale(root, from_=-640, to=640, length=245, orient=HORIZONTAL, command=update_image)
y_axis.grid(row=10, column=3)

rotate_label = Label(root, text="Rotate:")
rotate_label.grid(row=11, column=2)
rotate = Scale(root, from_=180, to=-180, length=244, orient=HORIZONTAL, command=update_image)
rotate.grid(row=11, column=3)

save_button = Button(root, text="Save Image", command=save_image)
save_button.grid(row=12, column=3)

root.mainloop()
