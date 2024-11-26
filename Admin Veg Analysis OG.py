import cv2
from cv2 import *
import numpy as np
import tkinter as tk
from tkinter import BOTTOM, E, LEFT, NE, W, NW, Label, Toplevel, filedialog
from PIL import ImageTk,Image
import os  
import time
from icecream import ic



def open_original_img(file_path):
    global btn_close
    global btn_img_close
    global og_img_label
    global new_img
    global resized_img
    global img

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



def img_data_gui(file_path):
    global tan_pixels_data
    global calcd_pixels
    global excluded_pixel
    global close_btn
    global percentage_result

    #Create Window for Stats
    img_data = tk.Toplevel()
    img_data.title('Image Data Statistics')
    img_data.geometry("+40+790")
    


    #Text to display
    tan_pixels_data = tk.Label(img_data, text=f"Total Without Vegetation: {total_tan_pixels}")
    calcd_pixels = tk.Label(img_data, text=f"Total - Excluded: {inCount_pixels}")
    excluded_pixel = tk.Label(img_data, text=f"Total Exlcuded: {excluded_pixels}")
    
    if(scanned_pixels==total_pixels):
        words = ["Total Comparison:","✅✅✅"]
        colours = ["black","green"]
        for index,word in enumerate(words):
            color_check_test = tk.Label(img_data,text = word,fg=colours[index])
            color_check_test.grid(column=index + 1,row=1, sticky=E)

    
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
    global total_pixels
    global total_tan_pixels
    global scanned_pixels
    global excluded_pixels
    global inCount_pixels
    global tan_percentage


    # Load the image
    image = cv2.imread(image_filename)

    if image is None:
        print(f"Error: Unable to load the image '{image_filename}'. Make sure the file exists.")
    else:

        # Get the screen resolution
        screen_width, screen_height = 1920, 1080  # Change to your screen resolution

        # Create a window with a custom size to fit the screen
        cv2.namedWindow("Red Pixels Counted as Without Vegetation", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Red Pixels Counted as Without Vegetation", screen_width, 1030)

        # Convert the image to HSV color space
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Define a range for tan color in HSV (you may need to adjust these values)
        lower_tan = np.array([0, 3, 180])
        upper_tan = np.array([45, 200, 255])

        lower_blue = np.array([90, 50, 70])
        upper_blue = np.array([128, 255, 255])

        lower_gray = np.array([0, 0, 40])
        upper_gray = np.array([180, 18, 230])

        # Lower and upper bounds for #a4896e
        lower_brown1 = np.array([15, 50, 100])
        upper_brown1 = np.array([25, 150, 200])

        # Lower and upper bounds for #6c5234
        lower_brown2 = np.array([15, 50, 50])
        upper_brown2 = np.array([25, 150, 100])

        # Create a mask for the additional tan color range
        tan_mask_additional = cv2.inRange(hsv_image, lower_brown1, upper_brown1)
        tan_mask_additional2 = cv2.inRange(hsv_image, lower_brown2, upper_brown2)

        # Create a mask for the tan color
        tan_mask = cv2.inRange(hsv_image, lower_tan, upper_tan)
        # Combine the original tan mask with the additional tan mask
        tan_mask = cv2.bitwise_or(tan_mask, tan_mask_additional, tan_mask_additional2)

        #black_mask = cv2.inRange(hsv_image, lower_black, upper_black)
        gray_mask = cv2.inRange(hsv_image, lower_gray, upper_gray)
        blue_mask = cv2.inRange(hsv_image, lower_blue, upper_blue)


        # Highlight tan pixels in red on the original image
        result_image = image.copy()
        #result_image[black_mask != 0] = [0, 0, 255] #highlight in Red
        result_image[gray_mask != 0] = [0, 0, 255] #highlight in Red
        result_image[blue_mask != 0] = [0, 0, 255] #highlight in Red
        result_image[tan_mask != 0] = [30, 255, 255]  # Highlight tan pixels in Yellow

        # Initialize a counter for scanned pixels
        scanned_pixels = 0

        # Calculate the number of pixels with S=0 and V=0
        s0_v0_pixels = np.count_nonzero((hsv_image[..., 1] == 0) & (hsv_image[..., 2] == 0))

        #black_pixels = np.count_nonzero(black_mask)
        gray_pixels = np.count_nonzero(gray_mask)
        panel_pixels = np.count_nonzero(blue_mask)
        # Variable for future implementation of Excluding Solar Panels
        #panel_pixels = 0
        # Test before distribution. 
        
        # Calculate the total number of pixels
        total_pixels = image.shape[0] * image.shape[1]

        # Calculate the total number of pixels marked as tan
        total_tan_pixels = np.count_nonzero(tan_mask)

        excluded_pixels = s0_v0_pixels + panel_pixels + gray_pixels
        # Calculate the total number of pixels excluded
        inCount_pixels = total_pixels - excluded_pixels
        ic(excluded_pixels, s0_v0_pixels, panel_pixels, gray_pixels)
        # Loop through the entire image and count scanned pixels
        for row in range(image.shape[0]):
            for col in range(image.shape[1]):
                scanned_pixels += 1


        # Calculate the tan color percentage while excluding S=0 and V=0 pixels
        tan_percentage = round((total_tan_pixels / (scanned_pixels - excluded_pixels)) * 100, 2)

        # Extract the file name from the full path
        file_name = os.path.basename(image_filename)

        # Show the original image with highlighted tan pixels in the "Image Viewer" window
        cv2.imshow("Red Pixels Counted as Without Vegetation", result_image)

        img_data_gui(image_filename)



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


# Start the main loop
root.mainloop()
