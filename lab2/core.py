import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from matplotlib import pyplot as plt
from scipy import ndimage
from skimage import color, io

def convolve2d(image, kernel):
    image_height, image_width = image.shape
    kernel_height, kernel_width = kernel.shape
    kernel = np.flipud(np.fliplr(kernel))

    output_height = image_height - kernel_height + 1
    output_width = image_width - kernel_width + 1

    image_windows = np.lib.stride_tricks.sliding_window_view(image, (kernel_height, kernel_width))
    output = np.sum(image_windows * kernel, axis=(2, 3))

    return output

def sobel_operators(image):
    sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    sobel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
    gradient_x = convolve2d(image, sobel_x)
    gradient_y = convolve2d(image, sobel_y)
    return gradient_x, gradient_y

def calculate_gradient_magnitude(gray):
    gray = gray.astype(np.float64)
    gradient_x, gradient_y = sobel_operators(gray)

    gradient_magnitude = np.sqrt(gradient_x**2 + gradient_y**2)
    gradient_magnitude = (255 * gradient_magnitude / np.max(gradient_magnitude)).astype(np.uint8)

    return gradient_magnitude

def detect_changes_in_brightness(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gradient_magnitude = calculate_gradient_magnitude(gray) 
    return cv2.cvtColor(gradient_magnitude, cv2.COLOR_GRAY2BGR)

def detect_lines(image):
    gray = image.mean(axis=2)

    kernel = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]]) / 9.0
    blurred = convolve2d(gray, kernel)

    gradient_x, gradient_y = sobel_operators(blurred)
    gradient_magnitude = np.sqrt(gradient_x**2 + gradient_y**2)
    edges = (gradient_magnitude > 100).astype(np.uint8)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=25, minLineLength=10, maxLineGap=10)
    
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

    return image


def detect_points(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    corners = cv2.goodFeaturesToTrack(gray, maxCorners=750, qualityLevel=0.0001, minDistance=10)

    if corners is not None:
        for corner in corners:
            x, y = corner.ravel()
            x, y = int(x), int(y)
            cv2.circle(image, (x, y), 6, (0, 255, 0), -1)

    return image

def simple_thresholding(image, threshold):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresholded = (gray > threshold).astype(np.uint8) * 255
    return thresholded

def adaptive_thresholding(image, block_size, constant):
    """ 
            # Slow straighforward impl
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        padded = np.pad(gray, block_size // 2, mode='constant')
        thresholded = np.zeros_like(gray)
   
        for i in range(gray.shape[0]):
            for j in range(gray.shape[1]):
                block = padded[i:i+block_size, j:j+block_size]
                mean = np.mean(block)
                threshold = mean - constant
                if gray[i, j] > threshold:
                    thresholded[i, j] = 255

        return cv2.cvtColor(thresholded, cv2.COLOR_GRAY2BGR)
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresholded = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, block_size, constant)
    return cv2.cvtColor(thresholded, cv2.COLOR_GRAY2BGR)

def browse_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        image = cv2.imread(file_path)
        
        # image segmentation
        points_image = detect_points(image.copy())
        lines_image = detect_lines(image.copy())
        brightness_image = detect_changes_in_brightness(image.copy())
        
        # local thresholding
        simple_thresholded = simple_thresholding(image, 120)
        adaptive_thresholded = adaptive_thresholding(image, 11, 2)
        
        # processed images
        plt.figure(figsize=(12, 8))
        plt.subplot(231), plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)), plt.title('Original Image')
        plt.subplot(232), plt.imshow(cv2.cvtColor(points_image, cv2.COLOR_BGR2RGB)), plt.title('Points Detection')
        plt.subplot(233), plt.imshow(cv2.cvtColor(lines_image, cv2.COLOR_BGR2RGB)), plt.title('Line Detection')
        plt.subplot(234), plt.imshow(cv2.cvtColor(brightness_image, cv2.COLOR_BGR2RGB)), plt.title('Brightness Changes')
        plt.subplot(235), plt.imshow(cv2.cvtColor(simple_thresholded, cv2.COLOR_BGR2RGB)), plt.title('Simple Thresholding')
        plt.subplot(236), plt.imshow(cv2.cvtColor(adaptive_thresholded, cv2.COLOR_BGR2RGB)), plt.title('Adaptive Thresholding')
        plt.show()

app = tk.Tk()
app.title("Image Processing Application")

browse_button = tk.Button(app, text="Browse Image", command=browse_image)
browse_button.pack()

app.mainloop()
