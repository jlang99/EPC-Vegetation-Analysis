import cv2
from cv2 import *
import numpy as np
import tkinter as tk
from tkinter import *
from tkinter import Label, Toplevel, filedialog
from PIL import ImageTk,Image
import os  
import time
import json
from icecream import ic



def open_original_img(file_path):

    #Create Window
    original_img = Toplevel()
    original_img.title('Image Processed')
    original_img.geometry("1920x1080+0+0")

    #Open and Resize Image, then pack onto window
    img= Image.open(file_path)
    resized_img= img.resize((1920, 960))
    new_img= ImageTk.PhotoImage(resized_img)
    og_img_label= Label(original_img, image= new_img)
    og_img_label.grid(column=0, row=0, columnspan=2)

    #Close program or Window Buttons
    btn_close = tk.Button(original_img, text="Close Program", command=root.destroy, height= 1, width= 12)
    btn_close.grid(row=1, column=0, padx=5, pady=5, sticky=E)   
    btn_img_close = tk.Button(original_img, text="Close Window", command=original_img.destroy, height= 1, width= 12)
    btn_img_close.grid(row=1, column=1, padx=5, pady=5, sticky=W)



def img_data_gui(file_path, total_pixels, marked_pixels, excluded_pixels):

    #Create Window for Stats
    img_data = tk.Toplevel()
    img_data.title('Image Data Statistics')
    img_data.geometry("+40+790")
    


    #Text to display
    tan_pixels_data = tk.Label(img_data, text=f"Total Without Vegetation: {marked_pixels}")
    calcd_pixels = tk.Label(img_data, text=f"Total: {total_pixels}")
    excluded_pixel = tk.Label(img_data, text=f"Total Exlcuded: {excluded_pixels}")

    tan_percentage = round((marked_pixels / total_pixels) * 100, 2)

    
    #Placed in Window
    tan_pixels_data.grid(row=0, column=0, sticky=E)
    calcd_pixels.grid(row=1, column=0, sticky=E)
    excluded_pixel.grid(row=0, column=1, sticky=E, columnspan=2)

    #Important variable/bigger for focal attention
    percentage_result = tk.Label(img_data, text=f"Without Vegetation: {tan_percentage}%", font=(None, 16, "bold"))
    percentage_result.grid(row=2, columnspan=3, pady=10)

    #Close Program Button
    close_btn = tk.Button(img_data, text="Close Program", command=root.destroy, height=2)
    close_btn.grid(row=3, column=0, pady=5, padx=5)
    #Comparison image Button
    open_img = tk.Button(img_data, text="Open Original Img", command= lambda: open_original_img(file_path), height=2)
    open_img.grid(row=3, column=1, padx=5, pady=5)

    #Minimize the File Dialog selection
    time.sleep(2)
    root.iconify()
        
def process_image(image_filename):
    # Load the image
    image = cv2.imread(image_filename)

    if image is None:
        print(f"Error: Unable to load the image '{image_filename}'. Make sure the file exists.")
    else:
        # Convert the image to RGB color space
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Initialize a counter for scanned pixels
        scanned_pixels = 0
        excluded_pixel = 0
        marked_pixels = 0

        filtered_pixels = 0

        exclusions = [(0, 0, 0), (255, 255, 255), (0, 0, 255)]

        color_dic = {}
        # Loop through the entire image and count scanned pixels
        for row in range(hsv_image.shape[0]):
            for col in range(hsv_image.shape[1]):
                scanned_pixels += 1
                pixel_color = hsv_image[row, col]
                hue = pixel_color[0]
                sat = pixel_color[1]
                val = pixel_color[2]
                xy = (row, col)

                
                if (hue, sat, val) in exclusions: #excludes outside areas
                    excluded_pixel += 1
                    image[row, col] = [0, 255, 100] #Green
                elif 85 < hue < 120: #Filters Panels
                    image[row, col] = [103, 255, 255] #yellow       
                    excluded_pixel += 1  
                elif (11 < hue < 23) and (30 < sat < 148) and (82 < val < 179):
                    image[row, col] = [203, 192, 255] #Pink
                    marked_pixels += 1
                else:
                    color_dic[f'{xy}'] = (hue, sat, val)
                    scanned_pixels += 1

        color_dic_serializable = {k: tuple(int(x) for x in v) for k, v in color_dic.items()}
        
        json_file_path = os.path.join(os.path.dirname(__file__), 'color_data.json')
        with open(json_file_path, 'w+') as txt_file:
            json.dump(color_dic_serializable, txt_file, indent= 1)

        # Extract the file name from the full path
        file_name = os.path.basename(image_filename)

        #cv2.imshow('Testing HSV', hsv_image)
        cv2.imshow('Testing', image)

        # Extract all the tuples
        values = list(color_dic.values())

        # Get the min and max for each item in the tuples
        min_hue = min(value[0] for value in values)
        max_hue = max(value[0] for value in values)

        min_sat = min(value[1] for value in values)
        max_sat = max(value[1] for value in values)

        min_val = min(value[2] for value in values)
        max_val = max(value[2] for value in values)

        ic(min_hue, max_hue, min_sat, max_sat, min_val, max_val)

        img_data_gui(image_filename, scanned_pixels, marked_pixels, excluded_pixel)



def open_file_dialog():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff;*.tif")])
    if file_path:
        process_image(file_path)
        
# Create the main application window
root = tk.Tk()
root.title("Vegetation Analysis")
root.geometry("+400+850")

# Create a label for the instruction
instruction_label = tk.Label(root, text="Please select an image to process", font=(None, 14))
instruction_label.grid(row=0, columnspan=3)

# Create a button to open the file dialog
button = tk.Button(root, text="File select", command=open_file_dialog, height=3, width=10)
close1_btn = tk.Button(root, text="Cancel", command=root.destroy)

close1_btn.grid(column=0, row=1)
button.grid(column=1, row=1, pady=10)

test_img = r"C:\Users\JosephLang\OneDrive - Narenco\Pictures\Screenshots\Screenshot 2024-06-20 164121.png"
#
# Testing
#process_image(test_img)


# Start the main loop
root.mainloop()
