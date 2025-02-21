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

def resize(image, width, height):

    resized_image = cv2.resize(image, (width, height), interpolation=cv2.INTER_LINEAR)

    return resized_image

def apply_blur(image, kernel_size=5):
    """
    Parameters:
    - image: Input RGB image (NumPy array).
    - method: Blurring method ("gaussian" or "median").
    - kernel_size: Size of the kernel (should be an odd number, default 5).
    """
    return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)

def detect_edges(image, threshold1=100):
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

    return cv2.Canny(gray, threshold1, threshold1 * 2)
    
def apply_threshold(image):
    
    gray = grayscale(image)

    # Apply binary thresholding (default threshold_value = 127)
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    return thresh

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
    
def adjust_brightness(image, beta=0):
    """
    Parameters:
    - image: Input RGB image (NumPy array).
    - beta: Brightness adjustment factor (default 0, positive values brighten, negative values darken).
    """
    # Apply brightness adjustment
    adjusted_image = cv2.convertScaleAbs(image, alpha=1.0, beta=beta)

    return adjusted_image