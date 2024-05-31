import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
import os 
import time

'''
counter_directory = "C:\\Apps"
counter_file = os.path.join(counter_directory, "Log.txt")

if not os.path.exists(counter_directory):
    os.makedirs(counter_directory)


def read_counter():
    if os.path.exists(counter_file):
        with open(counter_file, "r") as file:
            return int(file.read())
    else:
        return 0

def write_counter(count):
    with open(counter_file, "w") as file:
        file.write(str(count))
'''

def img_data_gui():
    global tan_pixels_data
    global calcd_pixels
    global excluded_pixels
    global math_all_pixels
    global all_scanned_pixels
    global close_btn
    global percentage_result
        
    img_data = tk.Toplevel()
    img_data.title('Image Data Statistics')
    img_data.geometry("300x200+50+780")

    tan_pixels_data = tk.Label(img_data, text=f"Total Tan Pixels: {total_tan_pixels}").pack()
    calcd_pixels = tk.Label(img_data, text=f"Total Pixels in % Calc: {inCount_pixels}").pack()
    excluded_pixels = tk.Label(img_data, text=f"Total Exlcuded Pixels: {s0_v0_pixels}").pack()
    math_all_pixels = tk.Label(img_data, text=f"Total Pixels: {total_pixels}").pack()
    all_scanned_pixels = tk.Label(img_data, text=f"Total Scanned Pixels: {scanned_pixels}").pack()
    percentage_result = tk.Label(img_data, text=f"Percent Bare: {tan_percentage}%", font=(None, 14, "bold")).pack()

    close_btn = tk.Button(img_data, text="Close Program", command=root.destroy, height=2).pack()
    root.iconify()
        
def process_image(image_filename):
    global total_pixels
    global total_tan_pixels
    global scanned_pixels
    global s0_v0_pixels
    global inCount_pixels
    global tan_percentage


    image = cv2.imread(image_filename)

    if image is None:
        print(f"Error: Unable to load the image '{image_filename}'. Make sure the file exists.")
    else:

        screen_width, screen_height = 1920, 1080

        cv2.namedWindow("Image Viewer", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Image Viewer", screen_width, screen_height)

        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        lower_tan = np.array([0, 3, 180])
        upper_tan = np.array([45, 200, 255])

        tan_mask = cv2.inRange(hsv_image, lower_tan, upper_tan)

        result_image = image.copy()
        result_image[tan_mask != 0] = [0, 0, 255] 

        scanned_pixels = 0

        s0_v0_pixels = np.count_nonzero((hsv_image[..., 1] == 0) & (hsv_image[..., 2] == 0))

        total_pixels = image.shape[0] * image.shape[1]

        total_tan_pixels = np.count_nonzero(tan_mask)

        inCount_pixels = total_pixels - s0_v0_pixels

        for row in range(image.shape[0]):
            for col in range(image.shape[1]):
                scanned_pixels += 1


        tan_percentage = round((total_tan_pixels / (scanned_pixels - s0_v0_pixels)) * 100, 2)

        file_name = os.path.basename(image_filename)

        cv2.imshow("Image Viewer", result_image)

        time.sleep(5)
        cv2.setWindowProperty("Image Viewer", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        img_data_gui()



def open_file_dialog():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff;*.tif")])
    if file_path:
        process_image(file_path)
        root.iconify()
        

root = tk.Tk()
root.title("Image Processing of Vegetation Analysis")
root.geometry("400x125+600+500")

instruction_label = tk.Label(root, text="Please select an image to process")
instruction_label.pack(pady=10)

button = tk.Button(root, text="File select", command=open_file_dialog, height=3, width=10).pack()

root.mainloop()
