import cv2
import numpy as np

def grayscale(image, alpha=1.0, beta=0):
    """
    Parameters:
    - image: Input RGB image (NumPy array).
    - alpha: Contrast factor (default 1.0, >1 increases intensity, <1 decreases it).
    - beta: Brightness factor (default 0, positive values brighten, negative values darken).
    """
    # Convert RGB image to grayscale
    grayscale_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply intensity adjustment
    adjusted_gray = cv2.convertScaleAbs(grayscale_img, alpha=alpha, beta=beta)

    return adjusted_gray

def apply_blur(image, method="gaussian", kernel_size=5):
    """
    Parameters:
    - image: Input RGB image (NumPy array).
    - method: Blurring method ("gaussian" or "median").
    - kernel_size: Size of the kernel (should be an odd number, default 5).
    """
    if kernel_size % 2 == 0:  # Ensure kernel size is odd
        kernel_size += 1

    if method == "gaussian":
        return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
    elif method == "median":
        return cv2.medianBlur(image, kernel_size)
    else:
        raise ValueError("Invalid blur method. Choose 'gaussian' or 'median'.")

def detect_edges(image, method="canny", threshold1=100, threshold2=200, ksize=3):
    """
    Parameters:
    - image: Input RGB image (NumPy array).
    - method: Edge detection method ("canny" or "sobel").
    - threshold1: Lower threshold for Canny edge detection.
    - threshold2: Upper threshold for Canny edge detection.
    - ksize: Kernel size for Sobel operator (must be odd).
    """
    # Convert to grayscale
    gray = grayscale(image)

    if method == "canny":
        return cv2.Canny(gray, threshold1, threshold2)
    elif method == "sobel":
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=ksize)  # X-gradient
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=ksize)  # Y-gradient
        sobel_edges = cv2.magnitude(sobelx, sobely)  # Compute edge magnitude
        return cv2.convertScaleAbs(sobel_edges)  # Convert to uint8
    else:
        raise ValueError("Invalid method. Choose 'canny' or 'sobel'.")

def apply_threshold(image):
    
    gray = grayscale(image)

    # Apply binary thresholding (default threshold_value = 127)
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    return thresh

def adjust_brightness(image, beta=0):
    """
    Parameters:
    - image: Input RGB image (NumPy array).
    - beta: Brightness adjustment factor (default 0, positive values brighten, negative values darken).
    """
    # Apply brightness adjustment
    adjusted_image = cv2.convertScaleAbs(image, alpha=1.0, beta=beta)

    return adjusted_image

def apply_morphology(image, operation="erode", kernel_size=3):
    """
    Parameters:
    - image: Input binary image (NumPy array).
    - operation: The morphological operation ("erode" or "dilate").
    - kernel_size: Size of the kernel (odd number, default 3).
    """
    # Create a kernel (default 3x3)
    kernel = np.ones((kernel_size, kernel_size), np.uint8)

    if operation == "erode":
        return cv2.erode(image, kernel, iterations=1)
    elif operation == "dilate":
        return cv2.dilate(image, kernel, iterations=1)
    else:
        raise ValueError("Invalid operation. Choose 'erode' or 'dilate'.")
    
def adjust_rgb_channels(image, red_factor=1.0, green_factor=1.0, blue_factor=1.0):
    """
    Parameters:
    - image: Input RGB image (NumPy array).
    - red_factor: Factor to adjust the red channel (default 1.0, >1 increases intensity).
    - green_factor: Factor to adjust the green channel (default 1.0, >1 increases intensity).
    - blue_factor: Factor to adjust the blue channel (default 1.0, >1 increases intensity).
    """
    # Split the image into RGB channels
    b, g, r = cv2.split(image)

    # Apply the intensity factor to each channel
    r = cv2.convertScaleAbs(r, alpha=red_factor)
    g = cv2.convertScaleAbs(g, alpha=green_factor)
    b = cv2.convertScaleAbs(b, alpha=blue_factor)

    # Merge the channels back together
    adjusted_image = cv2.merge([b, g, r])

    return adjusted_image