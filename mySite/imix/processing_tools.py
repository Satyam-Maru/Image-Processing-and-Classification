import cv2

def grayscale(image):
    """Convert image to grayscale."""
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def blur(image, ksize=15):
    """Apply Gaussian blur."""
    return cv2.GaussianBlur(image, (ksize, ksize), 0)

def edge_detection(image):
    """Apply Canny edge detection."""
    return cv2.Canny(image, 100, 200)